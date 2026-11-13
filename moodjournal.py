from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime
import random

# ==========================================
# 1. DATABASE SEMENTARA & LOGIKA PYTHON
# ==========================================
database_jurnal = []

# Balasan murni teks tanpa emoji
BALASAN = {
    "senang": [
        "Energi positif ini sangat berharga. Terus sebarkan hal baik hari ini.",
        "Melihat kamu senang membuat harimu lebih berwarna. Nikmati momennya.",
        "Pertahankan momentum baik ini. Kamu melakukan hal yang benar."
    ],
    "sedih": [
        "Tidak apa-apa untuk merasa sedih. Beri dirimu ruang untuk beristirahat.",
        "Badai pasti berlalu. Kamu sudah bertahan sejauh ini, itu luar biasa.",
        "Peluk jauh. Besok adalah hari baru dengan kesempatan baru."
    ],
    "capek": [
        "Kelelahan adalah tanda kamu sudah berusaha keras. Waktunya rehat sejenak.",
        "Tarik napas panjang, buang perlahan. Jangan paksakan dirimu terus berjalan.",
        "Kamu tidak harus produktif setiap saat. Beristirahatlah tanpa rasa bersalah."
    ],
    "marah": [
        "Tarik napas. Amarah itu valid, tapi jangan biarkan ia menguasai keputusanmu.",
        "Tenangkan pikiranmu sejenak. Kamu lebih bijak dari masalah yang menghadang.",
        "Lampiaskan dengan cara yang sehat. Kamu punya kendali penuh atas dirimu."
    ]
}

