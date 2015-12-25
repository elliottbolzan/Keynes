import csv, sys, os.path, retrieve_data

data = []
results = []
days = range(2, 20)

def writeHeader():
    header = []
    for day in days:
        header.append("Momentum (" + str(day) + ")")
    header.append("Stochastic")
    header.append("Williams %R")
    for day in days:
        header.append("PROC (" + str(day) + ")")
    for day in days:
        header.append("WCP(" + str(day) + ")")
    header.append("Direction")
    header.append("Close")
    results.append(header)

def momentum(output, close, x):
    for day in days:
        output.append(close - data[x - day][2])
    return output

def stochastic(output, low, high, close, x):
    lowest, highest = low, high
    for i in xrange(1, 15):
        currentLow = data[x - i][0]
        currentHigh = data[x - i][1]
        if currentLow < lowest:
            lowest = currentLow
        if currentHigh > highest:
            highest = currentHigh
    stochastic = 100 * (close - lowest) / (highest - lowest)
    williamsR = -100 * (highest - close) / (highest - lowest)
    output.append(stochastic)
    output.append(williamsR)
    return output

def proc(output, close, x):
    for day in days:
        PROC = (close - data[x - day][2]) / data[x - day][2]
        output.append(PROC)
    return output

def wcp(output, low, high, close, x):
    lowest, highest = low, high
    for day in days:
        currentLow = data[x - day][0]
        currentHigh = data[x - day][1]
        if currentLow < lowest:
            lowest = currentLow
        if currentHigh > highest:
            highest = currentHigh
        WCP = ((close * 2) + highest + lowest) / 4
        output.append(WCP)
    return output

def direction(output, x):
    if data[x + 1][2] - data[x][2] >= 0:
        output.append('1')
    else:
        output.append('0')
    return output

directory = os.path.dirname(os.path.realpath(__file__))

print "Creating features."

input = open(directory + "/data/hour/EURUSD_hour.csv", 'rt')
try:
    reader = csv.reader(input)
    for row in reader:
        if "<TICKER>" not in row:
            data.append([float(row[4]), float(row[5]), float(row[6])])
finally:
    input.close()

writeHeader()

data = data[-8760:]

for x in xrange(len(data) - 1):

    if x < max(days):
        continue

    output = []

    low = data[x][0]
    high = data[x][1]
    close = data[x][2]

    output = momentum(output, close, x)
    output = stochastic(output, low, high, close, x)
    output = proc(output, close, x)
    output = wcp(output, low, high, close, x)
    output = direction(output, x)
    output.append(data[x][2])

    results.append(output)


with open(directory + "/parsed.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(results)