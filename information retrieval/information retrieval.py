from __future__ import unicode_literals
import urllib.request as ur
from bs4 import BeautifulSoup
import codecs
from hazm import *


NumberOfDoc=0
pos_index ={}
Dic_Point={}

urlList = ["https://fa.wikipedia.org/wiki/%D8%AF%D8%A7%D9%86%D8%B4%DA%AF%D8%A7%D9%87_%D8%A2%D8%B2%D8%A7%D8%AF_%D8%A7%D8%B3%D9%84%D8%A7%D9%85%DB%8C_%D9%88%D8%A7%D8%AD%D8%AF_%DA%A9%D8%B1%D8%AC"
          ]

def createInvertedIndex(url):

 for doc in url:
  Templist = []
  html = ur.urlopen(doc).read()
  soup = BeautifulSoup(html)

  # kill all script and style elements
  for script in soup(["script", "style"]):
    script.extract()    # rip it out

  # get text
  text = soup.get_text()

  # break into lines and remove leading and trailing space on each
  lines = (line.strip() for line in text.splitlines())
  # break multi-headlines into a line each
  chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
  # drop blank lines
  text = '\n'.join(chunk for chunk in chunks if chunk)

  normalizer = Normalizer()
  NormalText= normalizer.normalize(text)
  word_tokenized= word_tokenize(NormalText)
  stemmer = Stemmer()






  Dic_Point[urlList.index(doc)]=word_tokenized

  for pos, term in enumerate(word_tokenized):

      # First stem the term.
      stemmer.stem(term)

      # If term already exists in the positional index dictionary.
      if term in pos_index:

          # Increment total freq by 1.
          pos_index[term][0] = pos_index[term][0] + 1

          # Check if the term has existed in that DocID before.
          if urlList.index(doc) in pos_index[term][1]:
              pos_index[term][1][urlList.index(doc)].append(pos)

          else:
              pos_index[term][1][urlList.index(doc)] = [pos]

              # If term does not exist in the positional index dictionary
      # (first encounter).
      else:

          # Initialize the list.
          pos_index[term] = []
          # The total frequency is 1.
          pos_index[term].append(1)
          # The postings list is initially empty.
          pos_index[term].append({})
          # Add doc ID to postings list.
          pos_index[term][1][urlList.index(doc)] = [pos]



def intersect(p1: list, p2: list) -> list:

    # Performs linear merge of 2x sorted lists of postings,
    # Returns the intersection between them (== matched documents):

    res, i, j = list(), 0, 0
    while i < len(p1) and j < len(p2):
        if p1[i] == p2[j]:
            res.append(p1[i])
            i, j = i + 1, j + 1
        elif p1[i] < p2[j]:
            i += 1
        else:
            j += 1
    return res

def Merge(d1: dict, d2: dict) -> dict:

    # Performs linear merge of 2x sorted lists of postings,
    # Returns the intersection between them (== matched documents):
    p1=list(d1)
    p2=list(d2)
    Dict={}


    res, i, j = list(),0, 0
    while i < len(p1) and j < len(p2):
        if p1[i] == p2[j]:


            #Dict.update({p1[i] : tuple (d1[p1[i]])})
            #Dict[p1[i]].append([p2[i]])
            Dict[p1[i]]=d1[p1[i]]
            for item in d2[p1[i]]:
             Dict[p1[i]].append(item)
            Dict[p1[i]].sort()
            i, j = i + 1, j + 1
        elif p1[i] < p2[j]:
            i += 1
        else:
            j += 1

    return Dict



def AND(A,B):

    if A not in pos_index:
         print("answer to "+ A + " AND " + B + ": no")
         return
    if B not in pos_index:
        print("answer to "+ A + " AND " + B + ": no")
        return

    postIA=pos_index[A]
    postIB=pos_index[B]

    Answer =intersect(list(postIA[1]),list(postIB[1]))

    if not Answer:
        print("answer to "+ A + " AND " + B + ": no")
    else:
     print("answer to "+ A + " AND " + B + ": yes in the following documents")
     print(Answer)


def OR(A,B):


    if A  not in pos_index:
        if B  not in pos_index:
            print("answer to "+ A + " OR " + B + ": no")
        else:
            print("answer to " + A + " OR " + B + ": yes")
    else:

            print("answer to " + A + " OR " + B + ": yes")

def search_2Wphrase(pharse):
    listOfWordsInPostIndez=[]
    PharaseWords=word_tokenize(pharse)
    for word in PharaseWords:
        if word in pos_index:
            listOfWordsInPostIndez.append(word)
    word1=pos_index[listOfWordsInPostIndez[0]]
    word2=pos_index[listOfWordsInPostIndez[1]]
    MergedDict=Merge(word1[1], word2[1])
    DocList=list(MergedDict)
    for item in DocList:
        i=0
        while i < len(MergedDict[item])-1:
            if MergedDict[item][i] - MergedDict[item][i+1]==-1:
                print("yes")
                if MergedDict[item][i]-1>0:
                    print("left token:" + Dic_Point[item][MergedDict[item][i] - 1])
                print("First word:"+ Dic_Point[item][MergedDict[item][i]]+"Second Word:"+ Dic_Point[item][MergedDict[item][i]+1])
                if MergedDict[item][i]+2 <= (len(Dic_Point[item])):
                    print("Right token:"+ Dic_Point[item][MergedDict[item][i]+2])


            i+=1

def search_1W(word):
    if word in pos_index:
        print("yes")
    elif (word + "ها") in pos_index:
        print("yes")
    else :
        print("no")


createInvertedIndex(urlList)


search_2Wphrase("مهندسی کامپیوتر")
search_2Wphrase("فیش هفتگی")
AND("دانشگاه","هیچ")
AND("اقتصاد","حضور")
OR("دانشگاه","هیچ")
search_1W("سمینار")



