# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 12:00:28 2018
@author: Sharq
"""

import csv, os, itertools, json, pprint, pdb, random, time
import codecs
import pdb
from io import StringIO
from PyPDF2 import utils, PdfFileReader

pp = pprint.PrettyPrinter(indent=3)


# generates the data format needed for sigma.js
def generateVis():
    test_set = []
    path = u'data/'
    edge_list = {}
    # loads relations that are created by human interpretation
    IRAS_data = loadIRAS()
    node_list = []

    # reading relation file between IRAS files
    with codecs.open(u'../data/IRAS_cleaned.csv', 'r', encoding="utf-8", errors='ignore') as infile:
        reader = csv.reader(infile)
        for x in reader:
            doc_name = (x[0].split(':')[1])[1:]
            if (doc_name not in IRAS_data.values()):
                print (doc_name)
                print (IRAS_data.values())
                continue
            nid = x[1]
            data = x[2:]
            rel_data = {}
            if "etaxguide_GST_GST Exemption of Investment Precious Metals" in doc_name:
                print("lol....")
            while len(data) > 0:
                rel_ = data.pop(0)
                doc_ = data.pop(0)
                if len(doc_) > 0:
                    if is_number(doc_) and doc_ in IRAS_data:
                        doc_ = IRAS_data[doc_]
                        rel_data[doc_] = rel_
                        edge_list["n" + nid] = rel_data
                    else:
                        doc_ = removeQuotes(doc_)
                        rel_data[doc_] = rel_
                        edge_list["n" + nid] = rel_data

            node_list.append(createNode(nid, doc_name[:-4], path + doc_name))

        edge_count = 0
        source_count = 0
        all_edges = []

        for key, value in edge_list.items():
            for key2, relations_item in value.items():
                # START - checks whether we have a missing document, then adds a new node
                if len(relations_item) > 0:
                    if key2[len(key2) - 4:] != '.pdf':
                        searchPath = "https://www.google.com.sg/search?q="
                        node_list.append(
                            createMissingNode(str(len(node_list)), key2, searchPath + '+'.join(key2.split())))
                    else:
                        node_list.append(createNode(str(len(node_list)), key2[:-4], path + key2))
                    # END - checks whether we have a missing document, then adds a new node
                    # createEdge returns an edge object in JSON
                    all_edges.append(
                        createEdge(str(edge_count), key[1:], str(len(node_list) - 1), relations_item, source_count))

                source_count += 5
                edge_count += 1

    toAppend = {
        "nodes": node_list
        , "edges": all_edges
    }

    path = u'../vis/datas.json'
    appendToFile(path, toAppend)


def appendToFile(pathName, data):
    with open(pathName, 'w') as outfile:
        json.dump(data, outfile)


# loadsIRAS() reads all the files in your directory, and indexes them by name
# the indexing is linked to the IRAS_cleaned dataset as the relation is done by human input
# human input follows the code that we generated from this list
def loadIRAS():
    indexer = {}
    pathName = "../data/IRAS/"
    lists = [[[y for y in x] for x in items if "C:\\" not in x] for items in os.walk(pathName)]
    IRAS_list = [[[x for x in item] for item in items[1:] if len(item) > 0] for items in lists]
    flattened_list = list(itertools.chain(*IRAS_list))
    IRAS_list = list(itertools.chain(*flattened_list))
    count_ = 0
    for items in IRAS_list:
        convert = False
        indexer[str(count_)] = items
        count_ += 1
    return indexer


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def removeQuotes(data):
    return data.replace('“', '').replace('”', '').replace('"', '').replace('‘', '').replace('’', '')


def createNode(id, label, path):
    node = {
        "id": "n" + id
        , "label": label
        , "x": random.randrange(-200, 200, 2)
        , "y": random.randrange(-200, 200, 2)
        , "size": 2
        , "type": "square"
        , "path": path
    }
    return node


def createMissingNode(id, label, path):
    missingNode = {
        "id": "n" + id
        , "label": label
        , "x": random.randrange(-200, 200, 2)
        , "y": random.randrange(-200, 200, 2)
        , "type": "circle"
        , "path": path
        , "size": 2
    }
    return missingNode


def createEdge(eid, nid, targetid, label, count):
    edge = {
        "id": "e" + eid
        , "source": "n" + nid
        , "target": "n" + targetid
        , "label": label
        , "type": "curvedArrow"
        , "size": 5
        , "count": count
    }
    return edge


# this method should return all the relevant nodes + corresponding edges
def filterByFileName(file_name):
    all_node_list = getAllNodes()
    all_edge_list = getAllEdges()

    # the two lists below are what we want to return based on the filter
    node_list = []
    edge_list = []

    node_found = None

    for node in all_node_list:
        # if found a file in our system...
        if file_name == node['label'] and len(node_list) < 1:
            node_found = node
            node_list.append(node_found)

    if node_found is not None:
        for edge in all_edge_list:
            if node_found['id'] == edge['source']:
                edge_list.append(edge)
                node_list.append(getNode(edge['target']))

    pp.pprint(node_list)
    pp.pprint(edge_list)
    path = u'../vis/filtered_datas.json'
    toAppend = {
        'nodes' : node_list
        ,'edges' : edge_list
    }
    appendToFile(path, toAppend)

    return None


def getAllNodes():
    data = json.load(codecs.open(u'../vis/datas.json',encoding="utf-8", errors='ignore'))
    return data['nodes']


def getAllEdges():
    data = json.load(codecs.open(u'../vis/datas.json',encoding="utf-8", errors='ignore'))
    return data['edges']


def getNode(nid):
    all_node_list = getAllNodes()
    node_found = None
    for node in all_node_list:
        if nid == node['id']:
            node_found = node
    return node_found

#For testing purposes:
# generateVis()
# getAllNodes()
# filterByFileName('etaxguides_GST_Exports_2013-12-31')
