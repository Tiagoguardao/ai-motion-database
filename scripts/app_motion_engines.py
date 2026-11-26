#!/usr/bin/env python3
"""
24 deeply engineered, distinct interactive UI motion engines for Motion Index.
Each engine returns (html, css, js, extractableCode) strictly scoped to `.m-app-<slug>`
with unique `@keyframes m-<slug>-*`, interactive pointer/click/drag handlers,
gentle auto-demo cycling, and a clean disposer function.
"""
import html as _h
import json as _j


def _e(s: str) -> str:
    return _h.escape(str(s), quote=True)


def _cid(slug: str) -> str:
    return "m-app-" + slug


def _kf(slug: str, name: str) -> str:
    return f"m-{slug}-{name}"


def _base_vars(c: dict) -> tuple[str, str, str, str, str, str]:
    dark = c.get("surface", "dark") == "dark"
    bg = c.get("bg") or ("#0d0f14" if dark else "#f5f6f8")
    card = c.get("card") or ("#171a22" if dark else "#ffffff")
    fg = c.get("fg") or ("#f4f5f7" if dark else "#101114")
    mute = c.get("mute") or ("rgba(255,255,255,.56)" if dark else "#6b7280")
    acc = c.get("accent") or "#2a94e2"
    acc2 = c.get("accent2") or acc
    return bg, card, fg, mute, acc, acc2


