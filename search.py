# -*- coding:utf-8 -*- 

##########################################################
#              Rutap Bot 2019 Search Module              #
#                 Under The MIT License                  #
##########################################################

import discord, requests, json, random, setting
from bs4 import BeautifulSoup as bs4

Setting = setting.Settings()

normal_neko_tag = ['neko', 'avatar', 'holo', 'kemonomimi', 'meow', 'waifu', 'tickle', 'feed', 'poke', 'slap', 'cuddle', 'hug', 'pat']
lewd_neko_tag = ['ero', 'eron', 'erofeet', 'erouri', 'lewd', 'keta', 'yuri', 'nsfw_avatar', 'hentai', 'anal', 'femdom', 'cum', 'solo', 'pussy', 'tits', 'smallboobs', 'feet', 'ngif', 'hentaig', 'nsfwg', 'classic', 'solog', 'pussyg', 'boobs', 'pwankg', 'feetg', 'trap', 'futanari', 'gasm', 'wallpaper']

def normal_neko(message, tag):
    tag = tag.replace('\t', '')
    tag = tag.replace(' ', '')
    if tag == None or tag == "" or tag == " ":
        tag = 'neko'
    if not tag in normal_neko_tag:
        return False
    r = requests.get("https://nekos.life/api/v2/img/%s" % tag)
    r = r.text
    data = json.loads(r)
    file = data["url"]
    return file, tag

def nsfw_neko(message, tag):
    tag = tag.replace('\t', '')
    tag = tag.replace(' ', '')
    if tag == None or tag == "" or tag == " ":
        tag = 'lewd'
    if not tag in lewd_neko_tag and not tag in normal_neko_tag:
        return False
    r = requests.get("https://nekos.life/api/v2/img/%s" % tag)
    r = r.text
    data = json.loads(r)
    file = data["url"]
    return file, tag

def img_search(message, q):
    q = q.encode("raw_unicode_escape")
    q = str(q)

    data = requests.get("https://www.google.co.kr/search?q=" + q + "&source=lnms&tbm=isch&sa=X")
    soup = bs4(data.text, "html.parser")
    imgs = soup.find_all("img")

    file = random.choice(imgs[1:])['src']

    return file
