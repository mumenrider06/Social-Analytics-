# function to analyzise a tweet and return the analysis score
def analyze_tweet(tweet):
    tweet = tweet._json
    #  Run Vader Analysis on each tweet
    score = analyzer.polarity_scores(tweet["text"])
    return score