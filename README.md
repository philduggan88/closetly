# The Closet — shop + manager

Public rent/resale storefront and client-side closet manager, on GitHub Pages.

- Shop (public): https://philduggan88.github.io/closetly/
- Manager (Jasmine's): https://philduggan88.github.io/closetly/manage/
  - Fully client-side: closet state lives in her browser's localStorage
    (photos as data URLs), with Export/Import JSON for backup + moving devices.
  - **Publish to shop** commits listed pieces (public fields only) + photos +
    a cache-bumped sw.js straight to this repo via the GitHub Contents API,
    using a fine-grained PAT (Contents read/write on this repo only) pasted
    once into Settings.
  - The manager page itself is public but holds no data — everything private
    stays in her browser.

## Source of truth

Since 2026-07-17 the closet data is owned by the manager (Jasmine's browser).
The original Mac-server app in `~/closetly` and its `build.py` flow still work
but are legacy/bootstrap — don't push from the Mac unless you know her copy
hasn't diverged. Seed/export files (`closet-export.json`) contain private data
and must never be committed here.
