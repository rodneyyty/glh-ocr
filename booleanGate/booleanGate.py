# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 12:00:28 2018

@author: Sharq

"""

import csv
import os
import itertools
import json


###START OF DEFINING RELATIONS BETWEEN NODES###

class Nodes:
    title = ""
    fileLocation = ""
    relationships = {}

    def __init_(self, title, fileLocation):
        self.title = title
        self.fileLocation = fileLocation

    def addRel(self, node, relation):
        self.relationships[node.title] = [node.title, node.rel, node.fileLocation]


def populateNodes(documents_list):
    # 1. populate list first
    temp_list = []

    # 2. for each document check for relations

    # 3. create nodes after checking all of the relations
    # it needs to be NODE FUCKING OBJECTS OKAY
    node_list = []

    # 4. return as dictionary of nodes
    for node in node_list:
        tempNode = {
            "title": node.title,
            "fileLocation": node.fileLocation,
            "relationships": node.relationships
        }


def searchRel():
    return "searchRel"


def searchClause():
    return "searchClause"


def searchInd():
    return "searchInd"


def searchAbb():
    return "searchAbb"


def searchAlgo():
    return "searchAlgo"


expressions = {
    0: searchRel,
    1: searchClause,
    2: searchInd,
    3: searchAbb,
    4: searchAlgo
}

relKeys = {
    0: "relationship",
    1: "clauses - number,number",
    2: "clauses - number and number",
    3: "indicators",
    4: "abbreviations",
    5: "algorithm"
}


def loadRelations():
    with open(u'C:\\Users\\AShafiqY\\Desktop\\expression.csv', 'r') as file:
        reader = csv.reader(file)
        item = [line for line in reader]
        colSize = len(item[0])

        # initialize relDict
        relDict = {k: [] for k in range(colSize)}

        # add values into relDict
        # consider changing to a lambda/functions
        for x in item[1:]:
            try:
                for num in range(0, colSize):
                    temp = x[num].lower()
                    if len(temp) > 0:
                        relDict[num].append(temp)
            except Exception as e:
                break
    #        print (relDict)
    return relDict


###END OF DEFINING RELATIONS BETWEEN NODES###


# laoding dataset from IRAS
# just getting the names
def loadIRAS():
    path = u'data\\IRAS'
    lists = [[[y for y in x] for x in items if "C:\\" not in x] for items in os.walk(path)]
    IRAS_list = [[[x for x in item] for item in items[1:] if len(item) > 0] for items in lists]

    flattened_list = list(itertools.chain(*IRAS_list))
    IRAS_list = list(itertools.chain(*flattened_list))

    IRAS_dict = {}

    for items in IRAS_list:
        #        print()
        #        print(items)
        IRAS_dict[items] = []
    #        print()

    print(IRAS_dict)


def loadTestSet():
    test_set = []
    with open(u'data\\test\\test.txt', 'r') as file:
        reader = csv.reader(file)

        #        item = [' '.join(line) for line in reader]
        #        item = [line[0].lower() for line in reader if len(line) > 0]
        #        item = [line for line in reader if len(line) > 0]
        #        flattened_list  = list(itertools.chain(*item))

        test_set = []

        for x in reader:
            if len(x) > 0:
                cleaned_x = []
                for item in x:
                    item = item.split()
                    for y in item:
                        cleaned_x.append(y)
                #                print(' '.join(cleaned_x))
                test_set.append(' '.join(cleaned_x))

    #
    #        test_set = flattened_list

    return test_set


# this method just zooms in on the phrasing required
def concatenateItem(text, word):
    items = text.split()
    pos = items.index(word)
    start = 0
    end = len(items)
    if (pos - 10) > start:
        start = pos - 10
    if (pos + 11) < end:
        end = pos + 11
    toReturn = items[start:end]

    return ' '.join(toReturn)


def callBoolGate():
    test_set = loadTestSet()
    rels = loadRelations()

    temp_test = []

    for item in test_set:
        #        print(item)
        for ex in rels:
            #        print(rels[ex])
            for phrases in rels[ex]:
                #            print(phrases)
                if phrases in item.split():
                    temp = {
                        "Phrase found": phrases,
                        "Type of relation": relKeys[ex],
                        "Corresponding item": item
                    }

                    temp_test.append(temp)

                    print("------------------------------------------------")
                    print("Phrase found : " + phrases)
                    print("Type of relation : " + relKeys[ex])
                    print("Corresponding item :  " + concatenateItem(item, phrases))
                    print("------------------------------------------------")

    with open('data.json', 'w') as outfile:
        json.dump(temp_test, outfile)
    print("END OF STATEMENT")


# loadIRAS()
# print(loadRelations())
# loadTestSet()
callBoolGate()