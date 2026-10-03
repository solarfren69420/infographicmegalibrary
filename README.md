# Infographic Mega Library

Browse: **https://solarfren69420.github.io/infographicmegalibrary/** (available after GitHub Pages is enabled).

SolarFren’s collection of AI-generated infographic concepts and archived guides, organized using the images and their original Discord discussion. These images are brainstorming and educational material, not demonstrations of working mods or software. Setup commands, offers, payment methods, and technical claims have not been independently verified. Open full-size originals at high zoom.

## Collections

| Folder | Contents | Files |
| --- | --- | ---: |
| `infographics/01-getting-started/` | Introductory guides and community overview | 2 |
| `infographics/02-rust-and-game-systems/` | Rust and modular game systems | 4 |
| `infographics/03-reverse-engineering-and-databases/` | Decompilation, debug builds, SQLite, and extraction pipelines | 5 |
| `infographics/04-passthrough-and-rewrites/` | Live bridges versus rewritten clients | 4 |
| `infographics/05-game-mashups/` | Elden Ring/Minecraft, GMod/Minecraft, and Postal 2/Minecraft | 7 |
| `infographics/06-mega-mashup-concepts/` | Larger fusion concepts | 4 |
| `infographics/07-ai-tools-and-setup/` | Desktop/CLI setup and Ghidra/Gemini | 3 |
| `infographics/08-subscriptions-and-offers/` | Archived, unverified subscription/payment material | 3 |
| `references/` | Supporting screenshots and notes | 3 |
| `prompts/` | Human-written Postal 2/Minecraft community prompt | 1 |
| `disclaimers/` | The owner’s concept-art and zoom notices | 2 |
| `spam/` | Chat-confirmed fake infographics, memes, and reactions | 8 |
| `duplicates/` | Exact repeated uploads | 3 |

Spam and repeated uploads are excluded from the gallery’s default view. They remain accessible in separate collections. Useful references and the human-written text prompt are retained rather than treated as spam. The gallery supports topic navigation, search, sorting, original downloads, and an image reader with zoom in/out, fit, 100% original-pixel size, scrolling, and drag-to-pan. SolarFren’s supplied portrait appears in the header and share cards.

Each file has a static share page such as `items/item-01/`, with its own title, description, canonical URL, and 1200 × 630 Open Graph/X preview image. Use **Share page** in the viewer or **Copy share link** on the individual page when sharing. Gallery fragments such as `#item-01` remain supported for browsing, but individual page links give shared items distinct previews.

## Archive accounting

The source chat has 295 messages and 52 attachment references. There were **49 downloaded files**, including three exact repeated uploads: 46 distinct file hashes. The opening message contains four different attachments named `content.png`; the export saved all four to the same local path, leaving just one surviving image. The other **three opening images are missing**. Their original Discord links returned HTTP 403 during recovery. The surviving image’s exact remote attachment identity is unresolved. No missing image is represented as recovered.

Every downloaded original is cataloged with its original filename, SHA-256 hash, message ID, timestamp, author, classification, and destination in [data/catalog.json](data/catalog.json). [data/organization-report.json](data/organization-report.json) summarizes the accounting.

The untouched export was backed up locally beside this project as `Infographic Mega Library.original-2026-10-03.zip`. The original chat and recovery records are retained in the ignored local `_archive/` directory. Raw chat and signed CDN URLs are excluded from Git and the public site.

## GitHub Pages setup

Publishing from `main` and `/(root)` is supported: generated share pages are checked in under `items/`, and `.nojekyll` keeps the static output intact. The Actions workflow also supports publishing the validated `_site/` output. Both serve the same gallery and share pages.

1. Open this repository’s **Settings → Pages**.
2. Set **Source** to **GitHub Actions**.
3. In **Actions → Publish infographic library**, use **Run workflow** on `main` (or rerun the initial run).

After deployment, the gallery is served at https://solarfren69420.github.io/infographicmegalibrary/. Future pushes to `main` validate and publish the collection automatically.

## Local preview and updates

No JavaScript framework, package installation, or external service is required.

```sh
python3 scripts/build.py
python3 -m http.server 8000 --directory _site
```

