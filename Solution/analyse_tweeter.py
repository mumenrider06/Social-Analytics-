# function to analyze latest 100 tweets of any given user.
def analyse_tweeter(user_handle):
    # latest tweet_id
    largest_id = 0

    # Counter
    counter = 1
    
    while counter < 100 :
       # Loop through 5 pages of tweets (total 100 tweets)
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

