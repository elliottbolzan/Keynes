# Keynes

Keynes strives to predict foreign exchange trends through the use of machine learning techniques.
The project is still in its infancy: while the model is more accurate in its predictions than a coin toss, it is unlikely that it could generate a profit.

Keynes is implemented in Python, and make use of both numpy and the [scikit-learn](https://github.com/scikit-learn/scikit-learn) module.

**Disclaimer**: I am not responsible for any financial losses caused by your use of Keynes.


## Inspiration
Most of Keynes's implementation is based on two papers:
* http://wseas.us/e-library/conferences/2011/Penang/ACRE/ACRE-05.pdf
* http://cs229.stanford.edu/proj2013/Potoski-PredictingGoldPrices.pdf

## Data

Keynes makes use of [hourly data](http://www.fxhistoricaldata.com). One month of EUR/USD data is included in the project, in CSV format. 

## Organization

Currently, Keynes can be run by calling `python keynes.py`.
This script will call parse.py, which is in charge of creating the features for the Logistic Regression model.
The features are only generated if the parsed.csv file does **not** exist; to regenerate the features, the parsed.csv file must be deleted.

At this point, running Keynes will simply output the model's accuracy.

## Features

Technical Analysis features (from the first paper:)

- [x] Stochastic Oscillator
- [x] Momentum
- [x] Williams %R
- [x] Price Rate of Change
- [x] Weighted Closing Price
- [ ] Williams Accumulation Distribution Line (WADL) and the Accumulation Distribution Oscillator (ADOSC)
- [ ] Moving Average Convergence, Divergence (MACD)
- [ ] Commodity Channel Index
- [ ] Bollinger Bands
- [ ] Heiken-Ashi candles indicator

Features from the second paper:

- [ ] Data concerning other instruments and markets
- [ ] Better feature selection
- [ ] Betting simulation and strategy

## Current Accuracy

Currently, using the Logistic Regression model, Keynes's accuracy is `0.53 (+/- 0.01)`.

This may seem unreasonnably low. The second paper, however, comes to similar conclusions: it is difficult to obtain accuracy superior to 0.53 when only using Technical Analysis features.
I expect Keynes will perform significantly better once features unrelated to the EUR/USD forex pair are integrated.

