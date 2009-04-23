

indir = '/home/dinesh/important/mir/simreco/audio'
outdir = '/home/dinesh/music'
import os
import sys
import subprocess

if __name__ == "__main__":
    if not indir: sys.exit(2)
    if not os.path.exists(outdir): os.mkdir(outdir)
    
    for root, dirs, files in os.walk(indir):
        for dir in dirs: 
            path = os.path.join(outdir,dir)
            if not os.path.exists(path): os.mkdir(path)
        
        for file in files:
            outfile = os.path.join(outdir,root.split('/')[-1:][0], file[:-4] + '.wav')
            #print outfile
            if file[-3:] == 'mp3':
                args = ['sox', os.path.join(root,file), outfile]
                if not os.path.exists(outfile):
                    p = subprocess.Popen(args,stdout=subprocess.PIPE,stderr = subprocess.PIPE)
                    out,err = p.communicate()
                    print out,err
                
        
         
    