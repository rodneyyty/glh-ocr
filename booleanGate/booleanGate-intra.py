# -*- coding: utf-8 -*-
"""

Created on Sat Feb 24 12:00:28 2018

@author: Sharq

"""



import docx2txt

path = u'../data/IRAS/Additional Conveyance Duties (ACD) On Residential Property-Holding Entities.docx'

para = "7.2 With regard to the ASK declaration, you must maintain the working templates in Section 3 of the ASK to support that the “ASK: Declaration Form on Completing Annual Review & Voluntary Disclosure of Errors” is accurately completed. We may request for the working templates in Paragraph 2.4 when reviewing your application in."
para = para.split()
page = [para,para,para, "1.3 lol Section 4.7".split(),"1.3 lol Section 5.4".split(),"1.3 ;p; Section 5.2".split(),para]
my_text = docx2txt.process(path)

import csv
import os
import itertools
import json
import pprint
from io import StringIO

# import PyPDF2
from PyPDF2 import utils,PdfFileReader
import subprocess

def tagParagraphs(page):
    for item in page:
        try:
            if isNumber(item[0]):
                return True
        except TypeError:
            pass
        except ValueError:
            pass
        except IndexError:
            pass
    return False

def identifyClauses(page):
    data = []
    for i in range(0,len(page)):
        word = page[i]
        if word.lower() in ["section", "sections"]:
            nextWord = page[i+1]
            if isNumber(nextWord):
                data.append(word + " " + nextWord)

        if word.lower() in ["article", "articles"]:
            nextWord = page[i + 1]
            if isNumber(nextWord):
                data.append(word + " " + nextWord)


        if word.lower() in ["paragraph", "paragraphs"]:
            nextWord = page[i + 1]
            if isNumber(nextWord):
                data.append(word + " " + nextWord)

    return data




    textdict_ = {
        "section" : ""
        ,"article" : ""
    }

def isSection(word):

    if word.lower() in ["section","sections"]:
        return True
    else:
        return False

def isNumber(word):
    try:
        float(word)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(word)
        return True
    except (TypeError, ValueError):
        pass
    return False

def checkPages(document):
    data = []
    for paragraphs in document:
        print("START")
        print(paragraphs)
        if tagParagraphs(paragraphs):
            print(paragraphs[0])
            data = identifyClauses(paragraphs)
            print("-----")
            print(data)
            print("-----")
            dict_ = {
                str(paragraphs[0]) : data
            }
    return


if __name__ == '__main__':
    identifyClauses(para)
    # print(checkPages(page))
    print(type(my_text))
