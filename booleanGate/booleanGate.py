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

# import PyPDF2
from PyPDF2 import utils,PdfFileReader
import subprocess



# take output file, everynode you have a type for i pass to cc
# entity/document name, draw edge, metadata

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

    return relDict


###END OF DEFINING RELATIONS BETWEEN NODES###


# laoding dataset from IRAS
# loads files individually and converts to text
def loadIRAS():
    path = u'../data/IRAS/'
    pathName = "..\\data\\IRAS\\"
    lists = [[[y for y in x] for x in items if "C:\\" not in x] for items in os.walk(path)]
    IRAS_list = [[[x for x in item] for item in items[1:] if len(item) > 0] for items in lists]

    flattened_list = list(itertools.chain(*IRAS_list))
    IRAS_list = list(itertools.chain(*flattened_list))

    IRAS_dict = {}

    for items in IRAS_list[1:]:
        # print()
        # print(items)
        IRAS_dict[items] = pdfToText(pathName,items)
        break
        # print()

    with open(u'..\\data\\IRAS_data.txt', 'w') as outfile:
        json.dump(IRAS_dict, outfile)

    return IRAS_dict

def pdfToText(pathName,items):
    file_location =pathName+items
    tempList = []
    listToReturn = []
    dictToReturn = {"relations" : []}

    # x = open('../data/IRAS/eTax Guide_GST_Zero-rating of tools and machines_2013_12_31.pdf', 'rb')
    pdfFileObj = open(file_location, 'rb')
    # with open(file, 'rb') as input_file:
    #     input_buffer = StringIO(input_file.read())
    try:
        input_pdf = PdfFileReader(open(file_location, 'rb'),strict=False)
        numPages = input_pdf.numPages

        for i in range(0, numPages):
            #for each page, read the text on the page
            pageObj = input_pdf.getPage(i)
            # print("---START OF READING A PAGE ONLY---")
            # print(pageObj.extractText().split())
            #remove whitespaces
            # tempList = ' '.join(pageObj.extractText().split())
            tempList = pageObj.extractText().split()
            # take note that this is in binary
            #high level joining
            # print(tempList)
            listToReturn.append(tempList)
            dictToReturn[str(i)] = tempList
            # print("---END OF READING A PAGE ONLY---")


    except OSError:
        with open(u'..\\data\\error.txt', 'a') as outfile:
            outfile.write("OSError: " + items + " cannot be opened")
            outfile.close()
            print(OSError)
    except utils.PdfReadError:
        with open(u'..\\data\\error.txt', 'a') as outfile:
            outfile.write("OSError: " + items + " cannot be opened")
            outfile.close()
            print(utils.PdfReadError)

    return dictToReturn

##END OF READING IRAS SET ###

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
    #    print(text)
    items = text.split()
    pos = items.index(word)
    start = 0
    end = len(items)
    if (pos - 10) >= start:
        start = pos - 10
    if (pos + 11) <= end:
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

#i added a break -> dun forget to remove
dict_ = loadIRAS()
pp = pprint.PrettyPrinter(indent=3)
# pp.pprint(dict_)


# print(dict_)
# pp.pprint(loadRelations())

def findRel(data,gate):
    for title, d in data.items():
        #title (which is the key) is the title of the pdf
        print(title)
        #d contains the data for each page and corresponding relations
        print(d)

        #we have to iterate through d to get the data on individual pages
        for page, d2 in d.items():
            #key is page, its in string, convert to int

            #page_no = int(page)

            #d2 is the data, break it down
            #

            print(d2)


        break
    return

def find(array):
    #relations dict
    rel_ = loadRelations()

    for x in range(0,3):
        print(rel_[x])

    for key,value in array.items():
        print(value)

# findRel(loadIRAS(),loadRelations())

find(loadIRAS())

# loadTestSet()
# callBoolGate()

# pdfToText()