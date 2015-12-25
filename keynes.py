import csv, numpy, os.path, parse_data

from sklearn import preprocessing
from sklearn.feature_selection import RFE
from sklearn import cross_validation
from sklearn.metrics import accuracy_score

from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

def simulate(values, labels, closes):

    classifier = LogisticRegression()

    data = []
    input = open(directory + "/data/hour/EURUSD_hour.csv", 'rt')
    try:
        reader = csv.reader(input)
        for row in reader:
            if "<TICKER>" not in row:
                data.append(float(row[6]))
    finally:
        input.close()

    bet = 18
    resources = 1000

    base = resources
    quote = 0

    predicted = cross_validation.cross_val_predict(classifier, values, labels, cv = 10)

    for x in range(1, len(predicted)):
        if predicted[x] == 1:
            base -= bet
            quote += bet * closes[x - 1]
        elif predicted[x] == 0:
            base += quote / closes[x - 1]
            quote = 0

    assets = base + quote / closes[x - 1]
    timespan = len(predicted) / 24

    profit = (assets - resources) / timespan
    percentage = profit / resources

    print "Average daily profit: %0.2f euros." % profit
    print "That's %0.4f%% a day." % percentage
    print "Model accuracy, determined through 10-fold cross-validation: %0.2f%%." % (accuracy_score(labels, predicted) * 100)

print "Reading in data."

directory = os.path.dirname(os.path.realpath(__file__))
data = numpy.genfromtxt(directory + "/parsed.csv", delimiter = ',', skip_header = 1)

values = preprocessing.scale(data[:,0:data.shape[1] - 2])
labels = data[:,data.shape[1] - 2]
closes = data[:,data.shape[1] - 1]

#classifier = svm.SVC()
#classifier = RandomForestClassifier(n_estimators = 160)
#classifier = GaussianNB()
classifier = LogisticRegression()

print "Selecting features."

rfe = RFE(estimator = classifier, step = 1)
rfe.fit(values, labels)

removed = 0
for i in range(len(rfe.support_)):
    if not rfe.support_[i]:
        values = numpy.delete(values, i - removed, 1)
        removed += 1

simulate(values, labels, closes)