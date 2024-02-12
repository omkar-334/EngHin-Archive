import json
import re
import numpy as np
import pandas as pd
import os
import codecs

path="C:\\Users\\omkar\\Downloads\\archive\\hindilyrics\\"
lyrics=pd.DataFrame({"Hindi":[]})

c=0
for i in os.listdir(path):
    temp = codecs.open(path+i, encoding = 'utf-8').read()
    lyrics.loc[c]=temp
    c+=1
print(lyrics.head())
lyrics.to_csv("Lyrics_db1.csv")
