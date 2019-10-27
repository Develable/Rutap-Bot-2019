# -*- coding:utf-8 -*- 

##########################################################
#               Rutap Bot 2019 API Module                #
#                 Under The MIT License                  #
##########################################################

import discord, asyncio, oauth2, json, datetime, time, urllib, random, sys, urllib.request, setting

Setting = setting.Settings()
app = discord.Client()

async def url_short(message, q):
    if Setting.api_type == 'naver':
        data = "url=%s" % (urllib.parse.quote(q))
        request = urllib.request.Request("https://openapi.naver.com/v1/util/shorturl")
        request.add_header("X-Naver-Client-Id", Setting.naver_api_id)
        request.add_header("X-Naver-Client-Secret", Setting.naver_api_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            response = response_body.decode('utf-8')
            url = json.loads(response)["result"]["url"]
            return url
    elif Setting.api_type == 'cutress':
        request = urllib.request.Request("https://openapi.naver.com/v1/util/shorturl")
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            response = response_body.decode('utf-8')
            url = json.loads(response)["result"]["url"]
            return url
    else:
        return 'Setting error'

def oauth2_request(consumer_key, consumer_secret, access_token, access_secret):
    consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
    token = oauth2.Token(key=access_token, secret=access_secret)
    client = oauth2.Client(consumer, token)
    return client

def get_user_timeline(client, screen_name, count, include_rts):
    base = "https://api.twitter.com/1.1"
    node = "/statuses/user_timeline.json"
    fields = "?screen_name=%s&count=%s&include_rts=%s" % (screen_name, count, include_rts)

    url = base + node + fields

    response, data = client.request(url)

    if response['status'] == '200':
        return json.loads(data.decode('utf-8'))

async def getTwitterTwit(message, tweet, jsonResult, embed):

    tweet_id = tweet['id_str']
    tweet_message = '' if 'text' not in tweet.keys() else tweet['text']

    screen_name = '' if 'user' not in tweet.keys() else tweet['user']['screen_name']

    tweet_link = ''
    if tweet['entities']['urls']: #list

        for i, val in enumerate(tweet['entities']['urls']):
            tweet_link = tweet_link + tweet['entities']['urls'][i]['url'] + ' '
    else:
        tweet_link = ''

    hashtags = ''
    if tweet['entities']['hashtags']: #list

        for i, val in enumerate(tweet['entities']['hashtags']):
            hashtags = hashtags + tweet['entities']['hashtags'][i]['text'] + ' '
    else:
        hashtags = ''

    if 'created_at' in tweet.keys():
        # Twitter used UTC Format. EST = UTC + 9(Korean Time) Format ex: Fri Feb 10 03:57:27 +0000 2017

        tweet_published = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        tweet_published = tweet_published + datetime.timedelta(hours=+9)
        tweet_published = tweet_published.strftime('%Y-%m-%d %H:%M:%S')
    else:
        tweet_published = ''

    num_favorite_count = 0 if 'favorite_count' not in tweet.keys() else tweet['favorite_count']
    num_comments = "?"
    num_shares = 0 if 'retweet_count' not in tweet.keys() else tweet['retweet_count']
    num_likes = num_favorite_count
    num_loves = num_wows = num_hahas = num_sads = num_angrys = 0

    url = await url_short(message, "https://twitter.com/statuses/%s" % (tweet_id))

    embed = embed.add_field(name=tweet_message, value="답글 : `%s`개 | 좋아요 : `%s`개 | 리트윗 : `%s`회\n링크 : %s" % (num_comments, num_likes, num_shares, url), inline = False)
    return embed

async def show_tweets(message, screen_name, num, include_rts, embed):
    jsonResult = []

    client = oauth2_request(Setting.twitter_api_key, Setting.twitter_api_secret, Setting.twitter_access_token, Setting.twitter_access_secret)
    tweets = get_user_timeline(client, screen_name, num, include_rts)

    try:
        for tweet in tweets:
            embed = await getTwitterTwit(message, tweet, jsonResult, embed)
    except TypeError:
        embed = embed.add_field(name="트윗을 가져올 수 없습니다.", value="비공개 계정으로 추측됩니다. 확인 후 다시 시도하여 주세요.", inline = False)

    return embed