import os,sys
from pathlib import Path

folder = ["data","src","data/raw/","data/processed/","data/final/"]

path1=Path(".")

for i in folder:
    print(path1.exists(),i)
    if path1:
        pass
    else : 
        os.chdir(i)