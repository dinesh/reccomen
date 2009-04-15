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
    
    
    ## Make demo dataset 
    
    
    # Take 25 samples of each genres
    frock = model.get_audio_files(tag='rock',limit=25)
    fpop = model.get_audio_files(tag='pop',limit=25)
    fjazz = model.get_audio_files(tag='jazz',limit=25)
    fblues = model.get_audio_files(tag='blues',limit=25)
    frap = model.get_audio_files(tag='raphiphop',limit=25)
    felec = model.get_audio_files(tag='electronic',limit=25)
    
    files = [frock,fpop,fjazz,fblues,frap,felec]
    
    ## Get user
    user = model.get_user('btp.com','btp')
    
    ## Make playlist
    for i in range(1,2):
        for Files in files:
            # pl = controller.add_playlist(user,Files[0].tag,audio_files=Files)
            pl = model.get_playlists(user.id,Files[0].tag)[0]
    
            pl.start_clustering(iter=i)
            print pl.clusters
#            r = 0.0
#            for cl in pl.clusters:
#                r += cl.radius
#            print 'cluster==> ',i,'for ',len(Files),Files[0].tag,r/i,'\n'