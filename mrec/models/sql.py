from sqlalchemy import create_engine, func
from sqlalchemy import Table, Column, Integer, String, PickleType, MetaData, ForeignKey, Float, Boolean
from sqlalchemy.orm import mapper
from sqlalchemy.orm import relation
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from numpy import mean, array, dot, sqrt
import os,sys

import mrec.models.abstract
from mrec.cfg import *

class Database(object):
    __shared_state = {'session': None}

    def createTables(self):
        return self.metadata.create_all(self.engine)

    def dropTables(self):
        return self.metadata.drop_all(self.engine)

    def add(self, object):
        return self.session.add(object)

    def delete(self, object):
        return self.session.delete(object)

    def query(self, *entities, **kwargs):
        return self.session.query(*entities, **kwargs)

    def commit(self):
        return self.session.commit()

    def __create_metadata(self):
        self.metadata = MetaData()

        self.plugins_table = Table(
            'plugins',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(255)),
            Column('module_name', String(255))
        )

        self.output_table = Table(
            'output',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('plugin_id', Integer, ForeignKey('plugins.id')),
            Column('audiofile_id', Integer, ForeignKey('audiofiles.id')),
            Column('vector', PickleType)
        )
	
        self.audiofiles_table = Table(
            'audiofiles',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('file_name', String(255)),
            Column('vector', PickleType),
	    Column('numplayed',Integer,default=0),
	    Column('tag',String(255)),
	    Column('state',String(255),default='undone')
        )
	
	self.users_table = Table(
			'users',
			self.metadata,
			Column('id',Integer,primary_key=True),
			Column('email',String(255)),
			Column('password',String(255)),
			)

	self.clusters_table = Table(
			'clusters',self.metadata,
			Column('id',Integer,primary_key=True),
			Column('radius',Float,default=0.0),
			Column('numsongs',Integer,default=0),
			Column('centriod',PickleType),
			Column('tag',String(255)),
			Column('playlist_id',Integer,ForeignKey('playlist.id'))
			)

        self.playlists_audiofiles = Table(
		       'playlists_audiofiles',self.metadata,
		       Column('playlist_id',Integer,ForeignKey('playlist.id')),
		       Column('audiofile_id',Integer,ForeignKey('audiofiles.id'))
		       )

        self.clusters_audiofiles = Table(
		       'clusters_audiofiles',self.metadata,
		       Column('cluster_id',Integer,ForeignKey('clusters.id')),
		       Column('audiofile_id',Integer,ForeignKey('audiofiles.id'))
		       )
       
        self.playlist_table = Table(
		       'playlist',self.metadata,
		       Column('id',Integer,primary_key=True),
		       Column('name',String(255)),
		       Column('user_id',Integer,ForeignKey('users.id')),
		       Column('vote',Integer),
		       Column('state',String(255))
		       )


    def __create_mappings(self):
        mapper(
            Plugin,
            self.plugins_table
        )
	
        mapper(
            PluginOutput,
            self.output_table,
            properties = {
                'plugin': relation(Plugin, backref='outputs'),
                'file': relation(AudioFile, backref='outputs')
            }
        )

        mapper(
            AudioFile,
            self.audiofiles_table
        )
      
	mapper(
	      User,
	      self.users_table,
	      properties = {
		      'playlists' : relation(Playlist)
		      }
	      )

	mapper(
	      Cluster,
	      self.clusters_table,
	      properties = {
		      'files' : relation(AudioFile,secondary = self.clusters_audiofiles)
		      }
	      )
	mapper(
	      Playlist,
	      self.playlist_table,
	      properties = {
		      'files' : relation(AudioFile,secondary=self.playlists_audiofiles),
		      'clusters' : relation(Cluster)
		      }
	      )


    def __init__(self):
        self.__dict__ = self.__shared_state

        if self.session == None:
	    args = 'mysql://%s:%s@localhost/%s' % (db_user,db_password,db_name)
            self.engine = create_engine(args, echo=False)

            self.__create_metadata();
            self.__create_mappings();

            Session = sessionmaker(bind=self.engine, autoflush=True)
            self.session = Session()


class Saveable(object):
    def save(self):
        if self.id is None:
            db.add(self)

