
if __name__ == "__main__":
    import sys
    import os
    import numpy,pickle
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print parent_dir
    if parent_dir not in sys.path:
          sys.path.append(parent_dir)
    
    import mrec
    import mrec.models
    import mrec.models.sql
    from mrec.models.sql import AudioFile, Plugin
    from mrec.controller import Controller
    from mrec import cfg
    
    model = mrec.models.sql
    controller = Controller(model)
    
    files = model.get_audio_files()
    store_dir = cfg.vector_storage
    dir = os.getcwd()
    os.chdir(store_dir)
    for file in files:
        vector,name = file.vector,file.file_name
        tagdir = os.path.dirname(name)
        if not os.path.exists(tagdir): os.mkdir(tagdir)
        vecfile = name + '.vec'
        if os.path.exists(vecfile): os.unlink(vecfile)
        numpy.array(vector).tofile(vecfile)
        
    os.chdir(dir)
    
      