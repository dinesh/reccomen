

from mrec.models.sql import AudioFile,Plugin, Playlist, Cluster, User 
class Controller:

    def __init__(self,model,learner=None):
	self.model = model
	self.learner = learner

    def is_user(self,email,passwd):
	    pass
  
    def add_user(self,email,passwd=None):
	if not passwd: passwd = 'test'
	users = self.model.get_users(email,passwd=passwd)
	if len(users) < 1:
		user = User(email,passwd)
		self.model.save(user)


    def getplaylists_by_user(self, user, playlist=[]):
	    pass

    def add_playlist(self,user, name, audio_files = []):
        pls = self.model.get_playlists(user_id = user.id,name = name)
        if not pls:
            pl = Playlist(name= name, user_id = user.id)
            pl.files.extend(audio_files)
            self.model.save(pl)
            return pl
        for pl in pls:
            pl.add_files(audio_files)

    def get_playlist(self,user_id, name):
	pls = self.model.get_playlists(user_id=user_id,name = name)
	return pls	


    def add_plugin(self,name,module_name):
	plugins = self.model.get_plugins(name=name,module_name=module_name)
	if len(plugins) < 1:
	      plugin = Plugin(name,module_name)
	      self.model.save(plugin)


    def draw_cluster(self):
	    pass



    def add_file(self,file_name,tag):
	files = self.model.get_audio_files(file_name=file_name,tag=tag)
	if len(files) < 1:
		f = AudioFile(file_name,tag)
		self.model.save(f)

    def tag_file(self,file_name,tag):
	  pass

    def update_playlist(self,file_name,user=None):
	  pass

    def initialize_store(self):
	self.model.initialize_storage()  
    
    
    def add_cluster(self,playlist):
      clusters = self.model.get_clusters(playlist.id)
      if len(clusters)<1:
        cl = Cluster(playlist.id)
        # cl.save()
        return cl
      return clusters[0]
    
    def init_vectors(self,plugin='charlotte',limit=10):
      try:
        query = self.model.db.query(AudioFile)
        query = query.filter_by(state='undone').limit(limit)
        files = query.all()
      #  query = self.model.db.query(AudioFile)
      #  query = query.filter_by(vector = None).limit(limit)
       # files.extend(query.all())
        print files
        plugins = self.model.get_plugins(name=plugin)
        for plugin in plugins:
          for file in files:
            po = self.model.update_vector(plugin,file)
            file.vector = po.vector
            file.state = 'done'
            file.save()
           

      except Exception,e:
		       print 'init_vectors controller.py ',e
    
    