# -*- coding:utf-8 -*- 

##########################################################
#             Rutap Bot 2019 Normal Module               #
#                 Under The MIT License                  #
##########################################################

import os, time, datetime
from preta import *
from mysql import *

def ping(message):
    now = datetime.datetime.now()
    msgarrived = float(str(time.time())[:-3])
    msgtime = timeform(message.created_at)
    msgdelay = msgarrived - msgtime - 32400
    ping = int(msgdelay * 1000)

    UTC = now + datetime.timedelta(hours=-9) # KST == UTC + 9h.
    if ping < 0:
        asdfping = ping * -1
    else:
        asdfping = ping
    mysql_do("INSERT INTO `ping`(`TIMESTAMP`, `Ping`) VALUES ('%s-%s-%s %s:%s:%s', %s)" % (UTC.year, UTC.month, UTC.day, UTC.hour, UTC.minute, UTC.second, asdfping))

    return ping