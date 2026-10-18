# EmilyGames

Small single-page HTML games that run in a phone browser.

Each game lives in its own folder on `main` (`<game>/index.html`), and [`index.html`](index.html)
at the root is a home page linking to all of them. With GitHub Pages on, the home page is
`https://pedrotung.github.io/EmilyGames/` and each game is at `/<game>/`.

## Playing full screen on a phone or tablet

Every game has a **Full screen** button, and on phones and tablets it also goes full screen by itself
after your first tap (Android, iPad and computers). iPhone Safari does not let web pages hide its
toolbars, so on iPhone use **Share > Add to Home Screen** and start the game from the new icon:
it then opens full screen with no browser bars. Each game folder has its own `manifest.webmanifest`
and icons for this.

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

## Meow Brigade

[`cat-rat-battle/index.html`](cat-rat-battle/index.html) is an auto-battle game drawn from hand sketches, all in black and white.
Up to 5 cats stand in a formation (melee in front, ranged and Nurse behind) and fight waves of rats on their own.
Tap a hurt cat and then **HEAL** to use a Nurse heal.

- 10 levels, each ending with a boss (Rat Queen, Legged Rat, Clone Rat, Long Rat, Rainbow Rat)
- 20 cats with their own attacks; win coins and spin the Common, Rare, Epic and Legendary wheels, or buy the two Secret cats
- 8-bit music (cute menu theme, tense battle theme, faster boss theme) and a sound for every cat attack and every rat, all synthesised in the browser
- Progress is saved on the device

The game loads its art from `cat-rat-battle/assets/` and its font from `cat-rat-battle/src/fonts/`, so serve the whole folder
(GitHub Pages: `/cat-rat-battle/`). Design notes and numbers are in `cat-rat-battle/stats-table.md`.
