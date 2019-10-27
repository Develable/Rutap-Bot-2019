# -*- coding:utf-8 -*- 

##########################################################
#              Rutap Bot 2019 Admin Module               #
#                 Under The MIT License                  #
##########################################################

import os, re
from mysql import *

def change_presence(message):
    playing = message.content.replace('rutap admin game', '')
    if playing == "":
        return None
    else:
        f = open("rpc.rts", 'w')
        f.write(playing)
        f.close()
        return playing

def user_ban(message):
    q = re.findall(r'\d+', message.content[16:])
    q = q[0]
    q = str(q)
    if q == message.author.id:
        return False
    else:
        asdfff = mysql_do_return("SELECT * FROM `banned_user` WHERE `user_id` = %s" % (q))
        if len(asdfff) == 1:
            mysql_do("INSERT INTO `banned_user`(`user_id`) VALUES (%s)" % (q))
            return q
        else:
            return q

def user_unban(message):
    q = re.findall(r'\d+', message.content[16:])
    q = q[0]
    q = str(q)
    asdfff = mysql_do_return("SELECT * FROM `banned_user` WHERE `user_id` = %s" % (q))
    if len(asdfff) == 1:
        mysql_do("DELETE FROM `banned_user` WHERE `user_id` = %s" % (q))
        return q
    else:
        return False
