from flask import Flask, render_template_string, request
import random
import re

app = Flask(__name__)

# Header ASCII Art khas VORTEXION (Kembali Hadir!)
ASCII_ART_VORTEXION = r"""--[[
VVV            VVV  OOOOOOO   RRRRRRRRRR TTTTTTTTTTTEEEEEEEEEE XXXXX      XXXXX I  OOOOOOO  NNNN   NNNN
 VVV          VVV OOOOOOOOOOO RRRRRRRRRRRTTTTTTTTTTTEEEEEEEEEE  XXXXX    XXXXX  I OOOOOOOOOOO NNNN   NNNN
  VVV        VVV OOOOO   OOOOO RRR     RRR   TTTT   EEE           XXXXX  XXXXX   I OOOOO   OOOOONNNNN  NNNN
   VVV      VVV  OOOO     OOOO RRRRRRRRRRR   TTTT   EEEEEEEE       XXXXXXXXXX    I OOOO     OOOONNNNNN NNNN
    VVV    VVV   OOOO     OOOO RRRRRRRRRR    TTTT   EEEEEEEE        XXXXXXXX     I OOOO     OOOONNN NNNNNNN
     VVV  VVV    OOOOO   OOOOO RRR   RRRR    TTTT   EEE            XXXXX  XXXXX  I OOOOO   OOOOONNN  NNNNNN
      VVVVVV      OOOOOOOOOOO RRR    RRRR   TTTT   EEEEEEEEEE   XXXXX    XXXXX  I OOOOOOOOOOO NNN   NNNNN
       VVVV        OOOOOOO   RRR     RRRR  TTTT   EEEEEEEEEE  XXXXX      XXXXXI  OOOOOOO  NNN    NNNN

      << VORTEXION NATIVE OBFUSCATOR (SAFE ONE-LINER) >>
]]--"""

VALID_KEYS = ["VORTEXION-VIP-2026", "REMI-PREMIUM-KEY", "VORTEX-PRO"]

def generate_var():
    chars = "lI1O0_v"
    return "_" + ''.join(random.choices(chars, k=14))

def encrypt_string_to_xor(text, key):
    bytes_list = [str(ord(c) ^ key) for c in text]
    return "{" + ",".join(bytes_list) + "}"

def obfuscate_native_safe_oneliner(lua_code):
    if not lua_code.strip():
        return ""

    xor_key = random.randint(11, 230)
    
    v_decrypt = generate_var()
    v_bytes = generate_var()
    v_key = generate_var()
    v_i = generate_var()
    v_res = generate_var()

    # 1. Hapus semua komentar Lua agar tidak merusak 1 baris
    clean_code = re.sub(r'--\[\[[\s\S]*?\]\]', '', lua_code)
    clean_code = re.sub(r'--.*$', '', clean_code, flags=re.MULTILINE)

    # 2. Enkripsi semua string / ID Lagu / RemoteEvent
    def string_replacer(match):
        raw_str = match.group(0)[1:-1]
        if not raw_str:
            return '""'
        encrypted_array = encrypt_string_to_xor(raw_str, xor_key)
        return f'{v_decrypt}({encrypted_array})'

    obfuscated_code = re.sub(r'"([^"\\]*(\\.[^"\\]*)*)"|\'([^\'\\]*(\\.[^\'\\]*)*)\'', string_replacer, clean_code)

    # 3. Gabungkan tiap baris & bersihkan spasi/titik koma ganda
    lines = [line.strip() for line in obfuscated_code.splitlines() if line.strip()]
    raw_joined = " ".join(lines)
    
    # Hapus double semicolon atau pembatas tidak valid yang memicu error 'got ;'
    cleaned_joined = re.sub(r';\s*;+', ';', raw_joined)
    cleaned_joined = re.sub(r'^\s*;+', '', cleaned_joined)

    # 4. Bungkus dalam One-Liner Native Engine
    one_liner_lua = f"local {v_key}={xor_key};local function {v_decrypt}({v_bytes}) local {v_res}={{}} for {v_i}=1,#{v_bytes} do {v_res}[{v_i}]=string.char(bit32.bxor({v_bytes}[{v_i}],{v_key})) end return table.concat({v_res}) end task.spawn(function() {cleaned_joined} end)"

    # Sertakan kembali ASCII Header khas VORTEXION!
    return f"{ASCII_ART_VORTEXION}\n{one_liner_lua}"


# Template Tampilan UI Web
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
        h1 { text-align: center; color: #58a6ff; font-size: 30px; margin-bottom: 5px; text-shadow: 0 0 10px rgba(88, 166, 255, 0.3); }
        .subtitle { text-align: center; color: #8b949e; margin-bottom: 25px; font-size: 14px; }
        
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
        
        .status-msg { text-align: center; margin-top: 15px; font-weight: bold; font-size: 14px; color: #f85149; background: rgba(248, 81, 73, 0.1); padding: 10px; border-radius: 6px; border: 1px solid rgba(248, 81, 73, 0.3); }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ VORTEXION OBFUSCATOR ⚡</h1>
        <div class="subtitle">🔒 No Loadstring Required - Safe One-Liner Output</div>

        <form method="POST">
            <div class="editor-container">
                <div class="box">
                    <label>📝 Script Roblox Asli (Input):</label>
                    <textarea name="input_code" placeholder="Paste script Music Server / UI kamu di sini...">{{ input_code }}</textarea>
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
                <input type="text" name="access_key" placeholder="Masukkan Kode Key Premium..." value="{{ access_key }}">
            </div>

            <button type="submit" class="btn-main">🛡️ Obfuscate Safe One-Liner</button>
        </form>

        {% if error %}
            <div class="status-msg">{{ error }}</div>
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

    if request.method == "POST":
        input_code = request.form.get("input_code", "")
        access_key = request.form.get("access_key", "").strip()

        if access_key and access_key not in VALID_KEYS:
            error = "❌ Kode Key Premium tidak valid!"
        else:
            output_code = obfuscate_native_safe_oneliner(input_code)

    return render_template_string(
        HTML_TEMPLATE, 
        input_code=input_code, 
        output_code=output_code, 
        access_key=access_key,
        error=error
    )

app = app
