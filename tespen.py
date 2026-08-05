import requests
import time
import random
import concurrent.futures

# --- Konfigurasi ---

# URL formResponse Google Form target
url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSfwSsqEf8K1LwIwygk9NiTTFTr30rblHWeN1Nsctu7G-MTCUg/formResponse"

# Jeda minimal antar *memulai* pengiriman (dalam detik)
jeda_antar_start_kirim = 0.05

# Jumlah maksimum permintaan yang berjalan bersamaan (thread)
max_concurrent_requests = 30

# --- Fungsi Bantuan untuk Membuat Parameter Dinamis ---
def generate_random_fbzx():
    """Menghasilkan string angka acak besar untuk parameter fbzx dan partialResponse."""
    return str(random.randint(-999999999999999999, 999999999999999999))

# --- Fungsi untuk Mengirim Satu Permintaan ---

def send_one_request(url, request_num):
    """Mengirim satu permintaan POST ke Google Form dengan payload spesifik."""
    try:
        current_timestamp_ms = int(time.time() * 1000)
        random_fbzx = generate_random_fbzx()

        # Teks pesan yang Anda tentukan
        pesan_protes = (
            "[[ SEMOGA SUARA INI TAK DIBUNGKAM. ]]\n\n"
            "To: Pihak yang Menuntut Disiplin Tanpa Keteladanan.\n"
            "From: Seluruh mahasiswa yang kecewa.\n"
            "Message:\n"
            "​Sejak derap langkah di orientasi fakultas hingga keheningan di ruang-ruang kelas, sampai kapan rasa kecewa harus menjadi salam kenal pertama kami?\n"
            "​Apakah lorong-lorong kampus ini hanya dibangun untuk menagih janji ketepatan waktu dari mahasiswa, selagi etika dan amanat Undang-Undang Guru dan Dosen dibiarkan menguap begitu saja?\n"
            "​Jika tanggung jawab pengabdian telah kehilangan suaranya di balik pintu yang terkunci, lantas kepada siapa lagi kami harus berguru tentang arti sebuah integritas?"
        )

        # --- PAYLOAD SESUAI PERMINTAAN ---
        payload = {
            'entry.285087845': pesan_protes,
            'entry.739872428': 'MATA AIR - HINDIA',
            'dlut': current_timestamp_ms,
            'fvv': '1',
            'partialResponse': f'[null,null,"{random_fbzx}"]',
            'pageHistory': '0',
            'fbzx': random_fbzx,
            'submissionTimestamp': current_timestamp_ms + random.randint(100, 500),
        }

        # --- Logika Pengiriman HTTP POST ---
        response = requests.post(url, data=payload, timeout=10)

        if response.status_code == 200:
            print(f"[{request_num}] Berhasil (Status 200 OK)! FBZX: {random_fbzx}")
        else:
            print(f"[{request_num}] Gagal (Status {response.status_code})! Respon: {response.text[:100]}...")

    except requests.exceptions.Timeout:
        print(f"[{request_num}] Timeout! Permintaan memakan waktu terlalu lama.")
    except requests.exceptions.RequestException as e:
        print(f"[{request_num}] Error Koneksi: {e}")
    except Exception as e:
        print(f"[{request_num}] Error Tak Terduga: {e}")

# --- Eksekusi Utama Pengujian ---

print(f"Memulai pengiriman payload khusus (Max Thread: {max_concurrent_requests}).")
print("Tekan Ctrl+C untuk menghentikan program.")

jumlah_kirim = 0

with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent_requests) as executor:
    try:
        while True:
            jumlah_kirim += 1
            executor.submit(send_one_request, url, jumlah_kirim)
            time.sleep(jeda_antar_start_kirim)

    except KeyboardInterrupt:
        print(f"\nProgram dihentikan oleh pengguna setelah {jumlah_kirim} percobaan.")
    except Exception as e:
        print(f"\nTerjadi kesalahan di loop utama: {e}")

print("Proses pengujian selesai.")