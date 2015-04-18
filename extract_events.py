#!/usr/bin/python
import os
import sys
import popen2
import time
import re

from tarsqi import TarsqiControl
from ttk_path import TTK_ROOT
from demo.display import HtmlGenerator
from docmodel.model import DocumentModel
from docmodel.xml_parser import Parser
from library.tarsqi_constants import PREPROCESSOR, GUTIME, EVITA, SLINKET, S2T
from library.tarsqi_constants import CLASSIFIER, BLINKER, CLASSIFIER, LINK_MERGER
import nltk
from nltk.tag.stanford import NERTagger
import jsonrpclib
import simplejson
from mysql import MySqlWrapper
server = jsonrpclib.Server("http://localhost:8080")


def get_json(events, times, sentence, named_entities):
    result = {}
    result["events"] = events
    result["times"] = times
    result["sentence"] = sentence
    result["named_entities"] = named_entities
    return result 
    
# function used to get a random key used
# as primary key for tables
def get_random_key(suffix):
    key = str(int(time.time())) + suffix
    return key


#get the word and its ner tag from a word_dict returned by stanford ner
#   [u'Jimmy', {u'NamedEntityTag': u'PERSON', u'CharacterOffsetEnd': u'5', u'CharacterOffsetBegin': u'0', u'PartOfSpeech': u'NNP', u'Lemma': u'Jimmy'}]
# return (Jimmy, PERSON)
def get_word_and_ner(word_dict):
    word = word_dict[0]
    ner_tag = word_dict[1]['NamedEntityTag']
    return word, ner_tag


def get_named_entities(words_with_ner):
    index = 0
    total_words = len(words_with_ner)
    named_entities = {"person":[], "location":[], "organization":[]}

    while index <  total_words:
        word_dict = words_with_ner[index]
        word, ner = get_word_and_ner(word_dict)
        ner = ner.lower()

        if ner in ["location", "organization", "person"]:
            if index + 1 < total_words:
                next_word_dict = words_with_ner[index + 1]
                next_word, next_ner = get_word_and_ner(next_word_dict)
                next_ner = next_ner.lower()
                index += 1
                while next_ner == ner:
                    word = word + ' ' + next_word
                    if index + 1 < total_words:
                        next_word_dict = words_with_ner[index + 1]
                        next_word, next_ner = get_word_and_ner(next_word_dict)
                        next_ner = next_ner.lower()
                        index += 1
            named_entities[ner].append(word)
        else:
            index += 1
    return named_entities

#returns the events description, if there is any event
def get_event_description(sentence, events, times, title):
    global server
    result = {}

    if len(events) == 0 or len(times) == 0:
        return result

    tokens = nltk.word_tokenize(sentence)
    tagged_tokens = nltk.pos_tag(sentence.split())

    result = simplejson.loads(server.parse(sentence))

    words_with_ner = result['sentences'][0]['words']

    #TODO: use indexed dependencies to resolve multiple events in one sentence
    #indexed_depend = result['sentences'][0]['indexeddependencies']

    named_entities = get_named_entities(words_with_ner)

    return get_json(events, times, sentence, named_entities)

def populate_events(result, doc_id, mysql):
    '''
    {"named_entities": {"person": ["John", "Paul", "Anthony", "Jeff Fatt"], "location": [], "organization": []}, "sentence": "Prior to writing for The Wiggles , John was a member of the Australian rock band , The Cockroaches , alongside his brothers Paul , Anthony and another future Wiggle , Jeff Fatt .", "events": ["writing"], "times": ["FUTURE_REF"]}
    '''
    for event in result['events']:
        event_key = get_random_key("_e")
        event_query = "INSERT INTO  event VALUES ('%s', '%s', '%s')" % (event_key, doc_id, result["sentence"])
        #print event_query
        mysql.execute_query(event_query)

        for year in result['times']:
            time_query = "INSERT INTO event_time VALUES ('%s', %s)" % (event_key, year)
            #print time_query
            mysql.execute_query(time_query)

        for entity in result['named_entities']['person']:
            entity_query = "INSERT INTO event_entity VALUES ('%s', '%s')" % (event_key, entity)
            #print entity_query
            mysql.execute_query(entity_query)

def populate_document(doc_id, title, mysql):
    document_query = "INSERT INTO document values ('%s', '%s');" % (doc_id, title)
    mysql.execute_query(document_query)

def populate_categories(doc_id, categories, mysql):    
    category_query = "INSERT INTO document_category values ('%s', '%s')"

    for category in categories:
        category = category.get_next().get_content()
        mysql.execute_query(category_query % (doc_id, category))

if __name__ == "__main__":
    input_file = sys.argv[1]
    #output_file = sys.argv[2]
    file = sys.stdout
    generator = HtmlGenerator(input_file)
    title = generator.xmldoc.get_tags("DOC-ID")[0].get_next().get_content().strip()
    doc_id = get_random_key("_d")
    title_tokens = title.split()


    mysql = MySqlWrapper()

    populate_document(doc_id, title, mysql)

    categories = generator.xmldoc.get_tags("CATEGORY")
    populate_categories(doc_id, categories, mysql)

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
                        times.append(int(year))
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
                    
                    result = get_event_description(output, events, times, title_tokens)
                    if result:
                        populate_events(result, doc_id, mysql)

                    events = []
                    times = []
                    output = ""