Open http://localhost:8000/. Opening `index.html` directly also works for image browsing; read text prompts through their original-file links when browser local-file restrictions apply.

For updates, add original files to their topic folders, generate WebP thumbnails, and add metadata to `data/catalog.json`. Update the organization report and validation counts if the collection grows. Run `python3 scripts/build.py` to verify all hashes, references, duplicate relationships, and file accounting, regenerate `assets/catalog.js`, and stage only public material in `_site/`.

## Link preview images

Preview images are checked in under `assets/social/`; publishing does not require Chrome. To regenerate them after changing titles, thumbnails, or branding, run `node scripts/social-cards.cjs` locally with Google Chrome and the Node `undici` module available, then run `python3 scripts/build.py`. The renderer uses existing source images and a temporary browser profile. Platforms decide how to display previews and may cache an older version.

## Catalog

### Infographics

- [Combining Game Clients with Rust](infographics/01-getting-started/combining-game-clients-with-rust.png) — Getting started
- [Why Rust Feels Supernatural](infographics/02-rust-and-game-systems/why-rust-feels-supernatural.png) — Rust & game systems
- [The Database Method](infographics/03-reverse-engineering-and-databases/the-database-method.png) — Reverse engineering & databases
- [CHASM Server Overview](infographics/01-getting-started/chasm-server-overview.png) — Getting started
- [decomp.dev Overview](infographics/03-reverse-engineering-and-databases/decomp-dev-overview.png) — Reverse engineering & databases
- [Why the Bully Debug Build Matters](infographics/03-reverse-engineering-and-databases/why-the-bully-debug-build-matters.png) — Reverse engineering & databases
- [GTA 6 as a Systems Goldmine](infographics/03-reverse-engineering-and-databases/gta-6-as-a-systems-goldmine.png) — Reverse engineering & databases
- [Combining Games with Rust and AI — Starter Path](infographics/05-game-mashups/elden-ring-and-minecraft/combining-games-with-rust-and-ai-starter-path.png) — Game mashups
- [AI Decompilation and Rust — Mashup Starter Path](infographics/05-game-mashups/elden-ring-and-minecraft/ai-decompilation-and-rust-mashup-starter-path.png) — Game mashups
- [Can I Combine Elden Ring and Minecraft](infographics/05-game-mashups/elden-ring-and-minecraft/can-i-combine-elden-ring-and-minecraft.png) — Game mashups
- [Minecraft Inside GTA V — Passthrough Mod](infographics/04-passthrough-and-rewrites/minecraft-inside-gta-v-passthrough-mod.png) — Passthrough & rewrites
- [Minecraft Inside Elden Ring — Passthrough Concept](infographics/05-game-mashups/elden-ring-and-minecraft/minecraft-inside-elden-ring-passthrough-concept.png) — Game mashups
- [Minecraft Character Inside Elden Ring](infographics/05-game-mashups/elden-ring-and-minecraft/minecraft-character-inside-elden-ring.png) — Game mashups
- [Any Game × Any Game × Any Game](infographics/06-mega-mashup-concepts/any-game-any-game-any-game.png) — Mega mashup concepts
- [The Full Pipeline](infographics/03-reverse-engineering-and-databases/the-full-pipeline.png) — Reverse engineering & databases
- [The Mega Game Combo Engine](infographics/06-mega-mashup-concepts/the-mega-game-combo-engine.png) — Mega mashup concepts
- [Metal Gear Rising — Absurd Fusion](infographics/06-mega-mashup-concepts/metal-gear-rising-absurd-fusion.png) — Mega mashup concepts
- [What the Hell Is This Combo](infographics/06-mega-mashup-concepts/what-the-hell-is-this-combo.png) — Mega mashup concepts
- [GMod × Minecraft — Voxel Sandbox Fusion](infographics/05-game-mashups/gmod-and-minecraft/gmod-minecraft-voxel-sandbox-fusion.png) — Game mashups
- [Passthrough Mod vs Rust Rewrite Client](infographics/04-passthrough-and-rewrites/passthrough-mod-vs-rust-rewrite-client.png) — Passthrough & rewrites
- [Passthrough Mod — First Prompt for the AI](infographics/04-passthrough-and-rewrites/passthrough-mod-first-prompt-for-the-ai.png) — Passthrough & rewrites
- [Rust Rewrite Client — First Prompt for the AI](infographics/04-passthrough-and-rewrites/rust-rewrite-client-first-prompt-for-the-ai.png) — Passthrough & rewrites
- [Claude and ChatGPT — Install Guide](infographics/07-ai-tools-and-setup/claude-and-chatgpt-install-guide.png) — AI tools & setup
- [Real Commands to Open Them](infographics/07-ai-tools-and-setup/real-commands-to-open-them.png) — AI tools & setup
- [Ghidra and Gemini CLI — Setup Guide](infographics/07-ai-tools-and-setup/ghidra-and-gemini-cli-setup-guide.png) — AI tools & setup
- [Pay-in-4 to Google Play — AI Subscription Guide](infographics/08-subscriptions-and-offers/pay-in-4-to-google-play-ai-subscription-guide.png) — Subscriptions & offers
- [Students — Four Months Free Offer](infographics/08-subscriptions-and-offers/students-four-months-free-offer.png) — Subscriptions & offers
- [Do Not Finance an AI Subscription Lightly](infographics/08-subscriptions-and-offers/do-not-finance-an-ai-subscription-lightly.png) — Subscriptions & offers
- [Postal 2 Inside Minecraft](infographics/05-game-mashups/postal-2-and-minecraft/postal-2-inside-minecraft.png) — Game mashups
- [What Even Is Rust](infographics/02-rust-and-game-systems/what-even-is-rust.png) — Rust & game systems
- [Why Rust Dominates This Pipeline](infographics/02-rust-and-game-systems/why-rust-dominates-this-pipeline.png) — Rust & game systems
- [Why Rust Is Perfect for This Pipeline](infographics/02-rust-and-game-systems/why-rust-is-perfect-for-this-pipeline.png) — Rust & game systems

