import snscrape.modules.twitter as sntwitter
import pandas as pd
from pymongo import MongoClient

import datetime
# Set the search query and number of tweets to scrape
query = 'from:elonmusk'
num_tweets = 1000

# Create a list to store the scraped tweets
tweets = []

# Iterate through the search results and extract the tweet data
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i >= num_tweets:
        break
    tweets.append({
        'date': tweet.date.strftime('%Y-%m-%d %H:%M:%S'),
        'id': tweet.id,
        'url': tweet.url,
        'content': tweet.content,
        'user': tweet.user.username,
        'reply_count': tweet.replyCount,
        'retweet_count': tweet.retweetCount,
        'lang': tweet.lang,
        'source': tweet.sourceLabel,
        'like_count': tweet.likeCount
    })

# Convert the list of tweets to a Pandas dataframe
df = pd.DataFrame(tweets, columns=['date', 'id', 'url', 'content', 'user', 'reply_count', 'retweet_count', 'lang', 'source', 'like_count'])

# Print the dataframe
print(df)

     

client = MongoClient('mongodb+srv://rootguvi:rootguvi@cluster0.u37z9wj.mongodb.net/test')

     

database_name = client.twitter
db_collection = database_name.scrapingnew
data = {
    'Scraped Word': query,
    'Scraped Date': str(datetime.datetime.now),
    'Scraped Data': df.to_dict('records')
}
db_collection.insert_one(data)


