# ✍️ PostCraft

> **Des posts techniques authentiques, générés par IA — sans le bullshit corporate.**

Tu connais le problème. Tu passes 6h à debugger un truc impossible, tu galères, tu apprends des trucs de ouf — mais quand tu veux en faire un post LinkedIn ou Twitter, ça sonne faux. Corporate. Générique.

**PostCraft** c'est l'inverse. Un prompt bien torché, DeepSeek, et un post qui ressemble à ce que tu dirais à un pote développeur.

## 🚀 Essayer

→ **[postcraft.taild09a06.ts.net](https://bugcrush.taild09a06.ts.net/)** ← (oui le domaine c'est temporaire, on va acheter mieux)

## 📸 En vrai ça donne quoi ?

```text
🔥 6 heures de debug pour une virgule. Et tout le site était down.

Vendredi 17h. Le monitoring explose. 503 partout.
Je lance un curl sur l'endpoint critique : rien.
Stack trace vide, juste un SyntaxError: Unexpected token
dans la console serveur.

30 minutes à chercher du mauvais côté.
Puis je fais un git diff du dernier déploiement.

Une virgule manquante dans un fichier de config JSON.

Le correctif : , ajoutée.
Service restored en 3 secondes.

Depuis, je valide TOUJOURS les fichiers de config avant déploiement.

Est-ce que vous avez déjà perdu une journée sur un bug
qui tenait dans un seul caractère ?
```

*Ça, c'est un vrai post. Pas de "nous sommes ravis d'annoncer". Pas de "notre équipe a travaillé dur". Juste un dev qui raconte sa galère.*

## 🎯 Comment ça marche

1. Tu tapes ton **sujet** (une galère, une astuce, une découverte)
2. Tu choisis **LinkedIn** ou **Twitter/X**
3. Tu sélectionnes un **ton** (Tech, War story, Astuce, Thread)
4. Tu ajoutes du **contexte** si tu veux (optionnel)
5. **Générer** → un post authentique, à la première personne, avec des détails techniques crédibles

## 🎭 Tons disponibles

| Ton | Style |
|-----|-------|
| 👨‍💻 Tech / Sincère | Récit technique simple, authentique |
| 🔥 War story | Galère épique, émotion, rebondissement |
| 💡 Astuce / Tutorial | Conseil pratique, solution à un problème |
| 🧵 Thread | Fil Twitter/X éducatif, en plusieurs parties |

## 🛠 Stack

- **Backend** : FastAPI (un seul fichier, 250 lignes)
- **IA** : DeepSeek V4
- **Hébergement** : Mon serveur Dell sous Ubuntu + Tailscale Funnel
- **Design** : AMICO TECH (dark, violet, minimal)

## 📦 Installation locale

```bash
git clone https://github.com/xalil05/postcraft.git
cd postcraft
pip install fastapi uvicorn httpx
export DEEPSEEK_KEY="sk-xxx"
python main.py
```

## 💡 Pourquoi j'ai fait ça

Parce que je poste sur LinkedIn et X (@Xalil_Ndiaye), et que je voulais un outil qui génère du contenu qui me ressemble — pas du contenu qui sent l'IA à plein nez. 

**PostCraft est mon premier mini-SaaS.** Si ça prend, cool. Si ça prend pas, j'aurai appris des trucs en le construisant.

## 📄 Licence

MIT — fais ce que tu veux.
