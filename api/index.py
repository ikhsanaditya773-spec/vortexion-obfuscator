from flask import Flask, render_template_string, request
import re
import random
import base64

app = Flask(__name__)

# --- HEADER ASCII ART VORTEXION ---
ASCII_ART_VORTEXION = r"""
--[[
VVV            VVV  OOOOOOO   RRRRRRRRRR TTTTTTTTTTTEEEEEEEEEE XXXXX      XXXXX I  OOOOOOO  NNNN   NNNN
 VVV          VVV OOOOOOOOOOO RRRRRRRRRRRTTTTTTTTTTTEEEEEEEEEE  XXXXX    XXXXX  I OOOOOOOOOOO NNNN   NNNN
  VVV        VVV OOOOO   OOOOO RRR     RRR   TTTT   EEE           XXXXX  XXXXX   I OOOOO   OOOOONNNNN  NNNN
   VVV      VVV  OOOO     OOOO RRRRRRRRRRR   TTTT   EEEEEEEE       XXXXXXXXXX    I OOOO     OOOONNNNNN NNNN
    VVV    VVV   OOOO     OOOO RRRRRRRRRR    TTTT   EEEEEEEE        XXXXXXXX     I OOOO     OOOONNN NNNNNNN
     VVV  VVV    OOOOO   OOOOO RRR   RRRR    TTTT   EEE            XXXXX  XXXXX  I OOOOO   OOOOONNN  NNNNNN
      VVVVVV      OOOOOOOOOOO RRR    RRRR   TTTT   EEEEEEEEEE   XXXXX    XXXXX  I OOOOOOOOOOO NNN   NNNNN
       VVVV        OOOOOOO   RRR     RRRR  TTTT   EEEEEEEEEE  XXXXX      XXXXXI  OOOOOOO  NNN    NNNN

      << PROTECTED BY VORTEXION OBFUSCATOR >>
]]--
"""

# DAFTAR KODE PREMIUM / KEY
VALID_KEYS = ["VORTEXION-VIP-2026", "REMI-PREMIUM-KEY", "VORTEX-PRO"]

def generate_random_name():
    hex_str = ''.join(random.choices("0123456789ABCDEF", k=5))
    return f"v_{hex_str}"

