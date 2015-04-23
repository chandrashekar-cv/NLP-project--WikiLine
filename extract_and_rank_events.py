#!/usr/bin/python
import os
import sys
import popen2
import time
import re
import glob

from tarsqi import TarsqiControl
from ttk_path import TTK_ROOT
from demo.display import HtmlGenerator
from docmodel.model import DocumentModel
from docmodel.xml_parser import Parser
from library.tarsqi_constants import PREPROCESSOR, GUTIME, EVITA, SLINKET, S2T
from library.tarsqi_constants import CLASSIFIER, BLINKER, CLASSIFIER, LINK_MERGER
import nltk
from nltk.tag.stanford import NERTagger
#from mysql import MySqlWrapper
from get_score import *
import json

from utility import *

OUTPUT_FOLDER="wikipedia/json_output/"

class Event:
    def __init__(self, date, event_name, description, entities, image):
        self.date = date
        self.event_name = event_name
        self.description = description
        self.entities = entities
        self.image = image

    def get_date(self):
        return self.date

    def get_json(self):
        event = {}
        event["date"] = str(self.date)[0:4]
        event["name"] = self.description.strip()
        event["bold"] = self.entities
        event["img"] = self.image 
        return event

class Sentence:
    def __init__(self, description, events, times):
        self.events = events
        self.description = description
        self.times = times


def extract_and_rank_events(xml_file, category, max_no_events):
    generator = HtmlGenerator(input_file)
    title = generator.xmldoc.get_tags("DOC-ID")[0].get_next().get_content().strip()
    
    categories = [cat.get_next().get_content() for cat in generator.xmldoc.get_tags("CATEGORY")]
    if category not in categories:
        return []
    
    sentences = []
    
    for sentence in generator.sentences:
        output = ""
        events = []
        times = []
        for element in sentence.elements:
            if element.is_opening_tag():
                if element.tag == 'EVENT':
                    event = element.attrs['text']
                    events.append(event)
                elif element.tag == 'TIMEX3':
                    try:
                        year = element.attrs['VAL']
                        year = int(year)
                        if year > 1900:
                            times.append(year)
                    except Exception, e:
                        pass
            elif element.is_closing_tag():
                if element.tag in ('EVENT', 'TIMEX3'):
                    pass
            else:
                output = output + element.content
                if element.content == ".":
    
                    #replace &amp; quot ; with "
                    #some strange reason " is replaced with &amp; quot ;   
                    output = output.replace("&amp; quot ;","\"")
    
                    if len(times) != 0 and len(events) != 0:
                        sentences.append(Sentence(output, events, times))
    
                    events = []
                    times = []
                    output = ""
    
    event_descriptions = [event.description for event in sentences]
    scores = get_scores(event_descriptions, category)
    event_score_pair = [(index, score) for index,score in enumerate(scores)]
    sorted_scores = sorted(event_score_pair, key=operator.itemgetter(1))
    
    sorted_events = []
    result = {"events":[]}
    for index, score in sorted_scores:
        sentence = sentences[i]
        event = {}
        event["date"] = str(sentence.times[0])
        event["name"] = sentence.description
        event["bold"] = []
        event["img"] = "1.png"
        result["events"].append(event) 

    return json.dumps(result)
       
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("./extract_and_rank_events.py category xml")
        sys.exit(0)

    category = sys.argv[1].strip()
    input_file = sys.argv[2].strip()
    generator = HtmlGenerator(input_file)
    title = generator.xmldoc.get_tags("DOC-ID")[0].get_next().get_content().strip()

    categories = [category.get_next().get_content().strip() for category in generator.xmldoc.get_tags("CATEGORY")]

    sentences = []

    for sentence in generator.sentences:
        output = ""
        events = []
        times = []
        for element in sentence.elements:
            if element.is_opening_tag():
                if element.tag == 'EVENT':
                    event = element.attrs['text']
                    events.append(event)
                elif element.tag == 'TIMEX3':
                    try:
                        year = element.attrs['VAL']
                        year = int(year)
                        if year > 1900:
                            times.append(year)
                    except Exception, e:
                        pass
            elif element.is_closing_tag():
                if element.tag in ('EVENT', 'TIMEX3'):
                    pass
            else:
                output = output + element.content
                if element.content == ".":

                    #replace &amp; quot ; with "
                    #some strange reason " is replaced with &amp; quot ;   
                    output = output.replace("&amp; quot ;","\"")

                    if len(times) != 0 and len(events) != 0:
                        sentences.append(Sentence(output, events, times))

                    events = []
                    times = []
                    output = ""

    event_descriptions = [event.description for event in sentences]
    scores = get_scores(event_descriptions, category)
    event_score_pair = [(index, score) for index,score in enumerate(scores)]
    sorted_scores = sorted(event_score_pair, key=operator.itemgetter(1))
    
    sorted_events = []
    result = {"events":[]}
    for index, score in sorted_scores:
        sentence = sentences[i]
        event = {}
        event["date"] = str(sentence.times[0])
        event["name"] = sentence.description
        event["bold"] = []
        event["img"] = "1.png"
        result["events"].append(event)
    print json.dumps(result)
        

