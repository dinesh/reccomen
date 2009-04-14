
import os
from mrec import utils

class Plugin(object):
    """
    Plugin Object

    Attributes:
        name
        module_name
        outputs

    Methods:
        createVector
    """

    def __init__(self, name, module_name):
        self.name = name
        self.module_name = module_name
        self.outputs = []

    def __getattr__(self, name):
        if name == "module":
            # Lazy load the plugin module
            if "module" not in self.__dict__:
		print self.module_name
                mod = __import__(self.module_name)
                components = self.module_name.split('.')
                for comp in components[1:]:
                    mod = getattr(mod, comp)
                self.__dict__["module"] = mod
            return self.__dict__["module"]
        else:
            return object.__getattr__(name)


    def __repr__(self):
        return "<Plugin('%s','%s')>" % (self.name, self.module_name)

    def createVector(self, audiofile):
        return PluginOutput(self.module.createVector(audiofile.file_name), self, audiofile)


class AudioFile(object):
    """
    Audio File Object

    Attributes:
        name
        vector
        tag
        generated_tags
    """

    def __init__(self, file_name,tag=None):
        self.file_name = file_name
        self.vector = []
        self.tag = tag
    

    def __repr__(self):
        return "<AudioFile('%s')>" % (self.file_name)


class Tag(object):
    """
    Tag Object

    Attributes:
        name
        files
        vector
    """

    def __init__(self, name):
        self.name = name
        self.vector = []
	
    def __repr__(self):
        return "<Tag('%s')>" % (self.name)


class PluginOutput(object):
    """
    Object to represent the output of a plugin

    Attributes:
        vecfile
        plugin
        file
    """

    def __init__(self, vector, plugin, audiofile):
      self.vector = vector
      self.plugin = plugin
      self.file = audiofile

    def __repr__(self):
        return "<PluginOutput('%s')>" % (self.vector)

class User(object):
    
    def __init__(self,email,password):
	self.email = email
	self.password = password
	self.playlists = []
	
    def getrecommendations(self,top=10):
	"""
	Return Top-N recommendation
	"""

	pass



class Cluster(object):
      cutoff = 0.001
      initial = 1

      def __init__(self,playlist_id,files= [],tag= None):
        
        self.playlist_id = playlist_id
        self.tag = tag
        self.radius = 0
        self.files = files
        self.centroid  = self.calculateCentroid()



      def calculateRadius(self):
        max = -1
        for p in self.files:
            dist = utils.getDistance(self.centroid,p.vector)
            if dist > max: max = dist
                
        self.radius = max
        return max
        
      def addfiles(self,files):
          for file in files:
              if file not in self.files:
                  self.files.append(file)      
      
      def calculateCentroid(self): 
          if self.files:
              centroid = []
              n = len(self.files[0].vector)
          
              for i in range(n):
                  centroid.append(0.0)
                  for p in self.files:
                      centroid[i] = centroid[i] + p.vector[i]
                  centroid[i] = centroid[i]/len(self.files)
              
              return centroid   
          return [] 
              
      def getfiles(self): pass
      def updateclusters(self):pass      

class Playlist(object):
      state = 'unclustered'
      def __init__(self,name, user_id,files=[]):
	  self.user_id = user_id
	  self.files = files
	  self.name = name
	  self.clusters = []

      def addfiles(self,files): 
	  self.files.extend[file_name]

      

def get_tags(name = None):
    """ Return a list of Tag objects. By default returns all tags.

    @param name: return only tags with tag.name matching provided name
    @type  name: unicode
    """
    pass

def get_tag(name):
    """ Returns a single Tag object with the provided name.

    If no existing tag is found, a new one is created and returned.

    @param name: the name of the tag object to return
    @type  name: unicode
    """
    pass

def initialize_storage():
    """ Initializes an empty storage environment.

    For a database, this might mean to (re)create all tables.
    """
    pass

def get_plugins(name = None, module_name = None):
    """ Return a list of Plugin objects. By default returns all plugins.

    @param name: if provided, returns only plugins with a matching name
    @type  name: unicode

    @param module_name: if provided, returns only plugins with a matching module_name
    @type  module_name: unicode
    """
    pass

def get_audio_files(file_name=None, tag_names=None, include_guessed=False):
    """ Return a list of AudioFile objects. By default returns all audio files.

    @param file_name: if provided, returns only files with a matching file name
    @type  file_name: unicode

    @param tag_names: if provided, returns only files with at least one of the provided tags
    @type  tag_names: list of unicode objects

    @param include_guessed: if provided, when looking for matching tags, includes generated_tags in the search
    @type  include_guessed: bool
    """
    pass

def get_audio_file(file_name):
    """ Return an AudioFile object. If no existing object is found, returns None.

    @param file_name: the file name of the audio file
    @type  file_name: unicode
    """
    pass

def save(obj):
    """ Save an object to permanent storage.

    @param obj: the object to save
    @type  obj: Saveable
    """
    pass

def update_vector(plugin, audio_file):
    """ Create or Replace the current PluginOutput object for the
    provided plugin/audio file pair. Saves the PluginObject to storage.

    @param plugin: the plugin object to use
    @type  plugin: Plugin

    @param audio_file: the audio file to run the plugin on
    @type  audio_file: AudioFile
    """
    pass