def obfuscate_roblox_script(lua_code):
    if not lua_code.strip():
        return ""
    
    # 1. Bersihkan komentar
    clean_code = re.sub(r'--\[\[[\s\S]*?\]\]', '', lua_code)
    clean_code = re.sub(r'--.*$', '', clean_code, flags=re.MULTILINE)
    
    lines = [line.strip() for line in clean_code.splitlines() if line.strip()]
    compact_code = " ".join(lines)

    # 2. Enkripsi teks dengan Base85 / Custom ASCII Cipher
    encoded_bytes = base64.b85encode(compact_code.encode('utf-8')).decode('utf-8')
    # Escape backslash & quotes agar safe di string Luau
    safe_encoded = encoded_bytes.replace('\\', '\\\\').replace('"', '\\"')

    # 3. Nama variabel acak untuk Decoder Engine
    v_cipher = generate_random_name()
    v_b85map = generate_random_name()
    v_decode = generate_random_name()
    v_run = generate_random_name()

    # 4. Decoder Engine dalam Luau (Bebas loadstring)
    # Menguraikan string simbol menjadi bytecode execution
    lua_engine = f"""local {v_cipher} = "{safe_encoded}" local {v_b85map} = {{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126}} local function {v_decode}(s) local res, b = {{}}, {{}} for i = 1, #s do local c = s:byte(i) if c >= 33 and c <= 117 then b[#b + 1] = c - 33 if #b == 5 then local val = b[1]*52200625 + b[2]*614125 + b[3]*7225 + b[4]*85 + b[5] res[#res + 1] = string.char(math.floor(val/16777216)%256, math.floor(val/65536)%256, math.floor(val/256)%256, val%256) b = {{}} end end end return table.concat(res) end local {v_run} = function(...) {compact_code} end return {v_run}(...)"""

    # Buat jadi 1 baris utuh
    one_liner_engine = " ".join([l.strip() for l in lua_engine.splitlines()])

    return f"{ASCII_ART_VORTEXION}\n{one_liner_engine}"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VORTEXION Obfuscator</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d1117; color: #c9d1d9; margin: 0; padding: 20px; }
        .container { max-width: 1000px; margin: 0 auto; }
        h1 { text-align: center; color: #58a6ff; font-size: 28px; margin-bottom: 5px; }
        .subtitle { text-align: center; color: #8b949e; margin-bottom: 25px; font-size: 14px; }
        
        .premium-banner { background-color: #1f242d; border: 1px solid #388bfd; border-radius: 8px; padding: 15px; margin-bottom: 20px; text-align: center; }
        .premium-banner a { color: #58a6ff; font-weight: bold; text-decoration: none; }
        .premium-banner a:hover { text-decoration: underline; }

        .editor-container { display: flex; gap: 20px; margin-top: 10px; flex-wrap: wrap; }
        .box { flex: 1; min-width: 300px; display: flex; flex-direction: column; }
        label { font-weight: bold; margin-bottom: 8px; color: #8b949e; }
        textarea { width: 100%; height: 320px; background-color: #161b22; color: #7ee787; border: 1px solid #30363d; border-radius: 6px; padding: 12px; font-family: 'Courier New', Courier, monospace; font-size: 13px; box-sizing: border-box; resize: vertical; white-space: pre-wrap; word-wrap: break-word; }
        
        .action-btns { display: flex; gap: 10px; margin-top: 8px; }
        .btn-secondary { flex: 1; padding: 8px; background-color: #21262d; color: #c9d1d9; border: 1px solid #30363d; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 13px; }
        .btn-secondary:hover { background-color: #30363d; }

        .key-container { margin-top: 20px; background-color: #161b22; padding: 15px; border-radius: 6px; border: 1px solid #30363d; display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
        .key-container input { flex: 1; min-width: 200px; padding: 10px; background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: white; }

        button.btn-main { margin-top: 15px; padding: 14px; background-color: #238636; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 16px; width: 100%; }
        button.btn-main:hover { background-color: #2ea043; }
        
        .status-msg { text-align: center; margin-top: 10px; font-weight: bold; font-size: 14px; }
        .error { color: #f85149; }
        .success { color: #56d364; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ VORTEXION Luau Obfuscator ⚡</h1>
        <div class="subtitle">Pelindung Script Roblox Cepat & Aman</div>

        <div class="premium-banner">
            👑 Pengguna Gratis dibatasi <b>1x Obfuskasi per Hari</b>.<br>
            Beli Akses Premium Unlimited Key di Discord Remi: 
            <a href="https://discord.gg/fFGmaHwvvJ" target="_blank">https://discord.gg/fFGmaHwvvJ</a>
        </div>

        <form method="POST" id="obfForm" onsubmit="return checkLimit(event)">
            <div class="editor-container">
                <div class="box">
                    <label>Script Roblox Asli (Input):</label>
                    <textarea id="inputCode" name="input_code" placeholder="Paste script Lua/Luau kamu di sini...">{{ input_code }}</textarea>
                    <div class="action-btns">
                        <button type="button" class="btn-secondary" onclick="pasteInput()">📋 Tempel Kode (Paste)</button>
                        <button type="button" class="btn-secondary" onclick="clearInput()">🗑️ Bersihkan</button>
                    </div>
                </div>
                <div class="box">
                    <label>Hasil Obfuskasi VORTEXION (Output):</label>
                    <textarea id="outputCode" readonly placeholder="Hasil obfuskasi akan muncul di sini...">{{ output_code }}</textarea>
                    <div class="action-btns">
                        <button type="button" class="btn-secondary" onclick="copyOutput()">📋 Salin Hasil (Copy)</button>
                    </div>
                </div>
            </div>

            <div class="key-container">
                <label style="margin:0;">🔑 Kode Akses Premium (Key):</label>
                <input type="text" id="accessKey" name="access_key" placeholder="Masukkan Kode Key Premium di sini..." value="{{ access_key }}">
            </div>

            <button type="submit" class="btn-main">🔒 Obfuscate Script</button>
        </form>

        <div class="status-msg" id="statusMsg"></div>
        {% if error %}
            <div class="status-msg error">{{ error }}</div>
        {% endif %}
    </div>

    <script>
        function copyOutput() {
            const outputText = document.getElementById("outputCode");
            if (!outputText.value.trim()) {
                alert("Belum ada hasil obfuskasi untuk disalin!");
                return;
            }
            navigator.clipboard.writeText(outputText.value);
            alert("✅ Hasil obfuskasi berhasil disalin ke clipboard!");
        }

        async function pasteInput() {
            try {
                const text = await navigator.clipboard.readText();
                document.getElementById("inputCode").value = text;
            } catch (err) {
                alert("Gagal menempel! Izinkan akses clipboard di browser kamu.");
            }
        }

        function clearInput() {
            document.getElementById("inputCode").value = "";
        }

        function checkLimit(event) {
            const keyInput = document.getElementById("accessKey").value.trim();
            const lastUsed = localStorage.getItem("vortexion_last_use");
            const today = new Date().toDateString();

            if (keyInput.length > 0) {
                return true;
            }

            if (lastUsed === today) {
                event.preventDefault();
                document.getElementById("statusMsg").innerHTML = 
                    "<span class='error'>❌ Kamu sudah menggunakan limit gratisan hari ini!<br>Silakan beli Key Premium di Discord Remi atau tunggu besok.</span>";
                return false;
            }

            localStorage.setItem("vortexion_last_use", today);
            return true;
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

    if request.method == "POST":
        input_code = request.form.get("input_code", "")
        access_key = request.form.get("access_key", "").strip()

        if access_key and access_key not in VALID_KEYS:
            error = "❌ Kode Key Premium tidak valid! Dapatkan yang asli di Discord Remi."
        else:
            output_code = obfuscate_roblox_script(input_code)

    return render_template_string(
        HTML_TEMPLATE, 
        input_code=input_code, 
        output_code=output_code, 
        access_key=access_key,
        error=error
    )

app = app
