
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
	model.populate_store(tags,depth=25)
	
	plugins = [
		    ('charlotte', 'mrec.analysis_plugins.charlotte'),
		#   ('bextraxt','mrec,analysis_plugins.bextract_plugin'),
		 #   ('centroid','mrec.analysis_plugins.centroid_plugin')
		    ]

	for plugin in plugins:
		controller.add_plugin(plugin[0],plugin[1])
	
	controller.init_vectors()

	# create user

	# create playlist


	# create playlists



	# analysis + run kmean


	# write to database


	# score the top-N items



	# list them and show cluster


		      
