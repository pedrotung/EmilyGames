# Meow Brigade: cat abilities (from Jason)

Numbers follow stats-table.md version 2 (balance pass, 2026-10-18). HP per cat is in stats-table.md.

Battle: cats fight automatically. Tap a hurt cat and a HEAL button shows, which restores half its HP. Each Nurse on the field gives one heal, and the button does not show once they are used up.

## Common
| Cat | Attack | Damage | Range / cooldown |
|---|---|---|---|
| Cat | Scratches | 5 per scratch | Short range, 2 s cooldown. Free starter cat |
| Cool cat | Laser shot from its sunglasses | 5 per shot | 2.5 s cooldown |
| Bad cat | Spits cigarettes (infinite) | 10 each | 5 s cooldown |
| Gentlemat | Attacks with a hat held in its hand, not worn on its head (Jason drew it: src/gentlemat-hat-sheet.jpg, cut to assets/hat.png and assets/cat_gentlemat.png) | 6 each | 3 s cooldown |
| Daisy | Flings petals | 2 each | Long range, 1 petal per second |
| Alert cat | No attack. Its head ball flashes and makes an alert sound when a boss approaches. In boss fights only: a random chance (under 10%) to put a shield on the whole team for 5 s; shielded cats take no damage but keep attacking | 0 | Roll 8% every 5 s during a boss fight (default) |

## Rare
| Cat | Attack | Damage | Range / cooldown |
|---|---|---|---|
| Rizz cat | Walks up to one rat and just stands there (no animation) for 4 s, then the rat runs away and counts as dead | Instant defeat | Then moves to the next rat. Does not work on bosses (default) |
| Water | At least 3 straight water lines from its mouth in a small fan; hits every rat in it, less damage the farther the rat | 6 near, 4 mid, 2 far | 1.5 s cooldown |
| Bleh | Shoots out its own drawn tongue like a frog, pulls the rat in, then chews (mouth opens/closes, tail sticks out) and swallows (lump slides down) during the cooldown | Instant defeat on normal rats; 30 on bosses (default) | Mid range, 8 s cooldown |
| Ghost cat | Front row. Flies around fast, so rats mostly miss it (rats hit it 30% of the time). Pokes very fast. Summons up to 4 clones of itself that last 5 s and have its abilities (clones cannot clone). Clones attack like the original and each targets a different rat | 1 per hit, 3 hits per second | Clone burst every 20 s |
| Nurse | Heals other cats: the player taps a hurt cat and a HEAL button appears on that cat's head; restores half its HP. Once per battle per Nurse; no button once used | Heal 50% | Once per battle |

## Team rule
Up to 5 cats on the field, duplicates allowed: rolling the same cat again gives another copy (5 Ghost cats + 4 clones each = 25 ghosts). So duplicate spins are NOT refunded.

## Epic
| Cat | Attack | Damage | Range / cooldown |
|---|---|---|---|
| Senpai | Stabs rats with the pen it holds (front row, melee). Art: assets/cat_senpai2.png from src/senpai-catcat-sheet.jpg | 8 per stab | 1 s cooldown |
| Cat kid | Headbutts rats (front row, melee); each knock also hurts itself | 20 to the rat, 2 to itself | 2.5 s cooldown |
| Cat cat | Kicks a football that crashes into a rat (back row, ranged); small chance to miss (10%, default). Art: assets/cat_catcat2.png + assets/football.png | 22 per ball | 2.5 s cooldown |
| Poison cat | Sprays a cloud of poison air over a medium area (Jason asked for larger; about 3 rats wide); every rat inside loses HP while the cloud lasts (back row) | 4 per second to each rat in the cloud | Cloud lasts 8 s, 4 s cooldown |

## Legendary (all back row)
| Cat | Attack | Damage | Range / cooldown |
|---|---|---|---|
| Fairy cat | Waves its magic wand; lightning strikes a rat from above | 20 per strike (Rainbow Rat's lightning is 8) | Long range, 1.5 s cooldown |
| Military cat | Shoots bullets from its gun | 3 per bullet | Rapid fire, 4.5 per second |
| Witch cat | Throws a potion that smashes and splashes | 15 to each rat in the splash + slows them | 3 s cooldown |

## Secret (not in spins; each bought for 6000 coins)
| Cat | Attack | Damage | Range / cooldown |
|---|---|---|---|
| Angel cat | Flies up to the top of the battlefield (3 s, default), plays a holy "meow" chorus sound, and hits every rat on the field at once. If it is hit while flying (bosses that can attack airborne cats: Long Rat's neck, Rainbow Rat's lightning, default), it drops back to the ground and has to start again | 30 to every rat on the field | 10 s cooldown after the blast (default) |
| Devil cat | Stabs with its trident (front row, melee). Defeats a normal rat at half HP or less in one stab; bosses only take damage | Instant defeat on rats at ≤50% HP, otherwise 40; 40 on bosses | 3.5 s cooldown (nerfed from 2 s, Jason 2026-10-18) |

Attack animations mockup: src/mock_attacks.py -> design/attacks/common-attacks.gif
Epic animations: src/mock_attacks_epic.py -> design/attacks/epic-attacks.gif
Legendary animations: src/mock_attacks_legendary.py -> design/attacks/legendary-attacks.gif
Secret animations: src/mock_attacks_secret.py -> design/attacks/secret-attacks.gif
