from twitterscraper import query_tweets
import datetime as dt
import pandas as pd
import re
from textblob import TextBlob
import webbrowser

def get_tweets(query, num_tweets, begin_date=dt.date(2019, 12, 20), end_date=dt.date.today()):
    limit = num_tweets
    lang = "english"
    
    tweets = query_tweets(query, begindate=begin_date, enddate=end_date, limit=limit, lang=lang)
    
    df = pd.DataFrame(t.__dict__ for t in tweets)
    return df['text']


# Remove special characters, links, and other garbage
def clean_tweets(tweets):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweets).split())


def get_tweet_sentiment(tweets):
    num_opinions = 0
    pos_opinions = 0
    neg_opinions = 0
    pos_df = {'Tweet': [], 'Polarity': [], 'Subjectivity':[]}
    neg_df = {'Tweet': [], 'Polarity': [], 'Subjectivity':[]}
    nut_df = {'Tweet': [], 'Polarity': [], 'Subjectivity':[]}
    for tweet in tweets:
        blob = TextBlob(tweet)
        if blob.sentiment.polarity > 0.1:
            num_opinions += 1
            pos_opinions += 1
            pos_df['Tweet'].append(tweet)
            pos_df['Polarity'].append(blob.sentiment.polarity)
            pos_df['Subjectivity'].append(blob.sentiment.subjectivity)
        elif blob.sentiment.polarity < -0.1:
            num_opinions += 1
            neg_opinions += 1
            neg_df['Tweet'].append(tweet)
            neg_df['Polarity'].append(blob.sentiment.polarity)
            neg_df['Subjectivity'].append(blob.sentiment.subjectivity)
        else:
            nut_df['Tweet'].append(tweet)
            nut_df['Polarity'].append(blob.sentiment.polarity)
            nut_df['Subjectivity'].append(blob.sentiment.subjectivity)
            
    print("\n{:.2%} analyzed tweets had a negative sentiment".format(neg_opinions / num_opinions))
    print("{:.2%} analyzed tweets had a positive sentiment".format(pos_opinions / num_opinions))
    
    pd.set_option('display.max_colwidth', -1)
    pd.set_option('display.width', 2000)
    while(True):
        choose = input("Type one of the following:\nN = View Negative Tweet \
Results\nP = View Positive Tweet Results\nU = View Uncatagorized Tweets\nE = Exit\n")
        df = pd.DataFrame({})
        if choose.upper() == 'E':
            break
        elif choose.upper() == 'P':
            df = pd.DataFrame(pos_df)
        elif choose.upper() == 'N':
            df = pd.DataFrame(neg_df)
        elif choose.upper() == 'U':
            df = pd.DataFrame(nut_df)
        df.to_html('temp.html')
        webbrowser.open_new_tab('temp.html')


def main():
    query = input("Enter a topic for twitter sentiment analysis: ")
    num_tweets = int(input("Enter number of tweets to analyze: "))
    custom_dates = input("Custom date range? (Y/N) ")
    if custom_dates.lower() == "y":
        start = input("Enter a start date (mm-dd-yyyy): ")
        end = input("Enter an end date (mm-dd-yyyy): ")
        dirty_tweets = get_tweets(query, num_tweets, dt.datetime.strptime(start, 
'%m-%d-%Y'), dt.datetime.strptime(end, '%m-%d-%Y'))
    else:    
        dirty_tweets = get_tweets(query, num_tweets)
    
    tweets = []
    for t in dirty_tweets:
        tweets.append(clean_tweets(t))
    get_tweet_sentiment(tweets)



if __name__=="__main__":
    main()