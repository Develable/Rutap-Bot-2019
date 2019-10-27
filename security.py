# -*- coding:utf-8 -*- 

##########################################################
#             Rutap Bot 2019 security Module             #
#                 Under The MIT License                  #
##########################################################

import random, time, setting
#import os

#key = os.urandom(64)

key = setting.Settings().security_key

def encrypt(message):
    letter_map_message = []
    ascii_msg_value = ''.join(str(ord(c)) for c in message)
    for c in message:
        ''.join(str(ord(c)))
        letter_map_message.append(ord(c))
    ascii_key_value = ''.join(str(ord(x)) for x in str(key))
    new_msg_encrypted = int(ascii_msg_value) * int(ascii_key_value)
    returned = (new_msg_encrypted, letter_map_message)
    return returned;

def decrypt(message, letter_map):
    ascii_key_value = ''.join(str(ord(x)) for x in str(key))
    msg_ascii_divided = int(message)//int(ascii_key_value)
    letters = []
    for c in range(len(letter_map)):
        li = letter_map[c]
        c = int(li)
        letter = chr(c)
        letters.append(letter)
    new_msg_decrypted = ''.join(letters)
    return new_msg_decrypted;

#encrypted = encrypt("안녕하세요 저는 프로 유튜버 마플입니다. 저는 독사과입니다. 놀이터에서 악마를 담당하고 있습니다.\n마플마플운터카운터각각독각별 100만 유튜버가 목표입니다.")
#print(encrypted[0])
#print(encrypted[1])
#decrypted = decrypt(encrypted[0], encrypted[1])
#print(decrypted)
