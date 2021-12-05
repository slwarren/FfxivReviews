import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud, ImageColorGenerator
from collections import Counter

nltk.download('stopwords')
stop = stopwords.words('english')
print(type(stop))
extra_stop = ["i've","i'd","ive","id","im","i'm","*am*","game","one","-","☐","also","would","dont","cant","wont","youre","isnt","theyre",
"ill","havent","couldnt","wasnt","youve","arent", "2", "1", "3","4","5","6","7","8","9",'0', "well","best","worst","trying","use","refund",
"square","doesnt","tried","able","got","made", "however","actually","love","give","far","keep","nothing","let","cannot","getting","could",
"thats","h1","already","may","take","bit","little","buying","due","unless","takes","literally","ago","finally","instead","wouldnt","either",
"definitely","someone","lots","yes","quite","come","probably","less","said","looking","overall","10","etc","everyone","set","fine","next",
"extremely","edit","20","yet","sure","shit","absolutely","later","others","started","list","amazing","job","done","especially","honestly",
"certain","else","keys","took","fucking","didnt","usually","past","cons","ff","based","found","cool","wait","seems","outside","told","wrong",
"que","basically","several","multiple","pros","comes","major","1010","seen","apparently","unable","maybe","minutes","months","running","email",
"random","company","spent","using","reason","guess","worse","oh","terrible","bought","log","purchase","realm","reborn","b","mmorpgs","tank",
"small","terms","current","key","fix","process","customer","register","issues","registration","hour","access"]

stop = stop + extra_stop


def get_reviews(appid, params={'json':1}):
    url = 'https://store.steampowered.com/appreviews/'
    response = requests.get(url=url+appid, params=params, headers={'User-Agent': 'Mozilla/5.0'})
    return response.json()

def get_n_reviews(appid, n=100, type='all'):
    reviews = []
    cursor = '*'
    params = {
        'json' : 1,
        'filter' : 'all',
        'language' : 'english',
        'day_range' : 9223372036854775807,
        'review_type' : type,
        'purchase_type' : 'all'
    }
    while n > 0:
        params['cursor'] = cursor.encode()
        params['num_per_page'] = min(100, n)
        n -= 100
        response = get_reviews(appid, params)
        cursor = response['cursor']
        reviews += response['reviews']
        if len(response['reviews']) < 100: break
    return reviews

def remove_common_terms(positive, negative):
    pos_list = positive
    pos_dict = dict(positive)
    neg_dict = dict(negative)
    for pos_word in pos_list:
        word = pos_word[0]
        if word in neg_dict:
            del neg_dict[word]
            del pos_dict[word]    
    return list(pos_dict.items()), list(neg_dict.items())

# Scrap reviews and save them to a csv to save time (so I don't have to scrap every time I run the program)

# pos_reviews=get_n_reviews('39210', 500, 'positive')
# neg_reviews=get_n_reviews('39210', 500, 'negative')
# pos_reviews = pd.DataFrame(pos_reviews)
# neg_reviews = pd.DataFrame(neg_reviews)

# all_reviews = get_n_reviews('39210', 1000, 'all')
# all_reviews = pd.DataFrame(all_reviews)
# all_reviews.to_csv('all_reviews.csv')
# pos_reviews.to_csv('pos_reviews.csv')
# neg_reviews.to_csv('neg_reviews.csv')


# all_reviews=pd.read_csv('C:/Users/aerof/3450/all_reviews.csv', usecols=[4,7,8,9,10])
pos_reviews=pd.read_csv('C:/Users/aerof/3450/pos_reviews.csv', usecols=[4,7,8,9,10])
neg_reviews=pd.read_csv('C:/Users/aerof/3450/neg_reviews.csv', usecols=[4,7,8,9,10])

# visualization of the sentiment of all 1000 top reviews

# counts=all_reviews['voted_up'].value_counts()
# print(counts)
# pyplot.bar([0,1], height=counts, tick_label=['Positive','Negative'])
# pyplot.xlabel("Sentiment of Reviews")
# pyplot.ylabel("Number of Reviews")
# pyplot.show()

# removing stop words and punctuation from reviews
pos_reviews['review']=pos_reviews['review'].str.lower()
pos_reviews['review']=pos_reviews['review'].str.replace('[^\w\s]','')
pos_reviews['review_no_stop_words']=pos_reviews['review'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

neg_reviews['review']=neg_reviews['review'].str.lower()
neg_reviews['review']=neg_reviews['review'].str.replace('[^\w\s]','')
neg_reviews['review_no_stop_words']=neg_reviews['review'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

# determining which words were most common in positive and negative reviews

# to get all words
pos_word_count = Counter(" ".join(pos_reviews['review_no_stop_words'].str.lower()).split()).most_common()
neg_word_count = Counter(" ".join(neg_reviews['review_no_stop_words'].str.lower()).split()).most_common()

# to get top 300 words
# pos_word_count = Counter(" ".join(pos_reviews['review_no_stop_words']).split()).most_common(500)
# neg_word_count = Counter(" ".join(neg_reviews['review_no_stop_words']).split()).most_common(500)

# remove words the two groups have in common and print the first 15
pos_words, neg_words = remove_common_terms(pos_word_count, neg_word_count)
print(pos_words[0:15])
print("\n===============\n")
print(neg_words[0:15])


# generate word clouds

# textt = " ".join(review for review in neg_reviews['review_no_stop_words'])
# wordcloud = WordCloud(max_words=50).generate(textt)
# pyplot.imshow(wordcloud, interpolation='bilinear')
# pyplot.axis("off")
# pyplot.savefig('wordcloudneg.png')
# pyplot.show()