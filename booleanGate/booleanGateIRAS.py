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
import io
import inspect
import codecs


# import PyPDF2
from PyPDF2 import utils,PdfFileReader
import subprocess
import random

def loadTestSet():
    test_set = []
    path = u'data/'
    edge_list = {}
    IRAS_data = loadIRAS()
    node_list = []

#nodelist
    with codecs.open(u'../data/IRAS_cleaned.csv','r',encoding="utf-8", errors='ignore') as infile:
        # json.dump("", outfile)
        reader = csv.reader(infile)
        count = 0
        try:
            reader.next()
        except Exception as e:
            print ('aosidjfoasdif')
            print (e)
        for x in reader:
            doc_name = x[0]
            id = x[1]
            data = x[2:]
            rel_data = {}
            while len(data) > 0:
                rel_ = data.pop(0)
                doc_ = data.pop(0)
                # if doc_ in IRAS_data:
                #     doc_ = IRAS_data[doc_]
                if len(doc_) > 0:
                    if len(doc_) > 4:
                        rel_data[doc_] = rel_
                        edge_list["n" + id] = rel_data
                        count += 1
                    else:
                        doc_ = IRAS_data[doc_]
                        rel_data[doc_] = rel_
                        edge_list["n" + id] = rel_data
                        count += 1
            abc = "n" + id
            if abc in ["n29", "n101", "n124", "n108", "n27", "n96"]:
                tempNode = {
                    "id": "n" + id
                    , "label": doc_name[:-4]
                    , "x": random.randrange(-200, 200, 2)
                    , "y": random.randrange(-200, 200, 2)
                    , "size": 1
                    , "type": "square"
                    , "path": path + ' '.join(doc_name.split()[2:])
                }
                node_list.append(tempNode)

            count += 5


            nodeEdges = {
                "id": "e0"
                ,"source": "n0"
                ,"target": "n1"
                ,"label": "relationship1"
            }
            # print("Appending :")
            pp = pprint.PrettyPrinter(indent=3)
            try:
                pp.pprint(edge_list)
            except:
                print ("edge list got problem")
                print (edge_list)
            print(len(edge_list))

            # appendToFile(u'..\\data\\booleanGate.json', tempNode)

        print()

        edge_count = 0
        ms_count = 0
        source_count = 0
        all_edges = []
        for key,value in edge_list.items():
            #remove for filtering

            print("The item len is " + key + " : "+ str(len(value)))

            if key in ["n29","n101","n124","n108","n27","n96"]:
                for key2,relations_item in value.items():
                    print(node_list)
                    if len(relations_item) > 5:
                        if key2[len(key2)-4:] != '.pdf':
                            #adding a missing document
                            tempNode = {
                                "id": "n" + str(len(node_list))
                                , "label": key2
                                , "x": random.randrange(-200, 200, 2)
                                , "y": random.randrange(-200, 200, 2)
                                , "type": "circle"
                                , "path": "https://www.google.com.sg/search?q="+'+'.join(key2.split())
                                , "size" : 1
                            }
                            ms_count -= 5
                            node_list.append(tempNode)
                            pp.pprint(tempNode)
                        else:
                            # adding a missing document
                            tempNode = {
                                "id": "n" + str(len(node_list))
                                , "label": key2[:-4]
                                , "x": random.randrange(-200, 200, 2)
                                , "y": random.randrange(-200, 200, 2)
                                , "type": "square"
                                , "path": path+key2
                                , "size": 1
                            }
                            ms_count -= 5
                            node_list.append(tempNode)
                            pp.pprint(tempNode)


                        nodeEdges = {
                            "id": "e" + str(edge_count)
                            , "source": "n" + key[1:]
                            , "target": "n" + str(len(node_list)-1)
                            , "label": relations_item
                            , "type" : "curvedArow"
                            , "size" : 5
                            , "count" : source_count
                        }
                        pp.pprint(nodeEdges)
                    else:
                        nodeEdges = {
                            "id": "e" + str(edge_count)
                            , "source": "n" + key[1:]
                            , "target": "n" + str(len(node_list)-1)
                            , "label": relations_item
                            , "type": "curvedArow"
                            , "size": 5
                            , "count": source_count
                        }

                    all_edges.append(nodeEdges)
                    source_count += 5
                    edge_count += 1


        final_all_edges = []

        filter_nodes = []

        alo = []

        super_filter = []

        for node in node_list:
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

        for node in node_list:
            id = node['id']
            if id in filter_nodes:
                super_filter.append(node)
    toAppend = {
        "nodes" : super_filter
        ,"edges" : final_all_edges
    }

    # print("nodelist : " + str(len(node)))
    # print("filter_nodes : " + str(len(filter_nodes)))
    path = u'../vis/datas.json'
    appendToFile(path,toAppend)

def chooseOne(node,node_list, edge_list):
    return



def appendToFile(pathName,data):
    with codecs.open(pathName, 'w', encoding="utf-8", errors='ignore') as outfile:
        json.dump(data, outfile)

def loadIRAS():
    indexer = {}
    path = u'../data/IRAS/'
    pathName = "..\\data\\IRAS\\"
    lists = [[[y for y in x] for x in items if "C:\\" not in x] for items in os.walk(path)]
    IRAS_list = [[[x for x in item] for item in items[1:] if len(item) > 0] for items in lists]

    flattened_list = list(itertools.chain(*IRAS_list))
    IRAS_list = list(itertools.chain(*flattened_list))

    count_ = 0

    for items in IRAS_list:

        convert = False

        indexer[str(count_)] = items
        count_ += 1

    return indexer

loadTestSet()
pp = pprint.PrettyPrinter(indent=3)
# pp.pprint(loadIRAS())
