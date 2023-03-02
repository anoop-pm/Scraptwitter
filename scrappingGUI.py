import streamlit as st
import pandas as pd
import snscrape.modules.twitter as sntwitter
from pymongo import MongoClient
from datetime import datetime
import json


tweets = []
df = pd.DataFrame()
# This Function is Used to Scrap data Keywords come from Fields
def scrape_tweets(keyword, start_date, end_date, max_tweets):


    num_tweets = max_tweets

    search_term = keyword


    splitTime=str(start_date).split('-')
    print(str(splitTime))
    date_time_start = datetime(int(splitTime[0]), int(splitTime[1]), int(splitTime[2]))
    splitTime=str(end_date).split('-')
    date_time_end = datetime(int(splitTime[0]), int(splitTime[1]), int(splitTime[2]))
   
    # Scrape Twitter data using snscrape
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{search_term} since:{date_time_start.date()} until:{date_time_end.date()}').get_items()):
        if i >= num_tweets: 
            break
        tweets.append({
            'date': tweet.date.strftime("%Y-%m-%d %H:%M:%S"),
            'id': tweet.id,
            'url': tweet.url,
            'content': tweet.content,
            'user': tweet.user.username,
            'reply_count': tweet.replyCount,
            'retweet_count': tweet.retweetCount,
            'language': tweet.lang,
            'source': tweet.sourceLabel,
            'like_count': tweet.likeCount
        })

    df = pd.DataFrame(tweets)

    print(df)
    return df

# Upload data to MongoDB
def upload_to_mongodb(keyword, start_date, end_date, max_tweets):

    df = scrape_tweets(keyword, start_date, end_date, max_tweets)
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://rootguvi:rootguvi@cluster0.u37z9wj.mongodb.net/test')

    database_name = client.twitter
    db_collection = database_name.scraping

    data = {
        'Name': "twitterRecord",
        'Date': str(datetime.now),
        'Scraped Data': df.to_dict('records')
    }
    data_insert=db_collection.insert_one(data)
    return "Data Uploaded"


def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://combo.imgix.net/images/projects/twitter-awards/_1200x630_crop_center-center_82_none/TwitterAwards_COMBO_Thumbnail_02.jpg?mtime=1651005018");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 


st.title(':blue[Twitter Scraping]')

# Sidebar with search options
st.sidebar.header(':blue[Search Options]')
keyword = st.sidebar.text_input(':blue[Keyword or Hashtag]',placeholder='Search')
start_date = st.sidebar.date_input(':blue[Start Date]')
end_date = st.sidebar.date_input(':blue[End Date]')
max_tweets = st.sidebar.slider(':blue[Max Tweets]', 1, 1000, 100)

# Scrape tweets and display in table
if st.sidebar.button('Search'):
    st.subheader('Search Results')
    df = scrape_tweets(keyword, start_date, end_date, max_tweets)
    st.write(df)



col1, col2, col3 = st.columns([1,1,1])

with col1:
# Upload data to MongoDB
    if st.button('Upload to MongoDB'):
        result = upload_to_mongodb(keyword, start_date, end_date, max_tweets)
    
        st.write('Documents uploaded to MongoDB')

with col2:
# Download data in CSV format
    if st.button('Download CSV'):
        df = scrape_tweets(keyword, start_date, end_date, max_tweets)
        st.download_button('Download CSV', df.to_csv(index=False), 'tweets.csv', 'text/csv')

with col3:
# Download data in JSON format
    if st.button('Download JSON'):
        df = scrape_tweets(keyword, start_date, end_date, max_tweets)
        st.download_button('Download JSON', json.dumps(df.to_dict('records')), 'tweets.json', 'application/json')


