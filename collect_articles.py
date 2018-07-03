"""
@author: hpfigueroa
"""
#%%
import datetime as dt
import random
from MediumAPI import mediumparser
import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#%%
HTML_PARSER = "html.parser"
from bs4 import BeautifulSoup
from selenium import webdriver
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#%%
def getPostsByTagsByDays(tag_list, day_list):
    MediumObj = mediumparser.Medium()
    allPosts = []
    allPublications = []
    counterpost = 0
    counterpub = 0
    post_list_ref = open('PostTagList' + str(dt.date.today()) + '.txt', 'w', encoding='utf-8')
    post_tag_num_ref = open('PostTagNumbers'+str(dt.date.today())+'.txt', 'w', encoding='utf-8')    
    pub_list_ref = open('PubTagList' + str(dt.date.today()) + '.txt', 'w', encoding='utf-8')
    pub_tag_num_ref = open('PubTagNumbers'+str(dt.date.today())+'.txt', 'w', encoding='utf-8')    

    for day in day_list:
        for tag in tag_list:
            try:
                tag_day_url = MediumObj.build_tag_day_url(tag,day)
                tag_payload = MediumObj._get_request_payload(tag_day_url)
                tag_payload_filename = 'payload_' + tag + '_' + day.replace('/','-') + str(dt.date.today()) + '.p'
                pickle.dump(tag_payload,open(tag_payload_filename, "wb" ))
                postlist = mediumparser.parse_post_list(tag_payload)
                publicationlist = mediumparser.parse_publication_list(tag_payload)
                if(postlist is not None):
                    allPosts.append(postlist)
                    num_posts = len(postlist)
                    counterpost += num_posts
                    print("Found ",num_posts,". Total posts collected so far: ", counterpost)
                    output = day + "," + tag + "," + str(num_posts) + "\n"
                    post_tag_num_ref.write(output)
                    for post in postlist:
                        linepost = post.post_id + "," + post.post_url + "," + str(post.word_count) + "\n"
                        post_list_ref.write(linepost)
                else:
                    continue
            except Exception as e:
                print("Problem assembling postlist ", counterpost, "Exception is: ", e)

            try:
                if(publicationlist is not None):
                    allPublications.append(publicationlist)
                    num_publications = len(publicationlist)
                    counterpub += num_publications
                    print("Found ", num_publications, ". Total publications collected so far: ", counterpub)
                    output = day + "," + tag + "," + str(num_publications) + "\n"
                    pub_tag_num_ref.write(output)
                    for publication in publicationlist:
                        linepub = publication.publication_id + "," + publication.pub_url + "," + str(publication.follower_count) + "\n"
                        pub_list_ref.write(linepub)
                else:
                    continue

                time.sleep(random.randint(10,30))
            except Exception as e:
                print("Problem assembling publicationlist ", counterpost, "Exception is: ", e)
    
                # if(browserdriverB == None):
                #     print("chromedriver shut off")
                #     browserdriverB = webdriver.Chrome(exec_path)
                #     print("chrome webdriver restarted")
                # continue
    pickle.dump(allPosts,open("allPosts_"+str(dt.date.today())+"_"+str(num_posts)+".p", "wb" ))
    pickle.dump(allPublications,open("AllPublications_"+str(dt.date.today())+"_"+str(num_publications)+".p", "wb" ))
    post_tag_num_ref.close()
    post_list_ref.close()
    pub_tag_num_ref.close()
    pub_list_ref.close()

    return allPosts,allPublications
#%%%
#popular_tags = ['health','writing']
#daylist = ['2018/06/07']
popular_tags = ['health','writing','design','entrepreneurship','politics','programming','business','data-science','machine-learning','artificial-intelligence','culture','sex','travel','fitness','science']
#daylist = ['2018/06/07','2018/06/08','2018/06/09','2018/06/10','2018/06/11','2018/06/12','2018/06/13']
#daylist = ['2018/05/19','2018/05/20','2018/05/21','2018/05/22','2018/05/23','2018/05/24','2018/05/25']
startdate = dt.datetime(2018,1,1)
daylist = []
for x in range(151):
    xdate = startdate + dt.timedelta(days=x)
    daylist.append(xdate.strftime('%Y/%m/%d'))
    
