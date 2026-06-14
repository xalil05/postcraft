"""
CommitCraft — Mini-SaaS de génération de messages de commit
MVP en 1 fichier, prêt à lancer sur Tailscale Funnel
"""

import json, os, sys
from pathlib import Path
from urllib.parse import quote
from datetime import datetime

try:
    from fastapi import FastAPI, Request, Form
    from fastapi.responses import HTMLResponse
    import uvicorn
except ImportError:
    os.system("pip install fastapi uvicorn httpx -q")
    from fastapi import FastAPI, Request, Form
    from fastapi.responses import HTMLResponse
    import uvicorn

import httpx

# ── Config ──
PORT = 8010
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_KEY", "")
SITE_NAME = "PostCraft"
SITE_URL = f"https://postcraft.taild09a06.ts.net"

app = FastAPI()

# ── Templates ──
LAYOUT = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} — {site}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:#050508; color:#f0f0f5; font-family:'Inter',sans-serif; min-height:100vh; }}
.container {{ max-width:720px; margin:0 auto; padding:32px 20px; }}
h1 {{ font-size:32px; font-weight:800; letter-spacing:-0.5px; margin-bottom:6px; background:linear-gradient(135deg,#f0f0f5,#8b6cf7); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
.sub {{ font-size:14px; color:#8888a0; margin-bottom:32px; line-height:1.6; }}
.card {{ background:#0a0a12; border:1px solid #1a1a2e; border-radius:12px; padding:24px; margin-bottom:20px; }}
.card h2 {{ font-size:14px; font-weight:700; color:#8888a0; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px; }}
label {{ font-size:12px; font-weight:600; color:#8888a0; display:block; margin-bottom:6px; text-transform:uppercase; letter-spacing:0.5px; }}
textarea, input, select {{ width:100%; background:#10101a; border:1px solid #1a1a2e; border-radius:8px; color:#f0f0f5; font-family:'Inter',sans-serif; font-size:14px; padding:12px 14px; outline:none; transition:border-color 0.2s; }}
textarea:focus, input:focus {{ border-color:#8b6cf7; }}
textarea {{ min-height:120px; resize:vertical; }}
.btn {{ display:inline-flex; align-items:center; gap:8px; padding:12px 28px; border-radius:100px; font-size:14px; font-weight:700; cursor:pointer; border:none; font-family:'Inter',sans-serif; transition:all 0.2s; text-decoration:none; }}
.btn-primary {{ background:linear-gradient(135deg,#8b6cf7,#6b4ce7); color:#fff; }}
.btn-primary:hover {{ transform:translateY(-1px); box-shadow:0 8px 24px rgba(139,108,247,0.25); }}
.btn-secondary {{ background:transparent; border:1px solid #1a1a2e; color:#8888a0; }}
.btn-secondary:hover {{ border-color:#8b6cf7; color:#f0f0f5; }}
.result {{ background:#10101a; border:1px solid #2a2a4a; border-radius:12px; padding:20px; margin-top:20px; }}
.result .post {{ font-size:14px; line-height:1.7; color:#e0e0f0; white-space:pre-wrap; }}
.result .meta {{ font-size:11px; color:#555570; margin-top:12px; padding-top:12px; border-top:1px solid #1a1a2e; }}
.spinner {{ display:none; text-align:center; padding:40px; }}
.spinner.show {{ display:block; }}
.spinner .dot {{ display:inline-block; width:8px; height:8px; border-radius:50%; background:#8b6cf7; margin:0 4px; animation:bounce 1.4s ease-in-out infinite; }}
.spinner .dot:nth-child(2) {{ animation-delay:0.16s; }}
.spinner .dot:nth-child(3) {{ animation-delay:0.32s; }}
@keyframes bounce {{ 0%,80%,100% {{ transform:scale(0); }} 40% {{ transform:scale(1); }} }}
.tone-badge {{ display:inline-block; font-size:10px; font-weight:700; padding:3px 10px; border-radius:100px; margin-right:6px; }}
.tone-tech {{ background:#6b4ce722; color:#8b6cf7; border:1px solid #6b4ce744; }}
.tone-war {{ background:#ff2d5522; color:#ff2d75; border:1px solid #ff2d5544; }}
.tone-tip {{ background:#00e67622; color:#00e676; border:1px solid #00e67644; }}
.tone-thread {{ background:#00f0ff22; color:#00f0ff; border:1px solid #00f0ff44; }}
footer {{ text-align:center; padding:24px; font-size:11px; color:#555570; }}
footer a {{ color:#8b6cf7; text-decoration:none; }}
.help {{ font-size:11px; color:#555570; margin-top:4px; }}
select {{ cursor:pointer; }}
option {{ background:#0a0a12; color:#f0f0f5; }}
</style>
</head>
<body>
<div class="container">
{content}
<footer><a href="https://github.com/xalil05">{site}</a> &middot; propulsé par DeepSeek &middot; © 2026</footer>
</div>
</body>
</html>"""

def page(title, content):
    return HTMLResponse(LAYOUT.format(title=title, site=SITE_NAME, content=content))

# ── Routes ──

HOME = """
<h1>✍️ PostCraft</h1>
<div class="sub">
    Des posts techniques qui ont du style. Pas de blabla corporate,<br>
    du contenu que les devs ont envie de lire.
</div>

<div class="card">
    <form id="postForm" onsubmit="generate(event)">
        <div style="margin-bottom:16px">
            <label>🎯 Sujet du post</label>
            <input type="text" id="topic" placeholder="Ex: J'ai debuggué un bug pendant 6h et voici ce que j'ai appris" required>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">
            <div>
                <label>📢 Plateforme</label>
                <select id="platform">
                    <option value="linkedin">LinkedIn</option>
                    <option value="twitter">Twitter / X</option>
                </select>
            </div>
            <div>
                <label>🎭 Ton</label>
                <select id="tone">
                    <option value="tech">👨‍💻 Tech / Sincère</option>
                    <option value="war">🔥 War story</option>
                    <option value="tip">💡 Astuce / Tutorial</option>
                    <option value="thread">🧵 Thread</option>
                </select>
            </div>
        </div>

        <div style="margin-bottom:16px">
            <label>📋 Contexte (optionnel)</label>
            <textarea id="context" placeholder="Détails techniques, galères, apprentissages... tout ce qui peut enrichir le post" style="min-height:80px"></textarea>
        </div>

        <button type="submit" class="btn btn-primary" id="submitBtn">🚀 Générer le post</button>
    </form>
</div>

<div class="spinner" id="spinner">
    <span class="dot"></span><span class="dot"></span><span class="dot"></span>
    <div style="font-size:12px;color:#555570;margin-top:12px">Génération en cours...</div>
</div>

<div id="result"></div>

<script>
async function generate(e) {
    e.preventDefault();
    const btn = document.getElementById('submitBtn');
    const spinner = document.getElementById('spinner');
    const result = document.getElementById('result');
    btn.disabled = true; btn.textContent = '⏳ Génération...';
    spinner.classList.add('show');
    result.innerHTML = '';

    const resp = await fetch('/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: new URLSearchParams({
            topic: document.getElementById('topic').value,
            platform: document.getElementById('platform').value,
            tone: document.getElementById('tone').value,
            context: document.getElementById('context').value,
        })
    });

    spinner.classList.remove('show');
    btn.disabled = false; btn.textContent = '🚀 Générer le post';

    if (!resp.ok) { result.innerHTML = '<div class="result" style="border-color:#ff2d55"><p style="color:#ff2d55">❌ Erreur: ' + (await resp.text()) + '</p></div>'; return; }
    const data = await resp.json();
    const toneClass = {'tech':'tone-tech','war':'tone-war','tip':'tone-tip','thread':'tone-thread'}[data.tone] || 'tone-tech';
    const toneLabel = {'tech':'👨‍💻 Tech','war':'🔥 War story','tip':'💡 Astuce','thread':'🧵 Thread'}[data.tone] || data.tone;
    result.innerHTML = `
        <div class="result">
            <div class="post">${escapeHtml(data.post)}</div>
            <div class="meta" style="display:flex;gap:8px;align-items:center">
                <span class="tone-badge ${toneClass}">${toneLabel}</span>
                <span>📢 ${data.platform === 'linkedin' ? 'LinkedIn' : 'Twitter/X'}</span>
                <span style="flex:1"></span>
                <button class="btn btn-secondary" style="padding:6px 14px;font-size:11px" onclick="copyPost()">📋 Copier</button>
            </div>
        </div>`;
    window._lastPost = data.post;
}
function escapeHtml(t) { return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\\n/g,'<br>'); }
function copyPost() {
    if (!window._lastPost) return;
    navigator.clipboard.writeText(window._lastPost).then(() => {
        const btn = document.querySelector('.result .btn-secondary');
        btn.textContent = '✅ Copié !';
        setTimeout(() => btn.textContent = '📋 Copier', 2000);
    });
}
</script>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return page(f"{SITE_NAME} — Des posts techniques qui claquent", HOME)

@app.post("/generate")
async def generate(topic: str = Form(""), platform: str = Form("linkedin"), tone: str = Form("tech"), context: str = Form("")):
    if not topic:
        return HTMLResponse("Sujet requis", status_code=400)

    tone_labels = {"tech": "👨‍💻 Tech / sincère", "war": "🔥 War story avec émotion", "tip": "💡 Astuce pratique", "thread": "🧵 Thread éducatif"}
    platform_labels = {"linkedin": "LinkedIn (professionnel, détaillé)", "twitter": "Twitter/X (court, percutant)"}

    prompt = f"""Tu es un développeur qui partage son expérience sur {platform_labels.get(platform, platform)}. 
Écris un post authentique avec le ton {tone_labels.get(tone, tone)}, en français, sur le sujet suivant :

SUJET: {topic}

CONTEXTE SUPPLÉMENTAIRE: {context if context else "Aucun"}

RÈGLES STRICTES :
- Écris à la PREMIÈRE PERSONNE DU SINGULIER ("je", "mon", "mes")
- Sois authentique et vulnérable (galères, doutes, apprentissages)
- Pas de langage corporate : pas de "nous", pas de "notre équipe"
- Inclus des détails techniques précis (timeout, stack trace, versions)
- Termine par une question ou réflexion ouverte
- Si Twitter/X : max 280 caractères (ou thread si tone=thread)
- Si LinkedIn : longueur naturelle (300-800 caractères)
- PAS d'emojis en excès, PAS de hashtags, PAS de "mon pote" — une voix dans ma tête
- Signé : — @Xalil_Ndiaye (uniquement si Twitter/X)

Génère UNIQUEMENT le contenu du post, rien d'autre."""

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.8,
                    "max_tokens": 1200,
                }
            )
            if resp.status_code != 200:
                return HTMLResponse(f"Erreur API: {resp.text}", status_code=500)
            data = resp.json()
            post = data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return HTMLResponse(f"Erreur: {str(e)}", status_code=500)

    return {
        "post": post,
        "platform": platform,
        "tone": tone,
    }

# ── Main ──
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
