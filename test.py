#test

import os
execfile("bayes.py")

#st = "movies-1-32"
#print st[7]

s = Bayes_Classifier()
#s.train()
#print s.load("posRev")
result = s.classify("not good at all")
print result

execfile("bayesbest.py")
bc = Bayes_Classifier()
#yay, oh =  bc.trainBi()
#print yay
#print oh
result = bc.classify("not good at all")
#print "a"
print result


