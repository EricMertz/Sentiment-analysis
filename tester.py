# Name: 
# Date:
# Description:
#
#

import os

execfile("bayes.py")

def main():
   normal = Bayes_Classifier()
   print "training..."
   normal.train()

   testing_data = []
   for fFileObj in os.walk("for_testing/"):
      testing_data = fFileObj[2]
      break

   pos_recall = recall_test(normal, True, testing_data)
   neg_recall = recall_test(normal, False, testing_data)
   pos_precision = precision_test(normal, True, testing_data)
   neg_precision = precision_test(normal, False, testing_data)
   print "positive recall: " + str(pos_recall)
   print "negative recall: " + str(neg_recall)
   print "positive precision: " + str(pos_precision)
   print "negative precision: " + str(neg_precision)

def recall_test(classifier, positive, data):
   exp_score = "1"
   exp_class = "negative"
   if positive:
      exp_score = "5"
      exp_class = "positive"
   total = 200
   correct = 0
   for review in data:
      print "classifying..."
      correct += is_correct(classifier, review, exp_score, exp_class)
      blah = classifier.classify(review)
      print blah
      print exp_class
      #raw_input()
   recall = float(correct) / float(total)
   return recall

def precision_test(classifier, positive, data):
   exp_score = "1"
   exp_class = "negative"
   if positive:
      exp_score = "5"
      exp_class = "positive"
   total = 1
   correct = 0
   for review in data:
      print "classifying..."
      correct += is_correct(classifier, review, exp_score, exp_class)
      blah = classifier.classify(review)
      print blah
      print exp_class
      #raw_input()
      if classifier.classify(review) == exp_class:
         total += 1
   recall = float(correct) / float(total)
   return recall

def is_correct(classifier, review, exp_score, exp_class):
   score = review[7]
   review_string = loadReview(review)
   prediction = classifier.classify(review_string)
   if score == exp_score and prediction == exp_class:
      return 1
   return 0

def loadReview(sFilename):
   f = open("for_testing/" + sFilename, "r")
   sTxt = f.read()
   f.close()
   return sTxt
