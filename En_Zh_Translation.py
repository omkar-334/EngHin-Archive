#Install libraries - enter in terminal
#pip install lingua-language-detector argostranslate numpy pandas

# Import Libraries
import argostranslate.package
import argostranslate.translate
import pandas as pd
import numpy as np
from lingua import Language, LanguageDetectorBuilder
import time

start=time.time()

# Language Detection Model
languages = [Language.ENGLISH, Language.CHINESE]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

from_code = "zh"
to_code = "en"

#Language Translation Package
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
available_package = list(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    ))[0]
download_path = available_package.download()
argostranslate.package.install_from_path(download_path)

installed_languages = argostranslate.translate.get_installed_languages()

from_lang = list(filter(
        lambda x: x.code == from_code,
        installed_languages))[0]

to_lang = list(filter(
        lambda x: x.code == to_code,
        installed_languages))[0]

translation = from_lang.get_translation(to_lang)

# Read Excel File
#Specified Column 1 as object to prevent data loss, can specify all columns as object if needed
df=pd.read_excel("Order Export.xls",dtype={0: object})
# Unmerging cells and filling values
df = df.fillna(method='ffill',axis=0)

#Translate Column Headers
def translate_headers(df : pd.DataFrame) -> pd.DataFrame :
    new_columns=list(map(lambda x:translation.translate(str(x)),df.columns))
    df.columns=new_columns
    return df

df=translate_headers(df)
cols=list(df.columns)
#Changed Column name to ensure Unique column names
cols[3]='Name of Company'
df.columns=cols


# Function to detect columns which have Chinese language
#There are 49 columns and we don't need to translate all of them
# Enabled vectorization to avoid iteration
def detect_lingua(text : str) -> str :
    res=[result.language.iso_code_639_1.name for result in detector.detect_multiple_languages_of(str(text))]
    if 'ZH' in res:
        return 'zh'
detect_lingua=np.vectorize(detect_lingua)


ctr=0
zh_cols=[]
for i in df:
    temp2=detect_lingua(df[i])
    if 'zh' in temp2:
        zh_cols+=[i]
        ctr+=1
# ctr = 13, there are 13 columns with chinese language
# zh_cols is a list of chinese columns

# Vectorized function to translate from Chinese to English
def translate_str(x : str) -> str :
    if x is not np.nan:
        return translation.translate(str(x))
vectrans=np.vectorize(translate_str)

# Mapping translate_str function to df[zh_cols]
df[zh_cols]=df[zh_cols].map(lambda x:vectrans(x))

#Writing to excel file
df.to_excel("output.xlsx")
print(f"Time taken - {round(time.time()-start,2)} seconds")


# Test results

#Time taken - 130.66 seconds
#Time taken - 142.90 seconds
#Time taken - 136.34 seconds
