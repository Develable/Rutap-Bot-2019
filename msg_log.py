# -*- coding:utf-8 -*- 

##########################################################
#          Rutap Bot 2019 Actvity Logging Module         #
#                 Under The MIT License                  #
##########################################################

import os, datetime, setting

Setting = setting.Settings()

def log_msg(server, server_id, channel, channel_id, usr, usr_tag, usr_id, msg):
    now = datetime.datetime.now()
    if os.path.isfile("log/%s" % (Setting.log_file)):
        f = open("log/%s" % (Setting.log_file), 'a', encoding="UTF8")
        f.write("\n%s / %s / %s | %s : %s | Server : %s(%s) | Channel : %s(%s) | Author : %s%s(%s) | Message : %s" % (now.year, now.month, now.day, now.hour, now.minute, server, server_id, channel, channel_id, usr, usr_tag, usr_id, msg))
        f.close()
    else:
        f = open("log/%s" % (Setting.log_file), 'w', encoding="UTF8")
        f.write("\n%s / %s / %s | %s : %s | Server : %s(%s) | Channel : %s(%s) | Author : %s%s(%s) | Message : %s" % (now.year, now.month, now.day, now.hour, now.minute, server, server_id, channel, channel_id, usr, usr_tag, usr_id, msg))
        f.close()
        print("%s 파일을 발견하지 못하여 해당 파일을 생성하였습니다.\n\n==============\n" % ("log/%s" % (Setting.log_file)))

def log_start_msg():
    now = datetime.datetime.now()
    if os.path.isfile("log/%s" % (Setting.log_file)):
        f = open("log/%s" % (Setting.log_file), 'a', encoding="UTF8")
        f.write("\n\n%s / %s / %s | %s : %s | Logging Started.\n" % (now.year, now.month, now.day, now.hour, now.minute))
        f.close()
    else:
        f = open("log/%s" % (Setting.log_file), 'w', encoding="UTF8")
        f.write("%s / %s / %s | %s : %s | Logging Started.\n" % (now.year, now.month, now.day, now.hour, now.minute))
        f.close()
        print("%s 파일을 발견하지 못하여 해당 파일을 생성하였습니다.\n\n==============\n" % ("log/%s" % (Setting.log_file)))