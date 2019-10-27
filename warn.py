# -*- coding:utf-8 -*- 

##########################################################
#              Rutap Bot 2019 Warn Module                #
#                 Under The MIT License                  #
##########################################################

import os, datetime
from mysql import *

def warn_give(message, mention_id, reason):
    now = datetime.datetime.now()
    lists = mysql_do_return("SELECT count, reason FROM `warn` WHERE `warn`.`server_id` = %s AND `warn`.`user_id` = %s" % (message.guild.id, mention_id))
    if len(lists) == 1:
        past_warn = lists[0][0]
        now_warn = int(past_warn) + 1
        reason = lists[0][1] + "\n- %s || 경고 부여됨 || %s" % ("%s/%s/%s %s:%s:%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second), reason)
        mysql_do("UPDATE `warn` SET `count`=%s,`reason`='%s' WHERE server_id = %s AND user_id = %s" % (now_warn, reason, message.guild.id, mention_id))
        return now_warn
    else:
        reason = "# 년/월/일 시:분:초 || 구분 || 사유\n- %s || 경고 부여됨 || %s" % ("%s/%s/%s %s:%s:%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second), reason)
        mysql_do("INSERT INTO `warn`(`server_id`, `user_id`, `count`, `reason`) VALUES (%s,%s,1,'%s')" % (message.guild.id, mention_id, reason))
        return "1"

def warn_cancel(message, mention_id, reason):
    now = datetime.datetime.now()
    lists = mysql_do_return("SELECT count, reason FROM `warn` WHERE `warn`.`server_id` = %s AND `warn`.`user_id` = %s" % (message.guild.id, mention_id))
    if len(lists) == 1:
        past_warn = lists[0][0]
        now_warn = int(past_warn) - 1
        reason = lists[0][1] + "\n- %s || 경고 제거됨 || %s" % ("%s/%s/%s %s:%s:%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second), reason)
        mysql_do("UPDATE `warn` SET `count`=%s,`reason`='%s' WHERE server_id = %s AND user_id = %s" % (now_warn, reason, message.guild.id, mention_id))
        return now_warn
    else:
        return False

def warn_reset(message, mention_id):
    lists = mysql_do_return("SELECT count FROM `warn` WHERE `warn`.`server_id` = %s AND `warn`.`user_id` = %s" % (message.guild.id, mention_id))
    if len(lists) == 1:
        mysql_do("DELETE FROM `warn` WHERE `warn`.`server_id` = %s AND `warn`.`user_id` = %s" % (message.guild.id, mention_id))
        return "0"
    else:
        return False

def warn_check(message, mention_id):
    lists = mysql_do_return("SELECT count, reason FROM `warn` WHERE `warn`.`server_id` = %s AND `warn`.`user_id` = %s" % (message.guild.id, mention_id))
    if len(lists) == 1:
        warn_num = lists[0][0]
        asdf = lists[0][1]
        return warn_num, asdf
    else:
        return "0", "> (없음)"
