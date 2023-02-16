from django.apps import AppConfig
import os
import json
from django.contrib.staticfiles.management.commands.runserver import Command as RunserverCommand

class MyflopConfig(AppConfig):
    name = 'MyFlOp'
    verbose_name = "My Application"
    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            corrupted = []
            found = False
            languages = ["fr/","en/"]
            path = 'TTapp/TTConstraints/doc/'
            for language in languages:
                entries = next(os.walk(path+language))[2]
                for file_name in entries:
                    f = open(path+language+file_name)
                    for line in f :
                        if (('< script' or '<script') in line) and not found:
                            found = True
                            corrupted.append(file_name)
                    found = False
                    f.close()
            if(len(corrupted)>0):
                print("\033[91mWARNING!! Check corrupted files: \033[00m")
                for file in corrupted:
                    print("- "+file)
                print("end")
            version_json = json.dumps(corrupted)
            with open("corrupted.json",'w') as file:
                file.write('{"corrupted": '+version_json+'}')
            file.close()
