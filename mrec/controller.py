
class Controller:

    def __init__(self,model,learner=None):
	self.model = model
	self.learner = learner

    def is_user(self,email,passwd):
	    pass

    def getplaylist_by_user(self, user, playlist=[]):
	    pass
    
    def addfile_to_playlist(self,user,file_name):
	    pass

    def add_plugin(self,name,module_name):
	print name,module_name 

    def draw_cluster(self):
	    pass


    def add_file(self,file_name,tag):
	    pass

    def tag_file(self,file_name,tag):
	  pass

    def update_playlist(self,file_name,user=None):
	  pass

    def initialize_store(self):
	self.model.initialize_storage()  

     
