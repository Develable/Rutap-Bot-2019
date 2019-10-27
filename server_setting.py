# -*- coding:utf-8 -*- 

##########################################################
#         Rutap Bot 2019 Server Setting Module           #
#                 Under The MIT License                  #
##########################################################

import os
from mysql import *

def prefix_change(message):
    prefix_change = message.content[5:6]
    if prefix_change == "`" or prefix_change == "'":
        return False
    else:
        mysql_do("UPDATE `and_so_on` SET `prefix`='%s' WHERE server_id = %s" % (prefix_change, message.guild.id))
        return True

def welcome_message(message):
    if message.content[5:].startswith('끄기'):
        say = mysql_do_return("SELECT say FROM `on_join` WHERE server_id = %s" % (message.guild.id))
        if len(say) == 1:
            mysql_do("DELETE FROM `on_join` WHERE server_id = %s" % (message.guild.id))
            return "Delete"
        else:
            return False
    else: 
        welcome_msg = message.content[5:]
        #welcome_msg = welcome_msg.replace("'", "")
        #if welcome_msg == "" or welcome_msg == " " or welcome_msg == None:
        #    return "asdf"
        say = mysql_do_return("SELECT say FROM `on_join` WHERE server_id = %s" % (message.guild.id))
        if len(say) == 1:
            mysql_do("UPDATE `on_join` SET `channel_id`=%s,`say`='%s' WHERE server_id = %s" % (message.channel.id, welcome_msg, message.guild.id))
            return welcome_msg
        else:
            mysql_do("INSERT INTO `on_join`(`server_id`, `channel_id`, `say`) VALUES (%s, %s, '%s')" % (message.guild.id, message.channel.id, welcome_msg))
            return welcome_msg

def bye_message(message):
    if message.content[6:].startswith('끄기'):
        say = mysql_do_return("SELECT say FROM `on_join` WHERE server_id = %s" % (message.guild.id))
        if len(say) == 1:
            mysql_do("DELETE FROM `on_leave` WHERE server_id = %s" % (message.guild.id))
            return "Delete"
        else:
            return False
    else: 
        bye_msg = message.content[6:]
        #bye_msg = bye_msg.replace("'", "")
        #if bye_msg == "" or bye_msg == " " or bye_msg == None:
        #    return "asdf"
        say = mysql_do_return("SELECT say FROM `on_join` WHERE server_id = %s" % (message.guild.id))
        if len(say) == 1:
            mysql_do("UPDATE `on_join` SET `channel_id`=%s,`say`='%s' WHERE server_id = %s" % (message.channel.id, bye_msg, message.guild.id))
            return bye_msg
        else:
            mysql_do("INSERT INTO `on_join`(`server_id`, `channel_id`, `say`) VALUES (%s, %s, '%s')" % (message.guild.id, message.channel.id, bye_msg))
            return bye_msg

def bot_selection_noti(message, p):
    asdf = message.content.replace(p + "공지수신 ")
    if asdf == "취소":
        return "OK"

    channel = mysql_do_return("SELECT channel_id FROM `bot_selection_noti` WHERE server_id = %s" % (message.guild.id))
    if len(channel) == 1:
        channel = channel[0][0]
        if message.channel.id == channel:
            return False
        else:
            mysql_do("UPDATE `bot_selection_noti` SET `server_id`=%s,`channel_id`='%s' WHERE server_id = %s" % (message.guild.id, message.channel.id, message.guild.id))
            return True
    else:
        mysql_do("INSERT INTO `bot_selection_noti`(`server_id`, `channel_id`) VALUES (%s, %s)" % (message.guild.id, message.channel.id))
        return True