class Plugin(Saveable, mrec.models.abstract.Plugin):
    def createVector(self, audiofile):
	file_name = os.path.join(training_dataset,audiofile.file_name)
        return PluginOutput(self.module.createVector(file_name), self, audiofile)


class AudioFile(Saveable, mrec.models.abstract.AudioFile):
     pass 

class Tag(Saveable, mrec.models.abstract.Tag):
    pass

class Cluster(Saveable, mrec.models.abstract.Cluster):
	pass

class Playlist(Saveable, mrec.models.abstract.Playlist):
	pass

class User(Saveable, mrec.models.abstract.User):
	pass

class PluginOutput(Saveable, mrec.models.abstract.PluginOutput):
    pass


# Global framework variables
db = Database()

def load_collection(tags,depth=25):
    dataset_dir = training_dataset
    list = []
    for tag in tags:
	collection = open(os.path.join(dataset_dir,tag + '.mf'),'r')
	count = 0
	for line in collection: 
		Filename, Tag = line.split()
		count+=1
		list.append((Filename,Tag))
		if count > depth: break 
    return list


def get_tags(name = None):
    """ Return a list of Tag objects. By default returns all tags.

    @param name: return only tags with tag.name matching provided name
    @type  name: unicode
    """
    query = db.query(Tag)
    if name is not None:
        query = query.filter_by(name = name)
    return query.all()

def get_tag(name):
    """ Returns a single Tag object with the provided name.

    If no existing tag is found, a new one is created and returned.

    @param name: the name of the tag object to return
    @type  name: unicode
    """
    query = db.query(Tag).filter_by(name = name)
    try:
        tag = query.one()
    except NoResultFound:
        tag = Tag(name)
        tag.save()

    return tag

def initialize_storage():
    """ Initializes an empty storage environment.

    For a database, this might mean to (re)create all tables.
    """
    # drop the old tables
    db.dropTables()
    # create the fresh tables
    db.createTables()

def get_plugins(name = None, module_name = None):
    """ Return a list of Plugin objects. By default returns all plugins.

    @param name: if provided, returns only plugins with a matching name
    @type  name: unicode

    @param module_name: if provided, returns only plugins with a matching module_name
    @type  module_name: unicode
    """
    query = db.query(Plugin).order_by(Plugin.name)
    if name is not None:
        query = query.filter_by(name = name)

    if module_name is not None:
        query = query.filter_by(module_name = module_name)

    return query.all()

def get_audio_files(file_name=None,tag = None, limit = None):
    """ Return a list of AudioFile objects. By default returns all audio files.
    """

    query = db.query(AudioFile)
    if file_name :
        query = query.filter_by(file_name=file_name)
    if tag: query = query.filter_by(tag=tag)
    if limit: query = query.limit(limit)
    return query.all()

def get_users(email=None,passwd=None):
      query = db.query(User)
      if email: query = query.filter_by(email=email)
      if passwd: query = query.filter_by(password=passwd)

      return query.all()

def get_user(email,passwd):
	try:
	    query = db.query(User).filter_by(email=email,password=passwd)
	    return query.one()
	except Exception,e:
	    print 'getuser in sql.py',e
	    
def get_audio_file(file_name):
    """ Return an AudioFile object. If no existing object is found, returns None.

    @param file_name: the file name of the audio file
    @type  file_name: unicode
    """
    try:
        query = db.query(AudioFile).filter_by(file_name=file_name)
        return query.one()
    except NoResultFound:
        return None

def save(obj):
    """ Save an object to permanent storage.

    @param obj: the object to save
    @type  obj: Saveable
    """
    obj.save()
    db.commit()

def update_vector(plugin, audio_file):
    """ Create or Replace the current PluginOutput object for the
    provided plugin/audio file pair. Saves the PluginObject to storage.

    @param plugin: the plugin object to use
    @type  plugin: Plugin

    @param audio_file: the audio file to run the plugin on
    @type  audio_file: AudioFile
    """
    for old_output in db.query(PluginOutput).filter_by(plugin=plugin,file=audio_file):
        # there should really only be one output with the same file/plugin combo
        db.delete(old_output)
    PO = plugin.createVector(audio_file)
    save(PO)
    return PO

def get_playlists(user_id,name):
	try:
	    query = db.query(Playlist).filter_by(user_id = user_id, name= name)
	    return query.one()
	except Exception,e:
	      print 'get_playlist in sql.py',e
