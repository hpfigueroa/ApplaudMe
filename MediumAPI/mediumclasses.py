#!/usr/bin/python
# -*- coding: utf8 -*-
from enum import Enum

class User:
    def __init__(self, user_id):
        self.user_id = user_id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def regular_name(self):
        return self._regular_name

    @regular_name.setter
    def regular_name(self, regular_name):
        self._regular_name = regular_name

    @property
    def publications(self):
        return self._publications

    @publications.setter
    def publications(self, publications):
        self._publications = publications

    @property
    def following_count(self):
        return self._following_count

    @following_count.setter
    def following_count(self, count):
        self._following_count = count

    @property
    def followedby_count(self):
        return self._followedby_count

    @followedby_count.setter
    def followedby_count(self, count):
        self._followedby_count = count

    @property
    def interest_tags(self):
        return self._interest_tags

    @interest_tags.setter
    def interest_tags(self, tags):
        self._interest_tags = tags

    @property
    def author_tags(self):
        return self._author_tags

    @author_tags.setter
    def author_tags(self, tags):
        self._author_tags = tags

    def __str__(self, *args, **kwargs):
        return str(to_dict(self))

    def __repr__(self, *args, **kwargs):
        return str(to_dict(self))


class Post:
    def __init__(self, post_id):
        self.post_id = post_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def subtitle(self):
        return self._subtitle

    @subtitle.setter
    def subtitle(self, title):
        self._subtitle = title

    @property
    def post_date(self):
        return self._post_date

    @post_date.setter
    def post_date(self, date):
        self._post_date = date

    @property
    def post_url(self):
        return self._post_url

    @post_url.setter
    def post_url(self, url):
        self._post_url = url

    @property
    def clap_count(self):
        return self._clap_count

    @clap_count.setter
    def clap_count(self, count):
        self._clap_count = count

    @property
    def response_count(self):
        return self._response_count

    @response_count.setter
    def response_count(self, count):
        self._response_count = count

    @property
    def read_time(self):
        return self._read_time

    @read_time.setter
    def read_time(self, time):
        self._read_time = time

    @property
    def word_count(self):
        return self._word_count

    @word_count.setter
    def word_count(self, count):
        self._word_count = count

    @property
    def image_count(self):
        return self._image_count

    @image_count.setter
    def image_count(self, count):
        self._image_count = count

    @property
    def post_tags(self):
        return self._post_tags

    @post_tags.setter
    def post_tags(self, tags):
        self._post_tags = tags
    
    @property
    def detected_language(self):
        return self._detected_language

    @detected_language.setter
    def detected_language(self, lang):
        self._detected_language = lang
        
    @property
    def post_creatorId(self):
        return self._post_creatorId

    @post_creatorId.setter
    def post_creatorId(self, user_id):
        self._post_creatorId = user_id

    @property
    def publication_follower_count(self):
        return self._publication_follower_count

    @publication_follower_count.setter
    def publication_follower_count(self, count):
        self._publication_follower_count = count

    @property
    def post_link_count(self):
        return self._post_link_count

    @post_link_count.setter
    def post_link_count(self, count):
        self._post_link_count = count

    @property
    def unique_slug(self):
         return self._unique_slug
    
    @unique_slug.setter
    def unique_slug(self, slug):
         self._unique_slug = slug

    @property
    def post_publication_id(self):
         return self._post_publication_id
    
    @post_publication_id.setter
    def post_publication_id(self, publication_id):
         self._post_publication_id = publication_id
    
  
    def getKeys():
        keys = ["post_id", "title", "subtitle", "post_date", "post_url", 
                "response_count", "read_time", "word_count", 
                "image_count", "post_tags", "detected_language", 
                "post_creatorId", "publication_follower_count",
                "post_link_count", "unique_slug", "post_publication_id"]
        return keys

    def __str__(self, *args, **kwargs):
        return str(to_dict(self))

    def __repr__(self, *args, **kwargs):
        return str(to_dict(self))


class Publication:
    def __init__(self, publication_id):
        self.publication_id = publication_id

    @property
    def pub_name(self):
        return self._pub_name

    @pub_name.setter
    def pub_name(self, name):
        self._pub_name = name

    @property
    def pub_url(self):
        return self._pub_url

    @pub_url.setter
    def pub_url(self, url):
        self._pub_url = url

    @property
    def creator_user_id(self):
        return self._creator_user_id

    @creator_user_id.setter
    def creator_user_id(self, user_id):
        self._creator_user_id = user_id


    @property
    def follower_count(self):
        return self._follower_count

    @follower_count.setter
    def follower_count(self, count):
        self._follower_count = count

    @property
    def post_count(self):
        return self._post_count

    @post_count.setter
    def post_count(self, count):
        self._post_count = count
    
    @property
    def unique_slug(self):
        return self._unique_slug

    @unique_slug.setter
    def unique_slug(self, slug):
        self._unique_slug = slug

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description
        
    def __str__(self, *args, **kwargs):
        return str(to_dict(self))

    def __repr__(self, *args, **kwargs):
        return str(to_dict(self))


class Tag:
    @property
    def unique_slug(self):
        return self._unique_slug

    @unique_slug.setter
    def unique_slug(self, slug):
        self._unique_slug = slug

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def post_count(self):
        return self._post_count

    @post_count.setter
    def post_count(self, count):
        self._post_count = count

    @property
    def follower_count(self):
        return self._follower_count

    @follower_count.setter
    def follower_count(self, count):
        self._follower_count = count

    def __str__(self, *args, **kwargs):
        return str(to_dict(self))

    def __repr__(self, *args, **kwargs):
        return str(to_dict(self))


class OutputFormat(Enum):
    PLAIN_TEXT = "text"
    JSON = "json"
    HTML = "html"
    MARKDOWN = "md"


class Sort(Enum):
    TOP = "top"
    LATEST = "latest"


def to_dict(model):
    return dict((get_key(key), value)
                for key, value in model.__dict__.items()
                if not callable(value) and not key.startswith("__"))


def get_key(key):
    return key.replace("_", "", 1) if key.startswith("_") else key
