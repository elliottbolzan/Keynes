import csv, numpy, os.path, parse_data

from sklearn import preprocessing
from sklearn import metrics

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.grid_search import GridSearchCV

from sklearn import cross_validation
from sklearn.metrics import accuracy_score

from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

def simulate(trends, closes, investment):
    base = investment
    quote = 0
    for x in range(0, len(trends) - 1):
        assets = base + quote / closes[x]
        if trends[x] == 1:
            # Sell what you already bought.
            base += quote / closes[x]
            quote = 0
        elif trends[x] == 0:
            # Buy what's going to be worth more.
            quote += base * closes[x]
            base = 0
        assets = base + quote / closes[x]
    return assets - investment

def estimate(values, labels, closes):

    classifier = LogisticRegression()

    predicted = cross_validation.cross_val_predict(classifier, values, labels, cv = 10)
    print "Model accuracy, determined through 10-fold cross-validation: %0.2f%%." % (accuracy_score(labels, predicted) * 100)

    investment = 100
    maximal = simulate(labels, closes, investment)
    actual = simulate(predicted, closes, investment)
    profitPotential = actual / maximal * 100

    timespan = len(labels) / 24
    percentage = actual / investment * 100
    daily = actual / timespan

    print "If the simulation lasts " + str(timespan) + " days and " + str(investment) + " euros are invested, then:"
    print " - Total profit is: %0.2f euros." % actual
    print " - Average daily profit is: %0.2f euros." % daily
    print " - ROI is %0.2f%%." % percentage
    print " - Profit is %0.2f%% of its \"potential\" with this betting strategy (if the model were to guess correctly every time, this value would be 100%%.)" % profitPotential

print "Reading in data."

directory = os.path.dirname(os.path.realpath(__file__))
data = numpy.genfromtxt(directory + "/parsed.csv", delimiter = ',', skip_header = 1)

values = preprocessing.scale(data[:,0:data.shape[1] - 2])
labels = data[:,data.shape[1] - 2]
closes = data[:,data.shape[1] - 1]

print "Selecting features."

pca = PCA(n_components = 2)
selection = SelectKBest(k = 1)
combined_features = FeatureUnion([("pca", pca), ("univ_select", selection)])

values = combined_features.fit(values, labels).transform(values)

estimate(values, labels, closes)