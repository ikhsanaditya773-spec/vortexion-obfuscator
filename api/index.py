from flask import Flask, render_template_string, request
import random
import re
from datetime import datetime, date

app = Flask(__name__)

# Header ASCII Art khas VORTEXION
ASCII_ART_VORTEXION = r"""--[[
VVV            VVV  OOOOOOO   RRRRRRRRRR TTTTTTTTTTTEEEEEEEEEE XXXXX      XXXXX I  OOOOOOO  NNNN   NNNN
 VVV          VVV OOOOOOOOOOO RRRRRRRRRRRTTTTTTTTTTTEEEEEEEEEE  XXXXX    XXXXX  I OOOOOOOOOOO NNNN   NNNN
  VVV        VVV OOOOO   OOOOO RRR     RRR   TTTT   EEE           XXXXX  XXXXX   I OOOOO   OOOOONNNNN  NNNN
   VVV      VVV  OOOO     OOOO RRRRRRRRRRR   TTTT   EEEEEEEE       XXXXXXXXXX    I OOOO     OOOONNNNNN NNNN
    VVV    VVV   OOOO     OOOO RRRRRRRRRR    TTTT   EEEEEEEE        XXXXXXXX     I OOOO     OOOONNN NNNNNNN
     VVV  VVV    OOOOO   OOOOO RRR   RRRR    TTTT   EEE            XXXXX  XXXXX  I OOOOO   OOOOONNN  NNNNNN
      VVVVVV      OOOOOOOOOOO RRR    RRRR   TTTT   EEEEEEEEEE   XXXXX    XXXXX  I OOOOOOOOOOO NNN   NNNNN
       VVVV        OOOOOOO   RRR     RRRR  TTTT   EEEEEEEEEE  XXXXX      XXXXXI  OOOOOOO  NNN    NNNN

      << VORTEXION NATIVE OBFUSCATOR (UNIVERSAL & DAILY LIMIT) >>
]]--"""

# MASUKKAN LINK DISCORD KELOMPOK / COMMUNITY KAMU DI SINI
DISCORD_INVITE_URL = "https://discord.gg/vortexior"  # Ganti dengan link Discord kamu!

VALID_KEYS = ["VORTEXION-VIP-2026", "REMI-PREMIUM-KEY", "VORTEX-PRO"]

# System Tracking Daily Limit
user_usage_tracker = {}

def generate_var():
    chars = "lI1O0_v"
    return "_" + ''.join(random.choices(chars, k=14))

def safe_encrypt_string(text, key):
    text = text.encode('utf-8', 'ignore').decode('utf-8')
    bytes_list = []
    for c in text:
        byte_val = (ord(c) ^ key) % 256
        bytes_list.append(str(byte_val))
    return "{" + ",".join(bytes_list) + "}"

