# Dependencies
import time
import random
import re
import tweepy
import json
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
import string
import datetime
import seaborn as sns
sns.axes_style('darkgrid')
sns.set_style('darkgrid')
# Import and Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Twitter API Keys
consumer_key = "TVWJaZ1J0GNIzrcL6DaTVe92b"
consumer_secret = "vYMdWen2vtC7UHtftq6CLd0oXI7PtG40eKh1gs2IIeq7mNLTQc"
access_token = "2280809480-xWf7aW6EdEg84sGeE8DiwACueGpa9DPUDltRFSF"
access_token_secret = "FbVtjlAUr7LQ6A9DOViaFzp0ISQdEoy1J7zvrEbTekESJ"

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
tweet_list = []


def analyze_user(target_user, request_user):
    df=pd.DataFrame()
    tweet_count=1
    compound_list  = []  
    # Loop through pages of tweets (total 100 tweets)
    for x in range(30): 
        if  tweet_count < 501:
            # Get all tweets from home feed        
            public_tweets = api.user_timeline(target_user,page=x)
            #print(public_tweets) 
            for tweet in public_tweets:
                text = tweet['text']
                #print(text)
                # Run Vader Analysis on each tweet
                compound = analyzer.polarity_scores(text)["compound"]
                # Add each value to the appropriate array
                compound_list.append(compound)                 
                tweet_count +=1
    # Generate column name and data
    user=target_user.translate({ord(i):None for i in '!@#$'}) 
    title="%s" % user
    #print(title)
    df[title]= compound_list
    #Genrate date
    dt = datetime.datetime.now().strftime('%m/%d/%Y')
    # Build a scatter plot for each data type
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.75, 0.8])
    ax.plot(df.index, df[user], color="skyblue", marker="o", linewidth=1)
    ax.legend(loc=2, bbox_to_anchor=(1,0.9), borderaxespad=0, title="Tweets")
    # Incorporate the other graph properties
    plt.title("Sentiment Analysis of Tweets for " + user + " (" + dt + ")")
    plt.ylabel("Tweet Polarity")
    plt.xlabel("Tweet Ago")
    plt.grid(True)
    plt.xlim([505, -5])
    plt.ylim([-1.0, 1.0])

    # Save the figure
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'analysis/')
    sample_file_name = "tweetout_" + target_user +".png"
    
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    plt.savefig(results_dir + sample_file_name)
    #plt.savefig('analysis/"tweetout_" + target_user +".png"')
    api.update_with_media((results_dir+sample_file_name), \
                            "Sentiment Analysis of Tweets for " +  user + \
                            " (" + dt + ") (Thx @" + request_user + "!!!)")

    # api.update_with_media(('analysis/"tweetout_" + target_user +".png"'), \
    #                        "Sentiment Analysis of Tweets for " +  user + \
    #                        " (" + dt + ") (Thx @" + request_user + "!!!)")
    # Show plot
    #plt.show()

while(True):
    #Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    # Target Search Term
    target_terms = ("@jingpc analyze:")
    # Variable for holding the oldest tweet
    received_tweets = api.search(target_terms, count=100, result_type="recent")
    for tweet in received_tweets["statuses"]:
        print(tweet["text"])
        if tweet["id_str"] not in tweet_list:
            tweet_list.append(tweet["id_str"]) 
            tweet_text=tweet["text"]
            #print(tweet["text"])
            tweet_text1=re.split('@', tweet_text)
            print(tweet_text1)
            try:
                #print(tweet_text1[2])
                target_user=tweet_text1[2]
            except:                             
                target_user="@nobody"
                continue                       
            request_user=tweet["user"]["screen_name"]
            print(request_user)
            print(target_user)
            analyze_user(target_user, request_user)                       
            
            
    print(tweet_list)
    # Once tweeted, wait 180 seconds before doing anything else
    time.sleep(180) 
