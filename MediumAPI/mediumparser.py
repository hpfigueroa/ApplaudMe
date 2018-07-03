#!/usr/bin/python3
# -*- coding: utf8 -*-

import re
import requests
import json
from bs4 import BeautifulSoup

from MediumAPI.mediumclasses import User, Post, Publication, Tag, to_dict, Sort
from MediumAPI.constant import ROOT_URL, JSON_HEADER, ESCAPE_CHARACTERS, COUNT

#%% These Functions use a payload obtained after bs4 extraction
def parse_user(payload, return_dict=False):
    user_dict = payload["payload"]["user"]
    user_id = user_dict["userId"]
    user = User(user_id)

    user.username = user_dict["username"]
    user.regular_name = user_dict["name"]
    ref_dict = payload["payload"]["references"]
    stats_dict = ref_dict["SocialStats"][user_id]

    user.following_count = stats_dict["usersFollowedCount"]
    user.followedby_count = stats_dict["usersFollowedByCount"]

    if return_dict:
        return to_dict(user)
    else:
        return user



def parse_publication_dict(publication_dict, pub_id=None, return_dict=False):
    if pub_id is None:
        pub_id = publication_dict["id"]
    publication = Publication(pub_id)
    publication.pub_name = publication_dict["name"]
    publication.description = publication_dict["description"]
    publication.creator_user_id = publication_dict["creatorId"]
    publication.follower_count = publication_dict["metadata"]["followerCount"]
    if "postCount" in publication_dict["metadata"]:
        publication.post_count = publication_dict["metadata"]["postCount"]

    if "domain" in publication_dict:
        publication.pub_url = "http://" + publication_dict["domain"]
    else:
        publication.pub_url = ROOT_URL + publication_dict["slug"]
    publication.unique_slug = publication_dict["slug"]
    if return_dict:
        return to_dict(publication)
    else:
        return publication

def parse_publication_list(list_payload):
    publication_detail_parsing_keys = ("payload", "references", "Collection")
    test_list_payload = list_payload
    for key in publication_detail_parsing_keys:
        test_list_payload = test_list_payload.get(key)
    if test_list_payload is None:
        print("Incorrect payload, returning None")
        return None

    publication_list = []
    if type(list_payload) is dict:
        for publication_id in test_list_payload.keys():
            publication_dict = test_list_payload.get(publication_id)
            publication_list.append(parse_publication_dict(publication_dict, publication_id))
    # payload -> value
    elif type(list_payload) is list:
        for publication_dict in list_payload:
            publication_list.append(parse_publication_dict(publication_dict))

    return publication_list    


#PARSE_POST
def parse_post_list(list_payload, return_dict=False):
    post_detail_parsing_keys = ("payload", "references", "Post")
    test_list_payload = list_payload
    for key in post_detail_parsing_keys:
        test_list_payload = test_list_payload.get(key)

    if test_list_payload is None:
        print("Incorrect payload, returning None")
        return None
    
    def parse_post_dict(post_dict, post_id=None):
        if post_id is None:
            post_id = post_dict["id"]
        post = Post(post_id)
        post_unique_slug = post_dict["uniqueSlug"]
        post_publication_id = post_dict["approvedHomeCollectionId"]
        creator_id = post_dict["creatorId"]

        post.unique_slug = post_unique_slug
        post.post_creatorId = creator_id
        post.post_publication_id = post_publication_id
        post.title = post_dict["title"]
        post.post_date = post_dict["firstPublishedAt"]
        post.detected_language = post_dict["detectedLanguage"]

        #Build URL It needs to be a function
        url = ROOT_URL
        post.publication_follower_count = 0
        if post_publication_id is not None and post_publication_id:
            publication_dict = ref_dict["Collection"][post_publication_id]
            post.publication_follower_count = publication_dict["metadata"]["followerCount"]
            # custom publication domain
            if "domain" in publication_dict and publication_dict["domain"]:
                url = "https://" + publication_dict["domain"]
            else:
                # simple publication
                url += publication_dict["slug"]
        else:
            # personal post, no publication
            username = ref_dict["User"][creator_id]["username"]
            url += "@{username}".format(username=username)
        url += u"/{path}".format(path=post_unique_slug)
        # Nick: Need to add post_content here. create new function from the payload
        post.post_url = url

        #Get post statistics
        virtual_dict = post_dict["virtuals"]
        post.subtitle = virtual_dict["subtitle"]
        post.clap_count = virtual_dict["totalClapCount"]
        post.response_count = virtual_dict["responsesCreatedCount"]
        post.read_time =  virtual_dict["readingTime"]
        post.word_count = virtual_dict["wordCount"]
        post.image_count = virtual_dict["imageCount"]
        post.post_tags = parse_tag_list(virtual_dict["tags"], return_dict)
        link_count = virtual_dict["links"]
        if link_count["entries"] is not None:
            post.post_link_count = len(link_count["entries"])
        else:
            post.post_link_count = 0
        if return_dict:
            return to_dict(post) #Nick - if flag for return_dict is true then this is what's returned.
        else:
            return post

        # print("{id}, {title}".format(id=post_id, title=title))
        # print("{recommend}, {response}, {read}".format(
        # recommend=recommend_count, response=response_count, read=read_time))


    post_list = []
    ref_dict = list_payload["payload"]["references"]    
    #print(list_payload)  #UNCOMMENT
    # payload -> references -> Post
    #list_payload can be dict or list
    # get the different parsing keys

    if type(list_payload) is dict:
        for post_id in test_list_payload.keys():
            post_dict = test_list_payload.get(post_id)
            post_list.append(parse_post_dict(post_dict, post_id))
    # payload -> value
    elif type(list_payload) is list:
        for post_dict in list_payload:
            post_list.append(parse_post_dict(post_dict))

    return post_list


