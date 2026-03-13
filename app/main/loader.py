# load data from json files


import os  # to know how mmuch langages e have
import json
import glob


langs = os.listdir("app/static/imgs/langs/")


def getLangs():
    return [image.replace(".svg","") for image in langs]
