import tweepy
from textblob import TextBlob
import pandas as pd 
from badwords import bad_words_highlight
import numpy as np
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

from nltk.stem.porter import *
stemmer = PorterStemmer()

def tweetAnalysis(search_tweet,count):
    # authenticating
    consumerKey = "TEQFrdbSGCbvi2kchzF82Cx67"
    consumerSecret = "b9xHHubPbKsGPOhwTqznh6xt8oAO3Noqo5R9nmgJCIrHpDxcPg"
    accessToken = "1266960995869618176-1fiUMxF6YniwRytzIKpiOOHhpykceH"
    accessTokenSecret = "Y6wAIo3HjcfpzfN9RLKDCKlDWYpsLVPWGSzXoG8jXFrAx"

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)

    api = tweepy.API(auth)

    #-------------------------------------------------------------------------
        
    t = []
    tweets = api.search_tweets(search_tweet,count=count, tweet_mode='extended')
    for tweet in tweets:
        polarity = TextBlob(tweet.full_text).sentiment.polarity
        subjectivity = TextBlob(tweet.full_text).sentiment.subjectivity
        t.append([tweet.created_at,tweet.full_text,tweet.entities,tweet.user.id,tweet.user.name,tweet.user.profile_image_url_https,tweet.user.location,polarity,subjectivity])
        

    filename = 'dataset.csv'
    testfields = ['created_at','full_text','user_details','user','user_name','image','location','polarity','subjectivity']

    df = pd.DataFrame(t)

    df.columns = testfields

    unique_text = df.full_text.unique()

    # Number of unique users
    unique_user = df.user.unique()

    # Number of Unique Locations
    unique_location = df.location.unique()

    df.location.value_counts().head(10)

    df.full_text.count()

    def remove_pattern(input_txt, pattern):
        r = re.findall(pattern, input_txt)
        for i in r:
            input_txt = re.sub(i, '', input_txt)
            
        return input_txt

    df['Clean_text'] = np.vectorize(remove_pattern)(df['full_text'], "@[\w]*")

    # remove special characters, numbers, punctuations
    df['Clean_text'] = df['Clean_text'].str.replace("[^a-zA-Z#]", " ")

    df['Clean_text'] = df['Clean_text'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))

    tokenized_tweet = df['Clean_text'].apply(lambda x: x.split())

    tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x]) # stemming
    tokenized_tweet.head()

    for i in range(len(tokenized_tweet)):
        tokenized_tweet[i] = ' '.join(tokenized_tweet[i])

    df['Clean_text'] = tokenized_tweet

    df.loc[:,('full_text','Clean_text')]

    # Number of unique tweets
    unique_clean_text = df.Clean_text.unique()
    unique_full_text = df.full_text.unique()

    df.drop_duplicates(subset=['Clean_text'], keep = 'first',inplace= True)

    df.reset_index(drop=True,inplace=True)

    df['Clean_text_length'] = df['Clean_text'].apply(len)


    df[df['Clean_text_length']==0]['Clean_text'] ## Looks like these are tweets with different languages or just hastags.
    # We can simply drop these tweets

    list = df[df['Clean_text_length']==0]['Clean_text'].index

    df.drop(index = list,inplace=True)

    df.reset_index(drop=True,inplace=True)

    def calculate_sentiment(Clean_text):
        return TextBlob(Clean_text).sentiment

    def calculate_sentiment_analyser(Clean_text):    
        return analyser.polarity_scores(Clean_text)

    tempr = df.Clean_text.apply(calculate_sentiment)
    tempd = [{"polarity":tempi[0],"subjectivity":tempi[1]} for tempi in tempr]
    df['sentiment'] = tempd
    df['sentiment_analyser']=df.Clean_text.apply(calculate_sentiment_analyser)


    s = pd.DataFrame(index = range(0,len(df)),columns= ['compound_score','compound_score_sentiment'])

    nfneg = 0
    nfneu = 0
    nfpos = 0

    for i in range(0,len(df)): 

        s['compound_score'][i] = df['sentiment_analyser'][i]['compound']
        
        if (df['sentiment_analyser'][i]['compound'] <= -0.05):
            s['compound_score_sentiment'][i] = 'Negative'
            nfneg += 1    
        if (df['sentiment_analyser'][i]['compound'] >= 0.05):
            s['compound_score_sentiment'][i] = 'Positive'
            nfpos += 1   
        if ((df['sentiment_analyser'][i]['compound'] > -0.05) & (df['sentiment_analyser'][i]['compound'] < 0.05)):
            s['compound_score_sentiment'][i] = 'Neutral'
            nfneu += 1   
        
    df['compound_score'] = s['compound_score']
    df['compound_score_sentiment'] = s['compound_score_sentiment']

    # print(df.head(4))

    # print(df.info())

    result = df.to_dict('records')

    finalR = {"nof":{"neg":nfneg,"neu":nfneu,"pos":nfpos},"result":result}

    sum=0
    for i in ['neg','neu','pos']:
        sum+=finalR['nof'][i]

    for i in ['neg','neu','pos']:
        finalR['nof'][i]=round((finalR['nof'][i]/sum)*100,2)

    for r in finalR["result"]:

        r["sentiment"]["polarity"] = round(r["sentiment"]["polarity"],4)
        r["sentiment"]["subjectivity"] = round(r["sentiment"]["subjectivity"],4)
        r["compound_score"] = round(r["compound_score"],4)
        r["full_text"] = bad_words_highlight(r["full_text"])["rtext"]

    return finalR

if __name__ == '__main__':
    
    result = tweetAnalysis("hate",3)

    print(result["nof"])



