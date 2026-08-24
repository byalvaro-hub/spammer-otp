# utils.py
import re

def validate_phone(phone):
    """Validasi dan format nomor telepon Indonesia (62xxx)"""
    # Hanya ambil angka
    phone = re.sub(r'\D', '', phone)
    
    # Jika diawali 0, ganti dengan 62
    if phone.startswith('0'):
        phone = '62' + phone[1:]
    # Jika tidak diawali 62 atau 0, anggap salah
    elif not phone.startswith('62'):
        return None, "Nomor harus diawali 0 atau 62 (format Indonesia)"
    
    # Cek panjang minimal (10-15 digit)
    if len(phone) < 10 or len(phone) > 15:
        return None, "Nomor tidak valid (panjang 10-15 digit)"
    
    return phone, "Nomor valid"

def lookup_number(phone):
    """
    Lacak/Lookup nomor telepon (sederhana)
    Mengembalikan dictionary info
    """
    phone, msg = validate_phone(phone)
    if not phone:
        return {"error": msg}
    
    # --- INFO DASAR ---
    info = {
        "nomor": phone,
        "valid": True,
        "kode_negara": "62",
        "nomor_tanpa_kode": phone[2:],
        "operator": "Tidak diketahui"
    }
    
    # --- DETEKSI OPERATOR (SEDERHANA) ---
    # Ini hanya contoh prefix untuk Indonesia
    # Anda bisa menambahkan data yang lebih lengkap
    prefixes = {
        "0811": "Telkomsel",
        "0812": "Telkomsel",
        "0813": "Telkomsel",
        "0814": "Telkomsel",
        "0815": "Indosat",
        "0816": "Indosat",
        "0817": "XL",
        "0818": "XL",
        "0819": "XL",
        "0821": "Telkomsel",
        "0822": "Telkomsel",
        "0823": "Telkomsel",
        "0851": "Indosat",
        "0852": "Indosat",
        "0853": "Indosat",
        "0855": "Indosat",
        "0856": "Indosat",
        "0857": "Indosat",
        "0858": "Indosat",
        "0859": "Indosat",
        "0877": "XL",
        "0878": "XL",
        "0879": "XL",
        "0881": "Smartfren",
        "0882": "Smartfren",
        "0883": "Smartfren",
        "0884": "Smartfren",
        "0885": "Smartfren",
        "0886": "Smartfren",
        "0887": "Smartfren",
        "0888": "Smartfren",
        "0889": "Smartfren",
        "0895": "Three (Tri)",
        "0896": "Three (Tri)",
        "0897": "Three (Tri)",
        "0898": "Three (Tri)",
        "0899": "Three (Tri)",
    }
    
    # Cek prefix 4 digit pertama (atau 5 untuk beberapa kasus)
    for prefix, operator in prefixes.items():
        if phone.startswith(prefix):
            info["operator"] = operator
            break
    
    # Jika tidak terdeteksi, cek prefix 3 digit
    if info["operator"] == "Tidak diketahui" and len(phone) >= 5:
        prefix_3 = phone[:4]
        if prefix_3 in prefixes:
            info["operator"] = prefixes[prefix_3]
    
    return info