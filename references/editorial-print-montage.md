# editorial-print — Multi-Asset Montage Kit

Companion to [`styles/editorial-print.html`](styles/editorial-print.html). The
13 original styles are single text-takeaway cards floating over a talking-head.
**`editorial-print` is different**: every card is a FULLSCREEN editorial *scene*
where user-supplied **images and video clips ARE the content**, arranged like a
printed spread (warm paper, 3px ink borders, hard offset shadows, grain, ghost
serif). This file gives you the asset-slot primitives, the signature
transitions, the asset-staging rules, and the two ways to use the style.

> Read `styles/editorial-print.html` for the visual DNA + tokens first. This
> file is the layout + motion + plumbing layer on top of it.

---

## When to reach for it

| the content is… | editorial-print fits because… |
|---|---|
| a product / project showcase, portfolio, case study | the assets are the story; text is captions, not paragraphs |
| 大事记 / timeline / milestone reel | poster + grid + counter primitives carry dates & proof |
| a company / brand intro montage | logo-strip + print-stack read as "real, shipped" |
| 数据陈列 with supporting imagery | grid captions + an animated counter |
| an editorial column / 宣言 | ghost serif + big serif headline + one hero poster |

If the content is a talking person explaining something, that's still the
normal口播 cut — reach for editorial-print only for the **asset-montage
beats**, then return to the speaker.

---

## Two usage modes (you confirmed: support BOTH)

### Mode A — woven B-roll inside a 口播 cut (no new pipeline)
The existing Steps 1–6 still drive timing from the transcript. For the cards
that should become an asset montage:
- set the card's `zone = "fullscreen"`;
- in the composition GSAP, **hide `#video-wrap`** for that card's window
  (`tl.to('#video-wrap', { opacity:0, duration:0.4 }, T)`), exactly like the
  `rhythm="dynamic"` HIDDEN beat in SKILL.md Step 7 — the speaker disappears,
  the montage scene takes the whole frame, then the video pops back after;
- author the card body from a primitive below instead of a text block.

This is the smallest change and needs nothing new from the user beyond the
images/clips for those beats.

### Mode B — standalone montage (no talking-head, like the YC reference)
No speaker, so the transcript-driven path doesn't apply. Branch the workflow:
1. **Skip Steps 1, 3–5** (extract / transcribe / correct) — there is no source
   口播 to transcribe.
2. **Input = an asset list + a short script** (the user provides ordered images/
   clips, optionally a VO script or just music). Ask for: the asset files, the
   running order, and per-scene copy (kicker / headline / captions).
3. **Storyboard** = scenes, not transcript cards. Each scene is one
   `zone="fullscreen"` editorial-print card. Pace scenes at ~3–5s each (a print
   spread needs dwell time — slower than a text takeaway).
4. **Narration**: if the user gives a VO script, generate it with
   `hyperframes tts` (see the hyperframes-cli skill) and mount it as the audio
   track; otherwise run music-only (a bed track at low volume) or silent.
5. **No `#video-wrap` spine** — either omit the source `<video>` entirely, or
   keep one as just another asset slot inside a scene. Scenes are full-canvas
   cards; transitions between them use the recipes below.
6. Steps 9–12 (assemble / preview / render / report) are unchanged.

Both modes share the same style file, primitives, and transitions — only the
front of the pipeline differs.

---

## Asset staging — get the user's files into `public/`

The card-HTML contract forbids external URLs but **allows relative paths into
`public/`**. Stage every user asset there, then reference it relatively.

```bash
mkdir -p "$WORK_DIR/public/assets"
# copy (or hardlink) each user image / clip in; keep stable, ordered names
cp "/path/to/poster.png"  "$WORK_DIR/public/assets/poster.png"
cp "/path/to/shot-01.jpg" "$WORK_DIR/public/assets/shot-01.jpg"
cp "/path/to/clip-01.mp4" "$WORK_DIR/public/assets/clip-01.mp4"
```

Reference inside a card with a relative path: `<img src="assets/shot-01.jpg">`.
Every asset slot below ships an `<img>`; swap it for a `<video>` per the slot
rules in the next section when the asset is a clip.

**Pre-flight every asset (cheap, saves a re-render):**
- **Phone clips are often rotated portrait.** A `.MOV` may report `1920×1080`
  but carry `rotation=-90` and actually display `1080×1920`. Bake it before
  staging: `ffmpeg -i in.mov -vf "format=yuv420p" out.mp4` (auto-rotates +
  strips the flag), and size the slot to the TRUE aspect so `object-fit:cover`
  doesn't crop to a center band. (Same gotcha as SKILL.md Step 9.)
- **Logos for the logo-strip** want transparent PNG/SVG and look best
  `object-fit: contain` on the white cell (not `cover`).
