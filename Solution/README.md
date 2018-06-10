
## News Mood Analysis
BBC, CBS, and FOX are all positive with BBC being more positive than the others (06/08).
CNN tweets this morning (06/08) seems to be more towards Positive side.
NY Times is a little bit more on negative side.
#### Load all dependencies


```python
# %load Dependecies.py
import json
import numpy as np
import pandas as pd

import config
import tweepy
import time

# Import and Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

import matplotlib.pyplot as plt
import seaborn as sns

```

#### Tweepy API Authentication


```python
# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)
```

#### Function to analyzise a tweet and return the analysis score


```python
def analyze_tweet(tweet):
    tweet = tweet._json
    #  Run Vader Analysis on each tweet
    score = analyzer.polarity_scores(tweet["text"])
    return score
```

#### Function to analyze latest 100 tweets of any given user.


```python
# %load analyse_tweeter.py

def analyse_tweeter(user_handle):
    # latest tweet_id
    largest_id = 0

    # Counter
    counter = 1
    
    while counter < 100 :
       # Loop through 4 pages of tweets, 25 tweets per page (total 100 tweets)
        for page in tweepy.Cursor(api.search, q=target_term, max_id=largest_id, count = 25).pages(4):

            if not largest_id:
                largest_id = page[0].id
            if counter < 100 :
                # Loop through all tweets
                for tweet in page:
                # Run Vader Analysis on each tweet
                    score = analyze_tweet(tweet)
                    tweets_ago = counter

                    # Add sentiments for each tweet into an array
                    sentiments.append({ "Source": user_handle,
                                       "Tweet Text": tweet.text,
                                       "Tweet Date" : tweet.created_at,
                                       "Compound": score["compound"],
                                       "Positive": score["pos"],
                                       "Negative": score["neg"],
                                       "Neutral": score["neg"],
                                       "Tweets Ago": counter})

                    # Add to counter 
                    counter = counter + 1


    return sentiments

```

### Sentiment Analysis of the Twitter activity of various news oulets


```python
# Target Account
target_users = ("@BBC", "@CBS", "@CNN", "@FoxNews", "@nytimes")
sentiments = []

for target_term in target_users:
    sentiments = analyse_tweeter(target_term)
# Convert sentiments to DataFrame
sentiments_pd = pd.DataFrame.from_dict(sentiments)

```


```python
sentiments_pd.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Compound</th>
      <th>Negative</th>
      <th>Neutral</th>
      <th>Positive</th>
      <th>Source</th>
      <th>Tweet Date</th>
      <th>Tweet Text</th>
      <th>Tweets Ago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-0.5423</td>
      <td>0.149</td>
      <td>0.149</td>
      <td>0.000</td>
      <td>@BBC</td>
      <td>2018-03-29 18:14:24</td>
      <td>@BBC If they don't inform you, it's a crime be...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.3415</td>
      <td>0.000</td>
      <td>0.000</td>
      <td>0.099</td>
      <td>@BBC</td>
      <td>2018-03-29 18:14:20</td>
      <td>RT @Femi_Sorry: Oh and as a side note @BBC, ev...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.8689</td>
      <td>0.000</td>
      <td>0.000</td>
      <td>0.412</td>
      <td>@BBC</td>
      <td>2018-03-29 18:14:07</td>
      <td>Thanks to the @BBC and Ewan and Colin McGregor...</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.0000</td>
      <td>0.000</td>
      <td>0.000</td>
      <td>0.000</td>
      <td>@BBC</td>
      <td>2018-03-29 18:13:52</td>
      <td>Someone should get a job @BBC @TheEconomist or...</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.3415</td>
      <td>0.000</td>
      <td>0.000</td>
      <td>0.099</td>
      <td>@BBC</td>
      <td>2018-03-29 18:13:35</td>
      <td>RT @Femi_Sorry: Oh and as a side note @BBC, ev...</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>




```python
# save data to CSV
sentiments_pd.to_csv("NewsMood.csv", encoding="UTF-8")
```


```python
# Save data to Excel
sentiments_pd.to_excel("NewsMood.xlsx", encoding="UTF-8")
```

### Sentiment Analysis of Tweets (Scatter Plot)


```python
plt.figure(figsize=(10,8))
sns.set()
plt.gca().invert_xaxis()

handle1 = plt.scatter(sentiments_pd[sentiments_pd["Source"]=="@BBC"]["Tweets Ago"], 
                      sentiments_pd[sentiments_pd["Source"]=="@BBC"]["Compound"], 
                      s = 100,alpha = 0.8, marker="o",edgecolors="black",label = "BBC")

