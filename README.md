# The Closet — static storefront

Public rent/resale storefront for the closetly app (the manager stays local).

- Live: https://philduggan88.github.io/closetly/
- Source of truth: `~/closetly` (shop.html + data/closet.json). This repo is a build artifact.
- Refresh flow after changing listings locally:
  1. `python3 ~/closetly/mobile/build.py`
  2. commit + push this repo
- `build.py` snapshots only listed pieces (status rent/sell) and public fields — notes, owner, and unlisted pieces never leave the laptop.
