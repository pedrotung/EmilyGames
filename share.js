/* EmilyGames sharing: after a win, a game calls EmilyShare.snap(...) to keep a picture of the
   screen with the game's web address on it, and shows a Share button that calls EmilyShare.open().
   The panel shares the picture through the phone's own share sheet when it can, and also offers
   links for the big social sites (they show the game's preview picture), saving the picture and
   copying the link. Web pages cannot post for the player, so the player always taps to share. */
(function () {
  const SITE = 'https://pedrotung.github.io/EmilyGames/';
  let last = null; // { blob, url, text, game, link }

  function card(canvas, game, text, link) {
    const W = 1200, H = 630, FOOT = 96, c = document.createElement('canvas');
    c.width = W; c.height = H; const x = c.getContext('2d');
    x.fillStyle = '#fff'; x.fillRect(0, 0, W, H);
    if (canvas) { // fit the game screen above the footer, centred
      const s = Math.min(W / canvas.width, (H - FOOT) / canvas.height), w = canvas.width * s, h = canvas.height * s;
      x.fillStyle = '#111'; x.fillRect(0, 0, W, H - FOOT);
      try { x.drawImage(canvas, (W - w) / 2, (H - FOOT - h) / 2, w, h); } catch (e) {}
    }
    x.fillStyle = '#111'; x.fillRect(0, H - FOOT, W, FOOT);
    x.fillStyle = '#fff'; x.textBaseline = 'middle';
    x.font = 'bold 30px system-ui, -apple-system, Segoe UI, Roboto, sans-serif';
    let t = text; while (x.measureText(t).width > W - 60 && t.length > 4) t = t.slice(0, -2);
    if (t !== text) t = t.slice(0, -1) + '…';
    x.fillText(t, 30, H - FOOT + 32);
    x.font = '24px system-ui, -apple-system, Segoe UI, Roboto, sans-serif'; x.fillStyle = '#ffd84a';
    x.fillText('Play ' + game + ' free: ' + link.replace('https://', ''), 30, H - FOOT + 70);
    return c;
  }

  function snap(o) {
    const link = SITE + (o.path || '');
    const c = card(o.canvas, o.game, o.text, link);
    last = { url: c.toDataURL('image/png'), text: o.text, game: o.game, link, blob: null };
    const mine = last; c.toBlob(b => { mine.blob = b; }, 'image/png');
    return last;
  }

  function css() {
    if (document.getElementById('emilyShareCss')) return;
    const s = document.createElement('style'); s.id = 'emilyShareCss';
    s.textContent = `
#emilyShare { position: fixed; inset: 0; z-index: 2147483000; background: rgba(0,0,0,.6); display: flex; align-items: center; justify-content: center; padding: 12px; box-sizing: border-box;
  font: 16px/1.3 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; color: #111; }
#emilyShare .box { background: #fff; border: 3px solid #111; border-radius: 14px; padding: 14px; width: min(560px, 100%); max-height: 100%; overflow: auto; box-sizing: border-box; }
#emilyShare h2 { margin: 0 0 8px; font-size: 22px; }
#emilyShare img { width: 100%; border: 2px solid #111; border-radius: 8px; display: block; }
#emilyShare .row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
#emilyShare button, #emilyShare a { flex: 1 1 30%; min-height: 42px; padding: 8px 6px; border: 2px solid #111; border-radius: 10px; background: #fff; color: #111;
  font: inherit; font-weight: 600; text-align: center; text-decoration: none; cursor: pointer; box-sizing: border-box; display: flex; align-items: center; justify-content: center; }
#emilyShare .main { background: #111; color: #fff; flex-basis: 100%; }
#emilyShare .note { margin: 10px 0 0; font-size: 13px; color: #555; }`;
    document.head.appendChild(s);
  }

  function open(o) {
    if (o) snap(o);
    if (!last) return;
    css(); close();
    const L = last, enc = encodeURIComponent, msg = L.text + ' Play it free:';
    const sites = [
      ['X', `https://twitter.com/intent/tweet?text=${enc(msg)}&url=${enc(L.link)}`],
      ['Facebook', `https://www.facebook.com/sharer/sharer.php?u=${enc(L.link)}`],
      ['WhatsApp', `https://wa.me/?text=${enc(msg + ' ' + L.link)}`],
      ['Telegram', `https://t.me/share/url?url=${enc(L.link)}&text=${enc(msg)}`],
      ['Reddit', `https://www.reddit.com/submit?url=${enc(L.link)}&title=${enc(L.text)}`],
      ['Weibo', `https://service.weibo.com/share/share.php?url=${enc(L.link)}&title=${enc(msg)}`],
    ];
    const d = document.createElement('div'); d.id = 'emilyShare';
    d.innerHTML = `<div class="box" role="dialog" aria-label="Share">
      <h2>Share your win!</h2><img alt="Your win, with the game's web address">
      <div class="row"><button class="main" data-a="native">Share picture…</button></div>
      <div class="row">${sites.map(([n, u]) => `<a href="${u}" target="_blank" rel="noopener">${n}</a>`).join('')}</div>
      <div class="row"><a data-a="save" download="${L.game.replace(/\W+/g, '-').toLowerCase()}-win.png" href="${L.url}">Save picture</a><button data-a="copy">Copy link</button><button data-a="close">Close</button></div>
      <p class="note">The site buttons share the game link with its picture. To post your own screenshot, use Share picture or Save picture.</p></div>`;
    d.querySelector('img').src = L.url;
    const nat = d.querySelector('[data-a="native"]');
    if (!navigator.share) nat.parentNode.remove();
    nat.addEventListener('click', async () => {
      try {
        const f = L.blob && new File([L.blob], 'my-win.png', { type: 'image/png' });
        if (f && navigator.canShare && navigator.canShare({ files: [f] })) await navigator.share({ files: [f], text: msg + ' ' + L.link });
        else await navigator.share({ title: L.game, text: msg, url: L.link });
      } catch (e) {}
    });
    d.querySelector('[data-a="copy"]').addEventListener('click', e => {
      const b = e.currentTarget, done = () => { b.textContent = 'Copied!'; };
      if (navigator.clipboard) navigator.clipboard.writeText(L.link).then(done, () => { b.textContent = L.link; });
      else b.textContent = L.link;
    });
    d.querySelector('[data-a="close"]').addEventListener('click', close);
    d.addEventListener('click', e => { if (e.target === d) close(); });
    // keep game keys and taps from reaching the game underneath
    ['pointerdown', 'keydown', 'touchstart'].forEach(t => d.addEventListener(t, e => e.stopPropagation()));
    document.body.appendChild(d);
  }
  function close() { const d = document.getElementById('emilyShare'); if (d) d.remove(); }
  const isOpen = () => !!document.getElementById('emilyShare');

  // while the panel is open, keys go to it and not to the game (Space, arrows...); Escape closes it
  window.addEventListener('keydown', e => { if (!isOpen()) return; if (e.key === 'Escape') close(); if (!e.target.closest || !e.target.closest('#emilyShare') || e.key === 'Escape') e.stopImmediatePropagation(); }, true);
  window.EmilyShare = { snap, open, close, isOpen, get last() { return last; } };
})();