# 1. Numpad spring amount bounce & send pill
def eng_numpad_spring(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    sym = _e(c.get("currency", "$"))
    amounts = c.get("amounts", ["25", "45", "120", "85"])
    cta = _e(c.get("cta", "Pay"))
    sub = _e(c.get("sub", "Instant transfer"))
    html = (
        f'<div class="{k}">'
        f'<div class="{k}__amt"><span>{sym}</span><b>{_e(amounts[0])}</b></div>'
        f'<div class="{k}__sub">{sub}</div>'
        f'<div class="{k}__pad">'
        f'<button type="button" data-d="1">1</button><button type="button" data-d="2">2</button><button type="button" data-d="5">5</button>'
        f'<button type="button" data-d="0">0</button><button type="button" class="{k}__cta">{cta}</button>'
        f'</div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__amt{{display:flex;align-items:baseline;gap:2px;font:800 38px/1 'Host Grotesk',sans-serif;letter-spacing:-.04em;transition:transform .28s cubic-bezier(.22,1.4,.36,1)}}"
        f".{k}__amt span{{font-size:22px;opacity:.75}}"
        f".{k}__amt.is-pop{{animation:{kf('pop')} .34s cubic-bezier(.22,1.45,.36,1)}}"
        f"@keyframes {kf('pop')}{{0%{{transform:scale(.84)}}55%{{transform:scale(1.12)}}100%{{transform:scale(1)}}}}"
        f".{k}__sub{{font:500 11px/1 'Geist Mono',monospace;color:{mute};letter-spacing:.02em}}"
        f".{k}__pad{{display:flex;align-items:center;gap:6px;margin-top:4px}}"
        f".{k}__pad button{{height:34px;min-width:34px;padding:0 10px;border:1px solid rgba(128,128,128,.2);border-radius:10px;background:{card};color:{fg};font:600 13px/1 'Geist Mono',monospace;cursor:pointer;transition:transform .12s,background .18s}}"
        f".{k}__pad button:active{{transform:scale(.9)}}"
        f".{k}__pad .{k}__cta{{padding:0 16px;border-radius:999px;border:0;background:{acc};color:#fff;font-family:'Host Grotesk',sans-serif;font-weight:700;box-shadow:0 6px 18px {acc}44}}"
        f".{k}__pad .{k}__cta.is-sent{{background:{acc2};transform:scale(1.06)}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var amt=el.querySelector('.{k}__amt'),num=amt.querySelector('b'),cta=el.querySelector('.{k}__cta');"
        f"var presets={_j.dumps(amounts)},idx=0,cur=presets[0],touched=false,dead=false;"
        f"function pop(v){{num.textContent=v;amt.classList.remove('is-pop');void amt.offsetWidth;amt.classList.add('is-pop');}}"
        f"el.querySelectorAll('[data-d]').forEach(function(b){{b.addEventListener('click',function(){{touched=true;cur=(cur.length>=4?'':cur)+b.dataset.d;pop(cur||'0');}});}});"
        f"cta.addEventListener('click',function(){{touched=true;cta.classList.add('is-sent');cta.textContent='Sent ✓';setTimeout(function(){{cta.classList.remove('is-sent');cta.textContent={_j.dumps(c.get('cta','Pay'))};}},900);}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden){{idx=(idx+1)%presets.length;cur=presets[idx];pop(cur);}}}},1750);"
        f"return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Numpad Spring')} -->\n<div class=\"{k}\">{html}</div>\n<style>{css}</style>"
    return html, css, js, code


# 2. Interactive SVG Sparkline Scrub & Price Ticker
def eng_sparkline_scrub(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    label = _e(c.get("label", "Portfolio"))
    unit = _e(c.get("unit", "$"))
    pts = c.get("points", [48, 42, 46, 34, 38, 24, 29, 18, 22, 12])
    vals = c.get("values", ["14,210", "14,390", "14,320", "14,680", "14,590", "15,040", "14,910", "15,320", "15,210", "15,640"])
    delta = _e(c.get("delta", "+6.4% today"))
    step = 200 / (len(pts) - 1)
    coords = [(round(i * step, 1), y) for i, y in enumerate(pts)]
    d_line = "M" + " L".join(f"{x} {y}" for x, y in coords)
    d_area = d_line + f" L200 66 L0 66 Z"
    html = (
        f'<div class="{k}"><div class="{k}__card">'
        f'<div class="{k}__top"><span>{label}</span><em class="{k}__d">{delta}</em></div>'
        f'<div class="{k}__val">{unit}<b>{_e(vals[-1])}</b></div>'
        f'<svg class="{k}__svg" viewBox="0 0 200 66" preserveAspectRatio="none">'
        f'<defs><linearGradient id="{kf("g")}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{acc}" stop-opacity=".35"/><stop offset="100%" stop-color="{acc}" stop-opacity="0"/></linearGradient></defs>'
        f'<path class="{k}__area" d="{d_area}" fill="url(#{kf("g")})"/>'
        f'<path class="{k}__line" d="{d_line}" fill="none" stroke="{acc}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<line class="{k}__guide" x1="{coords[-1][0]}" y1="4" x2="{coords[-1][0]}" y2="64" stroke="{acc}" stroke-opacity=".35" stroke-dasharray="2 3"/>'
        f'<circle class="{k}__dot" cx="{coords[-1][0]}" cy="{coords[-1][1]}" r="4.5" fill="{acc}" stroke="{card}" stroke-width="2"/>'
        f'</svg></div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__card{{width:min(86%,256px);padding:14px 16px;border-radius:16px;background:{card};border:1px solid rgba(128,128,128,.16);cursor:ew-resize;display:flex;flex-direction:column;gap:5px}}"
        f".{k}__top{{display:flex;justify-content:space-between;align-items:center;font-size:11px;color:{mute}}}"
        f".{k}__d{{font-style:normal;font:600 10.5px/1 'Geist Mono',monospace;color:{acc}}}"
        f".{k}__val{{font:700 22px/1.1 'Geist Mono',monospace;letter-spacing:-.03em}}"
        f".{k}__svg{{width:100%;height:66px;overflow:visible;margin-top:4px}}"
        f".{k}__dot,.{k}__guide{{transition:all .16s cubic-bezier(.22,1,.36,1)}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var card=el.querySelector('.{k}__card'),dot=el.querySelector('.{k}__dot'),guide=el.querySelector('.{k}__guide'),val=el.querySelector('.{k}__val b');"
        f"var coords={_j.dumps(coords)},vals={_j.dumps(vals)},idx=coords.length-1,touched=false,dead=false;"
        f"function setIdx(i){{i=Math.max(0,Math.min(coords.length-1,i));dot.setAttribute('cx',coords[i][0]);dot.setAttribute('cy',coords[i][1]);guide.setAttribute('x1',coords[i][0]);guide.setAttribute('x2',coords[i][0]);val.textContent=vals[i];}}"
        f"card.addEventListener('pointermove',function(e){{touched=true;var r=card.getBoundingClientRect();var p=Math.max(0,Math.min(1,(e.clientX-r.left)/r.width));setIdx(Math.round(p*(coords.length-1)));}});"
        f"card.addEventListener('click',function(){{touched=true;idx=(idx+2)%coords.length;setIdx(idx);}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden){{idx=(idx+1)%coords.length;setIdx(idx);}}}},900);"
        f"return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Sparkline Scrub')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 3. Radial Ring / Multi-Arc Score Gauge
def eng_ring_gauge(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    label = _e(c.get("label", "Readiness"))
    unit = _e(c.get("unit", ""))
    scores = c.get("scores", [88, 94, 72, 91])
    tag = _e(c.get("tag", "Optimal"))
    r = 42
    circ = round(2 * 3.14159 * r, 1)
    r2 = 31
    circ2 = round(2 * 3.14159 * r2, 1)
    html = (
        f'<div class="{k}"><button type="button" class="{k}__btn">'
        f'<svg class="{k}__svg" viewBox="0 0 112 112">'
        f'<circle cx="56" cy="56" r="{r}" fill="none" stroke="rgba(128,128,128,.18)" stroke-width="7"/>'
        f'<circle class="{k}__arc1" cx="56" cy="56" r="{r}" fill="none" stroke="{acc}" stroke-width="7" stroke-linecap="round" stroke-dasharray="{circ}" stroke-dashoffset="{circ}" transform="rotate(-90 56 56)"/>'
        f'<circle cx="56" cy="56" r="{r2}" fill="none" stroke="rgba(128,128,128,.12)" stroke-width="5"/>'
        f'<circle class="{k}__arc2" cx="56" cy="56" r="{r2}" fill="none" stroke="{acc2}" stroke-width="5" stroke-linecap="round" stroke-dasharray="{circ2}" stroke-dashoffset="{circ2}" transform="rotate(-90 56 56)"/>'
        f'</svg>'
        f'<div class="{k}__mid"><b>{scores[0]}{unit}</b><span>{label}</span></div>'
        f'<em class="{k}__tag">{tag}</em>'
        f'</button></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__btn{{position:relative;border:0;background:none;color:inherit;display:flex;flex-direction:column;align-items:center;gap:8px;cursor:pointer;padding:8px}}"
        f".{k}__svg{{width:116px;height:116px;overflow:visible;filter:drop-shadow(0 0 12px {acc}33)}}"
        f".{k}__arc1,.{k}__arc2{{transition:stroke-dashoffset .72s cubic-bezier(.22,1,.36,1)}}"
        f".{k}__mid{{position:absolute;top:40px;display:flex;flex-direction:column;align-items:center}}"
        f".{k}__mid b{{font:700 22px/1 'Geist Mono',monospace;letter-spacing:-.03em}}"
        f".{k}__mid span{{font:500 9.5px/1.2 inherit;color:{mute};margin-top:3px;text-transform:uppercase;letter-spacing:.06em}}"
        f".{k}__tag{{font-style:normal;font:600 11px/1 'Geist Mono',monospace;padding:4px 10px;border-radius:999px;background:{card};border:1px solid rgba(128,128,128,.18);color:{acc}}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var btn=el.querySelector('.{k}__btn'),a1=el.querySelector('.{k}__arc1'),a2=el.querySelector('.{k}__arc2'),num=el.querySelector('.{k}__mid b');"
        f"var scores={_j.dumps(scores)},unit={_j.dumps(c.get('unit',''))},c1={circ},c2={circ2},idx=0,touched=false,dead=false;"
        f"function apply(s){{var p=Math.max(8,Math.min(100,s))/100;a1.style.strokeDashoffset=(c1*(1-p)).toFixed(1);a2.style.strokeDashoffset=(c2*(1-Math.min(1,p*0.86))).toFixed(1);num.textContent=s+unit;}}"
        f"btn.addEventListener('click',function(){{touched=true;idx=(idx+1)%scores.length;apply(scores[idx]);}});"
        f"var t0=setTimeout(function(){{if(!dead)apply(scores[0]);}},180);"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden){{idx=(idx+1)%scores.length;apply(scores[idx]);}}}},2200);"
        f"return function(){{dead=true;clearTimeout(t0);clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Radial Ring Gauge')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 4. Spring Card Swipe Deck (LIKE / NOPE / Queue stamp)
def eng_card_swipe_deck(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    cards = c.get("cards", [("Maya, 26", "Product Designer · 2 mi"), ("Alex, 29", "Architect · 4 mi"), ("Sora, 25", "Motion Lead · 1 mi")])
    stamp_r = _e(c.get("stampR", "LIKE"))
    stamp_l = _e(c.get("stampL", "NOPE"))
    html = (
        f'<div class="{k}"><div class="{k}__stack">'
        f'<div class="{k}__back"></div>'
        f'<div class="{k}__front"><span class="{k}__st {k}__stR">{stamp_r}</span><span class="{k}__st {k}__stL">{stamp_l}</span>'
        f'<div class="{k}__meta"><b>{_e(cards[0][0])}</b><span>{_e(cards[0][1])}</span></div></div>'
        f'</div><div class="{k}__acts">'
        f'<button type="button" class="{k}__no">✕</button><button type="button" class="{k}__yes">♥</button>'
        f'</div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__stack{{position:relative;width:min(74%,204px);height:126px}}"
        f".{k}__back,.{k}__front{{position:absolute;inset:0;border-radius:16px;border:1px solid rgba(128,128,128,.18)}}"
        f".{k}__back{{background:{card};transform:scale(.93) translateY(8px);opacity:.65}}"
        f".{k}__front{{background:linear-gradient(145deg,{acc}dd,{acc2}99 55%,{card});color:#fff;padding:14px;display:flex;flex-direction:column;justify-content:flex-end;box-shadow:0 12px 26px rgba(0,0,0,.28);cursor:pointer;transition:transform .42s cubic-bezier(.22,1.2,.36,1),opacity .32s}}"
        f".{k}__front.is-r{{transform:translate(86px,-12px) rotate(14deg);opacity:0}}"
        f".{k}__front.is-l{{transform:translate(-86px,-12px) rotate(-14deg);opacity:0}}"
        f".{k}__st{{position:absolute;top:12px;padding:3px 8px;border-radius:6px;border:2px solid currentColor;font:800 10px/1 'Geist Mono',monospace;opacity:0;transition:opacity .16s}}"
        f".{k}__stR{{left:12px;color:#4ade80;transform:rotate(-10deg)}}"
        f".{k}__stL{{right:12px;color:#fb7185;transform:rotate(10deg)}}"
        f".{k}__front.is-r .{k}__stR,.{k}__front.is-l .{k}__stL{{opacity:1}}"
        f".{k}__meta b{{display:block;font:700 15px/1.15 inherit}}.{k}__meta span{{font-size:11px;opacity:.82}}"
        f".{k}__acts{{display:flex;gap:14px}}"
        f".{k}__acts button{{width:34px;height:34px;border-radius:50%;border:1px solid rgba(128,128,128,.2);background:{card};color:{fg};font-size:14px;cursor:pointer;transition:transform .16s}}"
        f".{k}__acts button:active{{transform:scale(.88)}}.{k}__yes{{color:{acc}!important}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var fr=el.querySelector('.{k}__front'),b=fr.querySelector('.{k}__meta b'),sp=fr.querySelector('.{k}__meta span');"
        f"var cards={_j.dumps(cards)},idx=0,touched=false,dead=false,busy=false;"
        f"function swipe(dir){{if(busy)return;busy=true;fr.classList.add(dir>0?'is-r':'is-l');setTimeout(function(){{if(dead)return;idx=(idx+1)%cards.length;b.textContent=cards[idx][0];sp.textContent=cards[idx][1];fr.style.transition='none';fr.classList.remove('is-r','is-l');fr.style.transform='scale(.92) translateY(8px)';fr.style.opacity='.6';void fr.offsetWidth;fr.style.transition='';fr.style.transform='';fr.style.opacity='';busy=false;}},380);}}"
        f"el.querySelector('.{k}__yes').addEventListener('click',function(){{touched=true;swipe(1);}});"
        f"el.querySelector('.{k}__no').addEventListener('click',function(){{touched=true;swipe(-1);}});"
        f"fr.addEventListener('click',function(){{touched=true;swipe(1);}});"
        f"var turn=0,iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden){{swipe(turn++%2===0?1:-1);}}}},2000);"
        f"return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Spring Card Swipe Deck')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 5. 3D Interactive Card Freeze / Tilt / Holographic Foil
def eng_card_freeze_tilt(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    brand = _e(c.get("brand", "CARD"))
    num = _e(c.get("num", "•••• 4821"))
    btn_lbl = _e(c.get("toggle", "Freeze card"))
    alt_lbl = _e(c.get("toggleAlt", "Frozen ❄"))
    html = (
        f'<div class="{k}"><div class="{k}__card">'
        f'<div class="{k}__sheen"></div><div class="{k}__frost"></div>'
        f'<div class="{k}__row"><b>{brand}</b><i>NFC</i></div>'
        f'<div class="{k}__num">{num}</div>'
        f'</div><button type="button" class="{k}__btn">{btn_lbl}</button></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;background:{bg};color:{fg};perspective:680px;user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__card{{position:relative;width:min(78%,222px);height:126px;border-radius:16px;padding:15px 16px;background:linear-gradient(135deg,{acc},{acc2});color:#fff;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden;box-shadow:0 16px 32px rgba(0,0,0,.32);transition:transform .35s cubic-bezier(.22,1,.36,1),filter .35s;cursor:pointer}}"
        f".{k}__sheen{{position:absolute;inset:-40%;background:linear-gradient(115deg,transparent 35%,rgba(255,255,255,.38) 50%,transparent 65%);transform:translateX(-60%);transition:transform .55s cubic-bezier(.22,1,.36,1);pointer-events:none}}"
        f".{k}__card:hover .{k}__sheen,.{k}__card.is-tilt .{k}__sheen{{transform:translateX(60%)}}"
        f".{k}__frost{{position:absolute;inset:0;background:linear-gradient(135deg,rgba(200,235,255,.68),rgba(235,248,255,.45));backdrop-filter:blur(5px);clip-path:inset(0 100% 0 0);transition:clip-path .48s cubic-bezier(.22,1,.36,1);pointer-events:none}}"
        f".{k}__card.is-frozen .{k}__frost{{clip-path:inset(0 0 0 0)}}"
        f".{k}__card.is-frozen{{filter:saturate(.35)}}"
        f".{k}__row{{position:relative;display:flex;justify-content:space-between;align-items:center;font-size:13px}}.{k}__row i{{font-style:normal;font:600 9.5px/1 'Geist Mono',monospace;opacity:.8}}"
        f".{k}__num{{position:relative;font:600 13.5px/1 'Geist Mono',monospace;letter-spacing:.08em}}"
        f".{k}__btn{{height:30px;padding:0 14px;border-radius:999px;border:1px solid rgba(128,128,128,.22);background:{card};color:{fg};font:600 11.5px/1 inherit;cursor:pointer;transition:transform .16s}}"
        f".{k}__btn:active{{transform:scale(.94)}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var card=el.querySelector('.{k}__card'),btn=el.querySelector('.{k}__btn');"
        f"var frozen=false,touched=false,dead=false,l1={_j.dumps(c.get('toggle','Freeze card'))},l2={_j.dumps(c.get('toggleAlt','Frozen ❄'))};"
        f"function flip(){{frozen=!frozen;card.classList.toggle('is-frozen',frozen);card.classList.toggle('is-tilt',!frozen);btn.textContent=frozen?l2:l1;card.style.transform=frozen?'rotateY(-8deg) rotateX(4deg) scale(.97)':'rotateY(8deg) rotateX(5deg)';}}"
        f"card.addEventListener('pointermove',function(e){{touched=true;var r=card.getBoundingClientRect();var x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;card.style.transform='rotateY('+(x*22).toFixed(1)+'deg) rotateX('+(-y*16).toFixed(1)+'deg)';}});"
        f"card.addEventListener('pointerleave',function(){{card.style.transform='';}});"
        f"btn.addEventListener('click',function(){{touched=true;flip();}});card.addEventListener('click',function(){{touched=true;flip();}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)flip();}},2200);"
        f"return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','3D Card Tilt & Freeze')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 6. Interactive Audio / Voice Waveform Scrubber
def eng_waveform_audio(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    title = _e(c.get("track", "Voice Note · 0:24"))
    bars = c.get("bars", [28, 52, 74, 44, 88, 66, 95, 58, 40, 82, 92, 54, 36, 70, 86, 48, 62, 34])
    bars_html = "".join(f'<i style="height:{h}%"></i>' for h in bars)
    html = (
        f'<div class="{k}"><div class="{k}__pill">'
        f'<button type="button" class="{k}__play" aria-label="Play">▶</button>'
        f'<div class="{k}__mid"><div class="{k}__bars">{bars_html}</div>'
        f'<div class="{k}__meta"><span>{title}</span><b class="{k}__t">0:11</b></div></div>'
        f'</div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__pill{{width:min(88%,266px);padding:12px 14px;border-radius:18px;background:{card};border:1px solid rgba(128,128,128,.18);display:flex;align-items:center;gap:12px}}"
        f".{k}__play{{width:38px;height:38px;flex:none;border:0;border-radius:50%;background:{acc};color:#fff;font-size:13px;cursor:pointer;display:grid;place-items:center;transition:transform .16s cubic-bezier(.22,1.3,.36,1)}}"
        f".{k}__play:active{{transform:scale(.88)}}"
        f".{k}__mid{{flex:1;min-width:0;display:flex;flex-direction:column;gap:7px}}"
        f".{k}__bars{{display:flex;align-items:center;gap:3px;height:34px;cursor:pointer}}"
        f".{k}__bars i{{flex:1;border-radius:3px;background:rgba(128,128,128,.28);transition:background .16s,transform .22s cubic-bezier(.22,1.2,.36,1)}}"
        f".{k}__bars i.is-on{{background:{acc}}}"
        f".{k}.is-play .{k}__bars i.is-cur{{transform:scaleY(1.22);background:{acc2}}}"
        f".{k}__meta{{display:flex;justify-content:space-between;font:500 10.5px/1 'Geist Mono',monospace;color:{mute}}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var play=el.querySelector('.{k}__play'),wrap=el.querySelector('.{k}__bars'),bars=[].slice.call(wrap.children),tm=el.querySelector('.{k}__t');"
        f"var playing=true,pos=6,dead=false;"
        f"function paint(){{bars.forEach(function(b,i){{b.classList.toggle('is-on',i<=pos);b.classList.toggle('is-cur',i===pos);}});tm.textContent='0:'+String(pos+4).padStart(2,'0');el.classList.toggle('is-play',playing);play.textContent=playing?'❚❚':'▶';}}"
        f"play.addEventListener('click',function(){{playing=!playing;paint();}});"
        f"wrap.addEventListener('click',function(e){{var r=wrap.getBoundingClientRect();pos=Math.max(0,Math.min(bars.length-1,Math.floor(((e.clientX-r.left)/r.width)*bars.length)));paint();}});"
        f"var iv=setInterval(function(){{if(playing&&!dead&&!document.hidden){{pos=(pos+1)%bars.length;paint();}}}},260);"
        f"paint();return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Audio Waveform Scrubber')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 7. Organic Breathing / Voice-Reactive Orb
def eng_orb_voice_aura(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    states = c.get("states", ["Listening…", "Thinking", "Speaking"])
    html = (
        f'<div class="{k}"><button type="button" class="{k}__stage">'
        f'<span class="{k}__r1"></span><span class="{k}__r2"></span>'
        f'<span class="{k}__orb"></span>'
        f'<em class="{k}__lbl">{_e(states[0])}</em>'
        f'</button></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__stage{{position:relative;border:0;background:none;color:inherit;display:flex;flex-direction:column;align-items:center;gap:16px;cursor:pointer;padding:12px}}"
        f".{k}__r1,.{k}__r2{{position:absolute;top:12px;width:82px;height:82px;border-radius:50%;border:1.5px solid {acc}66;animation:{kf('rip')} 2.6s cubic-bezier(.16,1,.3,1) infinite;pointer-events:none}}"
        f".{k}__r2{{animation-delay:1.3s}}"
        f"@keyframes {kf('rip')}{{0%{{transform:scale(.9);opacity:.7}}100%{{transform:scale(1.85);opacity:0}}}}"
        f".{k}__orb{{width:82px;height:82px;border-radius:50%;background:radial-gradient(circle at 32% 28%,#fff8,{acc} 48%,{acc2});box-shadow:0 0 32px {acc}55;transition:transform .52s cubic-bezier(.22,1.25,.36,1),border-radius .52s ease}}"
        f".{k}.s1 .{k}__orb{{transform:scale(1.14, .92);border-radius:46% 54% 52% 48%/54% 46% 54% 46%}}"
        f".{k}.s2 .{k}__orb{{transform:scale(.94, 1.12);border-radius:54% 46% 45% 55%/46% 55% 45% 54%}}"
        f".{k}__lbl{{font-style:normal;font:500 11.5px/1 'Geist Mono',monospace;color:{mute}}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var btn=el.querySelector('.{k}__stage'),lbl=el.querySelector('.{k}__lbl');"
        f"var states={_j.dumps(states)},idx=0,touched=false,dead=false;"
        f"function step(){{idx=(idx+1)%states.length;el.classList.remove('s1','s2');if(idx===1)el.classList.add('s1');if(idx===2)el.classList.add('s2');lbl.textContent=states[idx];}}"
        f"btn.addEventListener('click',function(){{touched=true;step();}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)step();}},1650);"
        f"return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Voice Orb Aura')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 8. Slide-to-Confirm / Unlock Rail
def eng_swipe_rail_cta(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    prompt = _e(c.get("prompt", "Slide to confirm"))
    done = _e(c.get("done", "Confirmed ✓"))
    html = (
        f'<div class="{k}"><div class="{k}__rail" role="button" tabindex="0">'
        f'<div class="{k}__fill"></div>'
        f'<span class="{k}__txt">{prompt}</span>'
        f'<div class="{k}__knob">→</div>'
        f'</div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__rail{{position:relative;width:min(84%,238px);height:48px;border-radius:999px;background:{card};border:1px solid rgba(128,128,128,.22);overflow:hidden;cursor:pointer;display:grid;place-items:center}}"
        f".{k}__fill{{position:absolute;inset:0;background:{acc};transform:scaleX(0);transform-origin:left center;transition:transform .52s cubic-bezier(.22,1,.36,1)}}"
        f".{k}__rail.is-done .{k}__fill{{transform:scaleX(1)}}"
        f".{k}__txt{{position:relative;z-index:2;font:600 12.5px/1 inherit;color:{mute};transition:color .25s}}"
        f".{k}__rail.is-done .{k}__txt{{color:#fff}}"
        f".{k}__knob{{position:absolute;left:4px;top:4px;width:40px;height:40px;border-radius:50%;background:{acc};color:#fff;font:700 16px/1 inherit;display:grid;place-items:center;z-index:3;box-shadow:0 4px 12px rgba(0,0,0,.28);transition:transform .52s cubic-bezier(.22,1.14,.36,1),background .25s}}"
        f".{k}__rail.is-done .{k}__knob{{transform:translateX(190px);background:#fff;color:{acc}}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var rail=el.querySelector('.{k}__rail'),txt=el.querySelector('.{k}__txt'),knob=el.querySelector('.{k}__knob');"
        f"var on=false,touched=false,dead=false,t1={_j.dumps(c.get('prompt','Slide to confirm'))},t2={_j.dumps(c.get('done','Confirmed ✓'))};"
        f"function tog(){{on=!on;rail.classList.toggle('is-done',on);txt.textContent=on?t2:t1;knob.textContent=on?'✓':'→';var w=rail.clientWidth-48;knob.style.transform=on?'translateX('+Math.max(120,w)+'px)':'translateX(0px)';}}"
        f"rail.addEventListener('click',function(){{touched=true;tog();}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)tog();}},2000);"
        f"return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Slide-to-Confirm Rail')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 9. Radar / Live Map Route Tracker
def eng_radar_map_tracker(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    badge = _e(c.get("badge", "3 min away"))
    marker = _e(c.get("marker", "●"))
    html = (
        f'<div class="{k}"><div class="{k}__map">'
        f'<svg class="{k}__svg" viewBox="0 0 240 130">'
        f'<path d="M22 104 Q90 88 122 60 T214 28" fill="none" stroke="rgba(128,128,128,.22)" stroke-width="5" stroke-linecap="round"/>'
        f'<path class="{k}__route" d="M22 104 Q90 88 122 60 T214 28" fill="none" stroke="{acc}" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="260" stroke-dashoffset="260"/>'
        f'<circle cx="214" cy="28" r="14" fill="{acc}" opacity=".18" class="{k}__ping"/>'
        f'<circle cx="214" cy="28" r="5" fill="{acc}"/>'
        f'</svg>'
        f'<span class="{k}__pin">{marker}</span>'
        f'<button type="button" class="{k}__eta">{badge}</button>'
        f'</div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__map{{position:relative;width:min(88%,262px);height:150px;border-radius:16px;background:{card};border:1px solid rgba(128,128,128,.16);overflow:hidden;background-image:radial-gradient(rgba(128,128,128,.14) 1px,transparent 1px);background-size:16px 16px}}"
        f".{k}__svg{{position:absolute;inset:0;width:100%;height:100%}}"
        f".{k}__route{{transition:stroke-dashoffset 1.2s cubic-bezier(.22,1,.36,1)}}"
        f".{k}.is-go .{k}__route{{stroke-dashoffset:0}}"
        f".{k}__ping{{transform-origin:214px 28px;animation:{kf('ping')} 1.8s ease-out infinite}}"
        f"@keyframes {kf('ping')}{{0%{{transform:scale(.5);opacity:.45}}100%{{transform:scale(1.8);opacity:0}}}}"
        f".{k}__pin{{position:absolute;left:18px;top:92px;width:24px;height:24px;border-radius:50%;background:{acc};color:#fff;font-size:11px;display:grid;place-items:center;box-shadow:0 4px 12px {acc}66;transition:transform 1.15s cubic-bezier(.22,1,.36,1)}}"
        f".{k}.is-go .{k}__pin{{transform:translate(168px,-68px)}}"
        f".{k}__eta{{position:absolute;left:12px;top:12px;border:0;border-radius:999px;padding:5px 11px;background:{bg};color:{fg};font:600 11px/1 'Geist Mono',monospace;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.22)}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var btn=el.querySelector('.{k}__eta'),go=false,touched=false,dead=false;"
        f"function run(){{go=!go;el.classList.toggle('is-go',go);}}"
        f"el.addEventListener('click',function(){{touched=true;run();}});"
        f"var t0=setTimeout(function(){{if(!dead)run();}},220);"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)run();}},2300);"
        f"return function(){{dead=true;clearTimeout(t0);clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Live Map Route Tracker')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 10. Segmented Pill Shared-Layout Glide
def eng_segmented_pill_morph(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    tabs = c.get("tabs", ["Overview", "Activity", "Vaults"])
    vals = c.get("tabVals", ["$8,420", "14 today", "4.8% APY"])
    btns = "".join(f'<button type="button" data-i="{i}">{_e(t)}</button>' for i, t in enumerate(tabs))
    html = (
        f'<div class="{k}"><div class="{k}__box">'
        f'<div class="{k}__seg"><span class="{k}__thumb"></span>{btns}</div>'
        f'<div class="{k}__out"><b>{_e(vals[0])}</b><span>{_e(tabs[0])}</span></div>'
        f'</div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__box{{width:min(86%,256px);display:flex;flex-direction:column;gap:12px}}"
        f".{k}__seg{{position:relative;display:grid;grid-template-columns:repeat({len(tabs)},1fr);padding:4px;border-radius:12px;background:{card};border:1px solid rgba(128,128,128,.16)}}"
        f".{k}__thumb{{position:absolute;top:4px;bottom:4px;left:4px;width:calc((100% - 8px)/{len(tabs)});border-radius:9px;background:{acc};transition:transform .38s cubic-bezier(.22,1.18,.36,1)}}"
        f".{k}__seg button{{position:relative;z-index:2;border:0;background:none;padding:7px 4px;font:600 11.5px/1 inherit;color:{mute};cursor:pointer;transition:color .2s}}"
        f".{k}__seg button.is-on{{color:#fff}}"
        f".{k}__out{{padding:14px;border-radius:14px;background:{card};border:1px solid rgba(128,128,128,.14);display:flex;justify-content:space-between;align-items:baseline;transition:transform .28s cubic-bezier(.22,1.2,.36,1)}}"
        f".{k}__out b{{font:700 18px/1 'Geist Mono',monospace}}.{k}__out span{{font-size:11px;color:{mute}}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var btns=[].slice.call(el.querySelectorAll('.{k}__seg button')),th=el.querySelector('.{k}__thumb'),b=el.querySelector('.{k}__out b'),sp=el.querySelector('.{k}__out span');"
        f"var tabs={_j.dumps(tabs)},vals={_j.dumps(vals)},idx=0,touched=false,dead=false;"
        f"function set(i){{idx=i;th.style.transform='translateX('+(i*100)+'%)';btns.forEach(function(x,j){{x.classList.toggle('is-on',j===i);}});b.textContent=vals[i];sp.textContent=tabs[i];}}"
        f"btns.forEach(function(x,i){{x.addEventListener('click',function(){{touched=true;set(i);}});}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)set((idx+1)%tabs.length);}},1800);"
        f"set(0);return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Segmented Pill Glide')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 11. Multi-Step Milestone / Delivery Progress Flow
def eng_stepper_progress_flow(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    steps = c.get("steps", ["Placed", "Preparing", "En Route", "Arrived"])
    nodes = "".join(f'<button type="button" class="{k}__n" data-i="{i}"><i>{i+1}</i><span>{_e(s)}</span></button>' for i, s in enumerate(steps))
    html = (
        f'<div class="{k}"><div class="{k}__card">'
        f'<div class="{k}__bar"><span class="{k}__fill"></span></div>'
        f'<div class="{k}__row">{nodes}</div>'
        f'</div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__card{{width:min(88%,268px);padding:18px 14px;border-radius:16px;background:{card};border:1px solid rgba(128,128,128,.16);position:relative}}"
        f".{k}__bar{{position:relative;height:4px;border-radius:999px;background:rgba(128,128,128,.2);margin:12px 18px 0}}"
        f".{k}__fill{{position:absolute;inset:0;width:33%;border-radius:999px;background:{acc};transition:width .45s cubic-bezier(.22,1.15,.36,1)}}"
        f".{k}__row{{display:flex;justify-content:space-between;margin-top:-15px;position:relative;z-index:2}}"
        f".{k}__n{{border:0;background:none;color:{mute};display:flex;flex-direction:column;align-items:center;gap:7px;cursor:pointer;padding:0}}"
        f".{k}__n i{{width:26px;height:26px;border-radius:50%;background:{card};border:2px solid rgba(128,128,128,.3);font:700 11px/1 'Geist Mono',monospace;font-style:normal;display:grid;place-items:center;transition:all .32s cubic-bezier(.22,1.35,.36,1)}}"
        f".{k}__n.is-done i{{background:{acc};border-color:{acc};color:#fff}}"
        f".{k}__n.is-cur i{{transform:scale(1.2);box-shadow:0 0 0 5px {acc}33}}"
        f".{k}__n span{{font:600 10px/1 inherit}}.{k}__n.is-cur span{{color:{fg}}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var ns=[].slice.call(el.querySelectorAll('.{k}__n')),fill=el.querySelector('.{k}__fill');"
        f"var idx=1,touched=false,dead=false;"
        f"function go(i){{idx=i;fill.style.width=(i/(ns.length-1)*100)+'%';ns.forEach(function(n,j){{n.classList.toggle('is-done',j<=i);n.classList.toggle('is-cur',j===i);}});}}"
        f"ns.forEach(function(n,i){{n.addEventListener('click',function(){{touched=true;go(i);}});}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)go((idx+1)%ns.length);}},1550);"
        f"go(1);return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Milestone Stepper Flow')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 12. Social Reaction Burst & Odometer
def eng_reaction_burst_social(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    author = _e(c.get("author", "@motionlab"))
    body = _e(c.get("body", "Crisp spring feedback makes every tap feel alive."))
    icon = _e(c.get("icon", "♥"))
    base_n = int(c.get("count", 142))
    html = (
        f'<div class="{k}"><div class="{k}__card">'
        f'<div class="{k}__top"><b>{author}</b><span>2m</span></div>'
        f'<p>{body}</p>'
        f'<div class="{k}__row"><button type="button" class="{k}__btn"><i>{icon}</i><em>{base_n}</em><span class="{k}__sparks"></span></button></div>'
        f'</div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__card{{width:min(86%,254px);padding:14px 15px;border-radius:16px;background:{card};border:1px solid rgba(128,128,128,.16);display:flex;flex-direction:column;gap:8px}}"
        f".{k}__top{{display:flex;justify-content:space-between;font-size:12px}}.{k}__top span{{color:{mute}}}"
        f".{k}__card p{{margin:0;font-size:12.5px;line-height:1.4;color:{mute}}}"
        f".{k}__btn{{position:relative;display:inline-flex;align-items:center;gap:6px;height:32px;padding:0 12px;border-radius:999px;border:1px solid rgba(128,128,128,.2);background:transparent;color:{fg};font:600 12px/1 'Geist Mono',monospace;cursor:pointer;transition:all .2s}}"
        f".{k}__btn i{{font-style:normal;font-size:14px;display:inline-block;transition:transform .38s cubic-bezier(.22,1.4,.36,1)}}"
        f".{k}__btn em{{font-style:normal}}"
        f".{k}__btn.is-on{{background:{acc}1f;border-color:{acc}66;color:{acc}}}"
        f".{k}__btn.is-on i{{transform:scale(1.3) rotate(-8deg)}}"
        f".{k}__sparks{{position:absolute;left:16px;top:16px;pointer-events:none}}"
        f".{k}__dot{{position:absolute;width:5px;height:5px;border-radius:50%;background:{acc};animation:{kf('sp')} .48s cubic-bezier(.16,1,.3,1) forwards}}"
        f"@keyframes {kf('sp')}{{0%{{transform:translate(0,0) scale(1);opacity:1}}100%{{transform:translate(var(--x),var(--y)) scale(0);opacity:0}}}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var btn=el.querySelector('.{k}__btn'),em=btn.querySelector('em'),sp=btn.querySelector('.{k}__sparks');"
        f"var on=false,base={base_n},touched=false,dead=false;"
        f"function fire(){{on=!on;btn.classList.toggle('is-on',on);em.textContent=String(on?base+1:base);if(on){{sp.innerHTML='';for(var i=0;i<6;i++){{var a=i*Math.PI/3,d=16+Math.random()*8,p=document.createElement('span');p.className='{k}__dot';p.style.setProperty('--x',(Math.cos(a)*d).toFixed(1)+'px');p.style.setProperty('--y',(Math.sin(a)*d).toFixed(1)+'px');sp.appendChild(p);}}}}}}"
        f"btn.addEventListener('click',function(){{touched=true;fire();}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)fire();}},1850);"
        f"return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Reaction Burst')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 13. Tactile Rotary Dial / Haptic Knob Scrub
def eng_dial_knob_scrub(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    label = _e(c.get("label", "FOCUS"))
    vals = c.get("vals", ["f/1.8", "f/2.4", "f/4.0", "f/5.6", "f/8.0"])
    ticks = "".join(f'<i style="transform:rotate({a}deg)"></i>' for a in range(-120, 121, 20))
    html = (
        f'<div class="{k}"><button type="button" class="{k}__dial">'
        f'<div class="{k}__ticks">{ticks}</div>'
        f'<div class="{k}__needle"><span></span></div>'
        f'<div class="{k}__val"><b>{_e(vals[2])}</b><small>{label}</small></div>'
        f'</button></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__dial{{position:relative;width:128px;height:128px;border-radius:50%;border:1px solid rgba(128,128,128,.22);background:{card};color:{fg};cursor:pointer;display:grid;place-items:center;box-shadow:0 10px 26px rgba(0,0,0,.25)}}"
        f".{k}__ticks{{position:absolute;inset:8px;pointer-events:none}}"
        f".{k}__ticks i{{position:absolute;left:50%;top:0;width:2px;height:8px;margin-left:-1px;background:rgba(128,128,128,.4);transform-origin:50% 56px;border-radius:1px}}"
        f".{k}__needle{{position:absolute;inset:14px;transition:transform .42s cubic-bezier(.22,1.22,.36,1);pointer-events:none}}"
        f".{k}__needle span{{position:absolute;left:50%;top:0;width:4px;height:14px;margin-left:-2px;border-radius:99px;background:{acc};box-shadow:0 0 10px {acc}}}"
        f".{k}__val{{display:flex;flex-direction:column;align-items:center;gap:2px}}"
        f".{k}__val b{{font:700 18px/1 'Geist Mono',monospace;color:{acc}}}"
        f".{k}__val small{{font:600 9.5px/1 'Geist Mono',monospace;color:{mute};letter-spacing:.08em}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var dial=el.querySelector('.{k}__dial'),nd=el.querySelector('.{k}__needle'),b=el.querySelector('.{k}__val b');"
        f"var vals={_j.dumps(vals)},idx=2,touched=false,dead=false;"
        f"function set(i){{idx=i;var deg=-100+(i/(vals.length-1))*200;nd.style.transform='rotate('+deg+'deg)';b.textContent=vals[i];}}"
        f"dial.addEventListener('click',function(){{touched=true;set((idx+1)%vals.length);}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)set((idx+1)%vals.length);}},1500);"
        f"set(2);return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Tactile Rotary Dial')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 14. Before / After Interactive Split Curtain Scrub
def eng_split_before_after(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    left_lbl = _e(c.get("leftLbl", "RAW"))
    right_lbl = _e(c.get("rightLbl", "EDITED"))
    html = (
        f'<div class="{k}"><div class="{k}__frame">'
        f'<div class="{k}__before"><span>{left_lbl}</span></div>'
        f'<div class="{k}__after"><span>{right_lbl}</span></div>'
        f'<div class="{k}__div"><i>↔</i></div>'
        f'</div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:#fff;user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__frame{{position:relative;width:min(86%,254px);height:146px;border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,.16);cursor:ew-resize}}"
        f".{k}__before,.{k}__after{{position:absolute;inset:0;padding:10px 12px;display:flex;align-items:flex-end}}"
        f".{k}__before{{background:linear-gradient(135deg,#2a2d35,#454b58);justify-content:flex-start}}"
        f".{k}__after{{background:linear-gradient(135deg,{acc},{acc2});justify-content:flex-end;clip-path:inset(0 0 0 50%);transition:clip-path .18s ease-out}}"
        f".{k}__before span,.{k}__after span{{font:600 10px/1 'Geist Mono',monospace;padding:4px 7px;border-radius:6px;background:rgba(0,0,0,.45)}}"
        f".{k}__div{{position:absolute;top:0;bottom:0;left:50%;width:2px;background:#fff;transition:left .18s ease-out;pointer-events:none}}"
        f".{k}__div i{{position:absolute;left:-12px;top:50%;margin-top:-12px;width:24px;height:24px;border-radius:50%;background:#fff;color:#111;font-style:normal;font:700 11px/24px inherit;text-align:center;box-shadow:0 4px 12px rgba(0,0,0,.35)}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var fr=el.querySelector('.{k}__frame'),af=el.querySelector('.{k}__after'),dv=el.querySelector('.{k}__div');"
        f"var seq=[26,74,50],idx=0,touched=false,dead=false;"
        f"function setP(p){{p=Math.max(12,Math.min(88,p));af.style.clipPath='inset(0 0 0 '+p+'%)';dv.style.left=p+'%';}}"
        f"fr.addEventListener('pointermove',function(e){{touched=true;var r=fr.getBoundingClientRect();setP(((e.clientX-r.left)/r.width)*100);}});"
        f"fr.addEventListener('click',function(){{touched=true;idx=(idx+1)%seq.length;setP(seq[idx]);}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden){{idx=(idx+1)%seq.length;setP(seq[idx]);}}}},1750);"
        f"return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Before/After Split Curtain')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 15. Inbox / Task Swipe-Action Row & Undo Snackbar
def eng_list_swipe_action(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    row_title = _e(c.get("rowTitle", "Ship v2.4 launch checklist"))
    row_sub = _e(c.get("rowSub", "Design · Today"))
    action_lbl = _e(c.get("actionLbl", "Archive"))
    html = (
        f'<div class="{k}"><div class="{k}__wrap">'
        f'<div class="{k}__bg"><span>{action_lbl} ✓</span></div>'
        f'<button type="button" class="{k}__row"><i class="{k}__chk"></i><div><b>{row_title}</b><span>{row_sub}</span></div></button>'
        f'</div><div class="{k}__toast"><span>{action_lbl}d</span><b>Undo</b></div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__wrap{{position:relative;width:min(88%,262px);height:56px;border-radius:14px;overflow:hidden}}"
        f".{k}__bg{{position:absolute;inset:0;background:{acc};color:#fff;display:flex;align-items:center;padding:0 16px;font:700 12px/1 inherit}}"
        f".{k}__row{{position:relative;width:100%;height:100%;border:1px solid rgba(128,128,128,.16);border-radius:14px;background:{card};color:{fg};padding:0 14px;display:flex;align-items:center;gap:11px;text-align:left;cursor:pointer;transition:transform .42s cubic-bezier(.22,1.14,.36,1)}}"
        f".{k}.is-sw .{k}__row{{transform:translateX(92px)}}"
        f".{k}__chk{{width:18px;height:18px;border-radius:50%;border:2px solid {acc};flex:none;transition:background .2s}}"
        f".{k}.is-sw .{k}__chk{{background:{acc}}}"
        f".{k}__row b{{display:block;font:600 12.5px/1.2 inherit}}.{k}__row span{{font-size:11px;color:{mute}}}"
        f".{k}__toast{{display:inline-flex;align-items:center;gap:14px;padding:7px 13px;border-radius:10px;background:#181a20;color:#fff;font-size:11.5px;opacity:0;transform:translateY(10px);transition:all .3s cubic-bezier(.22,1.2,.36,1)}}"
        f".{k}__toast b{{color:{acc}}}"
        f".{k}.is-sw .{k}__toast{{opacity:1;transform:translateY(0)}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var row=el.querySelector('.{k}__row'),toast=el.querySelector('.{k}__toast'),on=false,touched=false,dead=false;"
        f"function tog(){{on=!on;el.classList.toggle('is-sw',on);}}"
        f"row.addEventListener('click',function(){{touched=true;tog();}});toast.addEventListener('click',function(){{touched=true;if(on)tog();}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)tog();}},1950);"
        f"return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Swipe Action Row')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 16. Liquid Wave Vessel Fill
def eng_liquid_fill_vessel(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    label = _e(c.get("label", "Daily Goal"))
    vals = c.get("vals", ["35%", "62%", "85%", "100%"])
    html = (
        f'<div class="{k}"><button type="button" class="{k}__cup">'
        f'<div class="{k}__liq"><div class="{k}__wave"></div></div>'
        f'<div class="{k}__txt"><b>{_e(vals[1])}</b><span>{label}</span></div>'
        f'</button></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__cup{{position:relative;width:116px;height:138px;border-radius:26px;border:2px solid rgba(128,128,128,.24);background:{card};overflow:hidden;cursor:pointer;display:grid;place-items:center}}"
        f".{k}__liq{{position:absolute;left:0;right:0;bottom:0;height:62%;background:linear-gradient(180deg,{acc},{acc2});transition:height .68s cubic-bezier(.22,1.18,.36,1)}}"
        f".{k}__wave{{position:absolute;top:-10px;left:-25%;width:150%;height:20px;border-radius:42%;background:{acc};opacity:.65;animation:{kf('wv')} 2.4s ease-in-out infinite alternate}}"
        f"@keyframes {kf('wv')}{{0%{{transform:translateX(-12%) rotate(-2deg)}}100%{{transform:translateX(12%) rotate(2deg)}}}}"
        f".{k}__txt{{position:relative;z-index:2;display:flex;flex-direction:column;align-items:center;gap:3px;mix-blend-mode:normal;color:#fff;text-shadow:0 1px 6px rgba(0,0,0,.35)}}"
        f".{k}__txt b{{font:800 22px/1 'Geist Mono',monospace}}.{k}__txt span{{font:600 10px/1 inherit;opacity:.9}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var cup=el.querySelector('.{k}__cup'),liq=el.querySelector('.{k}__liq'),b=el.querySelector('.{k}__txt b');"
        f"var vals={_j.dumps(vals)},pcts=[35,62,85,98],idx=1,touched=false,dead=false;"
        f"function set(i){{idx=i;liq.style.height=pcts[i]+'%';b.textContent=vals[i];}}"
        f"cup.addEventListener('click',function(){{touched=true;set((idx+1)%vals.length);}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)set((idx+1)%vals.length);}},1900);"
        f"return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Liquid Wave Vessel Fill')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 17. Token / Asset Dual-Card Swap Flip
def eng_token_swap_flip(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    a1, v1 = _e(c.get("a1", "SOL")), _e(c.get("v1", "12.50"))
    a2, v2 = _e(c.get("a2", "USDC")), _e(c.get("v2", "2,184.20"))
    html = (
        f'<div class="{k}"><div class="{k}__wrap">'
        f'<div class="{k}__box {k}__top"><span>{a1}</span><b>{v1}</b></div>'
        f'<button type="button" class="{k}__swap" aria-label="Swap">⇅</button>'
        f'<div class="{k}__box {k}__bot"><span>{a2}</span><b>{v2}</b></div>'
        f'</div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__wrap{{position:relative;width:min(84%,244px);display:flex;flex-direction:column;gap:8px}}"
        f".{k}__box{{height:54px;padding:0 14px;border-radius:14px;background:{card};border:1px solid rgba(128,128,128,.18);display:flex;align-items:center;justify-content:space-between;transition:transform .42s cubic-bezier(.22,1.18,.36,1)}}"
        f".{k}__box span{{font:700 12px/1 'Geist Mono',monospace;padding:5px 8px;border-radius:8px;background:{acc}22;color:{acc}}}"
        f".{k}__box b{{font:700 16px/1 'Geist Mono',monospace}}"
        f".{k}.is-flip .{k}__top{{transform:translateY(62px)}}.{k}.is-flip .{k}__bot{{transform:translateY(-62px)}}"
        f".{k}__swap{{position:absolute;left:50%;top:50%;margin:-17px 0 0 -17px;z-index:3;width:34px;height:34px;border-radius:50%;border:2px solid {bg};background:{acc};color:#fff;font:700 15px/1 inherit;cursor:pointer;transition:transform .42s cubic-bezier(.22,1.3,.36,1)}}"
        f".{k}.is-flip .{k}__swap{{transform:rotate(180deg)}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var btn=el.querySelector('.{k}__swap'),fl=false,touched=false,dead=false;"
        f"function flip(){{fl=!fl;el.classList.toggle('is-flip',fl);}}"
        f"btn.addEventListener('click',function(){{touched=true;flip();}});el.addEventListener('click',function(e){{if(e.target!==btn){{touched=true;flip();}}}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)flip();}},1950);"
        f"return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Asset Swap Flip')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 18. Cinema Hero Spotlight & Progress Glow
def eng_cinema_hero_spotlight(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    title = _e(c.get("showTitle", "Now Playing"))
    meta = _e(c.get("showMeta", "4K HDR · Dolby Atmos"))
    html = (
        f'<div class="{k}"><div class="{k}__screen">'
        f'<div class="{k}__glow"></div>'
        f'<div class="{k}__rip">+10s</div>'
        f'<div class="{k}__info"><b>{title}</b><span>{meta}</span></div>'
        f'<div class="{k}__bar"><i class="{k}__prog"></i></div>'
        f'</div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:#fff;user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__screen{{position:relative;width:min(88%,262px);height:146px;border-radius:16px;padding:14px;background:linear-gradient(145deg,{card},#090a0d);border:1px solid rgba(255,255,255,.12);overflow:hidden;display:flex;flex-direction:column;justify-content:flex-end;gap:10px;cursor:pointer;box-shadow:0 16px 36px {acc}33}}"
        f".{k}__glow{{position:absolute;inset:-20%;background:radial-gradient(circle at 70% 25%,{acc}88,transparent 58%);transition:transform .6s ease,opacity .5s}}"
        f".{k}.is-pulse .{k}__glow{{transform:scale(1.18);opacity:.95}}"
        f".{k}__rip{{position:absolute;right:18px;top:36px;width:44px;height:44px;border-radius:50%;background:rgba(255,255,255,.18);display:grid;place-items:center;font:700 11px/1 'Geist Mono',monospace;opacity:0;transform:scale(.6)}}"
        f".{k}.is-pulse .{k}__rip{{animation:{kf('rp')} .62s cubic-bezier(.22,1,.36,1)}}"
        f"@keyframes {kf('rp')}{{0%{{opacity:0;transform:scale(.5)}}35%{{opacity:1;transform:scale(1.12)}}100%{{opacity:0;transform:scale(1.4)}}}}"
        f".{k}__info{{position:relative;z-index:2}}.{k}__info b{{display:block;font:700 15px/1.15 inherit}}.{k}__info span{{font-size:11px;color:rgba(255,255,255,.68)}}"
        f".{k}__bar{{position:relative;z-index:2;height:4px;border-radius:99px;background:rgba(255,255,255,.18);overflow:hidden}}"
        f".{k}__prog{{display:block;height:100%;width:28%;background:{acc};border-radius:99px;transition:width .55s cubic-bezier(.22,1,.36,1)}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var sc=el.querySelector('.{k}__screen'),pr=el.querySelector('.{k}__prog'),pct=28,touched=false,dead=false;"
        f"function bump(){{pct=pct>=92?20:pct+24;pr.style.width=pct+'%';el.classList.remove('is-pulse');void el.offsetWidth;el.classList.add('is-pulse');}}"
        f"sc.addEventListener('click',function(){{touched=true;bump();}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)bump();}},1900);"
        f"return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Cinema Spotlight')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 19. Interactive Graph / Multiplayer Cursor / Canvas Nodes
def eng_graph_cursor_canvas(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    tag1 = _e(c.get("tag1", "Alex"))
    tag2 = _e(c.get("tag2", "Maya"))
    nodes = [(44, 42), (126, 30), (196, 56), (86, 102), (168, 108)]
    edges = [(0, 1), (1, 2), (0, 3), (1, 3), (3, 4), (2, 4)]
    edge_svg = "".join(
        f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="rgba(128,128,128,.32)" stroke-width="1.5"/>'
        for a, b in edges
    )
    node_svg = "".join(
        f'<circle class="{k}__nd" data-i="{i}" cx="{x}" cy="{y}" r="8" fill="{card}" stroke="{acc}" stroke-width="2.2"/>'
        for i, (x, y) in enumerate(nodes)
    )
    html = (
        f'<div class="{k}"><div class="{k}__board">'
        f'<svg class="{k}__svg" viewBox="0 0 240 140">{edge_svg}{node_svg}</svg>'
        f'<span class="{k}__cur {k}__c1">▲ {tag1}</span>'
        f'<span class="{k}__cur {k}__c2">▲ {tag2}</span>'
        f'</div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__board{{position:relative;width:min(88%,262px);height:146px;border-radius:16px;background:{card};border:1px solid rgba(128,128,128,.18);overflow:hidden;cursor:pointer;background-image:radial-gradient(rgba(128,128,128,.16) 1px,transparent 1px);background-size:14px 14px}}"
        f".{k}__svg{{position:absolute;inset:0;width:100%;height:100%}}"
        f".{k}__nd{{transition:r .25s,fill .25s}}.{k}__nd.is-hi{{fill:{acc};filter:drop-shadow(0 0 8px {acc})}}"
        f".{k}__cur{{position:absolute;padding:3px 7px;border-radius:999px;font:600 9.5px/1 'Geist Mono',monospace;color:#fff;transition:transform .82s cubic-bezier(.22,1,.36,1);pointer-events:none;box-shadow:0 4px 10px rgba(0,0,0,.25)}}"
        f".{k}__c1{{background:{acc};left:24px;top:24px}}.{k}__c2{{background:{acc2};left:140px;top:92px}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var c1=el.querySelector('.{k}__c1'),c2=el.querySelector('.{k}__c2'),nds=[].slice.call(el.querySelectorAll('.{k}__nd'));"
        f"var pts=[[20,16,136,86],[106,12,68,84],[162,38,144,94],[64,84,110,16]],idx=0,touched=false,dead=false;"
        f"function move(i){{idx=i;var p=pts[i];c1.style.transform='translate('+p[0]+'px,'+p[1]+'px)';c2.style.transform='translate('+(p[2]-140)+'px,'+(p[3]-92)+'px)';nds.forEach(function(n,j){{n.classList.toggle('is-hi',j===i||j===(i+2)%nds.length);}});}}"
        f"el.addEventListener('click',function(){{touched=true;move((idx+1)%pts.length);}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)move((idx+1)%pts.length);}},1650);"
        f"move(0);return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Interactive Node Graph')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 20. 3D Tile / Card Flip Cascade Reveal
def eng_envelope_seal_reveal(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    letters = c.get("tiles", ["M", "O", "T", "I", "O", "N"])
    sub = _e(c.get("sub", "Tap to reveal"))
    tiles_html = "".join(f'<span class="{k}__t" style="transition-delay:{i*70}ms">{_e(ch)}</span>' for i, ch in enumerate(letters))
    html = f'<div class="{k}"><button type="button" class="{k}__stage"><div class="{k}__row">{tiles_html}</div><em class="{k}__sub">{sub}</em></button></div>'
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};perspective:600px;user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__stage{{border:0;background:none;color:inherit;display:flex;flex-direction:column;align-items:center;gap:14px;cursor:pointer}}"
        f".{k}__row{{display:flex;gap:6px}}"
        f".{k}__t{{width:34px;height:40px;border-radius:9px;border:1.5px solid rgba(128,128,128,.28);background:{card};font:800 17px/1 'Geist Mono',monospace;display:grid;place-items:center;transition:transform .48s cubic-bezier(.22,1.2,.36,1),background .3s,color .3s,border-color .3s}}"
        f".{k}.is-flip .{k}__t{{transform:rotateX(360deg);background:{acc};border-color:{acc};color:#fff}}"
        f".{k}.is-flip .{k}__t:nth-child(2n){{background:{acc2};border-color:{acc2}}}"
        f".{k}__sub{{font-style:normal;font:500 11px/1 'Geist Mono',monospace;color:{mute}}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var st=el.querySelector('.{k}__stage'),on=false,touched=false,dead=false;"
        f"function flip(){{on=!on;el.classList.toggle('is-flip',on);}}"
        f"st.addEventListener('click',function(){{touched=true;flip();}});"
        f"var t0=setTimeout(function(){{if(!dead)flip();}},320);"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)flip();}},2200);"
        f"return function(){{dead=true;clearTimeout(t0);clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','3D Tile Cascade Flip')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 21. Spring Bottom Sheet / Cart Widen Pill
def eng_sheet_detent_drawer(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    title = _e(c.get("sheetTitle", "Quick Reserve"))
    items = c.get("chips", ["7:00 PM", "7:30 PM", "8:15 PM"])
    cta = _e(c.get("cta", "Confirm"))
    chips_html = "".join(f'<button type="button" class="{k}__ch{" is-on" if i==0 else ""}" data-i="{i}">{_e(x)}</button>' for i, x in enumerate(items))
    html = (
        f'<div class="{k}"><div class="{k}__phone">'
        f'<div class="{k}__sheet"><span class="{k}__grab"></span><b>{title}</b>'
        f'<div class="{k}__chips">{chips_html}</div>'
        f'<button type="button" class="{k}__cta">{cta}</button>'
        f'</div></div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__phone{{position:relative;width:min(84%,244px);height:160px;border-radius:18px;background:rgba(128,128,128,.1);border:1px solid rgba(128,128,128,.16);overflow:hidden}}"
        f".{k}__sheet{{position:absolute;left:0;right:0;bottom:0;padding:10px 14px 14px;border-radius:18px 18px 0 0;background:{card};box-shadow:0 -10px 26px rgba(0,0,0,.22);display:flex;flex-direction:column;gap:9px;transform:translateY(56px);transition:transform .48s cubic-bezier(.22,1.18,.36,1)}}"
        f".{k}.is-up .{k}__sheet{{transform:translateY(0)}}"
        f".{k}__grab{{width:32px;height:4px;border-radius:99px;background:rgba(128,128,128,.32);margin:0 auto}}"
        f".{k}__sheet b{{font:700 13px/1 inherit}}"
        f".{k}__chips{{display:flex;gap:6px}}"
        f".{k}__ch{{flex:1;height:28px;border-radius:8px;border:1px solid rgba(128,128,128,.2);background:transparent;color:{mute};font:600 10.5px/1 'Geist Mono',monospace;cursor:pointer;transition:all .2s}}"
        f".{k}__ch.is-on{{background:{acc};border-color:{acc};color:#fff}}"
        f".{k}__cta{{height:32px;border:0;border-radius:10px;background:{acc};color:#fff;font:700 12px/1 inherit;cursor:pointer}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var chs=[].slice.call(el.querySelectorAll('.{k}__ch')),up=false,idx=0,touched=false,dead=false;"
        f"function toggle(){{up=!up;el.classList.toggle('is-up',up);}}"
        f"chs.forEach(function(b,i){{b.addEventListener('click',function(e){{e.stopPropagation();touched=true;idx=i;chs.forEach(function(x,j){{x.classList.toggle('is-on',j===i);}});el.classList.add('is-up');up=true;}});}});"
        f"el.addEventListener('click',function(){{touched=true;toggle();}});"
        f"var t0=setTimeout(function(){{if(!dead)toggle();}},260);"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden){{if(up){{idx=(idx+1)%chs.length;chs.forEach(function(x,j){{x.classList.toggle('is-on',j===idx);}});}}else toggle();}}}},1850);"
        f"return function(){{dead=true;clearTimeout(t0);clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Spring Bottom Sheet')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 22. Streaming AI Citation / Token Cascade Cards
def eng_streaming_ai_cards(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    chips = c.get("sources", ["Docs", "Specs", "Benchmarks"])
    lines = c.get("lines", ["Analyzing spring curves…", "Synthesizing clean motion IR"])
    ch_html = "".join(f'<span class="{k}__src" style="transition-delay:{i*90}ms">{_e(s)}</span>' for i, s in enumerate(chips))
    html = (
        f'<div class="{k}"><div class="{k}__card">'
        f'<div class="{k}__srcs">{ch_html}</div>'
        f'<div class="{k}__ln {k}__l1">{_e(lines[0])}</div>'
        f'<div class="{k}__ln {k}__l2">{_e(lines[1])}<i class="{k}__cur"></i></div>'
        f'</div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__card{{width:min(86%,256px);padding:14px 15px;border-radius:16px;background:{card};border:1px solid rgba(128,128,128,.16);display:flex;flex-direction:column;gap:9px;cursor:pointer}}"
        f".{k}__srcs{{display:flex;gap:6px;flex-wrap:wrap}}"
        f".{k}__src{{padding:4px 8px;border-radius:999px;background:{acc}1f;border:1px solid {acc}44;color:{acc};font:600 10px/1 'Geist Mono',monospace;opacity:0;transform:translateY(6px) scale(.92);transition:all .38s cubic-bezier(.22,1.2,.36,1)}}"
        f".{k}.is-on .{k}__src{{opacity:1;transform:none}}"
        f".{k}__ln{{font:500 12px/1.35 inherit;color:{mute};opacity:0;transform:translateY(5px);transition:all .42s cubic-bezier(.22,1,.36,1)}}"
        f".{k}__l2{{color:{fg};transition-delay:.22s}}"
        f".{k}.is-on .{k}__ln{{opacity:1;transform:none}}"
        f".{k}__cur{{display:inline-block;width:6px;height:12px;margin-left:4px;vertical-align:-2px;background:{acc};border-radius:1px;animation:{kf('bl')} .85s steps(2) infinite}}"
        f"@keyframes {kf('bl')}{{50%{{opacity:0}}}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var on=false,touched=false,dead=false;"
        f"function replay(){{el.classList.remove('is-on');void el.offsetWidth;el.classList.add('is-on');on=true;}}"
        f"el.addEventListener('click',function(){{touched=true;replay();}});"
        f"var t0=setTimeout(function(){{if(!dead)replay();}},180);"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)replay();}},2400);"
        f"return function(){{dead=true;clearTimeout(t0);clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Streaming Citation Cascade')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 23. Laser Scan Sweep & Instant Verified Badge
def eng_barcode_laser_scan(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    title = _e(c.get("scanTitle", "Receipt Matched"))
    score = _e(c.get("score", "94 / 100"))
    html = (
        f'<div class="{k}"><div class="{k}__box">'
        f'<div class="{k}__bars"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>'
        f'<div class="{k}__beam"></div>'
        f'<div class="{k}__res"><b>{score}</b><span>{title}</span></div>'
        f'</div></div>'
    )
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__box{{position:relative;width:min(84%,238px);height:132px;border-radius:16px;background:{card};border:1px solid rgba(128,128,128,.18);overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;cursor:pointer}}"
        f".{k}__bars{{display:flex;gap:5px;height:40px;align-items:stretch;opacity:.5}}"
        f".{k}__bars i{{width:4px;background:{fg};border-radius:2px}}.{k}__bars i:nth-child(2n){{width:8px}}.{k}__bars i:nth-child(3n){{width:2px}}"
        f".{k}__beam{{position:absolute;left:14px;right:14px;top:24px;height:2.5px;background:{acc};box-shadow:0 0 14px {acc};animation:{kf('sc')} 1.8s ease-in-out infinite alternate}}"
        f"@keyframes {kf('sc')}{{0%{{transform:translateY(0)}}100%{{transform:translateY(76px)}}}}"
        f".{k}__res{{display:inline-flex;align-items:center;gap:8px;padding:6px 12px;border-radius:999px;background:{acc}1f;border:1px solid {acc}55;transform:scale(.9);opacity:.65;transition:all .36s cubic-bezier(.22,1.3,.36,1)}}"
        f".{k}.is-hit .{k}__res{{transform:scale(1.04);opacity:1}}"
        f".{k}__res b{{font:700 12px/1 'Geist Mono',monospace;color:{acc}}}.{k}__res span{{font:600 11px/1 inherit}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var on=false,touched=false,dead=false;"
        f"function hit(){{on=!on;el.classList.toggle('is-hit',on);}}"
        f"el.addEventListener('click',function(){{touched=true;hit();}});"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)hit();}},1600);"
        f"hit();return function(){{dead=true;clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Laser Scan & Verified Badge')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


# 24. Metric Bar Cascade & Live Target Pop
def eng_metric_bars_cascade(slug: str, c: dict):
    k, kf = _cid(slug), lambda n: _kf(slug, n)
    bg, card, fg, mute, acc, acc2 = _base_vars(c)
    rows = c.get("rows", [("Protein", 84), ("Carbs", 68), ("Fat", 52)])
    rows_html = "".join(
        f'<div class="{k}__r"><span>{_e(lbl)}</span><div class="{k}__tr"><i data-p="{pct}" style="width:12%;transition-delay:{i*90}ms"></i></div><b>{pct}%</b></div>'
        for i, (lbl, pct) in enumerate(rows)
    )
    html = f'<div class="{k}"><div class="{k}__card">{rows_html}</div></div>'
    css = (
        f".{k}{{position:absolute;inset:0;display:grid;place-items:center;background:{bg};color:{fg};user-select:none;font-family:-apple-system,BlinkMacSystemFont,'Host Grotesk',sans-serif}}"
        f".{k}__card{{width:min(86%,254px);padding:15px 16px;border-radius:16px;background:{card};border:1px solid rgba(128,128,128,.16);display:flex;flex-direction:column;gap:11px;cursor:pointer}}"
        f".{k}__r{{display:grid;grid-template-columns:62px 1fr 34px;align-items:center;gap:8px;font-size:11.5px}}"
        f".{k}__r span{{color:{mute};font-weight:600}}.{k}__r b{{font:600 11px/1 'Geist Mono',monospace;text-align:right}}"
        f".{k}__tr{{height:8px;border-radius:99px;background:rgba(128,128,128,.18);overflow:hidden}}"
        f".{k}__tr i{{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,{acc},{acc2});transition:width .62s cubic-bezier(.22,1.16,.36,1)}}"
    )
    js = (
        f"var el=root.querySelector('.{k}');if(!el)return;"
        f"var bars=[].slice.call(el.querySelectorAll('.{k}__tr i')),full=false,touched=false,dead=false;"
        f"function apply(){{full=!full;bars.forEach(function(b){{b.style.width=(full?b.dataset.p:Math.max(18,Number(b.dataset.p)-42))+'%';}});}}"
        f"el.addEventListener('click',function(){{touched=true;apply();}});"
        f"var t0=setTimeout(function(){{if(!dead)apply();}},220);"
        f"var iv=setInterval(function(){{if(!touched&&!dead&&!document.hidden)apply();}},2100);"
        f"return function(){{dead=true;clearTimeout(t0);clearInterval(iv);}};"
    )
    code = f"<!-- {c.get('title','Metric Bars Cascade')} -->\n{html}\n<style>{css}</style>"
    return html, css, js, code


ENGINES = {
    "numpad_spring": eng_numpad_spring,
    "sparkline_scrub": eng_sparkline_scrub,
    "ring_gauge": eng_ring_gauge,
    "card_swipe_deck": eng_card_swipe_deck,
    "card_freeze_tilt": eng_card_freeze_tilt,
    "waveform_audio": eng_waveform_audio,
    "orb_voice_aura": eng_orb_voice_aura,
    "swipe_rail_cta": eng_swipe_rail_cta,
    "radar_map_tracker": eng_radar_map_tracker,
    "segmented_pill_morph": eng_segmented_pill_morph,
    "stepper_progress_flow": eng_stepper_progress_flow,
    "reaction_burst_social": eng_reaction_burst_social,
    "dial_knob_scrub": eng_dial_knob_scrub,
    "split_before_after": eng_split_before_after,
    "list_swipe_action": eng_list_swipe_action,
    "liquid_fill_vessel": eng_liquid_fill_vessel,
    "token_swap_flip": eng_token_swap_flip,
    "cinema_hero_spotlight": eng_cinema_hero_spotlight,
    "graph_cursor_canvas": eng_graph_cursor_canvas,
    "envelope_seal_reveal": eng_envelope_seal_reveal,
    "sheet_detent_drawer": eng_sheet_detent_drawer,
    "streaming_ai_cards": eng_streaming_ai_cards,
    "barcode_laser_scan": eng_barcode_laser_scan,
    "metric_bars_cascade": eng_metric_bars_cascade,
}


def build_motion_entry(app_meta: dict, spec: dict) -> dict:
    slug = app_meta["slug"]
    name = app_meta["name"]
    eng_fn = ENGINES[spec["engine"]]
    cfg = {
        "title": f"{name}: {spec['motionName']}",
        "surface": spec.get("surface", "dark"),
        "accent": spec.get("accent", app_meta["accent"]),
        **spec.get("cfg", {}),
    }
    html, css, js, code = eng_fn(slug, cfg)
    ease = spec.get("ease", {"t": "spring", "k": 310, "c": 22})
    if ease["t"] == "spring":
        ease_label = f"spring({ease['k']}, {ease['c']})"
    else:
        p = ease["p"]
        ease_label = f"cubic-bezier({p[0]}, {p[1]}, {p[2]}, {p[3]})"

    return {
        "id": f"app-{slug}-{spec['motionSlug']}",
        "title": f"{name}: {spec['motionName']}",
        "use": spec["use"],
        "stack": spec["stack"],
        "trigger": spec["trigger"],
        "feel": spec["feel"],
        "surface": spec.get("surface", "dark"),
        "dur": spec["dur"],
        "ease": ease,
        "easeLabel": ease_label,
        "props": spec["props"],
        "src": name,
        "srcUrl": app_meta.get("storeUrl", ""),
        "collection": "Apps",
        "app": {
            "name": name,
            "slug": slug,
            "category": app_meta.get("category", "Utilities"),
            "platform": app_meta.get("platform", ["iOS", "Android"]),
            "accent": app_meta.get("accent", "#2a94e2"),
            "iconUrl": app_meta.get("iconUrl", ""),
            "storeUrl": app_meta.get("storeUrl", ""),
            "bundleId": app_meta.get("bundleId", ""),
        },
        "summary": spec["summary"],
        "hint": spec["hint"],
        "choreography": spec["choreography"],
        "agentPrompt": spec["agentPrompt"],
        "extractableCode": code,
        "html": html,
        "css": css,
        "js": js,
    }