def obfuscate_native_safe(lua_code):
    if not lua_code.strip():
        return ""

    xor_key = random.randint(11, 230)
    
    v_decrypt = generate_var()
    v_bytes = generate_var()
    v_key = generate_var()
    v_i = generate_var()
    v_res = generate_var()

    clean_code = re.sub(r'--\[\[[\s\S]*?\]\]', '', lua_code)
    clean_code = re.sub(r'--.*$', '', clean_code, flags=re.MULTILINE)

    def string_replacer(match):
        raw_str = match.group(0)[1:-1]
        if not raw_str:
            return '""'
        encrypted_array = safe_encrypt_string(raw_str, xor_key)
        return f'{v_decrypt}({encrypted_array})'

    obfuscated_code = re.sub(r'"([^"\\]*(\\.[^"\\]*)*)"|\'([^\'\\]*(\\.[^\'\\]*)*)\'', string_replacer, clean_code)

    lines = [line.strip() for line in obfuscated_code.splitlines() if line.strip()]
    raw_joined = " ".join(lines)
    
    cleaned_joined = re.sub(r';\s*;+', ';', raw_joined)
    cleaned_joined = re.sub(r'^\s*;+', '', cleaned_joined)

    one_liner_lua = f"local {v_key}={xor_key};local function {v_decrypt}({v_bytes}) local {v_res}={{}} for {v_i}=1,#{v_bytes} do local b=bit32.bxor({v_bytes}[{v_i}],{v_key})%256 {v_res}[{v_i}]=string.char(b) end return table.concat({v_res}) end return (function() {cleaned_joined} end)()"

    return f"{ASCII_ART_VORTEXION}\n{one_liner_lua}"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VORTEXION - Native Obfuscator</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d1117; color: #c9d1d9; margin: 0; padding: 20px; }
        .container { max-width: 1050px; margin: 0 auto; }
        
        .header-box { text-align: center; margin-bottom: 25px; }
        h1 { color: #58a6ff; font-size: 30px; margin-bottom: 5px; text-shadow: 0 0 10px rgba(88, 166, 255, 0.3); }
        .subtitle { color: #8b949e; font-size: 14px; margin-bottom: 15px; }
        
        /* Tombol Discord */
        .discord-btn { display: inline-flex; align-items: center; gap: 8px; background-color: #5865F2; color: white; padding: 8px 18px; border-radius: 20px; text-decoration: none; font-weight: bold; font-size: 13px; transition: 0.2s; box-shadow: 0 4px 10px rgba(88, 101, 242, 0.3); }
        .discord-btn:hover { background-color: #4752C4; transform: translateY(-2px); }

        .editor-container { display: flex; gap: 20px; margin-top: 10px; flex-wrap: wrap; }
        .box { flex: 1; min-width: 320px; display: flex; flex-direction: column; }
        label { font-weight: bold; margin-bottom: 8px; color: #58a6ff; }
        textarea { width: 100%; height: 360px; background-color: #161b22; color: #7ee787; border: 1px solid #30363d; border-radius: 8px; padding: 12px; font-family: 'Courier New', Courier, monospace; font-size: 13px; box-sizing: border-box; resize: vertical; white-space: pre-wrap; word-break: break-all; }
        textarea:focus { outline: 1px solid #58a6ff; }
        
        .action-btns { display: flex; gap: 10px; margin-top: 10px; }
        .btn-secondary { flex: 1; padding: 10px; background-color: #21262d; color: #c9d1d9; border: 1px solid #30363d; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s; }
        .btn-secondary:hover { background-color: #30363d; color: #fff; }

        .key-container { margin-top: 20px; background-color: #161b22; padding: 15px; border-radius: 8px; border: 1px solid #30363d; display: flex; gap: 15px; align-items: center; }
        .key-container label { color: #d2a8ff; margin: 0; white-space: nowrap; }
        .key-container input { flex: 1; padding: 10px 14px; background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: white; font-size: 14px; }
        .key-container input:focus { outline: 1px solid #d2a8ff; }

        button.btn-main { margin-top: 15px; padding: 15px; background-color: #238636; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; width: 100%; transition: 0.2s; box-shadow: 0 4px 12px rgba(35, 134, 54, 0.3); }
        button.btn-main:hover { background-color: #2ea043; }
        
        .status-msg { text-align: center; margin-top: 15px; font-weight: bold; font-size: 14px; color: #f85149; background: rgba(248, 81, 73, 0.1); padding: 12px; border-radius: 6px; border: 1px solid rgba(248, 81, 73, 0.3); }
        .info-msg { text-align: center; margin-top: 15px; font-weight: bold; font-size: 14px; color: #7ee787; background: rgba(46, 160, 67, 0.1); padding: 12px; border-radius: 6px; border: 1px solid rgba(46, 160, 67, 0.3); }
        
        .discord-link-inline { color: #5865F2; text-decoration: underline; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-box">
            <h1>⚡ VORTEXION OBFUSCATOR ⚡</h1>
            <div class="subtitle">🔒 Universal Roblox Support (Limit: Free 1x/Hari | VIP Unlimited)</div>
            <a href="{{ discord_url }}" target="_blank" class="discord-btn">
                <svg width="18" height="18" viewBox="0 0 127.14 96.36" fill="white"><path d="M107.7,8.07A105.15,105.15,0,0,0,81.47,0a72.06,72.06,0,0,0-3.36,6.83A97.68,97.68,0,0,0,49,6.83,72.37,72.37,0,0,0,45.64,0,105.89,105.89,0,0,0,19.39,8.09C2.79,32.65-1.71,56.6.54,80.21h0A105.73,105.73,0,0,0,32.71,96.36,77.7,77.7,0,0,0,39.6,85.25a68.42,68.42,0,0,1-10.85-5.18c.91-.66,1.8-1.34,2.66-2a73.51,73.51,0,0,0,64.32,0c.87.69,1.76,1.37,2.66,2a68.68,68.68,0,0,1-10.87,5.19,77,77,0,0,0,6.89,11.1,105.25,105.25,0,0,0,32.19-16.14c2.64-27.38-4.51-51.11-18.91-72.12ZM42.45,65.69C36.18,65.69,31,60,31,53s5-12.74,11.43-12.74C48.86,40.21,54,45.92,53.86,53,53.86,60,48.78,65.69,42.45,65.69Zm42.24,0C78.41,65.69,73.25,60,73.25,53s5.08-12.74,11.44-12.74C91.13,40.21,96.2,45.92,96.07,53,96.07,60,91,65.69,84.69,65.69Z"/></svg>
                Join Discord VORTEXION
            </a>
        </div>

        <form method="POST">
            <div class="editor-container">
                <div class="box">
                    <label>📝 Script Roblox Asli (Input):</label>
                    <textarea name="input_code" placeholder="Paste Script, LocalScript, atau ModuleScript kamu di sini...">{{ input_code }}</textarea>
                </div>
                <div class="box">
                    <label>🛡️ Hasil Obfuscation (Output):</label>
                    <textarea id="outputCode" readonly placeholder="Hasil protection akan muncul di sini...">{{ output_code }}</textarea>
                    <div class="action-btns">
                        <button type="button" class="btn-secondary" onclick="copyOutput()">📋 Salin Script (Copy Output)</button>
                    </div>
                </div>
            </div>

            <div class="key-container">
                <label>🔑 Key Premium VIP:</label>
                <input type="text" name="access_key" placeholder="Kosongkan jika Free User (1x per hari)..." value="{{ access_key }}">
            </div>

            <button type="submit" class="btn-main">🛡️ Obfuscate Script</button>
        </form>

        {% if error %}
            <div class="status-msg">
                {{ error|safe }}
            </div>
        {% elif info %}
            <div class="info-msg">{{ info }}</div>
        {% endif %}
    </div>

    <script>
        function copyOutput() {
            const outputText = document.getElementById("outputCode");
            if (!outputText.value.trim()) return alert("Belum ada kode untuk disalin!");
            navigator.clipboard.writeText(outputText.value);
            alert("✅ Hasil Obfuscation berhasil disalin!");
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    input_code = ""
    output_code = ""
    access_key = ""
    error = None
    info = None

    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if user_ip and ',' in user_ip:
        user_ip = user_ip.split(',')[0].strip()

    today = date.today()

    if request.method == "POST":
        input_code = request.form.get("input_code", "")
        access_key = request.form.get("access_key", "").strip()

        is_vip = access_key in VALID_KEYS

        if access_key and not is_vip:
            error = f"❌ Kode Key Premium tidak valid! Minta Key VIP gratis di <a href='{DISCORD_INVITE_URL}' target='_blank' class='discord-link-inline'>Discord VORTEXION</a>."
        else:
            if not is_vip:
                last_used_date = user_usage_tracker.get(user_ip)
                if last_used_date == today:
                    error = f"⚠️ Jatah gratis harian kamu sudah habis (1x/hari)! Dapatkan Key VIP di <a href='{DISCORD_INVITE_URL}' target='_blank' class='discord-link-inline'>Discord VORTEXION</a> untuk penggunaan tanpa batas."
                else:
                    output_code = obfuscate_native_safe(input_code)
                    user_usage_tracker[user_ip] = today
                    info = "✅ Berhasil obfuscate! (Jatah gratis hari ini digunakan)"
            else:
                output_code = obfuscate_native_safe(input_code)
                info = "⚡ Berhasil obfuscate dengan VIP Access (Unlimited)!"

    return render_template_string(
        HTML_TEMPLATE, 
        input_code=input_code, 
        output_code=output_code, 
        access_key=access_key,
        error=error,
        info=info,
        discord_url=DISCORD_INVITE_URL
    )

app = app