#%%
PostList,PublicationList = getPostsByTagsByDays(popular_tags,daylist)
#%%
#%%% Creating a dictionary
postdf = pd.DataFrame()
tagindex = 0
post_tag_df = pd.read_csv('PostTagNumbers2018-06-25_2018.txt',header=None,names=['date','tag','post_count'])
archive_date = []
for postdict in PostList:
    tag = post_tag_df.iloc[tagindex]['tag']
    for post in postdict:
        if post.detected_language != 'en':
            continue
        if (post.word_count<200) or (post.word_count>5000):
            continue
        post.post_tags = tag
        archive_date = post_tag_df.iloc[tagindex]['date']
        if postdf.empty:
            count = 0
            postdf = pd.DataFrame(mediumparser.to_dict(post),index=[count])
        else:
            postdf = pd.concat([postdf,pd.DataFrame(mediumparser.to_dict(post),index=[count])])
        count += 1
    tagindex += 1 
    print(tagindex)
#%%% adding the archive date
archive_date = []
tagindex = 0
for postdict in PostList:
    for post in postdict:
        if post.detected_language != 'en':
            continue
        if (post.word_count<200) or (post.word_count>5000):
            continue
        archive_date.append(post_tag_df.iloc[tagindex]['date'])
    tagindex += 1 
    print(tagindex)

#%%
npostdf = postdf.drop_duplicates('post_id').copy()
#%%
npostdf['clap_count'].hist(bins=range(0,400,20))
#%%
npostdf['y_train'] = npostdf['clap_count']>99
#%%
#%%
def plot_hist(df,y_value,category):
    df1 = df[y_value][df[category]]
    df2 = df[y_value][df[category]==False]
    plt.figure()
    meandf1 = np.mean(df1)
    stddf1 = np.std(df1)
    #meandf2 = np.mean(df2)
    #stddf2 = np.std(df2)
    plt.hist(df1, alpha=0.5, bins = range(int(meandf1-3*stddf1),int(meandf1+3*stddf1),np.max(1,int(stddf1/20))))
    plt.hist(df2, alpha=0.5, bins = range(int(meandf1-3*stddf1),int(meandf1+3*stddf1),np.max(1,int(stddf1/20))))
#%%
plot_hist(npostdf,'word_count','y_train')
#%%
npostdf.hist('word_count',by='y_train',bins=range(0,5000,100))
#%%
npostdf_sort = npostdf.sort_values(by=['clap_count'],ascending=False)
npostdf_sort.index = range(len(npostdf))
#%%
browser = webdriver.Chrome()
posttxtlist = []
postidlist = []
#%%
for i in range(6000,6300):
    post_url = npostdf_sort['post_url'][i]
    try:
        browser.get(post_url)
    except Exception as e:
        print("Problem with: ", i)
        print("Exception: ", e)
        print(type(e))
        continue
    try:
        content_elements = browser.find_element_by_class_name("postArticle-content")
    except Exception as e:
        print("Problem with: ", i)
        print("Exception: ", e)
        print(type(e))
        continue
    inner_html = BeautifulSoup(content_elements.get_attribute("innerHTML"), HTML_PARSER)
    post_text = inner_html.get_text(separator=" ")
    posttxtlist.append(post_text)
    postidlist.append(npostdf_sort['post_id'][i])
    print(i,post_url)
    
    time.sleep(npostdf_sort['read_time'][i]*20)
    if i%30 == 29:
        pickle.dump(posttxtlist,open('posttxtlist'+str(i)+'.p','wb'))
        pickle.dump(postidlist,open('postidlist'+str(i)+'.p','wb'))
#%%
pickle.dump(posttxtlist,open('posttxtlist'+str(i)+'.p','wb'))
pickle.dump(postidlist,open('postidlist'+str(i)+'.p','wb'))

#%%
#plot_hist(npostdf,'image_count','y_train')
plt.legend(['Fail','Success'])
df1 = npostdf['word_count'][npostdf['y_train']]
df2 = npostdf['word_count'][npostdf['y_train']==False]
plt.figure()
plt.hist(df1, alpha=0.5, bins = range(0,5000,50), density=True)
plt.hist(df2, alpha=0.5, bins = range(0,5000,50), density=True)
plt.legend(['Success','Fail'])


