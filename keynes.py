import numpy, os.path, parse

from sklearn import preprocessing
from sklearn.feature_selection import RFE
from sklearn import cross_validation

from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

print "Reading in data."

directory = os.path.dirname(os.path.realpath(__file__))
data = numpy.genfromtxt(directory + "/parsed.csv", delimiter = ',', skip_header = 1)

values = preprocessing.scale(data[:,0:data.shape[1] - 1])
labels = data[:,data.shape[1] - 1]

#classifier = svm.SVC()
#classifier = RandomForestClassifier(n_estimators = 160)
#classifier = GaussianNB()
classifier = LogisticRegression()

'''print "Selecting features."

rfe = RFE(estimator = classifier, step = 1)
rfe.fit(values, labels)
print("Optimal number of features : %d" % rfe.n_features_)
print rfe.support_

removed = 0
for i in range(len(rfe.support_)):
    if not rfe.support_[i]:
        values = numpy.delete(values, i - removed, 1)
        removed += 1

print "Training classifier."'''

classifier.fit(values, labels)

print "Predicting."

scores = cross_validation.cross_val_score(classifier, values, labels, cv = 10)

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
