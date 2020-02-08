#Electricity carbon intensity prediction - predicting how clean and dirty electricity is
This repository contains the portfolio project which I have been working on during my time at the Data Science Retreat (DSR). Being a founding member of a smart farming startup dealing with the optimisation of ecological sustainability in farming, I desired to work on a project putting ecological sustainability into its focus as well.

It was Adam Green - technical director of the DSR at the time - who introduced us from the cotemporary batch from back then into his idea of optimising the usage of electricity in terms of minimised CO2 emissions. He explained to us how my decision WHEN I charge my phone can determine whether the electricity used for that comes from sustainable resources or from a coal plant. All that bases on the concept of marginal electricity generators and marginal CO2 emissions associated to that (see presentation for more details).

The approach was to FORECAST THE MARGINAL CO2 EMISSIONS of the Australian energy market which is liberalised and which prices are predominantly determined by bidding of the different energy generators. The different energy generators ranging from wind turbines to coal plants are dispatched to the energy grid from cheapest to most expensive. How many generators are and whether at a given time a new generator is being dispatched depends on the current overall energy demand. Here comes my power as a consumer into the picture. For instance, if I charge my phone when the energy resources of a low CO2 emitter such as of a nuclear plant are exhausted with a coal plant being the next generator dispatched to the energy grid, I cause a significant increase in marginal CO2 emissions if the coal plant dispatch occurs due to my additional energy consumption.

Adam and I hypothesised that the forecast may be a time series issue. Hence, the main goal of this portfolio project was to test this hypothesis and to hopefully get to some useful predicitons.
Unfortunately, my efforts at persuasion were insufficient to get one of my batch members on board for collaboration. In fact, out of 10 people of my batch, only two were collaborating. Yet on the bright side, that gave me the opportunity to organise and complete my first end-to-end machine learning project on my own. Since I was still fairly new to programming as well as to statistical learning, that constituted a challenge to me which I was more than happy to accept. 
Other than the topic, what convinced me of the project was its versatility in required skills. It started by writing code for data scraping from the Internet, then for data downloading and unpacking, a ton of code for week-long data cleaning of a massive dataset (originally ~84 000 000 lines!), and finally to attempt a time series forecast.
As I got more and more fluent with Python - getting it to know from various angles - the time to test different models on the dataset sufficed for a non-classical but very powerful one - namely xgboost.

As I mentioned above, the goal of the portfolio project was to test the hypothesis that forecasting marginal CO2 emissions can be treated as a time series issue. I indeed could find time-dependent correlations between a set of time features and our target of marginal CO2 emissions. Yet, we have not quite managed to succeed in forecasting CO2 emissions using xgboost. It was a bit of a late but particularly insightful observation exposing to me that any promising-looking error metric can be easily beaten by critical thinking. Unfortunately, I had run out of time to try out more models back then and starterd a new project right after. But the insights Adam and I obtained are going to be valuable to any new student who will pick up on and continue that project.

All in all, the portfolio project was an amazingly enriching experience to me, representing my entry into the world of data science (and by that I mean spending 90 % of your time with cleaning data), including its joys and frustrations. I hope you enjoy my journey and of course hope that you will take something out of my notebooks for you.

# Benchmark information of the liberal energy market in Australia.
- Each player contributing electricity to the grid (sustainable, nuclear, coal, gas, oil) bids a price for a specific quantitiy of electricity
- The different bidders are dispatched to the grid from cheapest to most expensive according to the energy demand
- Minimum and maximum prices allowed by the market regulators vary but are commonly between -1000 Australian Dollars (AUD) and 13,500 AUD
- The data acquisition of marginal CO2 emissions and price is of a 5 min granularity

#Before you start
Due to the massive dataset I was not able to upload that or even any preprocessed dataframe since all of them were too big for that on github. However, since I provide scraper and unpacking functions you can obtain the dataframe on your own.

# References & reading
- [A hackers guide to AEMO data](https://adgefficiency.com/hackers-aemo/)
- https://medium.com/electricitymap/marginal-emissions-what-they-are-and-when-to-use-them-ecd050ab0962
- https://medium.com/electricitymap/using-machine-learning-to-estimate-the-hourly-marginal-carbon-intensity-of-electricity-49eade43b421
- Li Thesis, Winds of Change & 2018_Dungey_stragetic_bidding_NEM.pdf (all of which I will put into a reference folder in the repo)

# Time series
What metric
- see [Hyndman & Koehler (2005) Another look at measures of forecast accuracy](https://robjhyndman.com/papers/mase.pdf)
- mae, mape, mase
- Lagging & horizioning
- Trend, seasonality
- sklearn.TimeSeriesSplit

Model candidates for time series
- SARIMA
- random forest, xgboost
- convolution (1 or 2D)
- lstm or gru
- [Facebook's Prophet](https://github.com/facebook/prophet)
- [Amazon's Forecast](https://aws.amazon.com/forecast/)
