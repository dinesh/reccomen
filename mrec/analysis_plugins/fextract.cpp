#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <marsyas/MarSystemManager.h>

using namespace std;
using namespace Marsyas;

int main(int argc, const char** argv)
{
	if (argc < 3) {
		cout << "Usage: " << argv[0] << " soundfile outputfile" << endl;
		return 1;
	}
	
	MarSystemManager mng;
	
//------------------ Feature Network ------------------------------

	// Decode the file, downmix to mono, and downsample
	MarSystem *fnet = mng.create("Series", "fnet");
	fnet->addMarSystem(mng.create("SoundFileSource", "src"));
	fnet->addMarSystem(mng.create("DownSampler", "ds"));
	fnet->addMarSystem(mng.create("Stereo2Mono", "s2m"));
	
	// Create the feature extractor
	fnet->addMarSystem(mng.create("TimbreFeatures", "tf"));
	fnet->updctrl("TimbreFeatures/tf/mrs_string/enableTDChild", "ZeroCrossings/zcrs");
	fnet->updctrl("TimbreFeatures/tf/mrs_string/enableSPChild", "MFCC/mfcc");
	fnet->updctrl("TimbreFeatures/tf/mrs_string/enableSPChild", "Centroid/cntrd");
	fnet->updctrl("TimbreFeatures/tf/mrs_string/enableSPChild", "Flux/flux");
	fnet->updctrl("TimbreFeatures/tf/mrs_string/enableSPChild", "Rolloff/rlf");
	
	// Add the texture statistics
	fnet->addMarSystem(mng.create("TextureStats", "tStats"));

//------------------- Set Parameters ------------------------------
	
	// Set the texture memory size to a 1-second window (22 analysis frames)
	fnet->updctrl("TextureStats/tStats/mrs_natural/memSize", 22);

	// Set the file name
	fnet->updctrl("SoundFileSource/src/mrs_string/filename", argv[1]);
	
	// Set the sample rate to 11250 Hz
	mrs_natural factor = round(fnet->getctrl("SoundFileSource/src/mrs_real/osrate")
		->to<mrs_real>()/11250.0);
	fnet->updctrl("DownSampler/ds/mrs_natural/factor", factor);
	
	// Set the window to 1024 samples at 11250 Hz
	// Should be able to set with simply TimbreFeatures/tf/mrs_natural/winSize,
	// but that doesn't seem to work
	fnet->updctrl("TimbreFeatures/tf/Series/timeDomain/ShiftInput/si/mrs_natural/winSize", 1024);
	fnet->updctrl("TimbreFeatures/tf/Series/spectralShape/ShiftInput/si/mrs_natural/winSize", 1024);
	fnet->updctrl("TimbreFeatures/tf/Series/lpcFeatures/ShiftInput/si/mrs_natural/winSize", 1024);
	
	// Find the length of the song
	mrs_natural slength = fnet->getctrl("SoundFileSource/src/mrs_natural/size")->to<mrs_natural>();
	
	// Find the number of samples resulting in a whole number of analysis windows by truncating
	mrs_natural numsamps = (mrs_natural)(((30*11250.0*factor)/512)*512);

	// Shift the start over so that the duration is in the middle
	mrs_natural start = (slength - numsamps)/2;

	fnet->updctrl("SoundFileSource/src/mrs_natural/start", start);
	fnet->updctrl("SoundFileSource/src/mrs_natural/duration", numsamps);

// ----------------- Accumulator ---------------------------------

	// Accumulate over the entire song
	MarSystem *acc = mng.create("Accumulator", "acc");
		
	// nTimes is measured in number of analysis windows
	acc->updctrl("mrs_natural/nTimes", (mrs_natural)((30*11250.0)/512));

//------------------ Song Statistics -----------------------------
	// Fanout and calculate mean and standard deviation
	MarSystem *sstats = mng.create("Fanout", "sstats");
	sstats->addMarSystem(mng.create("Mean", "smn"));
	sstats->addMarSystem(mng.create("StandardDeviation", "sstd"));

// ----------------- Top Level Network Wrapper -------------------
	
	// (src->downmix->downsample->features->texture stats)
	// --->accumulator->song stats->output
	MarSystem *tnet = mng.create("Series", "tnet");
	acc->addMarSystem(fnet);
	tnet->addMarSystem(acc);
	tnet->addMarSystem(sstats);
	
	// set the hop size to 512 (needs to be set for the top-level network)
	tnet->updctrl("mrs_natural/inSamples", factor*512);

	try {
		// Should only need to tick once
		tnet->tick();
	} catch (int i)
	{
		cout << "Error analyzing file" << endl;
		return 1;
	}

	realvec result = tnet->getctrl("mrs_realvec/processedData")->to<mrs_realvec>();

	try {
		result.normMaxMin();
		result.write(argv[2]);
	} catch (int i)
	{
		cout << "Error writing vector file" << endl;
		return 1;
	}
	
	// Success
	return 0;
}
