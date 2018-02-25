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
indexer = {'no' : ''}
###START OF DEFINING RELATIONS BETWEEN NODES###

class Node:
    title = ""
    fileLocation = ""
    relationships = {}
    pages = {}
    id = ""

    def __init__(self, title, fileLocation, pages, id):
        self.title = title
        self.fileLocation = fileLocation
        self.pages = pages
        self.id = "n" + str(id)

    def addRel(self, node, relation):
        self.relationships[node.id] = relation

def executeRel(node, node_dict, count):
    #node is the document name which has a dictionary of pages
    print("----Begin relation comparison for selected document-----")

    for key,value in indexer.items():
        print(key + " : " + value)
    print("Current document selected is : " + node.title)
    print("Current document id : " + node.id[1:])
    print("Number of documents remaining : " + str(len(node_dict)-count))
    data = ""

    while data != "n":
        chosen = input("Choose a related document   :   ")
        x = 0
        chosen = str(chosen)
        while chosen not in indexer.keys():
            text = "*Error* Please enter a number    :   "
            print("Number of documents remaining : " + str(len(node_dict) - count))
            x += 1
            if x > 5:
                text = ""
                print("Number of documents remaining : " + str(len(node_dict) - count))
            chosen = str(input(text))


        if len(chosen) > 0:
            relation = str(input("Enter the relation    :   "))
            node.addRel(node_dict[indexer[chosen]], str(relation))
            data = str(input("Add another document? : ").lower())

            x = 1
    return node

def populateNodes(documents_list):
    # 1. populate list first
    temp_dict = {}
    pathName = "..\\data\\IRAS\\"
    node_list = []
    x = 0
    for key,value in documents_list.items():
        node = Node(key,pathName+key,value, x)
        temp_dict[key] = node
        x+=1
    count = 0
    for key,value in temp_dict.items():
    # 2. for each document check for relations
        node = executeRel(temp_dict[key], temp_dict, count)
        count +=1
    # 3. create nodes after checking all of the relations

        node_list.append(node)

    # 4. return as dictionary of nodes
    csv_list = []
    x = 0
    y = 0
    e = 0

    csv_node = {}
    csv_edge = {}
    edge_list = []

    for node in node_list:
        print("Node recorded : " + str(node.id))
        tempNode = {
            "id" : node.id
            ,"label" : node.title[:-4]
            ,"x" : x
            ,"y" : y
            ,"size": 1
            ,"type": "square"
            ,"path": node.fileLocation
        }
        for id,relation in node.relationships.items():
            print("Edge recorded : " + str(node.id) + " " + relation + " " + str(id))
            tempedges = {
                "id": "e" + str(e)
                , "source": node.id
                , "target": id
                , "label": relation
            }
            e += 1
            edge_list.append(tempedges)

        x+=1
        y+=1
        csv_list.append(tempNode)

    csv_out = {
        "nodes" : csv_list
        ,"edges" : edge_list
    }

    with open('relation.json', 'w') as outfile:
        json.dump(csv_out, outfile)
    print("END OF PROGRAM, FILE OUTPUTTED TO CSV. THANK YOU YOU DID IT.")


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
    indexer = {}
    path = u'../data/IRAS/'
    pathName = "..\\data\\IRAS\\"
    lists = [[[y for y in x] for x in items if "C:\\" not in x] for items in os.walk(path)]
    IRAS_list = [[[x for x in item] for item in items[1:] if len(item) > 0] for items in lists]

    flattened_list = list(itertools.chain(*IRAS_list))
    IRAS_list = list(itertools.chain(*flattened_list))

    IRAS_dict = {}
    count_ = 0
    # print("-----    START IRAS_LOAD  -----")
    for items in IRAS_list:
        # print()
        # print("Loading " + items + " ...")
        convert = False
        if convert:
            IRAS_dict[items] = pdfToText(pathName,items)
        else:
            IRAS_dict[items] = ''
        indexer[str(count_)] = items
        count_ += 1
        # if count_ > 5:
        #     break
        #break
        # print()
    print("-----    END IRAS_LOAD   -----")
    with open(u'..\\data\\IRAS_data.txt', 'w') as outfile:
        json.dump(IRAS_dict, outfile)

    return indexer

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

    path = u'..\\data\\IRAS\\'

    with open(u'..\\data\\booleanGate.json','w') as outfile:
        # json.dump("", outfile)
        outfile.close() # create test set

    with open(u'..\\data\\IRAS_cleaned.csv', 'r') as file:
        reader = csv.reader(file)


        #        item = [' '.join(line) for line in reader]
        #        item = [line[0].lower() for line in reader if len(line) > 0]
        #        item = [line for line in reader if len(line) > 0]
        #        flattened_list  = list(itertools.chain(*item))

        test_set = []

        #[name, id, doc1, rel1, doc2, rel2...]
        for x in reader:
            doc_name = x[0]
            id = x[1]
            data = x[2:]
            rel_data = {}
            while len(data) > 0:
                doc_ = data.pop(0)
                rel_ = data.pop(0)
                rel_data[doc_] = rel_

            tempNode = {
                "id": "n"+id
                , "label": doc_name[:-4]
                , "x": x
                , "y": x
                , "size": 1
                , "type": "square"
                , "path": path+doc_name
            }

            toAppend = {
                "doc_name" : doc_name
                ,"id" : id
                ,"rel_data" : rel_data
            }
            print("Appending :")
            pp = pprint.PrettyPrinter(indent=3)
            pp.pprint(toAppend)
            appendToFile(u'..\\data\\booleanGate.json',toAppend)


    return test_set

