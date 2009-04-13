from marsyas import *
from numpy import array, mean

def createVector(filename):
    mng = MarSystemManager()
    net = mng.create("Series", "net")

    # Create the centroid network
    net.addMarSystem(mng.create("SoundFileSource", "src"))
    net.addMarSystem(mng.create("Windowing", "ham"))
    net.addMarSystem(mng.create("Spectrum", "spk"))
    net.addMarSystem(mng.create("PowerSpectrum", "pspk"))
    net.addMarSystem(mng.create("Centroid", "cntrd"))
    net.addMarSystem(mng.create("Memory", "mem"))
    net.addMarSystem(mng.create("Mean", "mean"))

    # Update the filename control for the centroid network
    net.updControl("SoundFileSource/src/mrs_string/filename", MarControlPtr.from_string(filename))

    vectors = []
    # Loop through the audio file until it reaches the end
    while (net.getControl("SoundFileSource/src/mrs_bool/notEmpty").to_bool()):

        # Tick the audio samples with each loop
        net.tick()

        # Obtain centroid values for this frame
        result = net.getControl("mrs_realvec/processedData").to_realvec()
        vectors.append(result[0])

    average = mean(array(vectors)) * 100

    return [average]

