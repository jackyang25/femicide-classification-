# import numpy as np
import glob
import os
import pandas as pd
from os import listdir
# from stop_words import get_stop_words
import advertools as adv
import re
import stanza 
# import dill as pickle
# from pathos.multiprocessing import ProcessingPool as Pool
# import tqdm

stop_words = adv.stopwords['turkish']
nlp = stanza.Pipeline(lang='tr', processors='tokenize,pos,lemma',tokenize_pretokenized=True)

from pathlib import Path

inputDir = Path("/Users/kk2352/Dropbox/RA Data/TweetsInCSV2")
# dirname = globals()['_dh'][0]

# inputDir = os.path.abspath(os.path.join(dirname, '..', '..', 'RA Data', 'TweetsInCSV2'))

os.chdir(inputDir)
Files = glob.glob('*.csv')

start = 'location'
end = 'protected'

def cleanTweets(tweet):
    #remove punctuation and numbers
    tweet = re.sub('\n', ' ',tweet)
    tweet = re.sub(r"http\S+", '', tweet)
    tweet = re.sub(r"#\S+", '', tweet)
    tweet = re.sub(r"(?:\@|https?\://)\S+", "", tweet)
    tweet = re.sub(r'[^\w\s]', ' ', tweet)  
    #remove stop words:
    tweet_clean = [w for w in tweet.split() if not w in stop_words]
    tweet_clean = ' '.join(tweet_clean)
    #lemmatization: 
    doc = nlp(tweet_clean)
    lemmas = [word.lemma for sent in doc.sentences for word in sent.words]
    lemmas = [w for w in lemmas if not w in stop_words]
    tweet_clean = ' '.join(lemmas)
    return tweet_clean


def ProcessCSV(file):
    data = pd.read_csv(file,lineterminator='\n', dtype = {'retweetedTweet': 'unicode', 'quotedTweet': 'unicode'})
    data = data.drop(['Unnamed: 0'],axis=1)
    data = data.drop_duplicates().reset_index()
    data = data.drop(['index'],axis=1)
    dataTR = data[data['lang']=='tr'].reset_index()
    dataTR = dataTR.drop(['index'],axis=1)
    dataTR['Hashtags'] = [re.findall(r"#(\w+)", tweet) for tweet in dataTR['content']]
    dataTR['location'] = [(x.split(start))[1].split(end)[0] for x in dataTR['user']]
    dataTR['location'] = [re.sub(r'[^\w\s]', '', x) for x in dataTR['location']]
    dataTR['cleanTweet'] = [cleanTweets(text) for text in dataTR['content']]
    dataTR =  dataTR[dataTR['cleanTweet'].notna()]
    return dataTR

j = 0
k = 0
df = []
# I did :1670 so far, then I did 1675:1675+682(=2357), 
# then 2360:4000 but it seems stuck at 1260
# so I did 2360:3500 instead, then 3500:3530 and now it worked?
# I think it's done until 3600, or just about
for file in Files:
    print(j)
    try:
        dta = ProcessCSV(file)
        if len(df)==0:
            df = dta
        else:
            df = pd.concat([df,dta],ignore_index=True)
    except IndexError:
        k += 1
        print(pd.read_csv(file,lineterminator='\n')['Location'][0] + " caused an IndexError")
    j += 1

dfFinal = df[['date','url','user','replyCount', 'retweetCount', 'likeCount','quoteCount',
                    'retweetedTweet', 'quotedTweet', 'Name', 'Location', 'Hashtags', 'content', 'cleanTweet','location']]


# dfFinal.to_csv(os.path.abspath(os.path.join(dirname, '..', '..', 'RA Data', 'CleanTweets3.csv')), header = False)

dfFinal.to_csv(Path("/Users/kk2352/Dropbox/RA Data/CleanTweets4.csv"))