# RUZ desk — your GitHub profile

This is not a copy of the usual “terminal + neofetch + green heatmap” profile.
It is built as a **trading desk**:

- a scrolling identity tape
- cockpit-cam ASCII (your photo, CRT scan, not a typewriter clone)
- a blotter card (SESSION / BOOK / BUILD), not neofetch keys
- a year tape whose boxes rise like candles in gold, not GitHub green

Upload the folder. GitHub plays the motion. A daily Action reprints the year tape.

---

## What to check once

Open `config.json`.

1. `"github_username"` must match your login exactly.
2. Change `"desk"` and `"ticker"` lines if you want different copy.
3. Optional: drop a clearer photo over `source-photo.jpg`.

---

## Upload (GitHub website, no coding)

1. Create a **public** repo named exactly your username.
2. **Add file → Upload files** and drop in this folder.
3. Make sure these land in the repo root:
   - `README.md`
   - `banner-ticker.svg`
   - `ascii-portrait.svg`
   - `desk-card.svg`
   - `year-tape.svg`
   - `config.json`
   - `scripts/`
   - `.github/workflows/update-profile-art.yml`
4. Repo → **Actions** → enable workflows → run **Update year tape**.

Visit `https://github.com/YOUR_USERNAME`.

If `.github` is hidden on your computer, create a new file named
`.github/workflows/update-profile-art.yml` and paste the kit file.

---

## Rebuild later

Need a new photo or new copy? In any AI coding app:

```text
Run python scripts/build_all.py
```

That reprints every SVG. Then upload the new files.

Or separately:

```text
python scripts/prep_photo.py
python scripts/make_ascii_svg.py
python scripts/make_desk_card.py
python scripts/make_ticker.py
python scripts/render_heatmap_svg.py
```

---

## Why it will not look like the tutorial you sent

| Their profile | Yours |
|---|---|
| Fake shell prompts (`user@github ~ $`) | Identity tape + LIVE / IST |
| Mac window dots + neofetch | Blotter rows + MARK OPEN |
| GitHub-green heatmap that pops | Gold/olive candles that grow |
| Row-by-row typewriter portrait | Full-frame CRT scan + HUD corners |
| Generic developer badges | Tape / Desk marks |

Same underlying trick (animated SVG, daily Action). Different product.
