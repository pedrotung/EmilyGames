# EmilyGames

Small single-page HTML games that run in a phone browser.

Each game lives in its own folder on `main` (`<game>/index.html`), and [`index.html`](index.html)
at the root is a home page linking to all of them. With GitHub Pages on, the home page is
`https://pedrotung.github.io/EmilyGames/` and each game is at `/<game>/`.

## Colour Jump

[`colour-jump/index.html`](colour-jump/index.html) is a one-button jump game drawn from a hand sketch.
Your block runs forward on its own; tap **JUMP** (or press Space) to clear gaps and blocks,
then walk through the coloured door into the next level.

- 7 levels in rainbow colours, each door with its own transition, rainbow and fireworks at the end
- 90s rave background music and voice-style effects, all synthesised in the browser
- Clouds, crows and their droppings (land on your head: "Ew!"; step in one on the ground: you slip forward), pause menu with Restart level / Back to Level 1

Everything is in the one HTML file. Open it in a browser, or serve the repo with GitHub Pages
and visit `/colour-jump/`.

## Disco Funkin'

[`disco-funkin/index.html`](disco-funkin/index.html) is a Friday Night Funkin'-style dance game drawn from hand sketches.
Arrows fall down four lanes (down, up, left, right); hit each one as it reaches the hit line with the
arrow keys, **D F J K**, or by tapping the lane. Every hit makes the stick dancer strike the matching pose.

- 5 original 80s/90s disco songs (120 to 148 BPM), all synthesised in the browser, unlocked one by one
- EASY / NORMAL / HARD charts with double arrows, fast runs and hold arrows
- PERFECT / GOOD / OK / MISS timing, combo, health bar, S to D rank and best scores saved on the device

Everything, including the hand-drawn art, is in the one HTML file. Open it in a browser, or visit `/disco-funkin/` on GitHub Pages.
