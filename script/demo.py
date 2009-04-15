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
    limit = 25
    frock = model.get_audio_files(tag='rock',limit=limit)
    fpop = model.get_audio_files(tag='pop',limit=limit)
    fjazz = model.get_audio_files(tag='jazz',limit=limit)
    fblues = model.get_audio_files(tag='blues',limit=limit)
    frap = model.get_audio_files(tag='raphiphop',limit=limit)
    felec = model.get_audio_files(tag='electronic',limit=limit)
    ffolk = model.get_audio_files(tag='folkcountry',limit=limit)
    ffunk = model.get_audio_files(tag='funksoulrnb',limit=limit)
    falter = model.get_audio_files(tag='alternative',limit=limit)
    
    files = [frock,fpop,fjazz,fblues,frap,felec,ffolk,ffunk,falter]
    
    ## Get user
    user = model.get_user('btp.com','btp')
    
    ## Make playlist
    
    iter = 2
    for i in range(1,iter):
        rmax = 0
        for Files in files:
            #pl = controller.add_playlist(user,Files[0].tag,audio_files=Files)
            pl = model.get_playlists(user.id,Files[0].tag)[0]
            pl.start_clustering(iter=i)
            #print pl.clusters
            r = 0.0
            for cl in pl.clusters:
                print cl.radius
                r += cl.radius
            print 'cluster==> ',i,'for ',len(pl.clusters),Files[0].tag,r/(len(pl.clusters)),'\n'
            rmax += r
        print rmax/9
        print '------------------------------'
    user.recommend()
    