from django.apps import AppConfig
import os
import json
import re
import shutil
from MyFlOp.colors import Tcolors
from pathlib import Path
from django.contrib.staticfiles.management.commands.runserver import Command as RunserverCommand
TEMP_DIR = os.path.join(os.getcwd(),'temp')
LANG_LIST = ["fr","en"]
CLEAR_TEMP_FILES = True

class MyflopConfig(AppConfig):
    name = 'MyFlOp'
    verbose_name = "My Application"
    def ready(self):
        createDiscardFile()
        purgeTempFolder()

def createDiscardFile():
    if os.environ.get('RUN_MAIN') != 'true':
            #lists of discarted files
            corrupted = []
            unavailable_pics = []
            #available languages
            languages = ["fr/","en/"]
            path = 'TTapp/TTConstraints/doc/'
            for language in languages:
                entries = next(os.walk(path+language))[2]
                for file_name in entries:
                    f = open(path+language+file_name,'r')
                    fString = f.read()
                    #Discard files with components tags
                    if((re.findall("<[ ]*component[ ]*",fString))):
                        corrupted.append(file_name)
                    #Discard files with unavailable pics's path
                    else:
                        invalid_path = False
                        founds = re.findall("(?:[!]\[(.*?)\])\((\.\.(.*?))\)",fString)
                        for found in founds:
                            if(not invalid_path):
                                pic = found[2]
                                pathPic = Path(path+pic)
                                if(not pathPic.is_file()):
                                    invalid_path = True
                        if(invalid_path):
                            unavailable_pics.append(file_name)
                    f.close()
            #Warning when a file is corrupted
            if(len(corrupted)>0):
                print("\033[91mWARNING!! Check corrupted files: \033[00m")
                for file in corrupted:
                    print(" - "+file)
                print(" end")
            #Append lists of discarded files and write them in a json
            list_discarded = list(set().union(list(corrupted), list(unavailable_pics)))
            version_json = json.dumps(list_discarded)
            with open("discarded.json",'w') as file:
                file.write('{"discarded": '+version_json+'}')
            file.close()

def purgeTempFolder():
    if(CLEAR_TEMP_FILES):
        for l in LANG_LIST:
            lang_dir_path = os.path.join(TEMP_DIR,l)

            try:
                shutil.rmtree(lang_dir_path)
            except:
                print(Tcolors.WARNING,"Directory",lang_dir_path,"does not exist",Tcolors.ENDC)

            try:
                os.mkdir(lang_dir_path)
            except:
                print(Tcolors.WARNING,"Directory",lang_dir_path,"has not been created")
    else:
        print(Tcolors.WARNING,"Temp directory will not be cleared, you can modify it in : \n","FlopEDT/MyFlOp/apps.py", Tcolors.ENDC)