- Down-res giant stills to ≤2× their on-screen size so the renderer isn't
  decoding 6000px JPEGs per frame.

---

## Image vs video in an asset slot

Every primitive's slot is `overflow:hidden` with the media at
`width:100%; height:100%; object-fit:cover; display:block`. To make a slot a
**video** instead of a still:

```html
<!-- inside any .slot / .window / .strip-img / .cell -->
<video src="assets/clip-01.mp4"
       muted playsinline
       data-start="0" data-duration="4.0"
       data-track-index="5"
       style="width:100%;height:100%;object-fit:cover;display:block;"></video>
```

**Hard rules (HyperFrames lint will bite otherwise — same as SKILL.md Step 9):**
- The timed `<video data-start>` must NOT be nested inside a wrapper that also
  has `data-start`. The card-host is timed; so the `<video>` is the only timed
  node in that subtree. Don't put `data-start` on the `.poster`/`.window` div —
  it's a plain positioned container.
- Each in-slot `<video>` needs a **unique `id`** and its own
  `data-track-index` (above the card-host's, below the next card's).
- Slot videos are usually B-roll → keep `muted` + `data-volume="0"`. If a clip
  carries sound you want, drop `muted`, add `data-has-audio="true"
  data-volume="1"` — but only ONE audible source at a time.
- A slot video shorter than its scene **freezes blank** past its
  `data-duration` (renders transparent, not a held frame). Either loop-extend it
  (`ffmpeg ... -stream_loop`) or freeze its tail
  (`-vf "tpad=stop_mode=clone:stop_duration=<gap>"`) so the panel never goes empty.
- Re-encode any slowed / `setpts` clip with dense keyframes
  (`-g 30 -keyint_min 30`) or the seek lands on a stale keyframe and it freezes.

---

## The 5 layout primitives (copy-paste; scoped to your card id)

Replace `CID` with your card's id (e.g. `card-03`) everywhere — both in the
`<style>` selectors and the `data-card-id`. All sizes are **landscape
1920×1080**; for portrait scale type ×1.3 and shrink side padding to 24–36px
(see DESIGN_INDEX "Portrait sizing"). Shared tokens (paste once per card):

```css
.card[data-card-id="CID"] .root {
  --paper:#F5F5EE; --ink:#16140F; --black:#000; --stone:#8A8575; --white:#FFF;
  --font-head: ui-serif, "Songti SC", "Times New Roman", serif;
  --font-ui: 'Inter', ui-sans-serif, system-ui, sans-serif;
  width:100%; height:100%; box-sizing:border-box; overflow:hidden;
  background:var(--paper); color:var(--ink); font-family:var(--font-ui);
  position:relative; isolation:isolate;
}
/* grain — paste the .grain rule from styles/editorial-print.html, add <div class="grain"></div> first child */
.card[data-card-id="CID"] .panel {            /* the universal asset frame */
  background:var(--white); border:3px solid var(--ink); padding:16px;
  box-shadow:24px 28px 0 rgba(22,20,15,0.16); overflow:hidden;
}
.card[data-card-id="CID"] .panel img,
.card[data-card-id="CID"] .panel video { width:100%; height:100%; object-fit:cover; display:block; }
```

### 1. `poster` — one hero asset, hard-shadowed
The single-image hero (see the reference file). One big panel, optionally beside
a text column. `box-shadow:24px 28px 0` (no blur) is the signature.
```html
<div class="panel" style="height:770px;"
     data-anim="settle" data-anim-from="right" data-anim-at="0.3" data-anim-duration="0.7">
  <img src="assets/poster.png" alt="">
</div>
```

### 2. `photo-grid` — 2×2 captioned, the workhorse
Four assets, each with a name + tag caption (the YC scene2 grid).
```html
<style>
  .card[data-card-id="CID"] .grid { display:grid; gap:22px;
    grid-template-columns:repeat(2,minmax(0,1fr)); grid-template-rows:repeat(2,minmax(0,1fr)); height:100%; }
  .card[data-card-id="CID"] .cell { display:flex; flex-direction:column; gap:10px; min-height:0;
    background:var(--white); border:3px solid var(--ink); padding:14px;
    box-shadow:14px 14px 0 rgba(22,20,15,0.12); overflow:hidden; }
  .card[data-card-id="CID"] .cell .win { flex:1 1 0; min-height:0; overflow:hidden; background:var(--black); }
  .card[data-card-id="CID"] .cell .cap { display:flex; justify-content:space-between; align-items:center;
    font-weight:800; font-size:24px; }
  .card[data-card-id="CID"] .cell .cap .t { color:var(--stone); font-weight:700; font-size:18px;
    letter-spacing:0.1em; text-transform:uppercase; }
</style>
<div class="grid">
  <div class="cell" data-anim="settle" data-anim-at="0.30" data-anim-duration="0.6"><div class="win"><img src="assets/a.jpg" alt=""></div><div class="cap"><span>名称 A</span><span class="t">S05</span></div></div>
  <div class="cell" data-anim="settle" data-anim-at="0.42" data-anim-duration="0.6"><div class="win"><img src="assets/b.jpg" alt=""></div><div class="cap"><span>名称 B</span><span class="t">W09</span></div></div>
  <div class="cell" data-anim="settle" data-anim-at="0.54" data-anim-duration="0.6"><div class="win"><img src="assets/c.jpg" alt=""></div><div class="cap"><span>名称 C</span><span class="t">S09</span></div></div>
  <div class="cell" data-anim="settle" data-anim-at="0.66" data-anim-duration="0.6"><div class="win"><img src="assets/d.jpg" alt=""></div><div class="cap"><span>名称 D</span><span class="t">S12</span></div></div>
</div>
```

