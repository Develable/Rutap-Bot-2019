# -*- coding:utf-8 -*- 

##########################################################
#               Rutap Bot 2019 Main Module               #
#                 Under The MIT License                  #
##########################################################

import asyncio, discord, os, requests, random, datetime, re, json, sys, parser, psutil, ctypes, setting
import time as module_time
from hurry.filesize import size
from server_setting import *
from msg_log import *
from normal import *
from search import *
from preta import *
from admin import *
from mysql import *
from warn import *
from api import *

app, Setting = discord.Client(), setting.Settings()
Copyright, a = Setting.copy, 0

# Discord.py 1.2.3
async def unknown_error(message, e):
    now = datetime.datetime.now()
    randcode = "ERR :: %s%s%s%s" % (now.month, random.randint(1,10000000), now.day, random.randint(1,10000))
    embed = discord.Embed(title="죄송합니다. 원인을 알 수 없는 문제가 발생했습니다.", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주시기 바랍니다.\nOfficial Support Server : https://invite.gg/rutapbot", color=Setting.error_embed_color)
    embed.set_footer(text=randcode)
    await message.channel.send(embed=embed)
    await app.get_channel(int(Setting.err_log_channel)).send("```Markdown\n# Unknown error\n* info : %s(%s) | %s(%s) | %s(%s)\n* Code : %s\n* Target msg : %s\n* errinfo : %s```" % (message.guild, message.guild.id, message.channel, message.channel.id, message.author, message.author.id, randcode, message.content, e))

async def http_error(message, e):
    now = datetime.datetime.now()
    randcode = "ERR :: %s%s%s%s" % (now.month, random.randint(1,10000000), now.day, random.randint(1,10000))
    embed = discord.Embed(title="죄송합니다. 예기치 못한 문제가 발생했습니다.", description="봇이 메시지에 관련된 충분한 권한을 가지고 있는지 다시 한 번 확인 해 주시기 바랍니다.\nOfficial Support Server : https://invite.gg/rutapbot", color=Setting.error_embed_color)
    embed.set_footer(text=randcode)
    await message.author.send(embed=embed)
    await app.get_channel(int(Setting.err_log_channel)).send("```Markdown\n# Unknown error\n* info : %s(%s) | %s(%s) | %s(%s)\n* Code : %s\n* Target msg : %s\n* errinfo : %s```" % (message.guild, message.guild.id, message.channel, message.channel.id, message.author, message.author.id, randcode, message.content, e))

@app.event
async def on_ready():
    try:
        rpc = open("rpc.rts", 'r').read()
        await app.change_presence(status=discord.Status.online, activity=discord.Game(rpc))
        print("rpc.rts 파일을 발견하였습니다.\n봇이 \"%s\" 을(를) 플레이 하게 됩니다.\n\n==============\n" % (rpc))
    except FileNotFoundError as e:
        print("rpc.rts 파일을 발견하지 못하였습니다.\n봇이 아무것도 플레이하지 않게 됩니다.\n\n애러 내용 : \"%s\"\n\n==============\n" % (e))

    print("Bot is Ready!\n\n==============\n\n= Rutap Bot 2019 Main Module =\n  Ver. TEST\n\n[로그인 정보]\n봇 이름 : %s\n봇 ID : %s\n\n\n[기본 설정 정보]\n기본 접두사 : %s\n버전 : %s\n\n[로그 설정 정보]\n로그파일 저장위치 : log/%s\n\n[채널 설정 정보]\n봇 관리자 ID : %s\n온라인 공지 채널 : %s\n애러 로그 채널 : %s\n\n[API 설정 정보]\nURL 단축 API 구분 : %s\n\n[공지 설정 정보]\n허용 키워드 : %s\n비허용 키워드 : %s\n자동생성 채널 이름 : %s\n\n[MYSQL 설정 정보]\nTarget IP : %s@%s\nTarget DB : %s\n\n© 2018-%s Develable. All Rights Reserved.\nUnder The MIT License\n\n==============\n" % (app.user.name, app.user.id, Setting.prefix, Setting.version, Setting.log_file, Setting.owner_id, Setting.online_notice_channel, Setting.err_log_channel, Setting.api_type, Setting.allow_keyword, Setting.disallow_keyword,  Setting.autochannel_name, Setting.mysql_id, Setting.mysql_ip, Setting.mysql_db, datetime.datetime.now().year))

    log_start_msg()

    now, count = datetime.datetime.now(), 1
    embed=discord.Embed(title="I'm online!", color=Setting.embed_color)
    embed.add_field(name="Last Checked in", value="`%s/%s/%s` | `%s:%s:%s` | `%s차`" % (now.year, now.month, now.day, now.hour, now.minute, now.second, count), inline=True)
    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
    online_notice = await app.get_channel(int(Setting.online_notice_channel)).send(embed=embed)

    while a < 1:
        await asyncio.sleep(299)
        count, snow = count + 1, datetime.datetime.now()
        embed=discord.Embed(title="I'm online!", color=Setting.embed_color).add_field(name="Last Checked in", value="`%s/%s/%s` | `%s:%s:%s` | `%s차`" % (snow.year, snow.month, snow.day, snow.hour, snow.minute, snow.second, count), inline=True)
        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
        await online_notice.edit(embed=embed)

# Logging
@app.event
async def on_message_delete(message):
    response = mysql_do_return("SELECT * FROM `logging` WHERE server_id = %s" % (message.guild.id))
    if not len(response) == 1:
        return None
    if not response[0][2] == 1:
        return None
    channel = response[0][2]

    mysystem = [(1024 ** 5, ' PB'), (1024 ** 4, ' TB'), (1024 ** 3, ' GB'),  (1024 ** 2, ' MB'),  (1024 ** 1, ' KB'), (1024 ** 0, ' B'),]
    embed = discord.Embed(color=Setting.embed_color)
    embed.set_author(name="%s#%s" % (message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
    embed.add_field(name="메시지가 삭제되었습니다.", value="채널 : <#%s> (`#%s`)\n내용 : %s%s%s" % (message.channel.id, message.channel.name, "`%s`" % message.content if not message.content == "" else "", "\n파일명 : %s (`%s`)\n파일 링크 : %s (접근이 불가할 수 있습니다)" % (message.attachments[0].filename, size(message.attachments[0].size, system=mysystem), await url_short(message, message.attachments[0].url)) if not message.attachments == [] else "", "\n\n이 메시지 하단에 임베드가 같이 첨부됩니다." if not message.embeds == [] else ""), inline=False)
    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
    await app.get_channel(int(channel)).send(embed=embed)
    if not message.embeds == []:
        await app.get_channel(int(channel)).send(embed=message.embeds[0])

@app.event
async def on_message_edit(past_message, now_message):
    response = mysql_do_return("SELECT * FROM `logging` WHERE server_id = %s" % (now_message.guild.id))
    if not len(response) == 1:
        return None
    if not response[0][2] == 1:
        return None
    channel = response[0][2]

    #if now_message.channel.id == int(channel) and now_message.author.id == app.user.id: # 이걸로 무한루프 막히길 바람 제발,,
    #    return None

    #if now_message.channel.id == int(channel): # 이건 문제없나
    #    return None

    if past_message.channel.id == int(channel): # 이게 제일 맘편할듯
        return None

    if past_message.content == now_message.content or past_message.embeds == now_message.embeds: # 가끔 이상하게 여기 실행되서 막는용임
        return None

    embed = discord.Embed(color=Setting.embed_color)
    embed.set_author(name="%s#%s" % (now_message.author.name, now_message.author.discriminator), icon_url=now_message.author.avatar_url)
    embed.add_field(name="메시지가 수정되었습니다.", value="채널 : <#%s> (`#%s`)\n수정 전 내용 : `%s`\n\n수정 후 내용 : `%s`%s" % (now_message.channel.id, now_message.channel.name, past_message.content, now_message.content, "\n\n이 메시지 하단에 수정 전 임베드와 수정 후 임베드가 같이 첨부됩니다." if not now_message.embeds == [] else ""), inline=False)
    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
    await app.get_channel(int(channel)).send(embed=embed)
    if not past_message.embeds == []:
        await app.get_channel(int(channel)).send(embed=past_message.embeds[0])
    if not now_message.embeds == []:
        await app.get_channel(int(channel)).send(embed=now_message.embeds[0])

@app.event
async def on_guild_channel_create(asdfchannel): # == class discord.abc.GuildChannel
    response = mysql_do_return("SELECT * FROM `logging` WHERE server_id = %s" % (asdfchannel.guild.id))
    if not len(response) == 1:
        return None
    if not response[0][3] == 1:
        return None
    channel = response[0][2]

    try:
        cid, cname = "<#%s>" % asdfchannel.category.id, "(`%s`)" % asdfchannel.category.name
    except:
        cid, cname = "(없음)", ""
    embed = discord.Embed(color=Setting.embed_color)
    embed.add_field(name="채널이 생성되었습니다.", value="채널 : <#%s> (`#%s`)\n상위 카테고리 : %s %s\n위치 : 아래에서 `%s`번째 (음성채널 제외)" % (asdfchannel.id, asdfchannel.name, cid, cname, asdfchannel.position + 1), inline=False)
    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
    await app.get_channel(int(channel)).send(embed=embed)

@app.event
async def on_guild_channel_delete(asdfchannel): # == class discord.abc.GuildChannel
    response = mysql_do_return("SELECT * FROM `logging` WHERE server_id = %s" % (asdfchannel.guild.id))
    if not len(response) == 1:
        return None
    if not response[0][3] == 1:
        return None
    channel = response[0][2]

    atime = asdfchannel.created_at
    created = "%s/%s/%s %s:%s:%s" % (atime.year, atime.month, atime.day, atime.hour, atime.minute, atime.second)
    try:
        cid, cname = "<#%s>" % asdfchannel.category.id, "(`%s`)" % asdfchannel.category.name
    except:
        cid, cname = "(없음)", ""
    embed = discord.Embed(color=Setting.embed_color)
    embed.add_field(name="채널이 제거되었습니다.", value="채널 : <#%s> (`#%s`)\n상위 카테고리 : %s %s\n위치 : 아래에서 `%s`번째 (음성채널 제외)\n생성일 : %s" % (asdfchannel.id, asdfchannel.name, cid, cname, asdfchannel.position + 1, created), inline=False)
    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
    await app.get_channel(int(channel)).send(embed=embed)

@app.event
async def on_reaction_add(reaction, member):
    response = mysql_do_return("SELECT * FROM `logging` WHERE server_id = %s" % (member.guild.id))
    if not len(response) == 1:
        return None
    if not response[0][2] == 1:
        return None
    channel = response[0][2]

    embed = discord.Embed(color=Setting.embed_color)
    embed.set_author(name="%s#%s" % (member.name, member.discriminator), icon_url=member.avatar_url)
    embed.add_field(name="반응이 추가되었습니다.", value="채널 : <#%s> (`#%s`)\n메시지 내용 : `%s`\n추가된 반응 : %s" % (reaction.message.channel.id, reaction.message.channel.name, reaction.message.content, reaction.emoji), inline=False)
    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
    await app.get_channel(int(channel)).send(embed=embed)

@app.event
async def on_reaction_remove(reaction, member):
    response = mysql_do_return("SELECT * FROM `logging` WHERE server_id = %s" % (member.guild.id))
    if not len(response) == 1:
        return None
    if not response[0][2] == 1:
        return None
    channel = response[0][2]

    embed = discord.Embed(color=Setting.embed_color)
    embed.set_author(name="%s#%s" % (member.name, member.discriminator), icon_url=member.avatar_url)
    embed.add_field(name="반응이 제거되었습니다.", value="채널 : <#%s> (`#%s`)\n메시지 내용 : `%s`\n제거된 반응 : %s" % (reaction.message.channel.id, reaction.message.channel.name, reaction.message.content, reaction.emoji), inline=False)
    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
    await app.get_channel(int(channel)).send(embed=embed)

@app.event
async def on_member_update(b, a): # == class discord.member || Includes status, game playing, nickname, roles
    response = mysql_do_return("SELECT * FROM `logging` WHERE server_id = %s" % (a.guild.id))
    if not len(response) == 1:
        return None
    if not response[0][4] == 1:
        return None
    channel = response[0][2]

    if not b.nick == a.nick:
        embed = discord.Embed(color=Setting.embed_color)
        embed.set_author(name="%s#%s" % (a.name, a.discriminator), icon_url=a.avatar_url)
        embed.add_field(name="서버에서의 별칭이 변경되었습니다.", value="이전 : `%s#%s`\n이후 : `%s#%s`" % (b.nick if not b.nick == None else b.name, b.discriminator, a.nick if not a.nick == None else a.name, a.discriminator), inline=False)
        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
        await app.get_channel(int(channel)).send(embed=embed)

@app.event
async def on_voice_state_update(member, b_vchannel, a_vchannel): # == class discord.member, discord.voicestate || Includes join, leave, (un)mute, (un)deaf
    response = mysql_do_return("SELECT * FROM `logging` WHERE server_id = %s" % (member.guild.id))
    if not len(response) == 1:
        return None
    if not response[0][6] == 1:
        return None
    channel = response[0][2]

    try:
        b_id, b_name = "<#%s>" % b_vchannel.channel.id, "#%s" % b_vchannel.channel.name
    except:
        b_id, b_name = "(없음)", "(없음)"
    try:
        a_id, a_name = "<#%s>" % a_vchannel.channel.id, "#%s" % a_vchannel.channel.name
    except:
        a_id, a_name = "(없음)", "(없음)"
    embed = discord.Embed(color=Setting.embed_color)
    embed.set_author(name="%s#%s" % (member.name, member.discriminator), icon_url=member.avatar_url)
    embed.add_field(name="음성 채널에서의 상태가 변경되었습니다.", value="<:twg_blank:580039918185611314>", inline=False)
    embed.add_field(name="이전", value="음성채널 : %s `%s`\n마이크 : `%s`\n스피커 : `%s`" % (b_id, b_name, "켜짐" if not b_vchannel.self_mute else "꺼짐", "켜짐" if not b_vchannel.self_deaf else "꺼짐"), inline=False)
    embed.add_field(name="이후", value="음성채널 : %s `%s`\n마이크 : `%s`\n스피커 : `%s`" % (a_id, a_name, "켜짐" if not a_vchannel.self_mute else "꺼짐", "켜짐" if not a_vchannel.self_deaf else "꺼짐"), inline=False)
    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
    await app.get_channel(int(channel)).send(embed=embed)

@app.event
async def on_guild_update(b, a): # == class discord.guild || Includes Guild name, AFK channel, AFK timeout, etc...
    response = mysql_do_return("SELECT * FROM `logging` WHERE server_id = %s" % (b.id))
    if not len(response) == 1:
        return None
    if not response[0][5] == 1:
        return None
    channel = response[0][2]

    if not b.name == a.name:
        embed = discord.Embed(color=Setting.embed_color)
        embed.add_field(name="서버 이름이 변경되었습니다.", value="이전 : `%s`\n이후 : `%s`" % (b.name, a.name), inline=False)
        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
        await app.get_channel(int(channel)).send(embed=embed)

    if not b.afk_timeout == a.afk_timeout: # Nonetype 대응필요
        embed = discord.Embed(color=Setting.embed_color)
        embed.add_field(name="잠수 시간이 변경되었습니다.", value="이전 : `%s`분\n이후 : `%s`분" % (int(b.afk_timeout/60), int(a.afk_timeout/60)), inline=False)
        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
        await app.get_channel(int(channel)).send(embed=embed)

    # afk_channel == class discord.voicechannel
    if not b.afk_channel.id == a.afk_channel.id: # Nonetype 대응필요
        embed = discord.Embed(color=Setting.embed_color)
        embed.add_field(name="잠수 채널이 변경되었습니다.", value="이전 :  <#%s> (`#%s`)\n이후 : <#%s> (`#%s`)" % (b.afk_channel.id, b.afk_channel.name, a.afk_channel.id, a.afk_channel.name), inline=False)
        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
        await app.get_channel(int(channel)).send(embed=embed)

@app.event
async def on_guild_role_create(role): # == class discord.Role
    guild = role.guild # == class discord.Guild
    response = mysql_do_return("SELECT * FROM `logging` WHERE server_id = %s" % (guild.id))
    if not len(response) == 1:
        return None
    if not response[0][5] == 1:
        return None
    channel = response[0][2]
    
    colour, atime = role.colour, role.created_at + datetime.timedelta(hours=+9)
    hexcode, created = '#%02x%02x%02x' % (colour.r, colour.g, colour.b), "%s/%s/%s %s:%s:%s" % (atime.year, atime.month, atime.day, atime.hour, atime.minute, atime.second)
    embed = discord.Embed(color=Setting.embed_color)
    embed.add_field(name="새 역할이 생성되었습니다.", value="<@&%s> (`@%s`)\n생성일 : %s (24시간 기준, KST)" % (role.id, role.name, created), inline=False)
    embed.add_field(name="설정 내용", value="역할 색상 : %s\n온라인 멤버와 분리하여 표시 : %s\n역할 언급 : %s\n유저에게 역할 부여 : %s" % (hexcode, "예" if role.hoist else "아니요", "가능" if role.mentionable else "불가능", "불가능" if role.managed else "가능"), inline=False)
    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
    await app.get_channel(int(channel)).send(embed=embed)

@app.event
async def on_guild_role_update(before, after): # == class discord.Role
    guild = before.guild # == class discord.Guild
    response = mysql_do_return("SELECT * FROM `logging` WHERE server_id = %s" % (guild.id))
    if not len(response) == 1:
        return None
    if not response[0][5] == 1:
        return None
    channel = response[0][2]

    old_colour, old_time = before.colour, before.created_at + datetime.timedelta(hours=+9)
    old_hexcode, old_created = '#%02x%02x%02x' % (old_colour.r, old_colour.g, old_colour.b), "%s/%s/%s %s:%s:%s" % (old_time.year, old_time.month, old_time.day, old_time.hour, old_time.minute, old_time.second)
    colour, atime = after.colour, after.created_at + datetime.timedelta(hours=+9)
    hexcode, created = '#%02x%02x%02x' % (colour.r, colour.g, colour.b), "%s/%s/%s %s:%s:%s" % (atime.year, atime.month, atime.day, atime.hour, atime.minute, atime.second)
    if old_hexcode == hexcode and old_colour == colour and old_created == created and old_time == atime:
        return None
    if old_hexcode == "#000000":
        old_hexcode = "(없음)"
    if hexcode == "#000000":
        hexcode = "(없음)"
    embed = discord.Embed(title="역할이 수정되었습니다", color=Setting.embed_color)
    embed.add_field(name="이전", value="<@&%s> (`@%s`)\n생성일 : %s (24시간 기준, KST)" % (before.id, before.name, old_created), inline=False)
    embed.add_field(name="설정 내용", value="역할 색상 : %s\n온라인 멤버와 분리하여 표시 : %s\n역할 언급 : %s\n유저에게 역할 부여 : %s" % (old_hexcode, "예" if before.hoist else "아니요", "가능" if before.mentionable else "불가능", "불가능" if before.managed else "가능"), inline=False)
    embed.add_field(name="이후", value="<@&%s> (`@%s`)\n생성일 : %s (24시간 기준, KST)" % (after.id, after.name, created), inline=False)
    embed.add_field(name="설정 내용", value="역할 색상 : %s\n온라인 멤버와 분리하여 표시 : %s\n역할 언급 : %s\n유저에게 역할 부여 : %s" % (hexcode, "예" if after.hoist else "아니요", "가능" if after.mentionable else "불가능", "불가능" if after.managed else "가능"), inline=False)
    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
    await app.get_channel(int(channel)).send(embed=embed)

@app.event
async def on_guild_role_delete(role): # == class discord.Role
    guild = role.guild # == class discord.Guild
    response = mysql_do_return("SELECT * FROM `logging` WHERE server_id = %s" % (guild.id))
    if not len(response) == 1:
        return None
    if not response[0][5] == 1:
        return None
    channel = response[0][2]

    colour, atime = role.colour, role.created_at + datetime.timedelta(hours=+9)
    hexcode, created = '#%02x%02x%02x' % (colour.r, colour.g, colour.b), "%s/%s/%s %s:%s:%s" % (atime.year, atime.month, atime.day, atime.hour, atime.minute, atime.second)
    embed = discord.Embed(color=Setting.embed_color)
    embed.add_field(name="기존 역할이 제거되었습니다.", value="<@&%s> (`@%s`)\n생성일 : %s (24시간 기준, KST)" % (role.id, role.name, created), inline=False)
    embed.add_field(name="설정 내용", value="역할 색상 : %s\n온라인 멤버와 분리하여 표시 : %s\n역할 언급 : %s\n유저에게 역할 부여 : %s" % (hexcode, "예" if role.hoist else "아니요", "가능" if role.mentionable else "불가능", "불가능" if role.managed else "가능"), inline=False)
    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
    await app.get_channel(int(channel)).send(embed=embed)

@app.event
async def on_member_ban(guild, user):
    response = mysql_do_return("SELECT * FROM `logging` WHERE server_id = %s" % (guild.id))
    if not len(response) == 1:
        return None
    if not response[0][5] == 1:
        return None
    channel = response[0][2]

    atime, joined = user.created_at + datetime.timedelta(hours=+9), user.joined_at + datetime.timedelta(hours=+9)
    embed = discord.Embed(color=Setting.embed_color)
    embed.set_author(name="%s#%s" % (user.name, user.discriminator), icon_url=user.avatar_url)
    embed.add_field(name="서버에서 차단되었습니다", value="디스코드 가입일 : %s (24시간 기준, KST)\n서버 참여일 : %s (24시간 기준, KST)\n봇 여부 : %s" % ("%s/%s/%s %s:%s:%s" % (atime.year, atime.month, atime.day, atime.hour, atime.minute, atime.second), "%s/%s/%s %s:%s:%s" % (joined.year, joined.month, joined.day, joined.hour, joined.minute, joined.second), "O" if user.bot else "X"), inline=False)
    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
    await app.get_channel(int(channel)).send(embed=embed)

# 옵션
# 
# 여기서 "유저"는 서버에 참여하거나 퇴장한 유저를 의미함!!!!
#
# [@유저] :: 유저 언급
# [@#유저] :: 유저 닉네임 (e.g. @유저#0000)
# [유저이미지] :: 유저 프로필 이미지 링크 (e.g. https://images-ext-1.discordapp.net/external/tZaHa81jnKvJ94trIIo8m9ep8hr_sy1DoyA69pycpSQ/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/357857022974230538/ee1a4467da940a2242f4a1eb625cb1e5.webp)
# [@소유자] :: 서버 소유자 언급
# [@#소유자] :: 소유자 닉네임 (e.g. @소유자#0000)
# [서버이름] :: 서버 이름 (e.g. Develable)
# [서버인원] :: 서버 인원 (e.g. 37)
# [서버이미지] :: 서버 대표 이미지 링크 (e.g. https://images-ext-1.discordapp.net/external/OSjkP4-PJUogbnWqZge90cbvIBqibULBNFIFlhQYBTE/%3Fsize%3D1024/https/cdn.discordapp.com/icons/464764907666145281/e26785d2b70abcf18493614cb2e70070.webp?width=454&height=454)

@app.event
async def on_member_join(member):
    achannel = mysql_do_return("SELECT channel_id FROM `on_join` WHERE server_id = %s" % (member.guild.id))
    say = mysql_do_return("SELECT say FROM `on_join` WHERE server_id = %s" % (member.guild.id))
    if len(say) == 1:
        achannel, say = int(achannel[0][0]), say[0][0]
        say = say.replace('[@유저]', '<@%s>' % (member.id))
        say = say.replace('[@#유저]', '@%s#%s' % (member.name, member.discriminator))
        say = say.replace('[유저이미지]', '%s' % (member.avatar_url))
        say = say.replace('[@소유자]', '<@%s>' % (member.guild.owner.id))
        say = say.replace('[@#소유자]', '@%s#%s' % (member.guild.owner.id, member.guild.owner.discriminator))
        say = say.replace('[서버이름]', '%s' % (member.guild.name))
        say = say.replace('[서버인원]', '%s' % (len(member.guild.members)))
        say = say.replace('[서버이미지]', '<@%s>' % (member.guild.icon_url))
        await app.get_channel(achannel).send(say)

    response = mysql_do_return("SELECT * FROM `logging` WHERE server_id = %s" % (member.guild.id))
    if not len(response) == 1:
        return None
    if not response[0][4] == 1:
        return None
    channel = response[0][2]

    stats, atime = str(member.status), member.created_at + datetime.timedelta(hours=+9)
    embed = discord.Embed(color=Setting.embed_color)
    embed.set_author(name="%s#%s" % (member.name, member.discriminator), icon_url=member.avatar_url)
    embed.add_field(name="서버에 참가했습니다!", value="현재 상태 : %s %s\n디스코드 가입일 : %s (24시간 기준, KST)\n봇 여부 : %s" % (":large_blue_circle: 온라인" if "online" in stats else ":red_circle: 다른 용무 중" if "dnd" in stats else "자리 비움" if "idle" in stats else ":black_circle: 오프라인", "" if not "online" in stats or "dnd" in stats or "idle" in stats else "(모바일 접속)" if member.is_on_mobile() else "(PC 접속)", "%s/%s/%s %s:%s:%s" % (atime.year, atime.month, atime.day, atime.hour, atime.minute, atime.second), "O" if member.bot else "X"), inline=False)
    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
    await app.get_channel(int(channel)).send(embed=embed)

@app.event
async def on_member_remove(member):
    achannel = mysql_do_return("SELECT channel_id FROM `on_leave` WHERE server_id = %s" % (member.guild.id))
    say = mysql_do_return("SELECT say FROM `on_leave` WHERE server_id = %s" % (member.guild.id))
    if len(say) == 1:
        achannel, say = int(achannel[0][0]), say[0][0]
        say = say.replace('[@유저]', '<@%s>' % (member.id))
        say = say.replace('[@#유저]', '@%s#%s' % (member.name, member.discriminator))
        say = say.replace('[유저이미지]', '%s' % (member.avatar_url))
        say = say.replace('[@소유자]', '<@%s>' % (member.guild.owner.id))
        say = say.replace('[@#소유자]', '@%s#%s' % (member.guild.owner.id, member.guild.owner.discriminator))
        say = say.replace('[서버이름]', '%s' % (member.guild.name))
        say = say.replace('[서버인원]', '%s' % (len(member.guild.members)))
        say = say.replace('[서버이미지]', '<@%s>' % (member.guild.icon_url))
        await app.get_channel(achannel).send(say)

    response = mysql_do_return("SELECT * FROM `logging` WHERE server_id = %s" % (member.guild.id))
    if not len(response) == 1:
        return None
    if not response[0][4] == 1:
        return None
    channel = response[0][2]

    atime, joined = member.created_at + datetime.timedelta(hours=+9), member.joined_at + datetime.timedelta(hours=+9)
    embed = discord.Embed(color=Setting.embed_color)
    embed.set_author(name="%s#%s" % (member.name, member.discriminator), icon_url=member.avatar_url)
    embed.add_field(name="서버를 떠났습니다.", value="디스코드 가입일 : %s (24시간 기준, KST)\n서버 참여일 : %s (24시간 기준, KST)\n봇 여부 : %s" % ("%s/%s/%s %s:%s:%s" % (atime.year, atime.month, atime.day, atime.hour, atime.minute, atime.second), "%s/%s/%s %s:%s:%s" % (joined.year, joined.month, joined.day, joined.hour, joined.minute, joined.second), "O" if member.bot else "X"), inline=False)
    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
    await app.get_channel(int(channel)).send(embed=embed)

# Reaction of message
@app.event
async def on_message(message):
    try:
        try:
            try:
                log_msg(message.guild, message.guild.id, message.channel, message.channel.id, message.author.name, "#"+message.author.discriminator, message.author.id, message.content)
            except Exception as e:
                print("msg log error : %s" % (e))

            if message.channel.id == 554301796328407050: # "checking-uptime" Channel
                if message.author.id == 554300338274959360:
                    if "I'll check the status of Bot Online." in message.content:
                        await message.channel.send("Rutap Online")
                        return None

            resp = mysql_do_return("SELECT * FROM `banned_user` WHERE `user_id`=%s" % (message.author.id))

            if message.author.bot or len(resp) > 0:
                return None

            if str(type(message.channel)) == "<class 'discord.channel.DMChannel'>":
                await message.channel.send("<@%s>, 개인 메시지에서는 명령어를 사용 할 수 없습니다!" % (message.author.id))
                return None

            def pred(m): # await app.wait_for('message', check=pred)
                return m.author == message.author and m.channel == message.channel

            now = datetime.datetime.now()

            response = mysql_do_return("SELECT * FROM `and_so_on` WHERE server_id = %s" % (message.guild.id))

            if not len(response) == 0:
                prefix = response[0][1]

                response = mysql_do_return("SELECT * FROM `afk` WHERE `user_id`=%s" % (message.author.id))
                if len(response) == 1:
                    mysql_do("DELETE FROM `afk` WHERE `user_id`=%s" % (message.author.id))

                    embed = discord.Embed(title="잠수종료!", color=Setting.embed_color)
                    embed.add_field(name="대상 유저", value="<@%s>" % (message.author.id), inline=False)
                    embed.add_field(name="사유", value=response[0][2], inline=False)
                    embed.add_field(name="잠수 시작 시간", value=response[0][1], inline=True)
                    embed.add_field(name="잠수 종료 시간", value="%s-%s-%s %s:%s:%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second), inline=True)
                    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                    await message.channel.send(embed=embed)

                if 'rutap admin' in message.content:

                    if not str(message.author.id) in Setting.owner_id:
                        await message.channel.send("<@%s>, 봇 관리자로 등록되어 있지 않습니다. `setting.py` 파일을 확인하여 주세요." % (message.author.id))
                        return None

                    if message.content.startswith('rutap admin debug'):
                        selector = message.content.replace('rutap admin debug', '')

                        if "help" in selector:
                            embed = discord.Embed(title="카테고리 : `디버그`", description="`rutap admin debug prefix` - 해당 서버의 접두사를 조회합니다.\n`rutap admin debug ping` - 핑 정보를 표시합니다.\n`rutap admin debug error` - 디버그용 애러를 출력합니다.\n`rutap admin debug view` - 전송된 메시지를 확인합니다.", color=Setting.embed_color)
                            embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                            await message.channel.send(embed=embed)
                    
                        if "prefix" in selector:
                            await message.channel.send("<@%s>, `%s` 서버에서의 접두사는 `%s` 입니다!" % (message.author.id, message.guild.name, prefix))

                        if "ping" in selector:
                            msgarrived = float(str(time.time())[:-3])
                            msgtime = timeform(message.created_at)
                            msgdelay = msgarrived - msgtime - 32400
                            pong = int(msgdelay * 1000)
                            await message.channel.send("<@%s>,\nmsgarrived : `%s`\nmsgtime : `%s`\nmsgdelay : `%s`\nping : `%sms`" % (message.author.id, msgarrived, msgtime, msgdelay, pong))

                        if "error" in selector:
                            await unknown_error(message, "triggered error")

                        if "view" in selector:
                            await message.channel.send("`%s`" % (message.content))

                    if 'rutap admin notice' in message.content:
                        selector = message.content.replace('rutap admin notice', '')

                        if "help" in selector:
                            embed = discord.Embed(title="카테고리 : `공지`", color=Setting.embed_color)
                            embed.add_field(name="카테고리 : `옵션`", value="모든 명령어는 `rutap admin notice <option>`를 **포함**합니다.\n`-r` - 해당되는 키워드가 들어가는 채널 중, 먼저 발견된 채널에 공지를 보냅니다.\n`-p` - 공지 수신을 선택한 서버에 한해 메시지를 전송합니다.\n`-o` - 각 서버의 소유자에게 DM으로 메시지를 전송합니다.", inline=False)
                            embed.add_field(name="카테고리 : `부가설정`", value="모든 명령어는 `rutap admin notice `로 **시작**합니다.\n`invite <Guild ID>` - 해당 서버에 활성되어 있는 모든 초대링크를 나열합니다.", inline=False)
                            embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                            await message.channel.send(embed=embed)

                        if "invite" in selector:
                            target = re.findall(r'\d+', selector)
                            target = target[0]
                            target = int(target)
                            try:
                                guild_inf = app.get_guild(target)
                                invites = await guild_inf.invites()
                            except Exception as e:
                                invites = "error"

                            if invites == "error":
                                embed = discord.Embed(title="\"%s\" 서버 초대링크 현황" % (target), color=Setting.embed_color)
                                embed.add_field(name="로드 도중 문제가 발생했습니다.", value="```%s```" % (e), inline=False)
                            else:
                                embed = discord.Embed(title="\"%s\" 서버 초대링크 현황" % (guild_inf.name), color=Setting.embed_color)
                                if len(invites) < 1:
                                    embed.add_field(name="초대링크 없음", value="현재 \"%s\" 서버에 활성화 되어있는 초대링크가 없습니다.\n\n다른 명령어를 시도 할 수 있습니다!\n`rutap admin invite help`를 참고하세요." % (guild_inf.name), inline=False)
                                else:
                                    number = 1
                                    for invite in invites:
                                        dt = invite.created_at + datetime.timedelta(hours=+9)
                                        embed.add_field(name="#%s" % (number), value="초대링크 %s\n생성자 : %s\n생성일 : %s (KST, 24H)\n대상 채널 : %s\n**%s/%s 사용됨**\n링크 : %s%s" % ("**만료됨**" if invite.revoked else "**유효함**", "@%s#%s" % (invite.inviter.name, invite.inviter.discriminator), "%s/%s/%s %s:%s:%s" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second), "**#%s**(`%s`)" % (invite.channel.name, invite.channel.id), invite.uses, "∞" if invite.max_uses == 0 else invite.max_uses, invite.url, "\n\n**이 링크는 임시 역할 부여가 적용된 링크입니다**\n**__서버 참여자는 임시 역할을 부여받게 되며, 접속이 끊길 시 자동 추방되므로 유의하시기 바랍니다__**"if invite.temporary else ""), inline=False)
                                        number += 1

                            await message.channel.send(embed=embed)

                        if "-o" in selector or "-p" in selector or "-r" in selector:
                            wsend = message.content.replace("rutap admin notice -r", '')
                            wsend = wsend.replace("rutap admin notice -o", '')
                            wsend = wsend.replace("rutap admin notice -p", '')

                            await message.channel.send("<@%s>, 정말로 아래의 메시지를 전송하시겠습니까?\n\n```%s```\n(선택된 옵션 : %s)\n\n`취소` 또는 `수락`을 입력 해 주세요." % (message.author.id, wsend, '-r' if "-r" in selector else "-p" if "-p" in selector else "-o"))
                            response = await app.wait_for('message', check=pred)
                            if response.content == "수락":

                                if "-r" in selector:
                                    embed = discord.Embed(title="Develable 공지 발신 시스템", color=Setting.embed_color)
                                    embed.add_field(name="상태", value="모듈 초기화 진행중", inline=False)
                                    embed.add_field(name="보낼 메시지", value="```{msg}```".format(msg=wsend), inline=False)
                                    embed.add_field(name="선택된 옵션", value="`-r` - 해당되는 키워드가 들어가는 채널 중, 먼저 발견된 채널에 공지를 보냅니다.", inline=False)
                                    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                    msg = await message.channel.send(embed=embed)

                                    allows = Setting.allow_keyword
                                    disallows = Setting.disallow_keyword
                                    channel_name = Setting.autochannel_name
                                    send_notices = Setting.autochannel_notice
                                    em_success = "# 공지 발신 서버 목록"
                                    em_fail = "# 공지 미발신 서버 목록"
                                    success = "# 공지 발신 서버 목록"
                                    fail = "# 공지 미발신 서버 목록"
                                    count_channel = 0
                                    asdf = False
                                    dkdkdkr = False

                                    msg_embed = discord.Embed(title="%s 전체공지" % (app.user.name), description="**본 공지는 공지 수신 동의 여부와 무관하게 발송됩니다.**\n\n%s" % wsend, color=Setting.embed_color)
                                    msg_embed.set_thumbnail(url=app.user.avatar_url)
                                    msg_embed.set_footer(icon_url=message.author.avatar_url, text="발신자 : %s#%s %s | %s" % (message.author.name, message.author.discriminator, "- 인증됨" if str(message.author.id) in Setting.owner_id else " - 인증되지 않음!!", Copyright))

                                    auto_noti_embed = discord.Embed(title="알립니다", description=send_notices, color=Setting.embed_color)
                                    auto_noti_embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))

                                    embed = discord.Embed(title="Develable 공지 발신 시스템", color=Setting.embed_color)
                                    embed.add_field(name="상태", value="공지 발신 진행중", inline=False)
                                    embed.add_field(name="보낼 메시지", value="```{msg}```".format(msg=wsend), inline=False)
                                    embed.add_field(name="선택된 옵션", value="`-r` - 해당되는 키워드가 들어가는 채널 중, 먼저 발견된 채널에 공지를 보냅니다.", inline=False)
                                    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                    await msg.edit(embed=embed)

                                    for now_guild in app.guilds:
                                        count_channel = 0
                                        asdf = False
                                        while not len(now_guild.text_channels) - 1 == count_channel:
                                            dkdkdkr = False
                                            up = False
                                            for allow_now in allows:
                                                if allow_now in now_guild.text_channels[count_channel].name:
                                                    for disallow_now in disallows:
                                                        if disallow_now in now_guild.text_channels[count_channel].name:
                                                            dkdkdkr = True
                                                    if not dkdkdkr:
                                                        try:
                                                            await now_guild.text_channels[count_channel].send(embed=msg_embed)
                                                            success = success + "\n%s : #%s" % (now_guild.name, now_guild.text_channels[count_channel].name)
                                                            em_success = em_success + "\n%s(%s) : #%s" % (now_guild.name, now_guild.id, now_guild.text_channels[count_channel].name)
                                                            count_channel = len(now_guild.text_channels) - 1
                                                            asdf = True
                                                        except Exception as e:
                                                            up = True
                                                            count_channel += 1
                                            if not asdf and not up:
                                                count_channel += 1
                                        if not asdf:
                                            try:
                                                c = await now_guild.create_text_channel(channel_name)
                                                await c.send(embed=auto_noti_embed)
                                                await c.send(embed=msg_embed)
                                                em_success = em_success + "\n%s : #%s (자동생성됨)" % (now_guild.name, c.name)
                                                success = success + "\n%s(%s) : #%s (자동생성됨)" % (now_guild.name, now_guild.id, c.name)
                                            except Exception as e:
                                                em_fail = em_fail + "\n%s : %s" % (now_guild.name, e)
                                                fail = fail + "\n%s(%s) : %s" % (now_guild.name, now_guild.id, e)

                                    try:
                                        embed = discord.Embed(title="Develable 공지 발신 시스템", color=Setting.embed_color)
                                        embed.add_field(name="상태", value="공지 발신 완료", inline=False)
                                        embed.add_field(name="보낸 메시지", value="```{msg}```".format(msg=wsend), inline=False)
                                        embed.add_field(name="선택된 옵션", value="`-r` - 해당되는 키워드가 들어가는 채널 중, 먼저 발견된 채널에 공지를 보냅니다.", inline=False)
                                        embed.add_field(name="서버 목록", value="```Markdown\n{success}```\n```Markdown\n{fail}```\n\n공지 미발신 서버에 직접 연락할 수 있습니다!\n`rutap admin notice help`를 참고하세요.".format(success=em_success, fail=em_fail), inline=False)
                                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                        await msg.edit(embed=embed)
                                    except:
                                        open('log/notice_%s_%s_%s %s_%s_%s.txt' % (now.year, now.date, now.day, now.hour, now.minute, now.second), 'w').write("`-r` - 해당되는 키워드가 들어가는 채널 중, 먼저 발견된 채널에 공지를 보냅니다.\n\n%s\n\n%s\n\n%s" % (wsend, success, fail))
                                        embed = discord.Embed(title="Develable 공지 발신 시스템", color=Setting.embed_color)
                                        embed.add_field(name="상태", value="공지 발신 완료", inline=False)
                                        embed.add_field(name="보낸 메시지", value="```{msg}```".format(msg=wsend), inline=False)
                                        embed.add_field(name="선택된 옵션", value="`-r` - 해당되는 키워드가 들어가는 채널 중, 먼저 발견된 채널에 공지를 보냅니다.", inline=False)
                                        embed.add_field(name="서버 목록", value="글자 제한(1200자) 초과로 인하여, `log/notice_%s_%s_%s %s_%s_%s.txt` 파일로 저장되었습니다.\n\n공지 미발신 서버에 직접 연락할 수 있습니다!\n`rutap admin notice help`를 참고하세요." % (now.year, now.date, now.day, now.hour, now.minute, now.second), inline=False)
                                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                        await msg.edit(embed=embed)

                                if "-p" in selector:
                                    embed = discord.Embed(title="Develable 공지 발신 시스템", color=Setting.embed_color)
                                    embed.add_field(name="상태", value="모듈 초기화 진행중", inline=False)
                                    embed.add_field(name="보낼 메시지", value="```{msg}```".format(msg=wsend), inline=False)
                                    embed.add_field(name="선택된 옵션", value="`-p` - 공지 수신을 선택한 서버에 한해 메시지를 전송합니다.", inline=False)
                                    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                    msg = await message.channel.send(embed=embed)

                                    em_success = "# 공지 발신 서버 목록"
                                    em_fail = "# 공지 미발신 서버 목록"

                                    success = "# 공지 발신 서버 목록"
                                    fail = "# 공지 미발신 서버 목록"

                                    msg_embed = discord.Embed(title="%s 일반공지" % (app.user.name), description="**본 공지는 수신을 희망한 서버에 한해 발송됩니다.**\n\n%s" % wsend, color=Setting.embed_color)
                                    msg_embed.set_thumbnail(url=app.user.avatar_url)
                                    msg_embed.set_footer(icon_url=message.author.avatar_url, text="발신자 : %s#%s %s | %s" % (message.author.name, message.author.discriminator, "- 인증됨" if str(message.author.id) in Setting.owner_id else " - 인증되지 않음!!", Copyright))

                                    embed = discord.Embed(title="Develable 공지 발신 시스템", color=Setting.embed_color)
                                    embed.add_field(name="상태", value="공지 발신 진행중", inline=False)
                                    embed.add_field(name="보낼 메시지", value="```{msg}```".format(msg=wsend), inline=False)
                                    embed.add_field(name="선택된 옵션", value="`-p` - 공지 수신을 선택한 서버에 한해 메시지를 전송합니다.", inline=False)
                                    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                    await msg.edit(embed=embed)

                                    guilds = mysql_do_return("SELECT * FROM `bot_selection_noti`")

                                    for now_server in guilds:
                                        try:
                                            channel = await app.get_channel(now_server[1])
                                            await channel.send(embed=msg_embed)
                                            em_success = em_success + "\n%s : #%s" % (channel.guild.name, channel.name)
                                            success = success + "\n%s(%s) : #%s" % (channel.guild.name, channel.guild.id, channel.name)
                                        except Exception as e:
                                            em_fail = em_fail + "\n%s : %s" % (channel.guild.name, e)
                                            fail = fail + "\n%s(%s) : %s" % (channel.guild.name, channel.guild.id, e)

                                    try:
                                        embed = discord.Embed(title="Develable 공지 발신 시스템", color=Setting.embed_color)
                                        embed.add_field(name="상태", value="공지 발신 완료", inline=False)
                                        embed.add_field(name="보낸 메시지", value="```{msg}```".format(msg=wsend), inline=False)
                                        embed.add_field(name="선택된 옵션", value="`-r` - 해당되는 키워드가 들어가는 채널 중, 먼저 발견된 채널에 공지를 보냅니다.", inline=False)
                                        embed.add_field(name="서버 목록", value="```Markdown\n{success}```\n```Markdown\n{fail}```\n\n공지 미발신 서버에 직접 연락할 수 있습니다!\n`rutap admin notice help`를 참고하세요.".format(success=success, fail=fail), inline=False)
                                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                        await msg.edit(embed=embed)
                                    except:
                                        open('log/notice_%s_%s_%s %s_%s_%s.txt' % (now.year, now.date, now.day, now.hour, now.minute, now.second), 'w').write("`-r` - 해당되는 키워드가 들어가는 채널 중, 먼저 발견된 채널에 공지를 보냅니다.\n\n%s\n\n%s\n\n%s" % (wsend, success, fail))
                                        embed = discord.Embed(title="Develable 공지 발신 시스템", color=Setting.embed_color)
                                        embed.add_field(name="상태", value="공지 발신 완료", inline=False)
                                        embed.add_field(name="보낸 메시지", value="```{msg}```".format(msg=wsend), inline=False)
                                        embed.add_field(name="선택된 옵션", value="`-r` - 해당되는 키워드가 들어가는 채널 중, 먼저 발견된 채널에 공지를 보냅니다.", inline=False)
                                        embed.add_field(name="서버 목록", value="글자 제한(1200자) 초과로 인하여, `log/notice_%s_%s_%s %s_%s_%s.txt` 파일로 저장되었습니다.\n\n공지 미발신 서버에 직접 연락할 수 있습니다!\n`rutap admin notice help`를 참고하세요." % (now.year, now.date, now.day, now.hour, now.minute, now.second), inline=False)
                                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                        await msg.edit(embed=embed)

                                if "-o" in selector:
                                    embed = discord.Embed(title="Develable 공지 발신 시스템", color=Setting.embed_color)
                                    embed.add_field(name="상태", value="모듈 초기화 진행중", inline=False)
                                    embed.add_field(name="보낼 메시지", value="```{msg}```".format(msg=wsend), inline=False)
                                    embed.add_field(name="선택된 옵션", value="`-o` - 각 서버의 소유자에게 DM으로 메시지를 전송합니다.", inline=False)
                                    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                    msg = await message.channel.send(embed=embed)

                                    em_success = "# 공지 발신 서버 목록"
                                    em_fail = "# 공지 미발신 서버 목록"

                                    success = "# 공지 발신 서버 목록"
                                    fail = "# 공지 미발신 서버 목록"

                                    owners = []

                                    msg_embed = discord.Embed(title="%s 전체공지" % (app.user.name), description="**본 공지는 각 서버의 소유자에게만 발송됩니다.**\n\n%s" % wsend, color=Setting.embed_color)
                                    msg_embed.set_thumbnail(url=app.user.avatar_url)
                                    msg_embed.set_footer(icon_url=message.author.avatar_url, text="발신자 : %s#%s %s | %s" % (message.author.name, message.author.discriminator, "- 인증됨" if str(message.author.id) in Setting.owner_id else " - 인증되지 않음!!", Copyright))

                                    embed = discord.Embed(title="Develable 공지 발신 시스템", color=Setting.embed_color)
                                    embed.add_field(name="상태", value="공지 발신 진행중", inline=False)
                                    embed.add_field(name="보낼 메시지", value="```{msg}```".format(msg=wsend), inline=False)
                                    embed.add_field(name="선택된 옵션", value="`-o` - 각 서버의 소유자에게 DM으로 메시지를 전송합니다.", inline=False)
                                    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                    await msg.edit(embed=embed)

                                    for now_guild in app.guilds:
                                        owner = now_guild.owner
                                        if not str(owner.id) in owners:
                                            try:
                                                await owner.send(embed=msg_embed)
                                                owners.append(str(owner.id))
                                                em_success = success + "\n%s" % (now_guild.name)
                                                success = success + "\n%s(%s)" % (now_guild.name, now_guild.id)
                                            except Exception as e:
                                                owners.append(str(owner.id))
                                                em_fail = fail + "\n%s : %s" % (now_guild.name, e)
                                                fail = fail + "\n%s(%s) : %s" % (now_guild.name, now_guild.id, e)
                                        else:
                                            em_fail = fail + "\n%s : 소유자 중복" % (now_guild.name)
                                            fail = fail + "\n%s(%s) : 소유자 중복" % (now_guild.name, now_guild.id)

                                    try:
                                        embed = discord.Embed(title="Develable 공지 발신 시스템", color=Setting.embed_color)
                                        embed.add_field(name="상태", value="공지 발신 완료", inline=False)
                                        embed.add_field(name="보낸 메시지", value="```{msg}```".format(msg=wsend), inline=False)
                                        embed.add_field(name="선택된 옵션", value="`-o` - 각 서버의 소유자에게 DM으로 메시지를 전송합니다.", inline=False)
                                        embed.add_field(name="서버 목록", value="```Markdown\n{success}```\n```Markdown\n{fail}```\n\n공지 미발신 서버에 직접 연락할 수 있습니다!\n`rutap admin notice help`를 참고하세요.".format(success=success, fail=fail), inline=False)
                                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                        await msg.edit(embed=embed)
                                    except:
                                        open('log/notice_%s_%s_%s %s_%s_%s.txt' % (now.year, now.date, now.day, now.hour, now.minute, now.second), 'w').write("`-r` - 해당되는 키워드가 들어가는 채널 중, 먼저 발견된 채널에 공지를 보냅니다.\n\n%s\n\n%s\n\n%s" % (wsend, success, fail))
                                        embed = discord.Embed(title="Develable 공지 발신 시스템", color=Setting.embed_color)
                                        embed.add_field(name="상태", value="공지 발신 완료", inline=False)
                                        embed.add_field(name="보낸 메시지", value="```{msg}```".format(msg=wsend), inline=False)
                                        embed.add_field(name="선택된 옵션", value="`-o` - 각 서버의 소유자에게 DM으로 메시지를 전송합니다.", inline=False)
                                        embed.add_field(name="서버 목록", value="글자 제한(1200자) 초과로 인하여, `log/notice_%s_%s_%s %s_%s_%s.txt` 파일로 저장되었습니다.\n\n공지 미발신 서버에 직접 연락할 수 있습니다!\n`rutap admin notice help`를 참고하세요." % (now.year, now.date, now.day, now.hour, now.minute, now.second), inline=False)
                                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                        await msg.edit(embed=embed)

                    selector = message.content.replace('rutap admin', '')

                    if "game" in selector:
                        result = change_presence(message)
                        if result == False:
                            await message.channel.send("<@%s>, 게임명은 비워둘 수 없습니다. 다시 시도 해 주세요." % (message.author.id))
                            return None
                        else:
                            open("rpc.rts", 'w').write(result)
                            await message.channel.send("<@%s>, 봇이 `%s`을(를) 플레이 하게 됩니다." % (message.author.id, result))
                            await app.change_presence(status=discord.Status.online, activity=discord.Game(result))
                            return None

                    if "ban" in selector:
                        result = user_ban(message)
                        if result == False:
                            await message.channel.send("<@%s>, 자기 자신을 밴 시킬 수 없습니다!" % (message.author.id))
                        else:
                            await message.channel.send("<@%s>, 앞으로 `%s`님의 모든 메시지를 무시합니다." % (message.author.id, result))

                    if "unban" in selector:
                        result = user_unban(message)
                        if result == False:
                            await message.channel.send("<@%s>, 해당 유저는 밴 되지 않았습니다!" % (message.author.id))
                        else:
                            await message.channel.send("<@%s>, 앞으로 `%s`님의 모든 메시지를 무시하지 않습니다." % (message.author.id, result))

                    if "shutdown" in selector:
                        await message.channel.send("<@%s>, 봇의 가동을 중지합니다." % (message.author.id))
                        await app.change_presence(status=discord.Status.offline, activity=discord.Game("Offline"))
                        exit()

                    if "info" in selector:
                        stat, cpu = setting.MEMORYSTATUSEX(), psutil.cpu_percent()
                        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                        mem = stat.dwMemoryLoad
                        servers = mysql_do_return("SELECT * FROM `and_so_on`")
                        embed = discord.Embed(title="정보", color=Setting.embed_color)
                        embed.add_field(name="봇 정보", value="`%s`/`%s`개의 서버에서 사용중" % (len(app.guilds), len(servers)), inline=False)
                        embed.add_field(name="하드웨어 정보", value="CPU : {cpu}% 사용중\nRAM : {mem}% 사용중".format(cpu=cpu, mem=mem), inline=False)
                        await message.channel.send(embed=embed)

                cc = mysql_do_return("SELECT content FROM `custom_command_data` WHERE custom_command_server_id = %s AND name = '%s'" % (message.guild.id, message.content))
                if len(cc) == 1:
                    await message.channel.send(cc[0][0])
                elif len(cc) > 1:
                    await message.channel.send("<@%s>, 동일한 명령어를 가진 커스텀 커맨드가 두개 이상인것이 확인되었습니다. 하나를 지워주시기 바랍니다." % message.author.id)

                if message.content == prefix + "도움말":
                    await message.channel.send("<@%s>, 아래 링크를 참조하여 주세요.\nhttps://develable.xyz/post/114" % (message.author.id))

                if message.content == prefix + "정보":
                    embed = discord.Embed(title="루탑봇 정보!", color=Setting.embed_color)
                    embed.add_field(name="[루탑봇 소개]", value="https://cutr.es/py7WS", inline=False)
                    embed.add_field(name="[루탑봇 개발자]", value="화향", inline=False)
                    embed.add_field(name="[오픈소스 라이선스]", value="This bot use nekos.life API. : https://discord.services/api/\nThis bot use Twitter API. : https://cutr.es/aZZ7F", inline=False)
                    embed.add_field(name="[Team. 화공 공식 링크]", value="공식 홈페이지 : https://develable.xyz/\n서버상태 조회 : https://status.develable.xyz/\n공식 페이스북 : https://cutr.es/uwXnJ\n공식 디스코드 : https://invite.gg/Develable", inline=False)
                    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                    await message.channel.send(embed=embed)

                if prefix + "서버정보" == message.content:
                    atime, server_v_lv, server_locate, cc_used, cc_total = message.guild.created_at + datetime.timedelta(hours=+9), str(message.guild.verification_level), str(message.guild.region), mysql_do_return("SELECT id FROM `custom_command_data` WHERE custom_command_server_id = %s" % message.guild.id), mysql_do_return("SELECT total FROM `custom_command` WHERE server_id = %s" % message.guild.id)[0][0]
                    embed = discord.Embed(title="\"%s\" 서버정보!" % (message.guild.name), color=Setting.embed_color)
                    embed.add_field(name="서버 소유자", value="<@%s> (`@%s#%s`)" % (message.guild.owner.id, message.guild.owner.name, message.guild.owner.discriminator), inline=False)
                    embed.add_field(name="서버 생성일", value="%s (24시간 기준, KST)" % "%s/%s/%s %s:%s:%s" % (atime.year, atime.month, atime.day, atime.hour, atime.minute, atime.second), inline=False)
                    embed.add_field(name="서버 보안등급", value="없음" if server_v_lv == "none" else "낮음 (디스코드 계정이 **이메일 인증**을 받아야 합니다.)" if server_v_lv == "low" else "보통 (서버에 접속한지 **5분**이 지나야 합니다)" if server_v_lv == "medium" else "높음 (서버에 접속한지 **10분**이 지나야 합니다)" if server_v_lv == "high" else "매우 높음 (**전화 인증**을 받아야만 합니다)", inline=False)
                    embed.add_field(name="서버 위치", value="브라질" if server_locate == "brazil" else "중부 유럽" if server_locate == "eu-central" else "홍콩" if server_locate == "hongkong" else "인도" if server_locate == "india" else "일본" if server_locate == "japan" else "러시아" if server_locate == "russia" else "싱가포르" if server_locate == "singapore" else "북아프리카" if server_locate == "southafrica" else "호주(시드니)" if server_locate == "sydney" else "미국 중부" if server_locate == "us-central" else "미국 동부" if server_locate == "us-east" else "미국 북부" if server_locate == "us-south" else "미국 서부" if server_locate == "us-west" else "동부 유럽" if server_locate == "us-east" else server_locate, inline=False)
                    embed.add_field(name="서버 잠수채널", value="%s %s" % ("없음" if str(message.guild.afk_channel) == "None" else message.guild.afk_channel, "" if str(message.guild.afk_channel) == "None" else "(%s분 이상 잠수이면 이동됨)" % int(message.guild.afk_timeout/60)), inline=False)
                    embed.add_field(name="커스텀커맨드 사용권", value="{per}% ({used}/{total} 개) 사용중".format(per=round(len(cc_used)/cc_total*100, 1), used=len(cc_used), total=cc_total), inline=False)
                    embed.set_thumbnail(url=message.guild.icon_url)
                    embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.guild.id, Setting.version, Copyright))
                    await message.channel.send(embed=embed)

                if message.content.startswith(prefix + '유저정보'):
                    target = message.author # class discord.member.Member
                    notification = True
                    replacea = message.content.replace(prefix + '유저정보', '')
                    if replacea[1:].startswith('<@') and message.content.endswith('>'):
                        target = re.findall(r'\d+', replacea)
                        target = target[0]
                        target = int(target)
                        target = app.get_user(target) # class discord.user.ClientUser
                        notification = False
                        if target.id == message.author.id:
                            notification, target = True, message.author

                    if target == None or target == "None" or os.path.isfile("%s_Banned.rts" % (target.id)):
                        await message.channel.send("<@%s>, 해당 유저의 정보를 받아오지 못했습니다. 입력값을 다시 한번 확인 해 주세요." % (message.author.id))

                    atime= target.created_at + datetime.timedelta(hours=+9)
                    embed = discord.Embed(title="%s#%s 유저정보!" % (target.name, target.discriminator), color=Setting.embed_color)
                    embed.set_thumbnail(url=target.avatar_url)
                    if notification:
                        stats, game = str(target.status), target.activities
                        embed.add_field(name="현재 상태", value="%s %s" % (":large_blue_circle: 온라인" if "online" in stats else ":red_circle: 다른 용무 중" if "dnd" in stats else "자리 비움" if "idle" in stats else ":black_circle: 오프라인", "" if not "online" in stats or "dnd" in stats or "idle" in stats else "(모바일 접속)" if target.is_on_mobile() else "(PC 접속)"), inline=False)
                        if len(game) == 1:
                            if str(game[0].type) == "ActivityType.playing":
                                btime, ctime = game[0].start + datetime.timedelta(hours=+9), datetime.datetime.now()
                                embed.add_field(name="현재 플레이중", value="`%s`\n%s ~ %s (24시간 기준, KST)" % (game[0].name, "%s/%s/%s %s:%s:%s" % (btime.year, btime.month, btime.day, btime.hour, btime.minute, btime.second), "%s/%s/%s %s:%s:%s" % (ctime.year, ctime.month, ctime.day, ctime.hour, ctime.minute, ctime.second)), inline=False)
                            elif str(game[0].type) == "ActivityType.streaming":
                                embed.add_field(name="현재 방송중", value="**%s**\n`%s` 플레이중\n링크 :: %s" % (game[0].name, game[0].details, game[0].url), inline=False)
                            else:
                                await app.get_channel(int(Setting.err_log_channel)).send("Error occured in `유저정보`.\n-- `%s`" % game[0].type)
                    else:
                        embed.add_field(name="현재 상태", value="다른 유저의 상태는 표시하지 않습니다.", inline=False)
                    embed.add_field(name="봇 여부", value="%s" % ("봇이 맞습니다." if target.bot else "봇이 아닙니다."), inline=False)
                    embed.add_field(name="디스코드 가입일", value="%s/%s/%s %s:%s:%s (24시간 기준, KST)" % (atime.year, atime.month, atime.day, atime.hour, atime.minute, atime.second), inline=False)
                    embed.add_field(name="이 서버에서의 별칭", value="%s" % (target.display_name if not target.name == target.display_name else "(없음)"), inline=False)
                    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                    await message.channel.send(embed=embed)

                if message.content.startswith(prefix + '투표 '):
                    admin_cmds = ["시작", "종료"]
                    split = message.content.split()
                    cursor = str(split[1])

                    if cursor == "현황" or cursor == "정보":
                        response = mysql_do_return("SELECT * FROM `vote` WHERE `server_id`=%s" % (message.guild.id))
                        if len(response) == 0:
                            embed = discord.Embed(title="\"%s\" 서버 투표현황" % (message.guild.name), color=Setting.embed_color)
                            embed.add_field(name="현재 진행중인 투표가 없습니다!", value="현재 해당 서버에서 진행중인 투표가 없습니다.\n다음 투표를 기다려 주세요!%s" % ("\n\n`%s투표 시작`을 입력하여 투표를 시작 할 수 있습니다." % (prefix) if message.author.guild_permissions.administrator or str(message.author.id) in Setting.owner_id else ""), inline=False)
                            embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                            await message.channel.send(embed=embed)
                        else:
                            starter = app.get_user(response[0][2])
                            embed = discord.Embed(title="\"%s\" 서버 투표현황" % (message.guild.name), description="안건 : {title}\n설명 : {description}\n투표 현황 : {per}% ({voted}/{all})\n발의자 : <@{id}> (`{starter}`)\n발의시간 : {datetime} (24시간 기준, KST)\n**서버 인원은 봇도 포함합니다**".format(title=response[0][4], id=response[0][2], starter="%s#%s" % (starter.name, starter.discriminator), datetime=response[0][3], description=response[0][5], per=round(((response[0][6] + response[0][7]) / len(message.guild.members)) * 100, 1), voted=response[0][6] + response[0][7], all=len(message.guild.members)), color=Setting.embed_color)
                            embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                            await message.channel.send(embed=embed)

                    if cursor == "하기":
                        response = mysql_do_return("SELECT * FROM `vote` WHERE `server_id`=%s" % (message.guild.id))
                        if len(response) == 0:
                            embed = discord.Embed(title="현재 \"%s\" 서버에서 진행중인 투표가 없습니다!" % (message.guild.name), description="현재 해당 서버에서 진행중인 투표가 없습니다.\n다음 투표를 기다려 주세요!%s" % ("\n\n`%s투표 시작`을 입력하여 투표를 시작 할 수 있습니다." % (prefix) if message.author.guild_permissions.administrator or str(message.author.id) in Setting.owner_id else ""), color=Setting.embed_color)
                            embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                            await message.channel.send(embed=embed)
                        else:
                            if str(message.author.id) in response[0][8]:
                                await message.channel.send("<@%s>, 이미 `%s` 안건에 대하여 투표를 하셨습니다!\n(참고 :: 발의자는 투표를 할 수 없습니다!)" % (message.author.id, response[0][4]))
                            else:
                                embed = discord.Embed(title="\"%s\" 안건에 대한 투표를 진행합니다" % (response[0][4]), description="설명 : %s\n\n1분의 기간내에 하단의 이모지를 클릭하여 진행하여 주시기 바랍니다." % (response[0][5]), color=Setting.embed_color)
                                embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                question = await message.author.send(embed=embed)
                                await message.channel.send("<@%s>, DM을 확인 해 주세요" % (message.author.id))
                                await question.add_reaction("1⃣")
                                await question.add_reaction("2⃣")
                                def vote_add_question_check(reaction, user):
                                    return (user == message.author and str(reaction.emoji) == '1⃣') or (user == message.author and str(reaction.emoji) == "2⃣")
                                try:
                                    reaction, user = await app.wait_for('reaction_add', timeout=60.0, check=vote_add_question_check)
                                except asyncio.TimeoutError:
                                    await message.author.send("1분 이상 미반응으로 인하여 취소되었습니다.")
                                else:
                                    if reaction.emoji == "1⃣":
                                        mysql_do("UPDATE `vote` SET `up_vote`=%s,`participants`='%s' WHERE `server_id`=%s" % (response[0][6] + 1, response[0][8] + " %s" % (message.author.id), message.guild.id))
                                        embed = discord.Embed(title="\"%s\" 안건에 대해 투표를 해주셔서 감사합니다!" % (response[0][4]), description="투표 결과는 추후 관리자가 투표를 종료하면 출력됩니다.", color=Setting.embed_color)
                                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                        await question.edit(embed=embed)
                                    elif reaction.emoji == "2⃣":
                                        mysql_do("UPDATE `vote` SET `down_vote`=%s,`participants`='%s' WHERE `server_id`=%s" % (response[0][7] + 1, response[0][8] + " %s" % (message.author.id), message.guild.id))
                                        embed = discord.Embed(title="\"%s\" 안건에 대해 투표를 해주셔서 감사합니다!" % (response[0][4]), description="투표 결과는 추후 관리자가 투표를 종료하면 출력됩니다.", color=Setting.embed_color)
                                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                        await question.edit(embed=embed)
                                    else:
                                        await message.author.send("지정되지 않은 이모지 추가로 인하여 취소되었습니다.")

                    if cursor in admin_cmds:
                        if not message.content[7:].startswith('<') and message.content.endswith('>'):
                            await message.channel.send("<@%s>, 유저를 언급해야 합니다!" % (message.author.id))
                            return None

                        if cursor == "시작":
                            response = mysql_do_return("SELECT * FROM `vote` WHERE `server_id`=%s" % (message.guild.id))
                            if not len(response) == 0:
                                await message.channel.send("<@%s>, 현재 진행중인 투표가 있습니다!" % (message.author.id))
                                return None
                            embed = discord.Embed(title="\"%s\" 서버에서 새로운 투표를 시작합니다" % (message.guild.name), description="투표 안건을 선정하여 주세요!", color=Setting.embed_color)
                            embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                            question = await message.channel.send(embed=embed)
                            user_response = await app.wait_for('message', check=pred)
                            title = user_response.content
                            await user_response.delete()
                            embed = discord.Embed(title="\"%s\" 서버에서 새로운 투표를 시작합니다" % (message.guild.name), description="투표 설명을 작성하여 주세요!", color=Setting.embed_color)
                            embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                            await question.edit(embed=embed)
                            user_response = await app.wait_for('message', check=pred)
                            description = user_response.content
                            await user_response.delete()
                            skipped = False
                            while not skipped:
                                embed = discord.Embed(title="\"%s\" 서버에서 새로운 투표를 시작합니다" % (message.guild.name), description="투표 시작 공지를 보낼 채널을 알려주세요!\ne.g.) <#%s>" % (message.channel.id), color=Setting.embed_color)
                                embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                await question.edit(embed=embed)
                                user_response = await app.wait_for('message', check=pred)
                                channel = user_response.content
                                await user_response.delete()
                                channel_int = re.findall(r'\d+', channel)
                                channel_int = channel_int[0]
                                channel_int = int(channel_int)
                                try:
                                    channel = app.get_channel(channel_int)
                                    now_t = "%s-%s-%s %s:%s:%s" % (now.year, now.month, now.second, now.hour, now.minute, now.second)
                                    noti_embed = discord.Embed(title="새로운 투표가 시작됩니다", description="발의자 : <@%s> (`%s#%s`)\n발의시간 : %s (24시간 기준, KST)\n\n안건 : %s\n설명 : %s" % (message.author.id, message.author.name, message.author.discriminator, now_t, title, description), color=Setting.embed_color)
                                    noti_embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                                    await channel.send(embed=noti_embed)
                                    mysql_do("INSERT INTO `vote`(`server_id`, `starter`, `datetime`, `title`, `description`, `participants`, `ch`) VALUES (%s, %s, '%s', '%s', '%s', '%s', %s)" % (message.guild.id, message.author.id, now_t, title, description, message.author.id, channel_int))
                                    skipped = True
                                except:
                                    skipped = False
                            embed = discord.Embed(title="\"%s\" 서버에서 새로운 투표를 시작합니다" % (message.guild.name), description="성공적으로 투표가 시작되었습니다!", color=Setting.embed_color)
                            embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                            await question.edit(embed=embed)

                        if cursor == "종료":
                            response = mysql_do_return("SELECT * FROM `vote` WHERE `server_id`=%s" % (message.guild.id))
                            if len(response) == 0:
                                await message.channel.send("<@%s>, 현재 진행중인 투표가 없습니다!" % (message.author.id))
                                return None
                            mysql_do("DELETE FROM `vote` WHERE `server_id`=%s" % (message.guild.id))
                            now_t = "%s-%s-%s %s:%s:%s" % (now.year, now.month, now.second, now.hour, now.minute, now.second)
                            try:
                                starter = app.get_user(response[0][2])
                            except:
                                starter = None
                            noti_embed = discord.Embed(title="투표가 종료되었습니다", description="발의자 : %s (`%s`)\n발의시간 : %s (24시간 기준, KST)\n종료시간 : %s (24시간 기준, KST)\n\n안건 : %s\n설명 : %s\n\n:one: : %s표\n:two: : %s표" % ("존재하지 않음" if starter == None else "<@%s>" % (starter.id), "존재하지 않음" if starter == None else "%s#%s" % (starter.name, starter.discriminator), response[0][3], now_t, response[0][4], response[0][5], response[0][6], response[0][7]), color=Setting.embed_color)
                            noti_embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                            try:
                                channel = app.get_channel(channel_int)
                                await channel.send(embed=noti_embed)
                            except:
                                await message.channel.send(embed=noti_embed)
                            await message.channel.send("<@%s>, 성공적으로 투표가 종료되었습니다!" % (message.author.id))

                if message.content.startswith(prefix + '경고 '):
                    warn_admin = ["부여", "제거", "리셋"]

                    except_cmd = message.content.replace(prefix + '경고 ', '')
                    sp = except_cmd.split()
                    cursor = str(sp[0])

                    if "확인" in cursor:
                        if message.content[7:].startswith('<') and message.content.endswith('>'):
                            asdf = str(sp[1])
                            mention_id = re.findall(r'\d+', asdf)
                            mention_id = mention_id[0]
                            mention_id = str(mention_id)
                        else:
                            mention_id = message.author.id

                        response = warn_check(message, mention_id)
                        uuuser = app.get_user(int(mention_id))

                        embed = discord.Embed(title="%s#%s님의 경고 현황!" % (uuuser.name, uuuser.discriminator), description="<@%s>님의 현재 경고는 `%s`회 이며, 상세 내용은 아래와 같습니다.\n```Markdown\n%s```%s" % (mention_id, response[0], response[1], "" if int(response[0]) == 0 else "\n`%s경고 리셋 @%s`(을)를 이용하여 경고 로그를 지울 수 있습니다." % (prefix, uuuser.name) if message.author.guild_permissions.administrator or str(message.author.id) in Setting.owner_id else ""), color=Setting.embed_color)
                        embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.guild.id, Setting.version, Copyright))
                        await message.channel.send(embed=embed)

                    if cursor in warn_admin:
                        if message.author.guild_permissions.administrator or str(message.author.id) in Setting.owner_id:
                            if not message.content[7:].startswith('<') and message.content.endswith('>'):
                                await message.channel.send("<@%s>, 유저를 언급해야 합니다!" % (message.author.id))
                                return None
                            asdf = str(sp[1])
                            mention_id = re.findall(r'\d+', asdf)
                            mention_id = mention_id[0]
                            mention_id = str(mention_id)

                            reason = message.content.replace("%s경고 %s <@%s>" % (prefix, cursor, mention_id), '')

                            if "부여" in cursor:
                                embed = discord.Embed(title="경고가 부여되었습니다!", description="<@%s>님에 의해 <@%s>님께서 경고를 `1`회 받으셨습니다!\n<@%s>님의 현재 경고는 `%s`회 입니다!\n사유 : `%s`" % (message.author.id, mention_id, mention_id, warn_give(message, mention_id, reason), "(없음)" if reason.replace('\t', '') == None else reason), color=Setting.embed_color)
                                embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.guild.id, Setting.version, Copyright))
                                await message.channel.send(embed=embed)

                            if "제거" in cursor:
                                result = warn_cancel(message, mention_id, reason)
                                if not result:
                                    await message.channel.send("<@%s>, 대상 유저는 경고를 보유하고 있지 않습니다!" % (message.author.id))
                                    return None
                                embed = discord.Embed(title="경고가 제거되었습니다!", description="<@%s>님에 의해 <@%s>님께서 경고를 `1`회 제거 받으셨습니다!\n<@%s>님의 현재 경고는 `%s`회 입니다!\n사유 : `%s`" % (message.author.id, mention_id, mention_id, result, "(없음)" if reason.replace('\t', '') == None else reason), color=Setting.embed_color)
                                embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.guild.id, Setting.version, Copyright))
                                await message.channel.send(embed=embed)

                            if "리셋" in cursor:
                                result = warn_reset(message, mention_id)
                                if not result:
                                    await message.channel.send("<@%s>, 대상 유저는 경고를 보유하고 있지 않습니다!" % (message.author.id))
                                    return None
                                embed = discord.Embed(title="경고가 초기화되었습니다!", description="<@%s>님에 의해 <@%s>님의 경고가 전부 제거되었습니다!\n<@%s>님의 현재 경고는 `%s`회 입니다!\n사유 : `%s`" % (message.author.id, mention_id, mention_id, result, "(없음)" if reason.replace('\t', '') == None else reason), color=Setting.embed_color)
                                embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.guild.id, Setting.version, Copyright))
                                await message.channel.send(embed=embed)
                        else:
                            await message.channel.send("<@%s>, 당신은 관리자가 아닙니다!" % (message.author.id))

                if message.content == prefix + "공지수신":
                    if message.author.guild_permissions.administrator or str(message.author.id) in Setting.owner_id:
                        result = bot_selection_noti(message, prefix)
                        if result:
                            await message.channel.send("<@%s>, 앞으로 <#%s> 채널에서 일반 공지를 수신합니다" % (message.author.id, message.channel.id))
                        elif result == "OK":
                            await message.channel.send("<@%s>, 앞으로 일반 공지를 수신하지 않습니다. (긴급공지 제외)" % (message.author.id))
                        else:
                            await message.channel.send("<@%s>, 이미 해당 채널에서 공지를 수신하고 있습니다!" % (message.author.id))
                    else:
                        await message.channel.send("<@%s>, 당신은 관리자가 아닙니다!" % (message.author.id))

                if message.content.startswith(prefix + "냥이"):
                    q = message.content.replace(prefix + '냥이', '')
                    if "태그" in q:
                        embed = discord.Embed(title="태그 정보!", color=Setting.embed_color)
                        embed.add_field(name="분류: `건전`", value="`neko` : 고양이 (기본)\n`avatar` : 프로필용\n`holo` : (저도 잘 모르겠어요 제보환영)\n`kemonomimi` : neko + fox + holo\n`meow` : 진짜 냥이\n`waifu` : 적절한 크기로 잘려진 냥이\n`tickle` : 간지럽히는 짤\n`feed` : 먹이주는 짤\n`poke` : 볼 찌르는 짤\n`slap` : 볼 때리는 짤\n`cuddle` : 부드럽게 안기는 짤\n`hug`: 격하게 안기는 짤\n`pat` : 쓰다듬는 짤", inline=False)
                        embed.add_field(name="분류: `nsfw`", value="이 분류의 태그는 **nsfw 등록이 되어있어야 사용이 가능합니다!**\n||`ero` : 일반적인 소녀 (기본)\n`eron` : 고양이\n`erofeet` : 발이 강조됨\n`lewd` : 고양이 소녀\n`keta` : ke-ta의 \n`yuri` : 백합\n`nsfw_avatar` : 프로필용\n`hentai` : 성관계\n`anal` : 후장 성관계\n`femdom` : 펨돔\n`solo` : 자위\n`pussy` : 성기 강조\n`tits` : 가슴 강조\n`smallboobs` : 빈유\n`feets` : 풋잡\n`classic` : 일반적인 성관계\n`trap` : 중성\n`futanari` : 제 손으로 못적겠어요 알아서 찾으세요\n`gasm` : 오르가즘 짤\n**__이 아래부턴 움짤__**\n`ngif` : 흔히 말하는 은꼴\n`hentaig` : 일반적 야함\n`nsfwg` : 고양이\n`solog` : 자위\n`pussyg` : 성기 강조\n`boobs` : 가슴 강조\n`pwankg` : 애무\n`feetg` : 발 강조\n`cum` : 사정||", inline=False)
                        embed.add_field(name="분류: `기타`", value="이 분류의 태그는 **nsfw 등록이 되어있어야 사용이 가능합니다!**\n`wallpaper` : 배경화면용 짤, nsfw짤도 포함됨.", inline=False)
                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                        await message.channel.send(embed=embed)
                        return None
                    waitmsg = await message.channel.send("<@%s>,\nAPI부터로의 응답을 기다리고 있습니다. 잠시만 기다려 주세요." % (message.author.id))
                    if message.channel.is_nsfw():
                        file = nsfw_neko(message, q)
                    else:
                        file = normal_neko(message, q)
                    if not file:
                        await waitmsg.delete()
                        await message.channel.send("<@%s>, 입력값이 유효하지 않습니다. 다시 시도 해 주세요." % (message.author.id))
                        return None
                    embed = discord.Embed(title="태그 : %s" % file[1], color=Setting.embed_color)
                    embed.set_image(url=file[0])
                    embed.set_footer(text="Powered By. nekos.life | Ver. %s | %s" % (Setting.version, Copyright))
                    await waitmsg.delete()
                    await message.channel.send("<@%s>," % (message.author.id), embed=embed)

                if message.content.startswith(prefix + '환영말'):
                    if message.author.guild_permissions.administrator or str(message.author.id) in Setting.owner_id:
                        result = welcome_message(message)
                        if not result:
                            await message.channel.send("<@%s>, 설정한 환영말이 없습니다!" % (message.author.id))
                        elif result == "Delete":
                            embed = discord.Embed(title="완료!", description="앞으로 유저 입장시 환영말이 뜨지 않습니다!", color=Setting.embed_color)
                            embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.guild.id, Setting.version, Copyright))
                            await message.channel.send(embed=embed)
                        elif result == "asdf":
                            await message.channel.send("<@%s>, 누락된 항목이 있습니다!" % (message.author.id))
                        else:
                            embed = discord.Embed(title="완료!", description="앞으로 이 채널에 환영말이 전송됩니다!", color=Setting.embed_color)
                            result = result.replace('[@유저]', '<@%s>' % (message.author.id))
                            result = result.replace('[@#유저]', '@%s#%s' % (message.author.name, message.author.discriminator))
                            result = result.replace('[유저이미지]', '%s' % (message.author.avatar_url))
                            result = result.replace('[@소유자]', '<@%s>' % (message.author.guild.owner.id))
                            result = result.replace('[@#소유자]', '@%s#%s' % (message.author.guild.owner.id, message.author.guild.owner.discriminator))
                            result = result.replace('[서버이름]', '%s' % (message.author.guild.name))
                            result = result.replace('[서버인원]', '%s' % (len(message.author.guild.members)))
                            result = result.replace('[서버이미지]', '<@%s>' % (message.author.guild.icon_url))
                            embed.add_field(name="설정한 환영말", value=result, inline=False)
                            embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.guild.id, Setting.version, Copyright))
                            await message.channel.send(embed=embed)
                    else:
                        await message.channel.send("<@%s>, 당신은 관리자 권한이 없습니다!" % (message.author.id))

                if message.content.startswith(prefix + '나가는말') or message.content.startswith(prefix + '떠나는말'):
                    if message.author.guild_permissions.administrator or str(message.author.id) in Setting.owner_id:
                        result = bye_message(message)
                        if result == False:
                            await message.channel.send("<@%s>, 설정한 나가는말이 없습니다!" % (message.author.id))
                        elif result == "Delete":
                            embed = discord.Embed(title="완료!", description="앞으로 유저 퇴장시 나가는말이 뜨지 않습니다!", color=Setting.embed_color)
                            embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.guild.id, Setting.version, Copyright))
                            await message.channel.send(embed=embed)
                        elif result == "asdf":
                            await message.channel.send("<@%s>, 누락된 항목이 있습니다!" % (message.author.id))
                        else:
                            embed = discord.Embed(title="완료!", description="앞으로 이 채널에 나가는말이 기록됩니다!", color=Setting.embed_color)
                            result = result.replace('[@유저]', '<@%s>' % (message.author.id))
                            result = result.replace('[@#유저]', '@%s#%s' % (message.author.name, message.author.discriminator))
                            result = result.replace('[유저이미지]', '%s' % (message.author.avatar_url))
                            result = result.replace('[@소유자]', '<@%s>' % (message.author.guild.owner.id))
                            result = result.replace('[@#소유자]', '@%s#%s' % (message.author.guild.owner.id, message.author.guild.owner.discriminator))
                            result = result.replace('[서버이름]', '%s' % (message.author.guild.name))
                            result = result.replace('[서버인원]', '%s' % (len(message.author.guild.members)))
                            result = result.replace('[서버이미지]', '<@%s>' % (message.author.guild.icon_url))
                            embed.add_field(name="설정한 나가는말", value=result, inline=False)
                            embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.guild.id, Setting.version, Copyright))
                            await message.channel.send(embed=embed)
                    else:
                        await message.channel.send("<@%s>, 당신은 관리자 권한이 없습니다!" % (message.author.id))

                if message.content.startswith(prefix + '접두사'):
                    if message.author.guild_permissions.administrator or str(message.author.id) in Setting.owner_id:
                        result = prefix_change(message)
                        if not result:
                            await message.channel.send("<@%s>, 해당 접두사는 오류가 발생 할 수 있어 사용 할 수 없습니다!" % (message.author.id))
                        else:
                            embed = discord.Embed(title="해당 서버의 접두사가 변경되었습니다!", description="접두사가 `%s`에서 `%s`으로 변경되었습니다!" % (prefix, message.content[5:6]), color=Setting.embed_color)
                            embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.guild.id, Setting.version, Copyright))
                            await message.channel.send(embed=embed)
                    else:
                        await message.channel.send("<@%s>, 당신은 관리자 권한이 없습니다!" % (message.author.id))

                if prefix + "핑" == message.content:
                    result = ping(message)
                    embed = discord.Embed(title="루탑봇 상태!", color=Setting.embed_color)
                    embed.add_field(name="서버 핑", value="`%sms`(%s)" % (result, ":large_blue_circle: 핑이 안정적입니다." if 0 < result < 400 else ":red_circle: 핑이 너무 높습니다." if result > 399 else ":question: 결과 도출 도중 문제가 발생했습니다."), inline=False)
                    embed.add_field(name="봇 업타임", value="https://status.develable.xyz/", inline=False)
                    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                    await message.channel.send("<@%s>, " % (message.author.id), embed=embed)

                if message.content.startswith(prefix + '잠수'):
                    imafk = message.content.replace(prefix + "잠수", "")
                    check = imafk.replace("\t", "")

                    if check == None or check == "" or check == " ":
                        imafk = "(없음)"

                    t = "%s-%s-%s %s:%s:%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second)

                    mysql_do("INSERT INTO `afk`(`user_id`, `since`, `reason`) VALUES (%s, '%s', '%s')" % (message.author.id, t, imafk))

                    embed = discord.Embed(title="잠수시작!", color=Setting.embed_color)
                    embed.add_field(name="대상 유저", value="<@%s>" % (message.author.id), inline=False)
                    embed.add_field(name="사유", value=imafk, inline=False)
                    embed.add_field(name="잠수 시작 시간", value=t, inline=True)
                    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                    await message.channel.send(embed=embed)

                if ("<@" in message.content and ">" in message.content) or ("<@" in message.content and ">" in message.content):
                    mention_id = re.findall(r'\d+', message.content)
                    mention_id = str(mention_id[0])
                    response = mysql_do_return("SELECT * FROM `afk` WHERE `user_id`=%s" % (mention_id))
                    if len(response) == 1:
                        embed = discord.Embed(title="잠수 상태!", color=Setting.embed_color)
                        embed.add_field(name="대상 유저", value="<@%s>" % (mention_id), inline=False)
                        embed.add_field(name="사유", value=response[0][2], inline=False)
                        embed.add_field(name="잠수 시작 시간", value=response[0][1], inline=True)
                        embed.add_field(name="현재 시간", value="%s-%s-%s %s:%s:%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second), inline=True)
                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                        await message.channel.send("<@%s>, 해당 유저는 현재 잠수 중 입니다!" % (message.author.id), embed=embed)

                if message.content.startswith(prefix + '트위터 '):
                    q = message.content.replace(prefix + '트위터 ', '')
                    q = q.replace(" ", "")
                    q = q.replace("\t", "")
                    
                    if q == "" or q == " " or q == None:
                        await message.channel.send("<@%s>, 누락된 항목이 있습니다!" % (message.author.id))
                        return None

                    data = requests.get("https://twitter.com/%s" % q)
                    status = data.status_code
                    if status == 404:
                        await message.channel.send("<@%s>, 존재하지 않는 유저로 추측됩니다. 입력값을 다시 한번 확인 해 주세요." % (message.author.id))
                    elif status != 200:
                        await message.channel.send("<@%s>, 서버의 일시적 다운으로 추측됩니다. 잠시 후 다시 시도 해 주세요." % (message.author.id))
                    else:
                        wait = await message.channel.send("<@%s>, 트위터에서 정보를 불러오고 있습니다. 잠시만 기다려 주세요." % (message.author.id))

                        soup = bs4(data.text, "html.parser")
                        results = str(soup.find_all('img', {'class' : 'ProfileAvatar-image'}))

                        split = results.split("src=")
                        image = str(split[1])
                        image = image.replace(""""/>]""", "")
                        image = image.replace(""""https://""", "")

                        split = results.split("alt=")
                        nickname = str(split[1])
                        nickname = nickname.replace('class="ProfileAvatar-image u-bgUserColor" src="https://%s"' % image, "")
                        nickname = nickname.replace('class="ProfileAvatar-image" src="https://%s"' % (image), "")
                        nickname = nickname.replace('class="ProfileAvatar-image " src="https://%s"' % (image), "")
                        nickname = nickname.replace("/>]", "")
                        nickname = nickname.replace("%22/%3E]", "")

                        embed = discord.Embed(title="%s님 트위터 최근 트윗" % (nickname), url="https://twitter.com/%s" % q, description="__**주의! 이 기능은 불안정합니다!**__\n**`최근 트윗`**은 **답글도 포함**합니다.", color=Setting.embed_color)
                        embed.set_thumbnail(url="https://%s" % (image))
                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))

                        response = await show_tweets(message, q, "5", "False", embed)

                        await wait.delete()
                        await message.channel.send("<@%s>," % (message.author.id), embed=embed)

                if message.content.startswith(prefix + '이미지'):
                    waitmsg = await message.channel.send("<@%s>,\nGoogle.co.kr 부터로의 응답을 기다리고 있습니다. 최장 10초가 소요됩니다." % (message.author.id))

                    q = message.content[5:]
                    if q == "" or q == " " or q == None:
                        await message.channel.send("<@%s>, 누락된 항목이 있습니다!" % (message.author.id))
                        return None

                    file = img_search(message, q)

                    await waitmsg.delete()
                    embed = discord.Embed(title="\"%s\"에 대한 검색 결과" % (message.content[5:]), color=Setting.embed_color)
                    embed.set_image(url=file)
                    embed.set_footer(text="Powered By. google.co.kr | Ver. %s | %s" % (Setting.version, Copyright))
                    await message.channel.send("<@%s>" % (message.author.id), embed=embed)

                if message.content == prefix + '시간':
                    hour = now.hour
                    if hour > 12:
                        hour = hour - 12

                    embed = discord.Embed(title="현재 서버 시간은 %s년 %s월 %s일 오전 %s시 %s분 %s초 입니다!" % (now.year, now.month, now.day, hour, now.minute, now.second), color=Setting.embed_color)
                    embed.set_footer(text="KST (GMT +09:00) | Ver. %s | %s" % (Setting.version, Copyright))
                    await message.channel.send(embed=embed)

                if message.content.startswith(prefix + '지우기'):
                    if message.author.guild_permissions.administrator or str(message.author.id) in Setting.owner_id:
                        if int(0) < int(message.content[5:]):
                            messages = []

                            async for m in message.channel.history(limit=int(message.content[5:])+1):
                                messages.append(m)

                            await message.channel.delete_messages(messages)

                            returnmsg = await message.channel.send(embed=discord.Embed(color=Setting.embed_color, title="%s개의 메세지를 삭제하였습니다." % (message.content[5:])))
                            await asyncio.sleep(3)
                            await returnmsg.delete()
                        else:
                            await message.channel.send("<@%s>, 지울 만큼의 메세지 수를 제대로 적어주세요!" % (message.author.id))
                    else:
                        await message.channel.send("<@%s>, 당신은 관리자 권한이 없습니다!" % (message.author.id))

            else:
                mysql_do("INSERT INTO `custom_command`(`server_id`, `total`) VALUES (%s, 5)" % (message.guild.id))
                mysql_do("INSERT INTO `and_so_on`(`server_id`, `prefix`) VALUES (%s, '%s')" % (message.guild.id, Setting.prefix))
                embed = discord.Embed(title="환영합니다!", description="해당 서버에 루탑봇이 자동적으로 활성화 되었습니다! 루탑봇 관련한 모든 기능을 사용하실 수 있습니다!", color=Setting.embed_color)
                embed.add_field(name="안내", value="기본 접두사는 `{prefix}` 이며, `{prefix}도움말`로 기본 명령어를 확인하세요!\n\n업데이트 공지를 수신하길 원하시나요?\n`{prefix}공지수신`을 입력하세요!".format(prefix=Setting.prefix))
                embed.add_field(name="링크", value="개인정보 처리방침 : https://develable.xyz/post/67\n이용약관 : https://develable.xyz/post/75\n루탑봇 웹패널 : https://rpanel.develable.xyz/")
                embed.add_field(name="문의", value="공식 홈페이지 : https://develable.xyz\n공식 지원서버 : https://invite.gg/develable\n디스코드 : HwaHyang - Official#8283\n공식 페이스북 : https://cutr.es/uwXnJ")
                embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.guild.id, Setting.version, Copyright))
                await message.channel.send(embed=embed)
        except discord.HTTPException as e:
            await http_error(message, e)
    except discord.HTTPException as e:
        try:
            await unknown_error(message, e)
        except discord.HTTPException:
            pass # 위에서 HTTPException 잡아서 출력하니까 여기서 HTTPException 애러나는데 왜나는지 모르겠음

app.run(Setting.token)