#%%%
df1 = npostdf['word_count'][npostdf['y_train']]
df2 = npostdf['word_count'][npostdf['y_train']==False]
#%%%
import seaborn as sns
#%%
sns.set(style="darkgrid")
#%%
ax = sns.countplot(x="post_tags", data=npostdf_sort)
#%%
ax = sns.countplot(x="post_tags", hue="y_train",data=npostdf_sort)

#%%
#%%
sns.set(style="darkgrid")
ax = sns.countplot(x="post_tags",
                   data=postdf)#,
                   #order = postdf['post_tags'].value_counts().index)
#ax = sns.countplot(x="post_tags", hue="y_train",data=npostdf_sort)


#%% Analyzing daily results, selecting a particular day
popular_tags = ['health','writing','design','entrepreneurship','politics','programming','business','data-science','machine-learning','artificial-intelligence','culture','sex','travel','fitness','science']

daily_stats = postdf[['post_id','archive_date']].groupby('archive_date').count()
daily_stats['clap_mean'] = postdf[['clap_count','archive_date']].groupby('archive_date').mean().values
daily_stats['q80'] = postdf[['clap_count','archive_date']].groupby('archive_date').quantile([0.8]).values

#%%
for tag in popular_tags:
    tempdf = postdf.loc[postdf['post_tags']==tag][['clap_count','archive_date']].groupby('archive_date').quantile(0.8)
    tempdf.columns = ['{}_q80'.format(tag)]
    daily_stats = pd.concat([daily_stats,tempdf], axis=1)
    tempdf = postdf.loc[postdf['post_tags']==tag][['clap_count','archive_date']].groupby('archive_date').count()
    tempdf.columns = ['{}_count'.format(tag)]
    daily_stats = pd.concat([daily_stats,tempdf], axis=1)
    tempdf = postdf.loc[postdf['post_tags']==tag][['clap_count','archive_date']].groupby('archive_date').mean()
    tempdf.columns = ['{}_mean'.format(tag)]
    daily_stats = pd.concat([daily_stats,tempdf], axis=1)

#%%
plot_tags = ['health','writing','design','politics','programming','business','machine-learning','artificial-intelligence','travel']

plot_list = [tag+'_q80' for tag in plot_tags]
daily_stats[plot_list].plot()
#%%
daily_stats[plot_list].rolling(21, min_periods=14).mean().plot()
#%%
plot_list = [tag+'_count' for tag in plot_tags]
daily_stats[plot_list].rolling(21, min_periods=14).mean().plot()
#%%
result =  postdf[postdf.post_id.duplicated()][['post_id','post_tags']]
result.index = result['post_id']
result.drop(['post_id'],axis=1, inplace=True)
for tag in ['health']:#popular_tags:
    tempdf = postdf.loc[postdf['post_tags']==tag][['post_id','post_tags']]
    tempdf.index = tempdf['post_id']
    tempdf.drop(['post_id'],axis=1, inplace=True)
    tempdf.columns = [tag]
    result = pd.merge(result,tempdf,how='inner',left_index=True, right_index=True)
    
#%%
tagdf = pd.DataFrame()
tagdf['total_count'] = postdf.post_tags.value_counts()
dupdf = postdf[postdf.post_id.duplicated()][['post_id','post_tags']]
dupdf.index = dupdf['post_id']
dupdf.drop(['post_id'],axis=1, inplace=True)
tagdf['duplicated'] = dupdf.post_tags.value_counts()
#%%
tagdf['dup_percent'] = 100*tagdf['duplicated']/tagdf['total_count']
#%%
postdf.post_id.nunique()
for tag in popular_tags:
    tempdf = postdf.loc[postdf['post_tags']==tag][['post_id','post_tags']]
    tempdf.index = tempdf['post_id']
    tempdf.drop(['post_id'],axis=1, inplace=True)
    tempdf.columns = [tag]
    result = pd.merge(dupdf,tempdf,how='inner',left_index=True, right_index=True)
    tagdf[tag] = result.post_tags.value_counts()
    
#%% Duplicates
tempdf = postdf.loc[postdf['post_tags']=='entrepreneurship'][['clap_count','archive_date','post_url','post_id','post_tags']]
dup1df = tempdf[tempdf.post_id.duplicated()]

    