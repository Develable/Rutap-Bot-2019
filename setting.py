# -*- coding: utf-8 -*- 

##########################################################
#              Rutap Bot 2019 Setting Module             #
#                 Under The MIT License                  #
##########################################################

"""
    [여는 말]
    저희 팀의 소스를 사용 해 주셔서 감사합니다!
    저희 소스의 라이선스는 MIT License 로써, 반드시 라이선스와 저작권 고지를 하셔야 합니다.
    언제든지 문의사항이 있으시면 아래 연락처로 연락 부탁드립니다!
    Discord Server :: https://invite.gg/rutapbot
    Discord DM :: @HwaHyang - Official#8283
    E-Mail :: hwahyang@adh.kro.kr

    [접두사(self.prefix) 권장사항]
    01. 접두사는 '한글자'로 해주세요. (루탑봇의 접두사에 맞게 설정을 하였기에, 두글자 이상으로 하시면 rutap.py 전체를 수정하셔야 합니다.)
    02. `는 되도록이면 접두사에 넣지 말아주세요.

    [봇 관리자 설정(self.owner_id) 유의사항]
    01. 봇 관리자가 두명 이상인 경우, 공백으로 유저를 구분합니다. (EX - "357857022974230538 440501082720960522")

    [온라인 알림 채널 설정(self.online_notice_channel) 안내]
    01. 봇이 온라인임을 5분마다 전송할 채널 ID를 넣어주세요.

    [애러 로깅 채널(self.err_log_channel) 안내]
    01. 오류가 발생했을 경우, 에러 로그가 보내질 채널 ID를 넣어주세요.

    [저작권 고지(self.copy) 안내]
    01. 도움말 같은 모든 명령어 하단에 들어가는 "© 2018-2019 Develable"을 의미합니다.

    [임베드 색상 설정(self.embed_color) 안내]
    01. 임베드 좌측 막대기(?)의 색상을 정할 수 있습니다.
    02. (0x) + (#을 제외한 Hex코드) 의 형식으로 입력 해 주세요.

    [Mysql 관련 안내]
    01. 루탑봇 20190602r 버전부터 새로이 도입되는 "웹 패널"을 위해 모든 데이터를 mysql로 이전하였습니다.
    02. 웹 패널은 저희 측에서 소스를 공개하지 않으므로, 참고하시기 바랍니다.
    03. mysql table 관련한 설정은 github를 참고하세요.

    [API 타입 (self.api_type) 안내]
    01. 기본값은 'naver' 입니다.
    02. 'cutress'를 입력하실 경우, cutress(https://cutr.es) API를 이용하실 수 있습니다.
    03. API의 ID와 비밀번호는 네이버 입력란에 기재 바랍니다.
    04. 다만, 현재까지는 cutress에서 API를 제공하지 않고 있으니 참고 부탁드립니다.

    [API 관련 안내]
    01. API 발급 방법에 대하여는 별도로 저희측에서 설명해드리지 않습니다.
    02. API 발급 & 관리에 대하여는 아래 사이트를 참고하세요
    03. 트위터 API :: https://developer.twitter.com/
    04. 네이버 API :: https://developers.naver.com/

    [공지 모듈 관련 안내]
    01. allow_keyword가 공지를 보낼 채널 키워드를 의미합니다. 공백으로 키워드 구분합니다.
    02. disallow_keyword는 공지를 보내지 않을 채널 키워드를 의미합니다. 공백으로 키워드 구분합니다.
    04. autochannel_name은 해당 키워드가 있는 채널을 발견하지 못할 시, 자동으로 공지채널을 만들때 채널명을 의미합니다.
    05. autochannel_notice는 해당 키워드가 있는 채널을 발견하지 못할 시, 자동으로 공지채널을 만들고 안내 메시지를 보낼 내용을 적습니다.

    [보안 모듈 관련 안내]
    01. 루탑봇의 20190602r 버전부터 보안을 위해 일부 파일에 대해 암호화를 진행합니다. byte 타입의 키가 없으면 암호화도, 복호화도 진행할 수 없습니다.
    02. security_key에 byte 타입의 키를 넣어주세요.
    03. key 생성방법 :: os.urandom(64)

    [참고하세요]
    01. 모든 구문 파일에서 "외부 소스 사용함" 이라는 주석이 달려져 있는 구문은 다른 소스의 구문이 일부 포함된 구문입니다. 해당 구문은 저희 라이선스와 별개로 적용이 되오니, 반드시 원 레포지토리를 찾아가서 라이선스를 확인하시기 바랍니다. (모든 구문 출처는 정보에 명시되어 있습니다.)
"""

import datetime

class Settings:
    def __init__(self):
        # Basic Setting #
        self.token = "token"
        self.prefix = "/"
        self.version = "Version"
        self.copy = "© %s Your Company" % datetime.datetime.now().year

        # log/filename #
        self.log_file = "msg_log.rtl"

        # Categorized by space (Ex. 000000001 000000002) #
        self.owner_id = "owner_id"

        # str Channel name #
        self.online_notice_channel = "channel_id"
        self.err_log_channel = "channel_id"

        # 0x + Hex CODE 6 Digits #
        self.embed_color = 0xb2ebf4
        self.error_embed_color = 0xff0000

        # url shorter API #
        self.api_type = 'naver'

        # Twitter API #
        self.twitter_api_key = "key"
        self.twitter_api_secret = "secret"
        self.twitter_access_token = "token"
        self.twitter_access_secret = "secret"

        # Naver API #
        self.naver_api_id = "id"
        self.naver_api_secret = "secret"

        # Notice Module #
        self.allow_keyword = ["notice", "공지", "알림", "announcement", "Team-화공", "Develable"]
        self.disallow_keyword = ["경고", "warn"]
        self.autochannel_name = "Develable-공지-자동생성됨"
        self.autochannel_notice = "__**공지채널을 발견하지 못하여 공지채널을 자동으로 생성하였습니다.**__\n자세한 내용은 봇 관리자에게 문의해주세요 : https://invite.gg/Develable"

        # Security Module #
        self.security_key = b''

        # Mysql info #
        self.mysql_ip = "ip"
        self.mysql_id = "id"
        self.mysql_pw = "pw"
        self.mysql_db = "db"

# ------ Don't touch from here ----- #

import ctypes

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]

    def __init__(self):
        self.dwLength = ctypes.sizeof(self)
        super(MEMORYSTATUSEX, self).__init__()