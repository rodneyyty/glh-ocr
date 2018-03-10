# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 12:00:28 2018
@author: Sharq
"""

import csv
import os
import itertools
import json
import pprint
from io import StringIO
import pdb

# import PyPDF2
from PyPDF2 import utils,PdfFileReader
import subprocess
import random

pp = pprint.PrettyPrinter(indent=3)

#generates the data format needed for sigma.js
def generateVis():
    test_set = []
    path = u'data/'
    edge_list = {}
    IRAS_data = loadIRAS()  #loads relations that are created by human interpretation
    node_list = []

    #reading relation file between IRAS files
    with open(u'..\\data\\IRAS_cleaned.csv','r') as infile:
        reader = csv.reader(infile)
        for x in reader:
            doc_name = (x[0].split(':')[1])[1:]
            id = x[1]
            data = x[2:]
            rel_data = {}
            while len(data) > 0:
                rel_ = data.pop(0)
                doc_ = data.pop(0)

                if len(doc_) > 0:
                    if is_number(doc_):
                        doc_ = IRAS_data[doc_]
                        rel_data[doc_] = rel_
                        edge_list["n" + id] = rel_data
                    else:
                        doc_ = removeQuotes(doc_)
                        rel_data[doc_] = rel_
                        edge_list["n" + id] = rel_data
                        # pp.pprint(edge_list["n" + id])
            node_list.append(createNode(id,doc_name,path))

        edge_count = 0
        source_count = 0
        all_edges = []

        for key,value in edge_list.items():
            for key2,relations_item in value.items():
                #START - checks whether we have a missing document, then adds a new node
                if len(relations_item) > 0:
                    if key2[len(key2)-4:] != '.pdf':
                        searchPath = "https://www.google.com.sg/search?q="
                        node_list.append(createMissingNode(str(len(node_list)),key2,searchPath+'+'.join(key2.split())))
                    else:
                        node_list.append(createNode(str(len(node_list)),key2[:-4],path+key2))
                # END - checks whether we have a missing document, then adds a new node
                    #createEdge returns an edge object in JSON
                    all_edges.append(createEdge(str(edge_count), key[1:], str(len(node_list)-1), relations_item, source_count))
                else:
                    # createEdge returns an edge object in JSON
                    all_edges.append(createEdge(str(edge_count), key[1:], str(len(node_list) - 1), relations_item, source_count))

                source_count += 5
                edge_count += 1

        final_all_edges = []
        filter_nodes = []
        alo = []
        super_filter = []

        for node in node_list:
            #bug, a None type was created somewhere
            if node is not None:
                id = node['id']
                alo.append(id)

        for items in all_edges:
            target = items["target"]
            source = items["source"]
            if target in alo and source in alo:
                final_all_edges.append(items)
                if target not in filter_nodes:
                    filter_nodes.append(target)
                if source not in filter_nodes:
                    filter_nodes.append(source)
        print(len(node_list))
        for node in node_list:
            # bug, a None type was created somewhere
            if node is not None:
                id = node['id']
                if id in filter_nodes:
                    super_filter.append(node)

    toAppend = {
        "nodes" : super_filter
        ,"edges" : final_all_edges
    }

    pp.pprint(toAppend)
    path = u'../vis/datas.json'
    appendToFile(path,toAppend)

def appendToFile(pathName,data):
    with open(pathName, 'w') as outfile:
        json.dump(data, outfile)

#loadsIRAS() reads all the files in your directory, and indexes them by name
#the indexing is linked to the IRAS_cleaned dataset as the relation is done by human input
#human input follows the code that we generated from this list
def loadIRAS():
    indexer = {}
    pathName = "..\\data\\IRAS\\"
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
    return data.replace('“','').replace('”','').replace('"','').replace('‘','').replace('’','')

def createNode(id,label,path):
    node = {
        "id": "n" + id
        , "label": label
        , "x": random.randrange(-200, 200, 2)
        , "y": random.randrange(-200, 200, 2)
        , "size": 1
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
        , "size" : 1
    }
    return missingNode

def createEdge(eid,nid,targetid,label,count):
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

generateVis()

