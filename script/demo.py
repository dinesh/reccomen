if __name__ == "__main__":
    import sys
    import os
    import random
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
    
    ## Get user
    user = model.get_user('btp.com','btp')
    
    ## Make playlist
    iter = 2
    for i in range(1,iter):
        rmax = 0
        limit = 50
        frock = model.get_audio_files(tag='rock',limit=1)
        fpop = model.get_audio_files(tag='pop',limit=1)
        fjazz = model.get_audio_files(tag='jazz',limit=20)
        fblues = model.get_audio_files(tag='blues',limit=1)
        frap = model.get_audio_files(tag='raphiphop',limit=20)
        felec = model.get_audio_files(tag='electronic',limit=1)
        ffolk = model.get_audio_files(tag='folkcountry',limit=1)
        #ffunk = model.get_audio_files(tag='funksoulrnb',limit=limit)
        falter = model.get_audio_files(tag='alternative',limit=1)
    
        files = [frock,fpop,fjazz,fblues,frap,felec,ffolk,falter]
    
        pl = controller.add_playlist(user, name= str(random.randint(1,1000)) )
        
        for Files in files:
            pl.add_files(Files)
            

        
        pl.start_clustering()
        #print pl.clusters,len(pl.files)
        r = 0.0
        for cl in pl.clusters:
            #print cl.radius
            r += cl.radius
        rmax = r
        print '------------------------------'
        #print 'For ',Files[0].tag,rmax
        print 'cluster==> ',len(pl.clusters),'for ',r,'\n'
        user.recommend(playlists=[pl])
    