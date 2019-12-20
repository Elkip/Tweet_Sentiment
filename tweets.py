from twitterscraper import query_tweets
import datetime as dt
import pandas as pd
import re
from textblob import TextBlob

def get_tweets(query, begin_date=dt.date(2019, 12, 17), end_date=dt.date.today()):
    
    limit = 10
    lang = "english"
    
    tweets = query_tweets(query, begindate=begin_date, enddate=end_date, limit=limit, lang=lang)
    
    df = pd.DataFrame(t.__dict__ for t in tweets)
    return df['text']


# Remove special characters, links, and other garbage
def clean_tweets(tweets):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweets).split())


def get_tweet_sentiment(tweet):
    sent = TextBlob(tweet)
    for s in sent.sentence:
        print(s.sentiment)


def main():
    dirty_tweets = get_tweets("Star Wars: The Rise of the Skywalker")
    tweets = []
    for t in dirty_tweets:
        tweets.append(clean_tweets(t))
        get_tweet_sentiment(t)


if __name__=="__main__":
    main()