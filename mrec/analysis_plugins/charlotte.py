from marsyas import *
from numpy import array
import os

mng = MarSystemManager()
fnet = mng.create("Series", "fnet")

def createVector(filename):
    #------------------ Feature Network ------------------------------
    print '\nExtracting Features for => ',filename

    # Decode the file, downmix to mono, and downsample
    fnet.addMarSystem(mng.create("SoundFileSource", "src"))
    fnet.addMarSystem(mng.create("DownSampler", "ds"))
    fnet.addMarSystem(mng.create("Stereo2Mono", "s2m"))

    # Create the feature extractor

    fnet.addMarSystem(mng.create("TimbreFeatures", "tf"))
    fnet.updControl("TimbreFeatures/tf/mrs_string/enableTDChild", MarControlPtr.from_string("ZeroCrossings/zcrs"))
    fnet.updControl("TimbreFeatures/tf/mrs_string/enableSPChild", MarControlPtr.from_string("MFCC/mfcc"))
    fnet.updControl("TimbreFeatures/tf/mrs_string/enableSPChild", MarControlPtr.from_string("Centroid/cntrd"))
    fnet.updControl("TimbreFeatures/tf/mrs_string/enableSPChild", MarControlPtr.from_string("Flux/flux"))
    fnet.updControl("TimbreFeatures/tf/mrs_string/enableSPChild", MarControlPtr.from_string("Rolloff/rlf"))

    # Add the texture statistics
    fnet.addMarSystem(mng.create("TextureStats", "tStats"))

    #------------------- Set Parameters ------------------------------

    # Set the texture memory size to a 1-second window (22 analysis frames)
    fnet.updControl("TextureStats/tStats/mrs_natural/memSize", MarControlPtr.from_natural(22))

    # Set the file name
    fnet.updControl("SoundFileSource/src/mrs_string/filename", MarControlPtr.from_string(filename))

    # Set the sample rate to 11250 Hz
    factor = int(round(fnet.getControl("SoundFileSource/src/mrs_real/osrate").to_real()/11250.0))
    fnet.updControl("DownSampler/ds/mrs_natural/factor", MarControlPtr.from_natural(factor))

    # Set the window to 1024 samples at 11250 Hz
    # Should be able to set with simply TimbreFeatures/tf/mrs_natural/winSize,
    # but that doesn't seem to work
    fnet.updControl("TimbreFeatures/tf/Series/timeDomain/ShiftInput/si/mrs_natural/winSize", MarControlPtr.from_natural(1024))
    fnet.updControl("TimbreFeatures/tf/Series/spectralShape/ShiftInput/si/mrs_natural/winSize", MarControlPtr.from_natural(1024))
    fnet.updControl("TimbreFeatures/tf/Series/lpcFeatures/ShiftInput/si/mrs_natural/winSize", MarControlPtr.from_natural(1024))

    # Find the length of the song
    slength = fnet.getControl("SoundFileSource/src/mrs_natural/size").to_natural()

    if slength is 0:
        raise Exception('InvalidLengthError', "File \"%s\" could not be read." % filename)

    # Find the number of samples resulting in a whole number of analysis windows by truncating
    numsamps = int(((30*11250.0*factor)/512)*512)

    # Shift the start over so that the duration is in the middle
    start = int((slength - numsamps)/2)

    fnet.updControl("SoundFileSource/src/mrs_natural/start", MarControlPtr.from_natural(start))
    fnet.updControl("SoundFileSource/src/mrs_natural/duration", MarControlPtr.from_natural(numsamps))

    # ----------------- Accumulator ---------------------------------

    # Accumulate over the entire song
    acc = mng.create("Accumulator", "acc")

    # nTimes is measured in number of analysis windows
    acc.updControl("mrs_natural/nTimes", MarControlPtr.from_natural(int(((30*11250.0)/512))))

    #------------------ Song Statistics -----------------------------
    # Fanout and calculate mean and standard deviation
    sstats = mng.create("Fanout", "sstats")
    sstats.addMarSystem(mng.create("Mean", "smn"))
    sstats.addMarSystem(mng.create("StandardDeviation", "sstd"))

    # ----------------- Top Level Network Wrapper -------------------

    # (src.downmix.downsample.features.texture stats)
    # --.accumulator.song stats.output
    tnet = mng.create("Series", "tnet")
    acc.addMarSystem(fnet)
    tnet.addMarSystem(acc)
    tnet.addMarSystem(sstats)

    # set the hop size to 512 (needs to be set for the top-level network)
    tnet.updControl("mrs_natural/inSamples", MarControlPtr.from_natural(factor*512))

    # Should only need to tick once
    tnet.tick()

    result = tnet.getControl("mrs_realvec/processedData").to_realvec()
    result.normMaxMin()

    # convert from useless marsyas vector to numpy array to normal python list
    result = array(result) * 100;
    return result.tolist()
    
