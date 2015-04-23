#!/usr/bin/python
import sys
import os
from lxml import etree
import json
from extract_and_rank_events import *
import subprocess

FILE_WITH_ARTICLES="wikipedia/articles"
ARTICLE_FOLDER="wikipedia/output_1"
JSON_FOLDER="wikipedia/json"
TMP_FOLDER = "tmp"
IGNORE_CATEGORIES = ['Living people']
num_category = 0
category_id_dict = {}
reverse_cat_dict = {}

def get_categories(xml_file):
    global num_category
    tree = etree.parse(xml_file)
    root = tree.getroot()
    categories = []
    for entry in root.find('CATEGORIES'):
        category = entry.text
        category = category.strip()
        if category in IGNORE_CATEGORIES:
            continue
        if category not in category_id_dict:
            num_category += 1
            category_id_dict[category] = num_category
            reverse_cat_dict[num_category] = category
        cat_id = category_id_dict[category]
        categories.append(cat_id)

    doc_id = root.findtext('DOC-INDEX')
    return doc_id, categories

def get_categories_of_article(article_name):
    xml_file = os.path.join(ARTICLE_FOLDER, article_name + ".xml")
    return get_categories(xml_file)

#global json
# {"articles":[{"name":name, "id":id}]}
def write_global_json(article_id_dict):
    articles = {}
    articles["articles"] = []
    for article_id in article_id_dict:
        article_name = article_id_dict[article_id]
        articles["articles"].append({"name":article_name, "id":article_id})
   
    file_name = os.path.join(JSON_FOLDER, "global.json")
    open(file_name, "wb").write(json.dumps(articles)) 

def write_article_json(article_id, categories, cat_id_dict):
    result = {}
    result["categories"] = []
    print(cat_id_dict)
    for cat in categories: 
        cat_id = cat_id_dict[cat]
        result["categories"].append({"name":cat, "id":cat_id})
    file_name = os.path.join(JSON_FOLDER, "article_"+str(article_id)+".json")
    open(file_name, "wb").write(json.dumps(result))

#article json
#file name is <article id>.json
#{ categories:[{"name":name, "id":id}]}

#event json 
#name: articleid_catid.json   
if __name__ == "__main__":
    try:
        os.makedirs(JSON_FOLDER)
    except Exception as e:
        pass

    try:
        os.makedirs(TMP_FOLDER)
    except Exception as e:
        pass

    article_names = open(FILE_WITH_ARTICLES).readlines()
    article_id_dict = {}
    reverse_id_dict = {}
    for article_name in article_names: 
        article_name = article_name.strip()
        article_id, category_ids = get_categories_of_article(article_name)
        write_article_json(article_id, category_ids, reverse_cat_dict)
        article_id_dict[article_id] = article_name
        article_file_name = os.path.join(ARTICLE_FOLDER, article_name+".xml") 
        command = "/usr/bin/python tarsqi.py simple-xml pipeline=PREPROCESSOR,GUTIME,EVITA \"%s\" \"%s/%s.xml\" 1>/dev/null 2>&1"%(article_file_name, TMP_FOLDER, article_name)
        print command
        return_code = subprocess.call(command, shell=True)
        print("ret=", return_code)
        for cat_id in category_ids:
            cat_name = reverse_cat_dict[cat_id]
            file_name = os.path.join(TMP_FOLDER , article_name + ".xml") 
            print("tmp=" + file_name)
            result = extract_and_rank_events(file_name, cat_name, 1000)
            file_name = os.path.join(JSON_FOLDER, "event_" + article_id + "_"+ str(cat_id) + ".xml")
            open(file_name, "wb").write(result)

    write_global_json(article_id_dict)
