import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
keyword='building construction techniques'
since_date = '2022-01-01'
until_date = '2023-01-01'
max_tweets = 100
def scrape_tweets(keyword,since_date,until_date,max_tweets):
    print(scrape_tweets)
tweets_list=[]
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{keyword} since:{since_date} until:{until_date}').get_items()):
    if i >= max_tweets:
        break
    tweets_list.append([tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount, tweet.lang, tweet.sourceLabel, tweet.likeCount])
tweets_df = pd.DataFrame(tweets_list, columns=['Date', 'ID', 'URL', 'Content', 'User', 'Reply Count', 'Retweet Count', 'Language', 'Source', 'Like Count'])
def upload_to_mongodb(keyword,since_date,last_date,max_tweets,tweets_df):
    return tweets_df
client = pymongo.MongoClient('mongodb://localhost:27017/')
my_db = client['twitter_data']
my_collection = my_db['tweets']
data = {
    'keyword': 'building construction techniques',
    'since_date':'2022-01-01',
    'until_date': '2023-01-01',
    'max_tweets': '100',
    'tweets': tweets_df.to_dict('records')
}
my_collection.insert_one(data)

import streamlit as st
with st.sidebar:
    keyword = st.text_input('Keyword or Hashtag')
    since_date = st.date_input('Since Date')
    until_date = st.date_input('Until Date')
    max_tweets = st.number_input('Maximum Tweets', value=100) 
    
tweets_df = scrape_tweets(keyword, since_date, until_date, max_tweets)
st.dataframe(tweets_df)

if st.button('Upload to MongoDB'):
    upload_to_mongodb(keyword, since_date, until_date, max_tweets, tweets_df)
    
if st.button('Download CSV'):
    st.download_button(label='Download CSV', data=tweets_df.to_csv(), file_name=f'{keyword}.csv', mime='text/csv')
    
if st.button('Download JSON'):
    st.download_button(label='Download JSON', data=tweets_df.to_json(), file_name=f'{keyword}.json', mime='application/json')
