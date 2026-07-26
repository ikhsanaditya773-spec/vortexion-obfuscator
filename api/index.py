from flask import Flask, render_template_string, request
import re
import random

app = Flask(__name__)

# --- HEADER ASCII ART ---
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

def generate_random_name():
    hex_str = ''.join(random.choices("0123456789ABCDEF", k=5))
    return f"_0x{hex_str}"

def encode_string_to_utf8(match):
    str_content = match.group(1) or match.group(2)
    if not str_content:
        return '""'
    
    codepoints = [str(ord(char)) for char in str_content]
    return f"utf8.char({', '.join(codepoints)})"

def obfuscate_roblox_script(lua_code):
    if not lua_code.strip():
        return ""
    
    # 1. Obfuskasi semua teks/string menjadi utf8.char(...)
    string_pattern = r'"([^"\\]*(?:\\.[^"\\]*)*)"|\'([^\'\\]*(?:\\.[^\'\\]*)*)\''
    obfuscated = re.sub(string_pattern, encode_string_to_utf8, lua_code)

    # 2. Obfuskasi variabel lokal sederhana
    var_pattern = r'\blocal\s+([a-zA-Z_][a-zA-Z0-9_]*)'
    variables = set(re.findall(var_pattern, lua_code))
    
    var_map = {}
    blacklist = ['self', 'script', 'game', 'workspace', 'plugin', 'shared', '_G']
    for var in variables:
        if var not in blacklist:
            var_map[var] = generate_random_name()

    for old_var, new_var in var_map.items():
        obfuscated = re.sub(r'\b' + old_var + r'\b', new_var, obfuscated)

    return f"{ASCII_ART_VORTEXION}\n{obfuscated}"

# --- TAMPILAN WEB ---
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
        h1 { text-align: center; color: #58a6ff; font-size: 28px; }
        .editor-container { display: flex; gap: 20px; margin-top: 20px; flex-wrap: wrap; }
        .box { flex: 1; min-width: 300px; display: flex; flex-direction: column; }
        label { font-weight: bold; margin-bottom: 8px; color: #8b949e; }
        textarea { width: 100%; height: 350px; background-color: #161b22; color: #7ee787; border: 1px solid #30363d; border-radius: 6px; padding: 12px; font-family: 'Courier New', Courier, monospace; font-size: 13px; box-sizing: border-box; resize: vertical; white-space: pre-wrap; word-wrap: break-word; }
        button { margin-top: 15px; padding: 12px; background-color: #238636; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 16px; width: 100%; }
        button:hover { background-color: #2ea043; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ VORTEXION Luau Obfuscator ⚡</h1>
        <form method="POST">
            <div class="editor-container">
                <div class="box">
                    <label>Script Roblox Asli (Input):</label>
                    <textarea name="input_code" placeholder="Paste script Lua/Luau kamu di sini...">{{ input_code }}</textarea>
                </div>
                <div class="box">
                    <label>Hasil Obfuskasi VORTEXION (Output):</label>
                    <textarea readonly placeholder="Hasil obfuskasi akan muncul di sini...">{{ output_code }}</textarea>
                </div>
            </div>
            <button type="submit">🔒 Obfuscate Script</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    input_code = ""
    output_code = ""
    if request.method == "POST":
        input_code = request.form.get("input_code", "")
        output_code = obfuscate_roblox_script(input_code)
    return render_template_string(HTML_TEMPLATE, input_code=input_code, output_code=output_code)

app = app
