# bextract implemented using the swig python Marsyas bindings
# Modified (December 2008) by Matt Pierce and Anthony Theocharis,
# from code by George Tzanetakis (January, 16, 2007)

import marsyas
from numpy import array

# Create top-level patch
mng = marsyas.MarSystemManager()

def createVector(filename):

    fnet = mng.create("Series", "featureNetwork")

    # Add the MarSystems
    fnet.addMarSystem(mng.create("SoundFileSource", "src"))
    fnet.addMarSystem(mng.create("TimbreFeatures", "featExtractor"))
    fnet.addMarSystem(mng.create("TextureStats", "tStats"))

    # update controls to setup things
    fnet.updControl("TimbreFeatures/featExtractor/mrs_string/disableTDChild", marsyas.MarControlPtr.from_string("all"))
    fnet.updControl("TimbreFeatures/featExtractor/mrs_string/disableLPCChild", marsyas.MarControlPtr.from_string("all"))
    fnet.updControl("TimbreFeatures/featExtractor/mrs_string/disableSPChild", marsyas.MarControlPtr.from_string("all"))
    fnet.updControl("TimbreFeatures/featExtractor/mrs_string/enableSPChild", marsyas.MarControlPtr.from_string("MFCC/mfcc"))
    fnet.updControl("SoundFileSource/src/mrs_string/filename", marsyas.MarControlPtr.from_string(filename))

    # do the processing extracting MFCC features and writing to weka file
    while fnet.getControl("SoundFileSource/src/mrs_bool/notEmpty").to_bool():
        fnet.tick()

    result = fnet.getControl("mrs_realvec/processedData").to_realvec()

    # use numpy to generate a list from the realvec
    return array(result).tolist()

