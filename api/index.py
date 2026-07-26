def obfuscate_native_one_liner(lua_code):
    if not lua_code.strip():
        return ""

    xor_key = random.randint(11, 230)
    
    v_decrypt = generate_var()
    v_bytes = generate_var()
    v_key = generate_var()
    v_i = generate_var()
    v_res = generate_var()

    # 1. HAPUS SEMUA KOMENTAR LUA (Agar tidak memotong baris waktu di-one-line)
    clean_code = re.sub(r'--\[\[[\s\S]*?\]\]', '', lua_code)
    clean_code = re.sub(r'--.*$', '', clean_code, flags=re.MULTILINE)
    
    # 2. ENKRIPSI STRING TEKS / ID LAGU
    def string_replacer(match):
        raw_str = match.group(0)[1:-1]
        if not raw_str:
            return '""'
        encrypted_array = encrypt_string_to_xor(raw_str, xor_key)
        return f'{v_decrypt}({encrypted_array})'

    obfuscated_code = re.sub(r'"([^"\\]*(\\.[^"\\]*)*)"|\'([^\'\\]*(\\.[^\'\\]*)*)\'', string_replacer, clean_code)

    # 3. GABUNGKAN SETIAP BARIS PAKAI TITIK KOMA (;)
    lines = [line.strip() for line in obfuscated_code.splitlines() if line.strip()]
    pure_one_line_code = ";".join(lines)

    # 4. WRAPPER 1 BARIS SEJATI (TANPA ASCII HEADER)
    one_liner_lua = f"local {v_key}={xor_key};local function {v_decrypt}({v_bytes}) local {v_res}={{}};for {v_i}=1,#{v_bytes} do {v_res}[{v_i}]=string.char(bit32.bxor({v_bytes}[{v_i}],{v_key})) end;return table.concat({v_res}) end;task.spawn(function() {pure_one_line_code};end)"

    return one_liner_lua