### 3. `collage` — overlapping tilted strips (depth)
3–4 panels absolutely positioned with slight rotation + overlap, behind a
centered stat/headline. The YC scene3 proof-wall.
```html
<style>
  .card[data-card-id="CID"] .collage { position:absolute; inset:0; z-index:0; opacity:0.3; }
  .card[data-card-id="CID"] .strip { position:absolute; width:560px; height:480px;
    background:var(--white); border:3px solid var(--ink); padding:12px; overflow:hidden; }
  .card[data-card-id="CID"] .strip img { width:100%; height:100%; object-fit:cover; display:block; filter:grayscale(0.08); }
  .card[data-card-id="CID"] .strip.a { left:80px;  top:100px;  transform:rotate(-4deg); }
  .card[data-card-id="CID"] .strip.b { right:120px;top:60px;   transform:rotate(3deg);  }
  .card[data-card-id="CID"] .strip.c { left:580px; bottom:50px;transform:rotate(-2deg); }
</style>
<div class="collage">
  <div class="strip a" data-anim="settle" data-anim-at="0.20" data-anim-duration="0.7"><img src="assets/p1.jpg" alt=""></div>
  <div class="strip b" data-anim="settle" data-anim-at="0.32" data-anim-duration="0.7"><img src="assets/p2.jpg" alt=""></div>
  <div class="strip c" data-anim="settle" data-anim-at="0.44" data-anim-duration="0.7"><img src="assets/p3.jpg" alt=""></div>
</div>
<!-- foreground stat box sits on top with z-index:1; pair with the count-up below -->
```

**Big animated counter** (pairs with `collage` for a "combined valuation" beat):
use `data-anim="count-up"` on a tabular-nums number, or step discrete labels via
the GSAP `tl.set('#CID-stat',{innerHTML:'$0.5T'},T)` pattern from the YC ref.

### 4. `logo-strip` — a row of proof logos
One bordered bar split into N cells with hairline dividers; logos
`object-fit:contain`.
```html
<style>
  .card[data-card-id="CID"] .logos { height:164px; display:grid; grid-template-columns:repeat(5,1fr);
    background:var(--white); border:3px solid var(--ink); box-shadow:14px 14px 0 rgba(22,20,15,0.14); overflow:hidden; }
  .card[data-card-id="CID"] .lcell { display:flex; align-items:center; justify-content:center; padding:24px;
    border-right:3px solid rgba(22,20,15,0.2); }
  .card[data-card-id="CID"] .lcell:last-child { border-right:0; }
  .card[data-card-id="CID"] .lcell img { max-width:78%; max-height:72px; object-fit:contain; display:block; }
</style>
<div class="logos">
  <div class="lcell" data-anim="fade-in" data-anim-at="0.30" data-anim-duration="0.4"><img src="assets/logo1.png" alt=""></div>
  <div class="lcell" data-anim="fade-in" data-anim-at="0.37" data-anim-duration="0.4"><img src="assets/logo2.png" alt=""></div>
  <div class="lcell" data-anim="fade-in" data-anim-at="0.44" data-anim-duration="0.4"><img src="assets/logo3.png" alt=""></div>
  <div class="lcell" data-anim="fade-in" data-anim-at="0.51" data-anim-duration="0.4"><img src="assets/logo4.png" alt=""></div>
  <div class="lcell" data-anim="fade-in" data-anim-at="0.58" data-anim-duration="0.4"><img src="assets/logo5.png" alt=""></div>
</div>
```

### 5. `print-stack` — overlapping prints, closing beat
2–3 hard-shadowed panels overlapping at different sizes/rotations (the YC
scene4 invitation prints). Same `.panel` token, absolutely positioned:
```html
<div style="position:relative;height:680px;">
  <div class="panel" style="position:absolute; width:430px;height:440px; right:220px;top:88px; transform:rotate(-4deg);"
       data-anim="settle" data-anim-at="0.30" data-anim-duration="0.65"><img src="assets/print1.jpg" alt=""></div>
  <div class="panel" style="position:absolute; width:560px;height:372px; right:12px;top:278px; transform:rotate(3deg);"
       data-anim="settle" data-anim-at="0.42" data-anim-duration="0.65"><img src="assets/print2.jpg" alt=""></div>
</div>
```