def appendToFile(pathName,data):
    with open(pathName, 'a') as outfile:
        json.dump(data, outfile)

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
# dict_ = loadIRAS()
# pp = pprint.PrettyPrinter(indent=3)
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

            print(d2)


        break
    return


def serRel(array):
    # relations dict
    rel_ = loadRelations()[0]
    for word in array:
        for item in rel_:
            try:
                while word in item:
                    max = 5
                    pos = array.index(word)
                    newWord = word
                    posArray = [pos]
                    for i in range(0,5):
                        newWord += array[pos+i]
                        posArray.append(pos+i)
                        if newWord == item:
                            # replacing the word with the correct string
                            array[posArray[0]] = newWord
                            # removing all of the unecessary characters
                            for x in range(0, len(posArray[1:])):
                                index = posArray[1:][0]
                                del array[index - len(array)]
                                return array
                                break
                    break
            except IndexError:
                pass
            except ValueError:
                pass


    return []

def serClauseType1(array):
    # relations dict
    rel_ = loadRelations()[1]
    for word in array:
        for item in rel_:
            try:
                while word in item:
                    max = 5
                    pos = array.index(word)
                    newWord = word
                    posArray = [pos]
                    for i in range(0, 5):

                        newWord += array[pos + i]
                        posArray.append(pos + i)
                        if newWord == item:
                            # replacing the word with the correct string
                            array[posArray[0]] = newWord
                            # removing all of the unecessary characters
                            for x in range(0, len(posArray[1:])):
                                index = posArray[1:][0]
                                del array[index - len(array)]
                                return array
                                break
                    break
            except IndexError:
                pass
            except ValueError:
                pass
    return []

def serClauseType2(array):
    # relations dict
    rel_ = loadRelations()[1]
    for word in array:
        for item in rel_:
            try:
                while word in item:
                    max = 5
                    pos = array.index(word)
                    newWord = word
                    posArray = [pos]
                    for i in range(0,5):

                        newWord += array[pos+i]
                        posArray.append(pos+i)
                        if newWord == item:
                            # replacing the word with the correct string
                            array[posArray[0]] = newWord
                            # removing all of the unecessary characters
                            for x in range(0, len(posArray[1:])):
                                index = posArray[1:][0]
                                del array[index - len(array)]
                                return array
                                break
                    break
            except IndexError:
                pass
            except ValueError:
                pass
    return []

def find(array):
    #relations dict
    rel_ = loadRelations()

    for x in range(0,3):
        print(rel_[x])

    for key,value in array.items():
        # print(value)
        for key2,value2 in value.items():
            if key2 != 'relations':
                if len(serRel(value2)) > 0:
                    print('relationship found : updating array...')
                    array[key2] = serRel(value2)

                if len(serClauseType1(value2)) > 0:
                    print('ClauseType1 found : updating array...')
                    array[key2] = serClauseType1(value2)

                if len(serClauseType2(value2)) > 0:
                    print('ClauseType2 found : updating array...')
                    array[key2] = serClauseType2(value2)


# findRel(loadIRAS(),loadRelations())

# find(loadIRAS())

# loadTestSet()
# callBoolGate()

# pdfToText()
# populateNodes(loadIRAS())
#
# v = ["doc1","relation1","doc2","relation2","doc3","relation3"]
#
# relation = {}
#
# while len(v) > 0:
#     doc_ = v.pop(0)
#     rel_ = v.pop(0)
#     relation[doc_] = rel_
#     print(doc_)
#     print(rel_)
#
pp = pprint.PrettyPrinter(indent=3)
# pp.pprint(relation)
pp.pprint(loadIRAS())