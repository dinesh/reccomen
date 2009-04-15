
if __name__ == "__main__":
	import sys
	import os
	parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	print parent_dir
	if parent_dir not in sys.path:
	      sys.path.append(parent_dir)
	
	import mrec
	import mrec.models
	import mrec.models.sql
	from mrec.models.sql import AudioFile, Plugin
	from mrec.controller import Controller

	model = mrec.models.sql
	controller = Controller(model)

#	controller.initialize_store()
	
	tags = ['alternative','blues','electronic','folkcountry','rock','jazz','raphiphop','pop','funksoulrnb']
	files = model.load_collection(tags)

	for file in files:
	      controller.add_file(file[0],file[1])

	
	plugins = [
		    ('charlotte', 'mrec.analysis_plugins.charlotte'),
		#   ('bextraxt','mrec,analysis_plugins.bextract_plugin'),
		 #   ('centroid','mrec.analysis_plugins.centroid_plugin')
		    ]

	for plugin in plugins:
		controller.add_plugin(plugin[0],plugin[1])
	
#	controller.init_vectors(limit=10)

	# create user
	users = [
		('btp.com','btp'),('dev.com','dev'),
		('prod.com','prod'),('test.com','test')
		]

	for user in users:
		controller.add_user(user[0],user[1])
	
	model.init_vectors(limit=10)