**Footer panel** (closing brand bar, YC scene4): a full-width black bar pinned
to the bottom with a serif motto + uppercase URL; slide it up with
`data-anim="slide-in" data-anim-from="bottom"`.

---

## Slow ambient on every asset (don't let the spread freeze)

Each scene still obeys the global Motion default — give the hero asset or the
ghost word ONE tiny `drift`, and let the still images breathe with a slow
`object-position`/`scale` push via a `morph-to`-style tween in the composition:
```js
// gentle Ken-Burns on a still inside a panel (finite repeat, never -1)
tl.to('.card[data-card-id="CID"] .panel img',
      { scale:1.05, x:-16, duration: Math.min(compDurationSec, 5),
        ease:'sine.inOut', repeat:0 }, T_cardStart);
```
Keep amplitude tiny — the spread is a printed page that's *barely* alive, not a
moving collage. ≤2 persistent motions per scene (see 恰到好处 guardrails).

---

## The 3 signature transitions (composition-level GSAP)

These extend the silky slip default with print-genre cuts. Author them in the
composition `<script>` between scene cards, just like the slip. `OUT` = outgoing
card-host selector, `IN` = incoming; `T` = the cut time; incoming card sits on a
higher `data-track-index`.

### whip-pan — horizontal smear between scenes
Outgoing pushes left + blurs out; incoming arrives from the right. Fast (~0.5s),
reads as a camera whip.
```js
tl.to(OUT, { x:-440, filter:'blur(18px)', opacity:0, duration:0.28, ease:'power3.in' }, T);
tl.set(IN, { visibility:'visible' }, T + 0.22);
tl.fromTo(IN, { x:440, filter:'blur(18px)', opacity:0 },
              { x:0, filter:'blur(0px)', opacity:1, duration:0.52, ease:'power4.out' }, T + 0.22);
```

### blinds-wipe — editorial vertical-blind reveal
Eight ink bars scale in then out, hiding the swap underneath. Add this once near
the end of `#stage` (sibling of the card-hosts, high z-index):
```html
<div class="wipe" aria-hidden="true" style="position:absolute;inset:0;z-index:20;
     display:grid;grid-template-columns:repeat(8,1fr);opacity:0;pointer-events:none;">
  <div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div>
</div>
<style> #stage .wipe>div { background:#16140F; transform:scaleY(0); transform-origin:top; } </style>
```
```js
tl.set('.wipe', { opacity:1 }, T);
tl.to('.wipe>div', { scaleY:1, duration:0.25, stagger:0.025, ease:'power2.in' }, T);
tl.set(OUT, { visibility:'hidden' }, T + 0.26);   // swap hidden behind closed blinds
tl.set(IN,  { visibility:'visible' }, T + 0.24);
tl.to('.wipe>div', { scaleY:0, transformOrigin:'bottom', duration:0.30, stagger:0.018, ease:'power3.out' }, T + 0.28);
tl.set('.wipe', { opacity:0 }, T + 0.7);
```

### paper-flash — warm-paper bloom (gentlest cut)
A full-canvas paper-colored sheet blooms to ~0.9 then fades, washing one scene
into the next. Add `<div class="flash" style="position:absolute;inset:0;
z-index:25;background:#F5F5EE;opacity:0;pointer-events:none;"></div>` to `#stage`.
```js
tl.to('.flash', { opacity:0.92, duration:0.18, ease:'power2.in' }, T);
tl.set(IN,  { visibility:'visible' }, T + 0.14);
tl.set(OUT, { visibility:'hidden' },  T + 0.16);
tl.to('.flash', { opacity:0, duration:0.38, ease:'power3.out' }, T + 0.16);
```

**Pick ONE transition per cut** (恰到好处). A good montage rhythm: open with a
`settle`, whip-pan into the grid, blinds-wipe into the proof collage, paper-flash
into the closing print-stack. Don't strobe all three every cut.

---

## Frame & outro notes

- **Frame = `clean` always.** Asset panels carry their own 3px ink border;
  adding a `hairline`/`polaroid` deco double-borders and cheapens it.
- **Re-theme the `card-cta` outro to match** (per SKILL.md Step 6): the shipped
  outro is dark "Editorial Cinema" — for an editorial-print video swap its
  palette to `--paper`/`--ink`, keep the entrance rig. A warm-paper footer-panel
  motto bar (primitive 5) can double as the closing beat before the CTA.
