# app.py - Updated with multiple endpoints and retry

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
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import threading

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# ============ KONFIGURASI ============
# Multiple endpoints untuk fallback
FREEFIRE_UPDATE_URLS = [
    "https://clientbp.ggblueshark.com/UpdateSocialBasicInfo",
    "https://clientbp.common.ggbluefox.com/UpdateSocialBasicInfo",
    "http://clientbp.ggblueshark.com/UpdateSocialBasicInfo",
    "http://clientbp.common.ggbluefox.com/UpdateSocialBasicInfo",
]

MAJOR_LOGIN_URLS = [
    "https://loginbp.ggblueshark.com/MajorLogin",
    "https://loginbp.common.ggbluefox.com/MajorLogin",
    "http://loginbp.ggblueshark.com/MajorLogin",
    "http://loginbp.common.ggbluefox.com/MajorLogin",
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

# ============ FUNGSI UTAMA ============
def encrypt_data(data_bytes):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    padded = pad(data_bytes, AES.block_size)
    return cipher.encrypt(padded)

def decode_jwt_info(token):
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        name = decoded.get("nickname")
        region = decoded.get("lock_region") or decoded.get("country_code", "")
        uid = decoded.get("account_id")
        return str(uid), name, region
    except Exception:
        return None, None, None

def upload_bio_request(jwt_token, bio_text, retry_count=3):
    """Upload bio dengan retry mechanism dan multiple endpoints"""
    
    if BioData is None:
        return {"status": "❌ Protobuf not loaded", "code": 500, "bio": bio_text}
    
    try:
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
        
        last_error = None
        
        # Try all endpoints with retry
        for endpoint in FREEFIRE_UPDATE_URLS:
            for attempt in range(retry_count):
                try:
                    resp = requests.post(
                        endpoint, 
                        headers=headers, 
                        data=encrypted, 
                        timeout=10,
                        verify=False
                    )
                    
                    status_text = "Unknown"
                    if resp.status_code == 200:
                        status_text = "✅ Success"
                        raw_hex = binascii.hexlify(resp.content).decode('utf-8')
                        return {
                            "status": status_text,
                            "code": resp.status_code,
                            "bio": bio_text,
                            "endpoint": endpoint,
                            "server_response": raw_hex,
                            "attempt": attempt + 1
                        }
                    elif resp.status_code == 401:
                        status_text = "❌ Unauthorized (Invalid JWT)"
                    else:
                        status_text = f"⚠️ Status {resp.status_code}"
                    
                    raw_hex = binascii.hexlify(resp.content).decode('utf-8')
                    return {
                        "status": status_text,
                        "code": resp.status_code,
                        "bio": bio_text,
                        "endpoint": endpoint,
                        "server_response": raw_hex,
                        "attempt": attempt + 1
                    }
                    
                except requests.exceptions.Timeout:
                    last_error = f"Timeout on {endpoint}"
                    continue
                except requests.exceptions.ConnectionError:
                    last_error = f"Connection error on {endpoint}"
                    continue
                except Exception as e:
                    last_error = str(e)
                    continue
                
                time.sleep(0.5)
        
        return {
            "status": f"❌ All endpoints failed: {last_error}",
            "code": 500,
            "bio": bio_text,
            "server_response": "N/A"
        }
        
    except Exception as e:
        return {
            "status": f"Error: {str(e)}", 
            "code": 500, 
            "bio": bio_text, 
            "server_response": "N/A"
        }

# ============ ROUTE ============
@app.route("/bio_upload", methods=["GET", "POST"])
def combined_bio_upload():
    bio = request.args.get("bio") or request.form.get("bio")
    jwt_token = request.args.get("jwt") or request.form.get("jwt")
    uid = request.args.get("uid") or request.form.get("uid")
    password = request.args.get("pass") or request.form.get("pass")
    access_token = request.args.get("access") or request.form.get("access")
    
    if not bio:
        return jsonify({
            "status": "❌ Error",
            "code": 400,
            "error": "Missing 'bio' parameter",
            "usage": {
                "jwt": "/bio_upload?bio=Hello&jwt=YOUR_JWT",
                "uid_pass": "/bio_upload?bio=Hello&uid=UID&pass=PASSWORD",
                "access": "/bio_upload?bio=Hello&access=ACCESS_TOKEN"
            }
        }), 400
    
    final_jwt = jwt_token
    login_method = "Direct JWT"
    final_name = None
    final_uid = None
    final_region = None
    
    # Decode info dari JWT
    if final_jwt:
        uid_from_jwt, name_from_jwt, region_from_jwt = decode_jwt_info(final_jwt)
        final_uid = uid_from_jwt
        final_name = name_from_jwt
        final_region = region_from_jwt
    
    if not final_jwt:
        return jsonify({
            "status": "❌ JWT Required",
            "code": 400,
            "error": "Please provide a valid JWT token"
        }), 400
    
    # Upload bio
    result = upload_bio_request(final_jwt, bio)
    
    response_data = {
        "Credit": "sulav_codex_ff",
        "Join For More": "Telegram: @sulav_don2",
        "status": result["status"],
        "login_method": login_method,
        "code": result["code"],
        "bio": result["bio"],
        "uid": final_uid,
        "name": final_name,
        "region": final_region,
        "server_response": result.get("server_response", "N/A"),
        "endpoint_used": result.get("endpoint", "N/A"),
        "attempt": result.get("attempt", 0),
        "generated_jwt": final_jwt
    }

    response = make_response(jsonify(response_data))
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Free Fire Bio Upload API",
        "endpoints": {
            "/bio_upload": "Upload bio (GET/POST)",
            "/": "This info page"
        },
        "usage": {
            "method_jwt": "/bio_upload?bio=YourBio&jwt=YOUR_JWT"
        },
        "example": "/bio_upload?bio=Hello+World&jwt=YOUR_JWT",
        "Credit": "sulav_codex_ff",
        "Telegram": "@sulav_don2"
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
