import mad
import ID3


def generate_list(name="songs_list.m3u", path=".", files=[],
                  sort=True, walk=False):
    """ generates the M3U playlist with the given file name

    and in the given path """

    fp = None
    try:
        try:
            if not files:
                if walk:
                # recursive version
                    mp3_list = [os.path.join(root, i) for root, dirs, files in os.walk(path) for i in files \
                            if i[-3:] == "mp3"]
                else:
                # non recursive version
                    mp3_list = [i for i in os.listdir(path) if i[-3:] == "mp3"]
            else:
                mp3_list = files
            #print mp3_list

            if sort:
                mp3_list.sort()

            fp = file(name, "w")
            fp.write(FORMAT_DESCRIPTOR + "\n")

            for track in mp3_list:
                if not walk:
                    track = os.path.join(path, track)
                else:
                    track = os.path.abspath(track)
                # open the track with mad and ID3
                mf = mad.MadFile(track)
                id3info = ID3.ID3(track)
        
                # M3U format needs seconds but
                # total_time returns milliseconds
                # hence i convert them in seconds
                track_length = mf.total_time() / 1000
        
                # get the artist name and the title
                artist, title = id3info.artist, id3info.title

                # if artist and title are there
                if artist and title:
                    fp.write(RECORD_MARKER + ":" + str(track_length) + "," +\
                             artist + " - " + title + "\n")
                else:
                    fp.write(RECORD_MARKER + ":" + str(track_length) + "," +\
                             os.path.basename(track)[:-4] + "\n")

                # write the fullpath
                fp.write(track + "\n")
                
        except (OSError, IOError), e:
            print e
    finally:
        if fp:
            fp.close()



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
    from mrec import utils
    from heapq import  nlargest,nsmallest
    from pprint import PrettyPrinter
    
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
        limit = iter+1 
        frock = model.get_audio_files(tag='rock',limit= limit)
        fpop = model.get_audio_files(tag='pop',limit= limit )
        fjazz = model.get_audio_files(tag='jazz',limit= limit)
        fblues = model.get_audio_files(tag='blues',limit = limit)
        frap = model.get_audio_files(tag='raphiphop',limit= limit)
        felec = model.get_audio_files(tag='electronic',limit= limit)
        ffolk = model.get_audio_files(tag='folkcountry',limit= limit)
        #ffunk = model.get_audio_files(tag='funksoulrnb',limit=limit)
        falter = model.get_audio_files(tag='alternative',limit= limit)
    
        files = [frock,fpop,fjazz,fblues,frap,felec,ffolk,falter]
        files = [falter,frock,felec] 
#        playlists = []
#        for Files in files:
#            n = raw_input('press Enter')
#            pl = controller.add_playlist(user,name = str(random.randint(1,10000)))
#            pl.add_files(Files)
#            pl.start_clustering()
#            print '\n-------------\nFor ',Files[0].tag,len(Files)
#            print 'clusters==> ',len(pl.clusters),'\n'
#            for cl in pl.clusters:
#                print 'radius ',cl.radius
#            playlists.append(pl)
#            recs = user.recommend([pl],topN=5)
#            for score,file in recs:
#                print score,'\t\t',file
#            
        ## calculating Genre similarity
#        scores = {}
#        for pl in playlists:
#            print '---------------for ',pl.files[0].tag
#            gscores = []
#            scores[pl.files[0].tag] = {}
#            for pl2 in playlists:
#                scores[pl.files[0].tag][pl2.files[0].tag] = 0
#                if pl != pl2:
#                    sum = 0
#                    for cl in pl.clusters:
#                        largest,smallest = -1,1000
#                        for cl2 in pl2.clusters:
#                            dist = utils.getDistance(cl.centroid,cl2.centroid)*100
#                            sum += dist
#                            if dist > largest: largest = dist
#                            if dist < smallest: smallest = dist
#                    #print pl.files[0].tag,pl2.files[0].tag,largest,smallest,sum/(len(pl.clusters)+ len(pl2.clusters))
#                    #print pl2.files[0].tag,sum/(len(pl.clusters)+ len(pl2.clusters))
#                    gscores.append((pl2.files[0].tag,sum/(len(pl.clusters)+ len(pl2.clusters))))
#                    scores[pl.files[0].tag][pl2.files[0].tag] = sum/(len(pl.clusters)+ len(pl2.clusters))
#                    print
#            print nlargest(8,gscores,key=lambda x:x[1])
#            print nsmallest(8,gscores,key=lambda x:x[1])
#            print '\n***********************\n'
#            
#            p = PrettyPrinter(10)
#            p.pprint(scores)
        pl = controller.add_playlist(user, name= str(random.randint(1,1000)) )
        
        for Files in files:
            pl.add_files(Files)
            

        print len(pl.files)
        pl.start_clustering()
        print pl.clusters,len(pl.files)
        r = 0.0
        for cl in pl.clusters:
            print cl.radius
            r += cl.radius
        rmax = r
        print '------------------------------'
        print 'For ',Files[0].tag,rmax
        print 'cluster==> ',len(pl.clusters),'for ',r,'\n'
        for file in pl.files:
            print file
        print
        recs = user.recommend(playlists=[pl],topN=10)
        for score,file in recs:
                print score,'\t\t',file
    