# ==========================================
# 2. KODE HTML/CSS/JS (Desain Glow in the Dark)
# ==========================================
HTML_PAGE = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mood Journal.</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');
  
  :root {
    --magenta: #F13E93;
    --pale-yellow: #FAFFCB;
    --dark-magenta: #8a1a52;
    
    --bg-color: #1a0b14; 
    --card-bg: rgba(30, 12, 22, 0.7);
    --text-main: #f5e6ec;
    --input-bg: rgba(255, 255, 255, 0.05);
    --border-color: rgba(241, 62, 147, 0.3);
  }

  * { box-sizing: border-box; }

  body {
    margin: 0; padding: 0; min-height: 100vh;
    background: var(--bg-color);
    background-image: radial-gradient(circle at 15% 20%, rgba(241, 62, 147, 0.15), transparent 40%),
                      radial-gradient(circle at 85% 80%, rgba(250, 255, 203, 0.1), transparent 40%);
    font-family: 'Inter', sans-serif;
    display: flex; justify-content: center; align-items: center;
    color: var(--text-main);
    overflow-x: hidden;
    transition: background 0.5s ease;
  }

  .container {
    position: relative;
    width: 100%; max-width: 520px; margin: 20px;
    background: var(--card-bg);
    backdrop-filter: blur(24px) saturate(150%);
    -webkit-backdrop-filter: blur(24px) saturate(150%);
    border: 1px solid var(--border-color);
    border-radius: 24px; padding: 40px;
    box-shadow: 0 0 50px rgba(241, 62, 147, 0.15), inset 0 0 20px rgba(241, 62, 147, 0.05);
    z-index: 10;
    transition: box-shadow 0.4s ease, border-color 0.4s ease;
  }

  /* Card Glow berubah sesuai Mood */
  .container[data-mood="senang"] { border-color: rgba(241, 62, 147, 0.6); box-shadow: 0 0 60px rgba(241, 62, 147, 0.3), inset 0 0 20px rgba(241, 62, 147, 0.1); }
  .container[data-mood="sedih"] { border-color: rgba(62, 147, 241, 0.6); box-shadow: 0 0 60px rgba(62, 147, 241, 0.3), inset 0 0 20px rgba(62, 147, 241, 0.1); }
  .container[data-mood="capek"] { border-color: rgba(250, 255, 203, 0.6); box-shadow: 0 0 60px rgba(250, 255, 203, 0.2), inset 0 0 20px rgba(250, 255, 203, 0.1); }
  .container[data-mood="marah"] { border-color: rgba(241, 62, 62, 0.6); box-shadow: 0 0 60px rgba(241, 62, 62, 0.3), inset 0 0 20px rgba(241, 62, 62, 0.1); }

  h1 { 
    font-family: 'Space Grotesk', sans-serif; 
    text-align: left; margin: 0 0 30px 0; 
    font-size: 28px; font-weight: 700; 
    color: var(--pale-yellow); letter-spacing: -0.5px;
    text-shadow: 0 0 15px rgba(250, 255, 203, 0.5);
  }
  h1 span { color: var(--magenta); text-shadow: 0 0 20px rgba(241, 62, 147, 0.7); }

  .mood-selector { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 30px; }
  
  .mood-btn {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px; font-weight: 600; padding: 12px 0; border-radius: 12px;
    border: 1.5px solid rgba(255, 255, 255, 0.1); cursor: pointer;
    background: var(--input-bg); color: #ccc; transition: all 0.3s ease;
    text-align: center;
  }
  .mood-btn:hover { border-color: rgba(241, 62, 147, 0.5); color: white; }
  
  .mood-btn.active {
    background: var(--magenta); color: white; border-color: var(--magenta);
    box-shadow: 0 0 20px rgba(241, 62, 147, 0.6);
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
  }

  textarea {
    width: 100%; height: 110px; padding: 20px; box-sizing: border-box;
    border: 1.5px solid rgba(255, 255, 255, 0.1); border-radius: 16px;
    background: var(--input-bg); font-family: 'Inter', sans-serif;
    resize: none; outline: none; margin-bottom: 20px; color: var(--text-main);
    font-size: 15px; transition: all 0.3s; line-height: 1.5;
  }
  textarea::placeholder { color: rgba(255, 255, 255, 0.3); }
  textarea:focus { 
    background: rgba(255, 255, 255, 0.1); 
    border-color: var(--magenta); 
    box-shadow: 0 0 20px rgba(241, 62, 147, 0.3); 
  }

  button.submit {
    width: 100%; padding: 16px; border: none; border-radius: 14px;
    background: var(--magenta); color: white; font-family: 'Space Grotesk', sans-serif;
    font-size: 16px; font-weight: 700; cursor: pointer;
    transition: all 0.3s ease; 
    box-shadow: 0 0 25px rgba(241, 62, 147, 0.4);
    text-shadow: 0 0 8px rgba(255,255,255,0.5);
  }
  button.submit:hover { 
    transform: translateY(-2px); 
    box-shadow: 0 0 40px rgba(241, 62, 147, 0.8); 
  }
  button.submit:disabled { background: #444; color: #888; cursor: not-allowed; transform: none; box-shadow: none; text-shadow: none; }

  .history-title { 
    margin-top: 40px; font-family: 'Space Grotesk', sans-serif; font-weight: 700; 
    font-size: 12px; color: var(--pale-yellow); opacity: 0.7; 
    letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 15px;
    text-shadow: 0 0 10px rgba(250, 255, 203, 0.3);
  }
  
  .journal-card {
    background: rgba(255, 255, 255, 0.03); border-radius: 16px; padding: 20px; margin-bottom: 15px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    animation: slideIn 0.4s ease-out;
    transition: all 0.3s ease;
  }
  .journal-card:hover { background: rgba(255, 255, 255, 0.06); border-color: rgba(241, 62, 147, 0.2); }
  @keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
  
  .journal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
  .journal-date { font-size: 11px; font-weight: 600; color: #888; letter-spacing: 0.5px; }
  .journal-mood-tag { 
    font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 4px; 
    background: rgba(241, 62, 147, 0.15); color: #ff7eb6; text-transform: uppercase; letter-spacing: 0.5px;
    box-shadow: 0 0 10px rgba(241, 62, 147, 0.2);
  }

  .journal-text { font-size: 14px; margin-bottom: 15px; color: #ddd; line-height: 1.6; }
  
  .journal-reply { 
    font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 500;
    background: rgba(250, 255, 203, 0.05); padding: 15px; border-radius: 12px; 
    border-left: 3px solid var(--pale-yellow); color: var(--pale-yellow);
    line-height: 1.5;
    box-shadow: inset 0 0 15px rgba(250, 255, 203, 0.05);
  }
  
  /* Kursor Terminal yang Nyala */
  .cursor-blink { 
    display: inline-block; width: 6px; height: 14px; 
    background: var(--pale-yellow); 
    box-shadow: 0 0 8px var(--pale-yellow);
    animation: blink 1s step-end infinite; 
    vertical-align: middle; margin-left: 2px; 
  }
  @keyframes blink { 50% { opacity: 0; } }

</style>
</head>
<body>

<div class="container" id="mainContainer" data-mood="senang">
  <h1>Mood <span>Journal.</span></h1>
  
  <div class="mood-selector" id="moodSelector">
    <div class="mood-btn active" data-mood="senang">SENANG</div>
    <div class="mood-btn" data-mood="sedih">SEDIH</div>
    <div class="mood-btn" data-mood="capek">CAPEK</div>
    <div class="mood-btn" data-mood="marah">MARAH</div>
  </div>

  <textarea id="journalText" placeholder="Tuliskan apa yang ada di pikiranmu..."></textarea>
  <button class="submit" id="saveBtn">SIMPAN JURNAL</button>

  <div class="history-title">Riwayat Jurnal</div>
  <div id="journalHistory"></div>
</div>

<script>
  let selectedMood = "senang";
  const moodBtns = document.querySelectorAll('.mood-btn');
  const saveBtn = document.getElementById('saveBtn');
  const textInput = document.getElementById('journalText');
  const historyContainer = document.getElementById('journalHistory');
  const mainContainer = document.getElementById('mainContainer');

  // Ganti Mood
  moodBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      moodBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedMood = btn.dataset.mood;
      mainContainer.setAttribute('data-mood', selectedMood);
    });
  });

  async function loadHistory() {
    try {
      const res = await fetch('/api/journals');
      const data = await res.json();
      historyContainer.innerHTML = '';
      
      data.reverse().forEach((item, index) => {
        const div = document.createElement('div');
        div.className = 'journal-card';
        
        const moodText = item.mood.charAt(0).toUpperCase() + item.mood.slice(1);
        
        div.innerHTML = `
          <div class="journal-header">
            <div class="journal-date">${item.waktu}</div>
            <div class="journal-mood-tag">${moodText}</div>
          </div>
          <div class="journal-text">${item.teks}</div>
          <div class="journal-reply" id="reply-${item.id}"></div>
        `;
        historyContainer.appendChild(div);
        
        // Efek Typing Terminal
        if (index === 0) {
          const el = document.getElementById('reply-'+item.id);
          el.innerHTML = '<span class="cursor-blink"></span>';
          typeWriter(el, item.balasan, 0);
        } else {
          document.getElementById('reply-'+item.id).textContent = item.balasan;
        }
      });
    } catch (err) { console.log("Gagal load", err); }
  }

  function typeWriter(element, text, i) {
    if (i < text.length) {
      element.innerHTML = text.substring(0, i + 1) + '<span class="cursor-blink"></span>';
      setTimeout(() => typeWriter(element, text, i + 1), 25);
    } else {
      element.innerHTML = text;
    }
  }

  saveBtn.addEventListener('click', async () => {
    const text = textInput.value.trim();
    if (!text) return alert("Tulis dulu jurnalnya!");

    saveBtn.disabled = true;
    saveBtn.textContent = "MEMPROSES...";

    try {
      const res = await fetch('/api/journal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mood: selectedMood, text: text })
      });
      if (res.ok) {
        textInput.value = "";
        loadHistory();
      }
    } catch (err) {
      alert("Gagal nyambung ke server Python.");
    } finally {
      saveBtn.disabled = false;
      saveBtn.textContent = "SIMPAN JURNAL";
    }
  });

  loadHistory();
</script>
</body>
</html>
"""

# ==========================================
# 3. SERVER HANDLER
# ==========================================
class JournalHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
            
        elif self.path == '/api/journals':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(database_jurnal).encode('utf-8'))
            
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/journal':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            mood = data.get('mood', 'senang')
            teks = data.get('text', '')

            balasan_python = random.choice(BALASAN.get(mood, BALASAN["senang"]))

            jurnal_baru = {
                "id": int(datetime.now().timestamp()), 
                "waktu": datetime.now().strftime("%d %b %Y, %H:%M"),
                "mood": mood,
                "teks": teks,
                "balasan": balasan_python
            }
            database_jurnal.append(jurnal_baru)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "sukses"}).encode('utf-8'))

# ==========================================
# 4. JALANKAN SERVER
# ==========================================
if __name__ == '__main__':
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, JournalHandler)
    print(f"🔥 Server menyala! Buka: http://localhost:{port}")
    httpd.serve_forever()