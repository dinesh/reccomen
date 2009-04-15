
def addfile(file,tag):
    pass

def usage():
    use = 'python add_files.py [-c collection1,collection2,..] \
    [-l limit] [filename:tag ... [filename:tag]]'
    return use

if __name__ == "__main__":    
    import sys
    import os
    from getopt import getopt
    
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
          sys.path.append(parent_dir)
    
    import mrec
    import mrec.models
    import mrec.models.sql
    from mrec.models.sql import AudioFile, Plugin
    from mrec.controller import Controller

    model = mrec.models.sql
    controller = Controller(model)
    try:
        opts,args = getopt(sys.argv[1:],'ac:l:')
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        print usage()
        sys.exit(2)
    
    collection,limit,analysis = [],10,False
    print opts
    for o,a in opts:
        if o == '-c':
            collection = a.split(',')
        elif o == '-l':
            limit = a
        elif o== '-a':
            analysis = True
    print collection
    
    if collection:
        files = model.load_collection(collection)
        for file in files:
          controller.add_file(file[0],file[1])  
    if analysis:
        controller.init_vectors(limit=20)
            