### References

- [What You Are Really Doing — Screenshot](references/screenshots/what-you-are-really-doing-screenshot.png) — References
- [System Combination Math](references/notes/system-combination-math.png) — References
- [Minecraft in Elden Ring — Gameplay Reference](references/screenshots/minecraft-in-elden-ring-gameplay-reference.png) — References

### Prompts

- [Postal 2 and Minecraft — Community Prompt](prompts/postal-2-and-minecraft/postal-2-and-minecraft-community-prompt.txt) — Text prompts

### Disclaimers

- [AI Generated Concept Art Disclaimer](disclaimers/ai-generated-concept-art-disclaimer.png) — Disclaimers
- [Read the Infographics at High Zoom](disclaimers/read-the-infographics-at-high-zoom.png) — Disclaimers

### Spam

- [World of Warcraft Foreverscape — Joke Poster](spam/memes-and-parodies/world-of-warcraft-foreverscape-joke-poster.png) — Spam
- [Foreverscape Mashup — Joke Poster](spam/memes-and-parodies/foreverscape-mashup-joke-poster.png) — Spam
- [GMod and Minecraft — Reaction Thumbnail](spam/memes-and-parodies/gmod-and-minecraft-reaction-thumbnail.png) — Spam
- [Rainbow Background — Follow-up Meme](spam/memes-and-parodies/rainbow-background-follow-up-meme.png) — Spam
- [Gentlemen — Reaction GIF](spam/reaction-gifs/gentlemen-reaction-gif.gif) — Spam
- [Students — 47 Months Free Fake Offer](spam/fake-infographics/students-47-months-free-fake-offer.png) — Spam
- [Wiping Formalized — Fake Infographic](spam/fake-infographics/wiping-formalized-fake-infographic.png) — Spam
- [Your Actions Anger Israel — Reaction GIF](spam/reaction-gifs/your-actions-anger-israel-reaction-gif.gif) — Spam

### Duplicates

- [Minecraft Inside GTA V — Reposted Copy](duplicates/minecraft-inside-gta-v-reposted-copy.png) — Duplicates
- [Rust and AI Starter Path — Reposted Copy](duplicates/rust-and-ai-starter-path-reposted-copy.png) — Duplicates
- [Why Rust Feels Supernatural — Reposted Copy](duplicates/why-rust-feels-supernatural-reposted-copy.png) — Duplicates
