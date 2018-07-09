"""
@author: hpfigueroa
"""
#%%
import datetime as dt
import pickle
import random
import time

import pandas as pd
import matplotlib.pyplot as plt

from MediumAPI import mediumparser
#%%
HTML_PARSER = "html.parser"
#%%
def open_log_files(marker = "", data_dir = "./"):
    post_list_ref = open(data_dir + 'PostTagList' + str(dt.date.today()) + marker +'.txt', 'a', encoding='utf-8')
    post_tag_num_ref = open(data_dir + 'PostTagNumbers'+str(dt.date.today()) + marker +'.txt', 'a', encoding='utf-8')    
    pub_list_ref = open(data_dir + 'PubTagList' + str(dt.date.today()) +  marker +'.txt', 'a', encoding='utf-8')
    pub_tag_num_ref = open(data_dir + 'PubTagNumbers'+str(dt.date.today())+ marker +'.txt', 'a', encoding='utf-8')
    return [post_list_ref, post_tag_num_ref, pub_list_ref, pub_tag_num_ref]

def close_log_files(logfile_list):    
    for file_ref in logfile_list:
        file_ref.close()
    return

def get_metadata_by_tags(tag_list = ["machine-learning"], day = dt.date.today().strftime('%Y/%m/%d'), log_marker = "", data_dir ="./"):
    MediumObj = mediumparser.Medium()
    day_post_list = []
    day_publication_list = []       
    post_list_ref, post_tag_num_ref, pub_list_ref, pub_tag_num_ref = open_log_files(log_marker, data_dir)
    
    for tag in tag_list:
        tag_day_url = MediumObj.build_tag_day_url(tag,day)
        
        try:
            tag_payload = MediumObj._get_request_payload(tag_day_url)
        except Exception as e:
            print("Problem getting payload from tag ", tag, " in ", day, ". Exception is: ", e)
            continue
        #logging payloads for future analysis          
        tag_payload_filename = 'payload_' + tag + '_' + day.replace('/','-') + "_" + str(dt.date.today()) + '.p'
        pickle.dump(tag_payload,open(data_dir + tag_payload_filename, "wb" ))
        
        try: 
            post_list = mediumparser.parse_post_list(tag_payload)
            publication_list = mediumparser.parse_publication_list(tag_payload)
        except Exception as e:
            print("Problem parsing payload from tag ", tag, " in ", day, ". Exception is: ", e)
            continue
        #When successful retrieval and parsing is achieved
        post_tag_num_ref.write(day + "," + tag + "," + str(len(post_list)) + "\n")
        for post in post_list:
            linepost = post.post_id + "," + post.post_url + "," + str(post.word_count) + "\n"
            post_list_ref.write(linepost)

        pub_tag_num_ref.write(day + "," + tag + "," + str(len(publication_list)) + "\n")
        for publication in publication_list:
            linepub = publication.publication_id + "," + publication.pub_url + "," + str(publication.follower_count) + "\n"
            pub_list_ref.write(linepub)
        
        day_post_list.append(post_list)
        day_publication_list.append(publication_list)
        time.sleep(random.randint(10,30))  

    close_log_files([post_list_ref, post_tag_num_ref, pub_list_ref, pub_tag_num_ref])          
        
    return day_post_list, day_publication_list
    

def get_metadata_by_days(day_list = [dt.date.today().strftime('%Y/%m/%d')], tag_list = ["machine-learning"], log_marker = "", data_dir ="./"):
    all_post_list = []
    all_publication_list = []
    
    post_count = 0
    publication_count = 0
    
    for day in day_list:
        day_post_list, day_publication_list = get_metadata_by_tags(tag_list, day, log_marker, data_dir)

        for post_list in day_post_list:
            if(post_list is not None):
                all_post_list.append(post_list)
                post_count += len(post_list)
                print("Found ",len(post_list),". Total posts collected so far: ", post_count)

        for publication_list in day_publication_list:
            if(publication_list is not None):
                all_publication_list.append(publication_list)
                publication_count += len(publication_list)
                print("Found ", len(publication_list), ". Total publications collected so far: ", publication_count)

    pickle.dump(all_post_list,open(data_dir + "all_post_list_"+str(dt.date.today())+"_"+str(post_count)+".p", "wb" ))
    pickle.dump(all_publication_list,open(data_dir + "all_publication_list_"+str(dt.date.today())+"_"+str(publication_count)+".p", "wb" ))

    return all_post_list,all_publication_list

#%% Gathering daily metadata for popular tags from Jan 01 2018 to 
popular_tags = ['health','writing','design','politics','programming','business','machine-learning','artificial-intelligence','travel']
startdate = dt.datetime(2018,7,7)
enddate = dt.datetime(2018,7,8)
daylist = []
for x in range((enddate-startdate).days+1):
    xdate = startdate + dt.timedelta(days=x)
    daylist.append(xdate.strftime('%Y/%m/%d'))
   
#%%
log_marker = '_July'
log_dir = './data_july/'
july_posts,july_publications = get_metadata_by_days(daylist,popular_tags,log_marker,log_dir)

#%%% Creating a DataFrame from the results
scrape_date = str(dt.date.today())
post_tag_file = open(log_dir + 'PostTagNumbers'+ scrape_date + log_marker +'.txt', 'r', encoding='utf-8')
post_tag_df = pd.read_csv(post_tag_file,header=None,names=['date','tag','post_count'])
postdf = pd.DataFrame()
tagindex = 0
all_post_list = july_posts
archive_date = []
for post_list in all_post_list:
    tag = post_tag_df.iloc[tagindex]['tag']
    for post in post_list:
        #Selecting content only in English
        if post.detected_language != 'en':
            continue
        #Eliminating thin content and too large content 
        if (post.word_count<200) or (post.word_count>5000):
            continue
        post.post_tags = tag
        archive_date.append(post_tag_df.iloc[tagindex]['date'])
        if postdf.empty:
            count = 0
            postdf = pd.DataFrame(mediumparser.to_dict(post),index=[count])
        else:
            postdf = pd.concat([postdf,pd.DataFrame(mediumparser.to_dict(post),index=[count])])
        count += 1
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

#%% Dropping duplicated records 

