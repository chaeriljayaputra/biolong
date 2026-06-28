import asyncio
import json
import random
import ssl
from datetime import datetime

import aiohttp
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import runtime_version as _runtime_version
from google.protobuf.internal import builder as _builder

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


def random_ua():
    versions = ['4.0.18P6', '4.0.19P7', '4.1.0P3', '5.0.1B2', '5.2.5P3', '5.3.2P2', '5.4.3B2', '5.5.2P3']
    models = ['SM-A125F', 'POCO M3', 'Redmi 9A', 'RMX2185', 'moto g(9) play', 'ASUS_Z01QD', 'OnePlus Nord']
    android = random.choice(['9', '10', '11', '12', '13'])
    lang = random.choice(['en-US', 'hi-IN', 'pt-BR', 'id-ID'])
    country = random.choice(['USA', 'IND', 'BRA', 'IDN'])
    return f"GarenaMSDK/{random.choice(versions)}({random.choice(models)};Android {android};{lang};{country};)"


def aes_encrypt(data):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    return cipher.encrypt(pad(data, AES.block_size))


def aes_decrypt(data):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    return unpad(cipher.decrypt(data), AES.block_size)


async def get_garena_tokens(uid, password):
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

    async with aiohttp.ClientSession() as session:
        async with session.post(GARENA_OAUTH_URL, headers=headers, data=payload) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Garena OAuth failed — HTTP {resp.status}")
            body = await resp.json()

    open_id = body.get("open_id")
    access_token = body.get("access_token")

    if not open_id or not access_token:
        raise RuntimeError(f"Missing tokens in response: {body}")

    return {"open_id": open_id, "access_token": access_token}


def build_major_login_payload(open_id, access_token):
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

    return aes_encrypt(ml.SerializeToString())


async def major_login(encrypted_payload):
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        async with session.post(MAJORLOGIN_URL, data=encrypted_payload, headers=HTTP_HEADERS, ssl=ssl_ctx) as resp:
            if resp.status != 200:
                raise RuntimeError(f"MajorLogin failed — HTTP {resp.status}")
            raw = await resp.read()

    proto = MajorLoginRes()
    proto.ParseFromString(raw)

    return {
        "token": proto.token,
        "region": proto.region,
        "url": proto.url,
        "tcp_key": proto.key.hex() if proto.key else None,
        "tcp_iv": proto.iv.hex() if proto.iv else None,
    }


async def generate_jwt_from_access_token(open_id, access_token):
    encrypted = build_major_login_payload(open_id, access_token)
    return await major_login(encrypted)


async def generate_jwt_from_credentials(uid, password):
    oauth = await get_garena_tokens(uid, password)
    login_res = await generate_jwt_from_access_token(oauth["open_id"], oauth["access_token"])
    return {"open_id": oauth["open_id"], "access_token": oauth["access_token"], **login_res}


def save_token(result, filepath="token.json"):
    token_data = {
        "open_id": result.get("open_id"),
        "access_token": result.get("access_token"),
        "jwt_token": result.get("token"),
        "region": result.get("region"),
        "url": result.get("url"),
    }
    with open(filepath, "w") as f:
        json.dump(token_data, f, indent=2)
    return filepath


async def run():
    print()
    print("╔═══════════════════════════════════════════════╗")
    print("║     Free Fire JWT / Access Token Generator    ║")
    print("╚═══════════════════════════════════════════════╝")
    print()

    print("Select input mode:")
    print("  [1] Guest UID + Password  (full pipeline)")
    print("  [2] Access Token + Open ID (skip OAuth step)")
    print()
    mode = input("Enter choice (1/2): ").strip()

    if mode == "2":
        open_id = input("Enter Open ID      : ").strip()
        access_token = input("Enter Access Token : ").strip()

        print("\n[1/2] Building & encrypting MajorLogin payload...")
        result = await generate_jwt_from_access_token(open_id, access_token)
        result["open_id"] = open_id
        result["access_token"] = access_token
    else:
        uid = input("Enter Guest UID      : ").strip()
        password = input("Enter Guest Password : ").strip()

        print("\n[1/3] Requesting Garena OAuth tokens...")
        oauth = await get_garena_tokens(uid, password)
        print(f"      ✔  open_id      = {oauth['open_id']}")
        print(f"      ✔  access_token = {oauth['access_token'][:30]}...")

        print("\n[2/3] Building & encrypting MajorLogin payload...")
        print("\n[3/3] Calling MajorLogin endpoint...")
        result = await generate_jwt_from_credentials(uid, password)

    print()
    print("╔═══════════════════════════════════════════════╗")
    print("║                  RESULTS                      ║")
    print("╠═══════════════════════════════════════════════╣")
    print(f"  Open ID       : {result.get('open_id', 'N/A')}")
    print(f"  Access Token  : {result.get('access_token', 'N/A')}")
    print(f"  JWT Token     : {result.get('token', 'N/A')}")
    print(f"  Region        : {result.get('region', 'N/A')}")
    print(f"  Server URL    : {result.get('url', 'N/A')}")
    print(f"  TCP Key (hex) : {result.get('tcp_key', 'N/A')}")
    print(f"  TCP IV  (hex) : {result.get('tcp_iv', 'N/A')}")
    print("╚═══════════════════════════════════════════════╝")
    print()

    path = save_token(result)
    print(f"✔  Saved to {path}")
    print()

    return result


def get_jwt_sync(uid, password):
    return asyncio.run(generate_jwt_from_credentials(uid, password))


def get_jwt_from_token_sync(open_id, access_token):
    return asyncio.run(generate_jwt_from_access_token(open_id, access_token))


if __name__ == "__main__":
    asyncio.run(run())
    