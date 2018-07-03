"""
@author: hpfigueroa
"""
#%%
import datetime as dt
import random
from MediumAPI import mediumparser
import pickle
import time
import pandas as pd
import matplotlib.pyplot as plt
#%%
HTML_PARSER = "html.parser"
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
    
    pickle.dump(allPosts,open("allPosts_"+str(dt.date.today())+"_"+str(num_posts)+".p", "wb" ))
    pickle.dump(allPublications,open("AllPublications_"+str(dt.date.today())+"_"+str(num_publications)+".p", "wb" ))
    post_tag_num_ref.close()
    post_list_ref.close()
    pub_tag_num_ref.close()
    pub_list_ref.close()

    return allPosts,allPublications

#%% Gathering daily metadata from Jan 01 2018 to 
popular_tags = ['health','writing','design','politics','programming','business','machine-learning','artificial-intelligence','travel']
startdate = dt.datetime(2018,1,1)
#%%
daylist = []
for x in range(181):
    xdate = startdate + dt.timedelta(days=x)
    daylist.append(xdate.strftime('%Y/%m/%d'))
   
#%%
PostList,PublicationList = getPostsByTagsByDays(popular_tags,daylist)
#%%
#%%% Creating a dictionary from the results
PostTag_filename = 'PostTagNumbers2018-07-03.txt'
postdf = pd.DataFrame()
tagindex = 0
post_tag_df = pd.read_csv(PostTag_filename,header=None,names=['date','tag','post_count'])
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
#%% Adding the scraping date
#%% Eliminating thin content and too large content 
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

#%% Visualizing the number of articles
import seaborn as sns
sns.set(style="darkgrid")
ax = sns.countplot(x="post_tags", data=postdf)

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

#%% Visualizing topic timeseries
plot_tags = ['health','writing','design','politics','programming','business','machine-learning','artificial-intelligence','travel']
plot_list = [tag+'_q80' for tag in plot_tags]
plt.figure()
daily_stats[plot_list].plot()
daily_stats[plot_list].rolling(7, min_periods=4).mean().plot()
#%%
plt.figure()
plot_list = [tag+'_count' for tag in plot_tags]
daily_stats[plot_list].plot()
daily_stats[plot_list].rolling(7, min_periods=4).mean().plot()
 
#%% Analyzing topic overlapping
tagdf = pd.DataFrame()
tagdf['total_count'] = postdf.post_tags.value_counts()
dupdf = postdf.loc[postdf.post_id.duplicated(),['post_id','post_tags']]
dupdf.index = dupdf['post_id']
dupdf.drop(['post_id'],axis=1, inplace=True)
tagdf['duplicated'] = dupdf.post_tags.value_counts()
tagdf['dup_percent'] = 100*tagdf['duplicated']/tagdf['total_count']
#%% Duplicates per topic
for tag in popular_tags:
    tempdf = postdf.loc[postdf['post_tags']==tag][['post_id','post_tags']]
    tempdf.index = tempdf['post_id']
    tempdf.drop(['post_id'],axis=1, inplace=True)
    tempdf.columns = [tag]
    result = pd.merge(dupdf,tempdf,how='inner',left_index=True, right_index=True)
    tagdf[tag] = result.post_tags.value_counts()

#%%Saving information 

#%% Dropping duplicated records 