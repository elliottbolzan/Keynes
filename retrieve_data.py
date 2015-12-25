import urllib, os, zipfile

pairs = ["EURUSD", "AUDUSD", "EURGBP", "EURJPY", "GBPUSD", "USDCAD", "USDJPY"]

directory = os.path.dirname(os.path.realpath(__file__)) + "/data"

if not os.path.exists(directory):
    os.makedirs(directory)
if not os.path.exists(directory + "/hour/"):
    os.makedirs(directory + "/hour/")
if not os.path.exists(directory + "/day/"):
    os.makedirs(directory + "/day/")

for pair in pairs:
    versions = ["hour", "day"]
    for version in versions:
        if not os.path.isfile(directory + "/" + version + "/" + pair + "_"
                               + version + ".csv"):
            print "Downloading " + version + "ly data for " + pair + "."
            destination = directory + "/" + version + "/" + pair + ".zip"
            file = urllib.URLopener()
            file.retrieve("http://www.fxhistoricaldata.com/download/" + pair + "_" + version + ".zip", destination)
            zipped = zipfile.ZipFile(destination)
            zipped.extractall(directory + "/" + version + "/")
            os.remove(destination)