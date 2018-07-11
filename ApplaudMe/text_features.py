#%% Readability
from nltk.corpus import cmudict
from nltk.tokenize import sent_tokenize, word_tokenize

prondict = cmudict.dict()

numsyllables_pronlist = lambda l: len(list(filter(lambda s: s.lower()[-1].isdigit(), l)))


def text_statistics(text):
    word_count = get_word_count(text)
    sent_count = get_sent_count(text)
    syllable_count = sum(map(lambda w: max(numsyllables(w)), word_tokenize(text)))
    complex_count = sum(map(lambda w: max(numsyllables(w))>2, word_tokenize(text)))
    return word_count, sent_count, syllable_count, complex_count

def get_words(text):
    def is_valid_word(word):
        valid_word = word.isalpha()
        return valid_word
    word_list = [word for word in word_tokenize(text) if is_valid_word(word)]
    return word_list 
   
def get_word_count(text):
    word_in_text = get_words(text)
    return len(words_in_text)

def get_sentence_count(text):
    return len(sent_tokenize(text))

def get_syllable_count(text):
    word_list = get_words(text)
    for word in word_list:
        try:
            
    try:
        return list(set(map(numsyllables_pronlist, prondict[word.lower()])))
    except KeyError:
        return [0]
    
def flesch_grade_level(text):
    word_count = get_word_count(text)
    sentence_count = get_sentence_count(text)
    syllable_count = get_syllable_count(text)
    return 206.835 - 1.015*word_count/sentence_count - 84.6*syllable_count/word_count
 
fk_formula = lambda word_count, sent_count, syllable_count : 0.39 * word_count / sent_count + 11.8 * syllable_count / word_count - 15.59
def flesch_kincaid(text):
    word_count, sent_count, syllable_count, _ = text_statistics(text)
    return fk_formula(word_count, sent_count, syllable_count)

#Loading modules
import pickle
#Third party modules
from sklearn.externals import joblib
#Custom modules
from applaudMeNLP import get_text_topic_prob, get_article_topic, get_sentiment,\
                         get_readability, get_word_count

#loading topic models for transformation
lda_model = joblib.load('lda_model.pkl')
lda_topic_labels =  pickle.load(open('lda_topic_labels.p','rb'))
tf_vectorizer = joblib.load('tf_vect.pkl')

#Select a preloaded examples 
example_number = 2
with open('article{}.txt'.format(example_number),'rb') as fid:
     article = pickle.load(fid)
article_text = article['text']
article_title = article['title']
article_subtitle = article['subtitle']


#Transform article text
def get_text_topic_prob(article_text,tf_vectorizer,lda_model,lda_topic_labels):
    tf_text_vector = tf_vectorizer.transform([article_text])
    text_topic_probability = lda_model.transform(tf_text_vector)
    text_topic_probability = list(lda_topic_probability[0])
    return text_topic_probability

def get_article_topic(article_text,tf_vectorizer,lda_model,lda_topic_labels):
    article_topic = []
    text_topic_probability = get_text_topic_prob(article_text,tf_vectorizer,lda_model,lda_topic_labels)
    article_topic.append(lda_topic_labels[text_topic_probability.argmax()])
    text_topic_probability[text_topic_probability.argmax()]=0
    if text_topic_probability[text_topic_probability.argmax()]>0.3:
        article_topic.append = lda_topic_labels[text_topic_probability.argmax()]
    return article_topic

def get_readability(article_text):
    grade_level = flesch_kincaid(article_text)
    gunning_fog_index = gunning_fog(article_text)
    return {'grade_level':grade_level,'gunning_fog':gunning_fog_index} 

def get_sentiment(article_text):    
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sentiment_analyzer = SentimentIntensityAnalyzer()
    sentiment_list = sentiment_analyzer.polarity_scores(article_text)
    return sentiment_list
    
#FK_ease = '{0:.2f}'.format(flesch_kincaid(article))   
fkarticle = '{0:.2f}'.format(flesch_kincaid(article))
question_count = article.count('?')

#%% Machine Learning
image_count = 3
title = 'Great title for a Medium blog'
article_word_count = get_word_count(article)
article_title_word_count = get_word_count(title)
ml_classifier = joblib.load('classifier.pkl')
ml_scaler = joblib.load('scaler.pkl')
def get_article_features(article_text,article_title,article_subtitle,image_count,publication_follower_count):
    X_raw = []
    X_raw.append(image_count)
    X_raw.append(publication_follower_count)
    X_raw.append(get_word_count(article_text))
    X_raw.append(get_word_count(article_title))
    X_raw.append(get_word_count(article_subtitle))
    for topic_prob in get_text_topic_prob(article_text):
        X_raw.append(topic_prob)
    X_raw.append(question_count)
    X_raw.append(FK_ease)
    for article_readability_index in get_readability(article_text):
        X_raw.append(article_readability_index)
    for sentiment_metric in get_sentiment(article_text):
        X_raw.append(sentiment_metric)
    return X_raw

X_raw = get_article_features(article_text,article_title,article_subtitle,image_count,publication_follower_count)
feature_labels = pickle.load(open('feature_labels.p','rb'))
X_scaled = ml_scaler.transform([X_raw])
y_pred = ml_classifier.predict(X_scaled)
prob = floor(100 * ml_classifier.predict_proba(X_scaled)[0, 1])

article_topic = get_article_topic(article_text,tf_vectorizer,lda_model,lda_topic_labels)
if len(article_topic)>1:
    message_topic = "We believe your topic tag should be "+article_topic[0]
elif len(article_topic)>1:
    message_topic = "We believe your topic tags should be "+article_topic[0]+" and "+article_topic[1]

#article_title, color_choice, probability, message, topic, image_location

def render_template(base_text, probability, title, message, message_topic,readability,X_raw):
    if y_pred:
        message = 'Congratulations, your article is likely to become popular in Medium'
        render_template(
            'result.html',
            probability=prob,
            article_title=title,
            image_location=image_location,
            css_hash=css_link,
            message=message,
            topic = message_topic,
            readability = readability_index,
            color_choice=color_choice
            )
    else:
        message = 'Unfortunately we believe your article will not receive enough applause in Medium. \n' + \
                  'Use the following tips to improve your article'



#Print metrics:
if FK_grade>7:
        msg2 = 'Your current grade level is '\
        + fkarticle +', aim to write for a 6th-grade reading level' 
    if (question_count < 6) | (question_count > 8):
        msg3 = 'For articles in topic ' + topic1\
        + ' try to include 6 questions and a simple call to action at the end'

print(msg2)
print(msg3)

print(               'Your article has a {} chance to reach {} claps in 4 weeks' 
e)


#%%

# Compute meta feature ranks
import pandas as pd
feature_ranks = pd.Series(
    clf.coef_.T.ravel()[:len(features)],
    index=features
)



#%%
from bs4 import BeautifulSoup
import requests
url = 'https://medium.com/airbnb-engineering/unboxing-the-random-forest-classifier-the-threshold-distributions-22ea2bb58ea6'
json_req = requests.get(url)#, headers={"Accept": "application/json"})
#%%
html = BeautifulSoup(json_req.text, "html.parser")
#%%
content_tag = html.find("div", attrs={"class": "postArticle-content"})
print(content_tag)

#%%
ESCAPE_CHARACTERS = "])}while(1);</x>"

test_json = json.loads(json_req.text.replace(ESCAPE_CHARACTERS, "").strip())
#json.loads(json_req.text.strip())
