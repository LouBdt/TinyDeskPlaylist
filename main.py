import scrapetube
from pytube import YouTube
import re

videos = scrapetube.get_channel("UC4eYXhJI4-7wSWc8UNRwD4A")

c = 0
everything = []
for video in videos:
    video = YouTube("https://www.youtube.com/watch?v="+video["videoId"])
    try:
        titre = video.title
        artiste = re.split(":|\|", titre)[0]
        try:
            desc = video.description
            desc = desc.split()
            tot = len(desc)
            i = 0
            tiny = False
            
        
            
            while i< len(desc)-1:
                if desc[i].lower()=="set" and desc[i+1].lower()=="list":
                    tiny = True
                    break
                i+=1
                
            
            if tiny:
                print(artiste)
                c+=1
                titres = []
                j = i+1
                compte_titres = 0
                
                desc = ' '.join(desc[j:])
                desc = re.split('\" \"|” “|\" • \"', desc)
                desc[0] = re.split('\"|“', desc[0])
                desc[0] = desc[0][1]
                
                for part in desc:
                    if len(re.split('\"|”', part))>1:
                        desc[-1] = re.split('\"|”', part)[0][:25]
                print(desc)
                everything.append([artiste, len(desc), desc])
                
        except:
            pass
    except:
        pass
    
    
with open('setlists.txt', 'w') as f:
    for artiste in everything:
        for titre in artiste[2]:
            f.write(artiste[0]+' '+titre+'\n')
            
            
    