def parse_tag_list(tags_list_dict, return_dict=False):
    if tags_list_dict is not None and len(tags_list_dict) > 0:
        tags_list = []
        for tag_dict in tags_list_dict:
            tag = Tag()
            tag.unique_slug = tag_dict["slug"]
            tag.name = tag_dict["name"]
            tag.post_count = tag_dict["postCount"]
            metadata_dict = tag_dict["metadata"]
            if metadata_dict is not None:
                tag.follower_count = metadata_dict["followerCount"]
            if return_dict:
                tags_list.append(to_dict(tag))
            else:
                tags_list.append(tag)
        return tags_list


def strip_space(text, trim_space=True):
    text = re.sub(r'\s+', ' ', text)
    if trim_space:
        return text.strip()
    else:
        return text

class Medium(object):
    def __init__(self):
        pass

    def get_user_profile(self, username):
        url = "{}@{}/latest".format(ROOT_URL, username)
        return self._send_request(url, parse_user)

    def get_publication_profile(self, publication_name):
        url = "{}{}/latest".format(ROOT_URL, publication_name)
        return self._send_request(url, parse_publication_dict)

    def get_user_posts(self, username, n=COUNT):
        return self._send_post_request(ROOT_URL + "@{0}/latest?limit={count}".format(username, count=n))

    def get_publication_posts(self, publication_name, n=COUNT):
        return self._send_post_request(ROOT_URL + "{0}/latest?limit={count}".format(publication_name, count=n))

    def get_top_posts(self, n=COUNT):
        return self._send_post_request(ROOT_URL + "browse/top?limit={count}".format(count=n))

    def get_posts_by_tag(self, tag, n=COUNT, sort=Sort.TOP):
        url = "{}tag/{tag}".format(ROOT_URL, tag=tag)
        if sort == Sort.LATEST:
            url += "/latest"
        url += "?limit={}".format(n)
        return self._send_post_request(url)

    def get_posts_by_tag_by_day(self, tag, day, n=COUNT):
        url = "{}tag/{tag}/{date}".format(ROOT_URL, tag=tag, date=day)
        return self._send_post_request(url)

    def build_tag_day_url(self, tag, day):
        url = "{}tag/{tag}/archive/{date}".format(ROOT_URL, tag=tag, date=day)
        return url

    @staticmethod
    def _get_request_payload(url):
        req = requests.get(url, headers=JSON_HEADER) #PAYLOAD
        print(url, req.status_code)
        if req.status_code == requests.codes.ok:
            return json.loads(req.text.replace(ESCAPE_CHARACTERS, "").strip())
        else:
            return None


    @staticmethod
    def _send_request(url, parse_function):
        payload = Medium._get_request_payload(url)
        if payload is not None:
            return parse_function(payload)
        else:
            return None

    @staticmethod
    def _send_post_request(url):
        return Medium._send_request(url, parse_post_list)



##### - NICK SECTION - #######    
    #Nick - added this function to return search results.
    #how to I change the number of search results returned
    #need to create my own parse function
    def get_posts_by_search(self, keyword):
        url = "{}search?q={tag}".format(ROOT_URL, tag=keyword)  #{}search/posts?q={tag}
        parsed_post_list = self._send_post_request(url) #this is after, "parse_post" is called
        return parsed_post_list
   

    #get payload for a single post
    def get_single_post(self, url):
        req = requests.get(url, headers=JSON_HEADER) #PAYLOAD
        print(url, req.status_code)
        
        if req.status_code == requests.codes.ok:
            payload = json.loads(req.text.replace(ESCAPE_CHARACTERS, "").strip())
            return payload
        else:
            return None
    


