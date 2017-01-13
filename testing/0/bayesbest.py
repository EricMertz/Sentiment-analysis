# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re, copy

class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""
      self.posRev = dict()
      self.negRev = dict()
      self.posBi = dict()
      self.negBi = dict()
      a = False
      b = False
      c = False
      d = False
      if os.path.isfile("posRev"):
         print os.path.isfile("posRev")
         a = self.load("posRev")
      if os.path.isfile("negRev"):
         b = self.load("negRev")
      if os.path.isfile("posBi"):
         c = self.load("posBi")
      if os.path.isfile("negBi"):
         d = self.load("negBi")

      if a and b:
         self.posRev = a
         self.negRev = b
      else:
         self.train()

      if c and d:
         self.posBi = c
         self.negBi = d
      else:
         self.trainBi()





   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""
      lFileList = []
      for fFileObj in os.walk("movies_reviews/"):
         lFileList = fFileObj[2]
         break
      for rev in lFileList:
         if int(rev[7])== 1:
            contents = self.loadFile("movies_reviews/" + rev)
            listOfWords = self.tokenize(contents)
            for word in listOfWords:
               self.negRev[word] = self.negRev.get(word, 0) + 1
         if int(rev[7])== 5:
            contents = self.loadFile("movies_reviews/" + rev)
            listOfWords = self.tokenize(contents)
            for word in listOfWords:
               self.posRev[word] = self.posRev.get(word, 0) + 1
      self.save(self.posRev, "posRev")
      self.save(self.negRev, "negRev")

   def trainBi(self):
      sum1, sum2 = self.count()

      thing = 0.01*(sum1+sum2)

      posS = []
      negS = []
      for word in self.posRev:
         if self.posRev[word] >= thing:
            posS.append(word)
      for word in self.negRev:
         if self.negRev[word] >= thing:
            negS.append(word)

      lFileList = []
      for fFileObj in os.walk("movies_reviews/"):
         lFileList = fFileObj[2]
         break

      for rev in lFileList:
         if int(rev[7])== 1:
            contents = self.loadFile("movies_reviews/" + rev)
            listOfWords = self.tokenize(contents)
            for i in range(len(listOfWords)-1):
               w1 = listOfWords[i]
               w2 = listOfWords[i+1]
               if w1 in negS or w2 in negS:
                  self.negBi[w1+' '+w2] = self.negBi.get(w1+' '+ w2, 0) + 1
         if int(rev[7])== 5:
            contents = self.loadFile("movies_reviews/" + rev)
            listOfWords = self.tokenize(contents)
            for i in range(len(listOfWords)-1):
               w1 = listOfWords[i]
               w2 = listOfWords[i+1]
               if w1 in posS or w2 in posS:
                  self.posBi[w1+' '+w2] = self.posBi.get(w1+' '+w2, 0) + 1

      tempPos = copy.deepcopy(self.posBi)
      tempNeg = copy.deepcopy(self.negBi)
      for item in tempPos:
         if self.posBi[item] < 0.005*sum1 or self.posBi[item] < 3:
            del self.posBi[item]

      for item in tempNeg:
         if self.negBi[item] < 0.005*sum2 or self.negBi[item] < 3:
            del self.negBi[item]



      self.save(self.posBi, "posBi")
      self.save(self.negBi, "negBi")

      return self.posBi, self.negBi

   def count(self):
      lFileList = []
      negsum = 0
      possum = 0
      for fFileObj in os.walk("movies_reviews/"):
         lFileList = fFileObj[2]
         break
      for rev in lFileList:
         #print "hi"
         if int(rev[7]) == 1:
               negsum += 1
         if int(rev[7]) == 5:
               possum += 1
      return possum, negsum


    
   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """

      sum1, sum2 = self.count()

      #len1 = len(self.posRev)
      #len2 = len(self.negRev)

      probPos = 0 #math.log(float(sum1)/(sum1+sum2))
      probNeg = 0 #math.log(float(sum2)/(sum1+sum2))

      ls = self.tokenize(sText)

      #test Positive case
      for i in range(len(ls)-1):
         const = 1
         if (ls[i]+ ' ' + ls[i+1]) in self.posBi:
            print ls[i]+ ' ' + ls[i+1]
            const = self.posBi.get(ls[i], 1)
         prob = (const*float(self.posRev.get(ls[i], 0) + 1))/(sum1)
         if prob != 0:
            probPos += math.log(prob)
         if i == (len(ls)-2):
            prob = (const*float(self.posRev.get(ls[i+1], 0) + 1))/(sum1)
         if prob != 0:
            probPos += math.log(prob)



      #test Negative case
      for i in range(len(ls)-1):
         const = 1
         if (ls[i]+ ' ' + ls[i+1]) in self.negBi:
            const = self.negBi.get(ls[i], 1)
         prob = (const*float(self.negRev.get(ls[i], 0) + 1))/(sum2)
         if prob != 0:
            probNeg += math.log(prob)
         if i == (len(ls)-2):
            prob = (const*float(self.negRev.get(ls[i+1], 0) + 1))/(sum2)
         if prob != 0:
            probNeg += math.log(prob)


      print probPos
      print probNeg

      print probPos-probNeg
      if (probPos - probNeg) > 2:
         return "positive"
      elif (probNeg - probPos) > 2:
         return "negative"
      else:
         return "neutral"




   def loadFile(self, sFilename):
      """Given a file name, return the contents of the file as a string."""

      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt
   
   def save(self, dObj, sFilename):
      """Given an object and a file name, write the object to the file using pickle."""

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
   def load(self, sFilename):
      """Given a file name, load and return the object stored in the file."""

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText): 
      """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order)."""

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))
               
      if sToken != "":
         lTokens.append(sToken)

      return lTokens





