

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
	return pls

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

    def init_vectors(self,plugin='charlotte'):
	try:
	    query = self.model.db.query(AudioFile)
	    query.filter_by(state='undone')
	    files = query.all()
	    plugins = self.model.get_plugins(name=plugin)
	    for plugin in plugins:
	      for file in files:
		  self.model.update_vector(plugin,file)


	except Exception,e:
		print 'init_vectors controller.py ',e