handle2 = plt.scatter(sentiments_pd[sentiments_pd["Source"]=="@CBS"]["Tweets Ago"], 
                      sentiments_pd[sentiments_pd["Source"]=="@CBS"]["Compound"], 
                      s = 100,alpha = 0.8, marker="o",edgecolors="black",label = "CBS")

handle3 = plt.scatter(sentiments_pd[sentiments_pd["Source"]=="@CNN"]["Tweets Ago"], 
                      sentiments_pd[sentiments_pd["Source"]=="@CNN"]["Compound"], 
                      s = 100,alpha = 0.8, marker="o",edgecolors="black",label = "CNN")

handle4 = plt.scatter(sentiments_pd[sentiments_pd["Source"]=="@FoxNews"]["Tweets Ago"], 
                      sentiments_pd[sentiments_pd["Source"]=="@FoxNews"]["Compound"], 
                      s = 100,alpha = 0.8, marker="o",edgecolors="black",label = "FOX")

handle5 = plt.scatter(sentiments_pd[sentiments_pd["Source"]=="@nytimes"]["Tweets Ago"], 
                      sentiments_pd[sentiments_pd["Source"]=="@nytimes"]["Compound"], 
                      s = 100,alpha = 0.8, marker="o",edgecolors="black",label = "NYTimes")


lgnd = plt.legend(handles= [handle1, handle2, handle3, handle4, handle5], loc=(1.1, 0.55), title= 'Media Sources')

# Incorporate the other graph properties
plt.title("Sentiment Analysis of Media Tweets for %s" % (time.strftime("%x")))
plt.ylabel("Tweet Polarity")
plt.xlabel("Tweets Ago")
plt.ylim(-1, 1)

plt.show()
```



#### Aggregate Compound sentiments


```python
sentiments_grp = sentiments_pd.groupby("Source")
aggr_comp_sentiments = sentiments_grp["Compound"].mean()
aggr_comp_sentiments
```




    Source
    @BBC       -0.083672
    @CBS        0.047934
    @CNN       -0.066505
    @FoxNews    0.014742
    @nytimes   -0.014788
    Name: Compound, dtype: float64



### Bar plot visualizing the Overall Sentiments 


```python
sns.set_style("dark") # grid off by default in seaborn

# Set the font dictionaries (for plot title and axis titles)
title_font = {'fontname':'Arial', 'size':'16', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'} # Bottom vertical alignment for more space
axis_font = {'fontname':'Arial', 'size':'14'}

# Splice the data between different news channels
fig, ax = plt.subplots(figsize=(10,8))
ticks_loc = np.arange(len(comp_sentiments))
width = 1
rectsBBC = ax.bar(ticks_loc[0], aggr_comp_sentiments[0], width, color='skyblue', edgecolor = 'black')
rectsCBS = ax.bar(ticks_loc[1], aggr_comp_sentiments[1], width, color='green', edgecolor = 'black')
rectsCNN = ax.bar(ticks_loc[2], aggr_comp_sentiments[2], width, color='red', edgecolor = 'black')
rectsFOX = ax.bar(ticks_loc[3], aggr_comp_sentiments[3], width, color='blue', edgecolor = 'black')
rectsNYT = ax.bar(ticks_loc[4], aggr_comp_sentiments[4], width, color='yellow', edgecolor = 'black')

# Set labels, tick marks, and axis limits.
ax.set_title("Overall Media Sentiment based on Twitter (%s)" % (time.strftime("%x")), **title_font)
ax.set_xlabel("News Channel", **axis_font)
ax.set_ylabel("Tweet Polarity", **axis_font)
ax.set_xticks(ticks_loc)
ax.set_xticklabels(('BBC', 'CBS', 'CNN', 'Fox', 'NYTimes'))
ax.set_xlim(-0.5)

# Use functions to label the polarity bars
def autolabel(rects, value):
    for rect in rects:
        height = float(rect.get_height())
        ax.text(rect.get_x() + rect.get_width()/2, height,
                value,
                ha='center', va='bottom', color="black")

# Call functions to implement the function calls
autolabel(rectsBBC,round(aggr_comp_sentiments[0],3) )
autolabel(rectsCBS,round(aggr_comp_sentiments[1],3))
autolabel(rectsCNN, round(aggr_comp_sentiments[2],3))
autolabel(rectsFOX,round(aggr_comp_sentiments[3],3))
autolabel(rectsNYT,round(aggr_comp_sentiments[4],3))


# Show the Figure
plt.show()
```



