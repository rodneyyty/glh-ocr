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
    data_list = produceDataList(loadRelations(), loadFolderFiles())
    mnl = data_list[1]  #list of missing nodes
    el = data_list[0]   #initial edge list created
    nl = populateNodeList(loadRelations(),el,mnl) #initial node list created

    defg = fixMissingValues(mnl, nl, el)
    node_list = defg[0]
    edge_list = defg[1]
    toAppend = {
        "nodes": node_list
        , "edges": edge_list
    }

    path = u'../vis/datas.json'

    appendToFile(path, toAppend)


def appendToFile(pathName, data):
    with open(pathName, 'w') as outfile:
        json.dump(data, outfile)


# loadsIRAS() reads all the files in your directory, and indexes them by name
# the indexing is linked to the IRAS_cleaned dataset as the relation is done by human input
# human input follows the code that we generated from this list
def loadRelations():
    temp = {}
    count_ = 0
    with codecs.open(u'../data/IRAS_cleaned.csv', 'r', encoding="utf-8", errors='ignore') as infile:
        reader = csv.reader(infile)
        for items in reader:
            convert = False
            temp[str(count_)] = items
            count_ += 1
    indexer = {}
    for item, value in temp.items():
        label = (value[0].split(':')[1])[1:]
        cid = item
        data = value[2:]
        relations = {}
        rel_count = 0

        while len(data) > 0:
            rel_ = data.pop(0)
            doc_ = data.pop(0)
            if len(rel_) and len(doc_) > 0:
                relations["r" + str(rel_count)] = [rel_,doc_]
                rel_count+=1
        temp = {
            'label': label
            , 'relations': relations
        }
        if len(label) > 0:
            indexer[cid] = temp
    return indexer

def produceDataList(relations_list,folder_items):
    data_list = []
    edge_list = []
    missing_nl = {} #label, path
    eid_count = 0
    mid_count = 0
    count = 0

    for folder_key,folder_value in folder_items.items():
        # folder_name = folder_value
        # key_id = "n" + str(folder_key)

        for key,value in relations_list.items():
            if len(value['relations']) > 0 and key == folder_key:
                for r in value['relations']:
                    if is_number(value['relations'][r][1]):
                       edge = createEdge(str(eid_count), "n"+str(key), "n"+value['relations'][r][1], value['relations'][r][0], count)
                       edge_list.append(edge)
                       eid_count+=1
                       count+=5
                    else:
                        searchPath = "https://www.google.com.sg/search?q=1"
                        label = value['relations'][r][1]
                        path = searchPath + '+'.join(label.split())
                        mid = "m"+str(mid_count)
                        temp = {
                            'label' : label
                            ,'path' : path
                        }
                        missing_nl[mid] = temp
                        # missing_nl.append(mnl)
                        edge = createEdge(str(eid_count), "n" + str(key), "m"+str(mid_count),
                                          value['relations'][r][0], count)
                        edge_list.append(edge)
                        mid_count += 1

    data_list.append(edge_list)
    data_list.append(missing_nl)
    return data_list


def loadFolderFiles():
    indexer = {}
    pathName = "../data/IRAS/"
    lists = [[[y for y in x] for x in items if "C:\\" not in x] for items in os.walk(pathName)]
    folder_list = [[[x for x in item] for item in items[1:] if len(item) > 0] for items in lists]
    flattened_list = list(itertools.chain(*folder_list))
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


def is_not_number(s):
    try:
        float(s)
        return False
    except ValueError:
        return True


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
        , "source": nid
        , "target": targetid
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


def populateNodeList(nl,el,mnl):
    path = u'data/'
    node_list = []
    folder_list = loadFolderFiles()
    list_names = []
    for item in folder_list.values():
        list_names.append(item)

    for id,values in nl.items():
        if checkList(list_names,values['label'][:-4]):
            tempN = createNode(id,values['label'][:-4],path+values['label'])
            node_list.append(tempN)
        # else:
        #     searchPath = "https://www.google.com.sg/search?q=1"
        #     path = searchPath + '+'.join(values['label'].split())
        #     tempN = createMissingNode(id, values['label'][:-4], path)
        #     node_list.append(tempN)
    return node_list


def fixMissingValues(mnl,nl,el):
    node_list = nl
    fixed_list = []
    for item in el:
        target = item['target']
        for keys in mnl:
            if target == keys:
                nid = len(node_list)
                label = mnl[target]['label']
                path = mnl[target]['path']
                node = createMissingNode(str(nid), label, path)
                item['target'] = ("n"+str(nid))
                node_list.append(node)

    fixed_list.append(node_list)
    fixed_list.append(el)
    return fixed_list

def checkList(list, value):
    for item in list:
        if value in item:
            return True
    return False

#For testing purposes:
generateVis()
# filterByFileName('etaxguides_GST_Exports_2013-12-31')
# produceDataList(loadRelations(),loadFolderFiles())
# pp.pprint(loadFolderFiles())