#import libraries
import os
import json
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
import glob
import random
from collections import defaultdict
import pandas as pd

#Dataset Path
path="/home/neha/Desktop/News_Name_Entity1/"





def extract_entities(json_text):
 try:
   for item in json_text:
     for k,v in item.items():
       
       description= v['description']

           
       doc = nlp(description)
       for ent in doc.ents:
         
            if ent.label_=="PERSON":
              new=ent.text
              docs = list(nlp.pipe(list(new), disable=['ner']))
             
              (beams, not_relevant) = nlp.entity.beam_parse(docs, beam_width=16, beam_density=0.0001)


              for beam in beams:
               for score, ents in nlp.entity.moves.get_beam_parses(beam):
                
                  entity_scores = defaultdict(float)
                  for start, end, label in ents:
                    if label=="PERSON":
                    

                         entity_scores[(start, end, label)] += score
              for k,v in entity_scores.items():
          
                print ('entity_name:',ent.text + "  entity_score:",str(v))

 except Exception as e:
    print(e)
 return True



try:
 folders=[]

 json_text=[]
 for r, d, f in os.walk(path):
    for folder in d:
       folders.append(os.path.join(r, folder))

       for f in folders:
         files = [f for f in glob.glob(path + "**/*.json")]
         for f in files:
            
             json2 = json.load(open(f))
             json_text.append(json2)



           
except:
    print('bad json: ')


extract_entities(json_text)




