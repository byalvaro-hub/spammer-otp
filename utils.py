# utils.py
import re
import requests
import json

def validate_phone(phone):
    """Validasi dan format nomor telepon Indonesia (62xxx)"""
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'):
        phone = '62' + phone[1:]
    elif not phone.startswith('62'):
        return None, "Nomor harus diawali 0 atau 62"
    if len(phone) < 10 or len(phone) > 15:
        return None, "Nomor tidak valid (panjang 10-15 digit)"
    return phone, "Nomor valid"

def lookup_number(phone):
    """Lacak/Lookup nomor telepon (sederhana)"""
    phone, msg = validate_phone(phone)
    if not phone:
        return {"error": msg}
    
    info = {
        "nomor": phone,
        "valid": True,
        "kode_negara": "62",
        "nomor_tanpa_kode": phone[2:],
        "operator": "Tidak diketahui"
    }
    
    # Database prefix operator (contoh sederhana)
    prefixes = {
        "0811": "Telkomsel", "0812": "Telkomsel", "0813": "Telkomsel",
        "0814": "Telkomsel", "0815": "Indosat", "0816": "Indosat",
        "0817": "XL", "0818": "XL", "0819": "XL",
        "0821": "Telkomsel", "0822": "Telkomsel", "0823": "Telkomsel",
        "0851": "Indosat", "0852": "Indosat", "0853": "Indosat",
        "0855": "Indosat", "0856": "Indosat", "0857": "Indosat",
        "0858": "Indosat", "0859": "Indosat",
        "0877": "XL", "0878": "XL", "0879": "XL",
        "0881": "Smartfren", "0882": "Smartfren", "0883": "Smartfren",
        "0884": "Smartfren", "0885": "Smartfren", "0886": "Smartfren",
        "0887": "Smartfren", "0888": "Smartfren", "0889": "Smartfren",
        "0895": "Three (Tri)", "0896": "Three (Tri)", "0897": "Three (Tri)",
        "0898": "Three (Tri)", "0899": "Three (Tri)",
    }
    
    for prefix, operator in prefixes.items():
        if phone.startswith(prefix):
            info["operator"] = operator
            break
    
    return info

def check_whatsapp_number(phone, api_key="kyuuxr:alvaroaptaapa"):
    """
    Mengecek status nomor WhatsApp menggunakan API kyuurzy.dev
    """
    phone, _ = validate_phone(phone)
    if not phone:
        return {"error": "Nomor tidak valid"}
    
    url = "https://kyuurzy.dev/api/v1/whatsapp/check-banned"
    params = {
        "apikey": api_key,
        "phone": phone
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("success"):
            return data
        else:
            return {"error": "Gagal memeriksa nomor"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Error koneksi: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Respons dari server tidak valid"}