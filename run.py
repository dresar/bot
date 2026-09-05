import random
import time
from playwright.sync_api import sync_playwright

# ==========================================
# KONFIGURASI PENGGUNA (EDIT DI SINI)
# ==========================================

TARGET_URL = "https://clicky.id/arifex21/khusussempro"  # Ganti dengan URL website Anda
JUMLAH_KUNJUNGAN = 1000              # Total kunjungan ditingkatkan jadi 100

# Konfigurasi Proxy (Biarkan None jika tidak menggunakan proxy)
PROXY_SERVER = None 

# Rentang waktu tunggu (dipercepat agar ringan, sekitar 3 detik total)
MIN_WAIT = 2
MAX_WAIT = 4

# ==========================================
# DATA SAMARAN (SPOOFING DATA) - DIPERBANYAK
# ==========================================

USER_AGENTS = [
    # --- Windows ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0",
    # --- Mac ---
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    # --- Linux ---
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    # --- Mobile (iPhone) ---
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1",
    # --- Mobile (Android) ---
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
]

REFERRERS = [
    # Search Engines
    "https://www.google.com/",
    "https://www.google.co.id/",
    "https://www.bing.com/",
    "https://duckduckgo.com/",
    "https://search.yahoo.com/",
    # Social Media
    "https://www.facebook.com/",
    "https://m.facebook.com/",
    "https://t.co/", 
    "https://twitter.com/",
    "https://www.instagram.com/",
    "https://www.linkedin.com/",
    "https://www.pinterest.com/",
    "https://www.reddit.com/",
    "https://www.tiktok.com/",
    # Direct / None (kadang string kosong)
    "",
    "https://www.youtube.com/"
]

# ==========================================
# FUNGSI PERILAKU MANUSIA
# ==========================================

def simulate_human_behavior(page):
    """
    Melakukan simulasi gerakan mouse acak dan scrolling
    agar tidak terdeteksi sebagai bot statis.
    """
    try:
        # Mendapatkan ukuran layar
        viewport_size = page.viewport_size
        width = viewport_size['width']
        height = viewport_size['height']

        print("   -> Memulai simulasi perilaku manusia (Cepat)...")

        # 1. Random Mouse Movement (Gerakan Kursor - Lebih Singkat)
        for _ in range(random.randint(1, 3)): # Dikurangi langkahnya
            x = random.randint(0, width)
            y = random.randint(0, height)
            page.mouse.move(x, y, steps=3)
            # Sleep sangat singkat
            time.sleep(random.uniform(0.1, 0.2))

        # 2. Scroll Simulation (Scroll Atas Bawah - Dipercepat)
        total_height = page.evaluate("document.body.scrollHeight")
        current_scroll = 0
        
        # Batasi loop scroll agar tidak terlalu lama (max 3-4 kali scroll)
        max_scrolls = 3
        scroll_count = 0

        while current_scroll < total_height and scroll_count < max_scrolls:
            scroll_amount = random.randint(300, 700) # Scroll lebih jauh per langkah
            current_scroll += scroll_amount
            page.mouse.wheel(0, scroll_amount)
            
            # Jeda antar scroll sangat singkat
            time.sleep(random.uniform(0.2, 0.8))
            
            scroll_count += 1
            
            # Sangat jarang scroll ke atas untuk efisiensi waktu
            if random.random() > 0.9:
                page.mouse.wheel(0, -random.randint(50, 100))

    except Exception as e:
        print(f"   [!] Error saat simulasi perilaku: {e}")

# ==========================================
# LOGIKA UTAMA
# ==========================================

def run_load_test():
    with sync_playwright() as p:
        print(f"=== Memulai Load Test ke: {TARGET_URL} ===")
        print(f"=== Total Kunjungan: {JUMLAH_KUNJUNGAN} (Mode: Ringan/Headless) ===\n")

        # Setup Proxy jika ada
        proxy_config = {"server": PROXY_SERVER} if PROXY_SERVER else None

        # Luncurkan browser HEADLESS=TRUE (Latar belakang, tidak muncul window)
        browser = p.chromium.launch(headless=True, proxy=proxy_config)

        for i in range(1, JUMLAH_KUNJUNGAN + 1):
            # Pilih User Agent dan Referrer secara acak untuk setiap sesi
            chosen_ua = random.choice(USER_AGENTS)
            chosen_referrer = random.choice(REFERRERS)
            
            print(f"[{i}/{JUMLAH_KUNJUNGAN}] Membuka sesi baru...")
            # print(f"   UA: {chosen_ua[:30]}...") # Komentar agar log lebih bersih
            
            context = browser.new_context(
                user_agent=chosen_ua,
                extra_http_headers={
                    "Referer": chosen_referrer
                },
                viewport={"width": random.randint(1024, 1920), "height": random.randint(720, 1080)}
            )

            page = context.new_page()

            try:
                # Buka Website
                start_time = time.time()
                # Timeout diperpendek jadi 30 detik agar jika macet langsung skip
                page.goto(TARGET_URL, timeout=30000) 
                load_time = time.time() - start_time
                print(f"   -> Sukses! Load: {load_time:.2f}s | Ref: {chosen_referrer[:20]}...")

                # Simulasi Perilaku (Versi Cepat)
                simulate_human_behavior(page)

                # Random Wait Time (Sangat singkat, ~1-3 detik)
                wait_time = random.uniform(MIN_WAIT, MAX_WAIT)
                print(f"   -> Stay: {wait_time:.2f}s")
                time.sleep(wait_time)

            except Exception as e:
                # Ini akan menangkap jika IP Anda diblokir (Timeout atau Error Access)
                print(f"   [!] GAGAL/BLOKIR: {e}")
            finally:
                context.close()
                # Jeda antar request dipercepat (0.5 - 1.5 detik) agar kejar target 100
                time.sleep(random.uniform(0.5, 1.5))

        browser.close()
        print("=== Load Test Selesai ===")

if __name__ == "__main__":
    run_load_test()