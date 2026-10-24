# Five Wisdom Traditions

A single-page app on the common principles of the major religions, and the most-quoted passages of the Bible, Tao Te Ching, Quran, Buddhist sutras and the Analects of Confucius: what each one means, where it comes from, and how to live it today.

**Live site:** https://deanho1-ui.github.io/Wisdom-Traditions/

## What's inside

- **Primer:** 14 short chapters adapted from the discussion series *Common Principles of the Major Religions* (2017–2018): the Five Constant Virtues, cause and effect, the Six Paramitas, the Five Human Relationships and more. You can skip it.
- **Today:** a passage of the day with one practice to try.
- **Passages:** 500 passages, 100 from each tradition, searchable and filterable by tradition and theme. Each one has its meaning, context, what it meant then and how it's used today, where it's most often quoted (settings, famous uses, and cross-references within the scriptures), daily practices, a reflection question and a link to the full source text.
- **Common threads:** passages grouped by shared themes.
- **Learn:** a quiz, side-by-side answers from all five traditions to 24 life questions, 8 reading plans, a family section with 50 retellings for children, an introduction to each tradition, a timeline, a glossary, and guidance on hard passages.
- **Practice:** reflections, saved passages and an optional practice streak.

## Podcast

Thirty five-minute episodes (one per Primer chapter, one per tradition, one per theme) as two-host conversations, playable in the app with transcripts. Voices are AI-generated with the open-source [Kokoro](https://github.com/hexgrad/kokoro) text-to-speech model, recorded for free on GitHub Actions (`scripts/render_podcast.py`, `.github/workflows/podcast.yml`). Follow it in a podcast app with the feed: https://deanho1-ui.github.io/Wisdom-Traditions/podcast/feed.xml

## For discussion groups

- **Guess the sage:** in any Primer chapter, hide who said each quote and reveal them one by one.
- **Handouts:** "Make a handout" prints a session sheet with the quotes, discussion questions and an answer key (or save it as a PDF).

## Corrections

Every passage has a "Suggest a correction" link that opens a GitHub issue with the passage details filled in.

## Installing it as an app

The site is an installable web app: it opens full-screen with its own icon and works offline.

- **iPhone / iPad:** open the site in Safari, tap Share, then Add to Home Screen.
- **Android:** open the site in Chrome, tap the menu, then Add to Home screen (or Install app).
- **Computer:** in Chrome or Edge, click the install icon in the address bar.

## Files

- `index.html`: the whole app (no build step). It also works when opened directly from disk.
- `manifest.webmanifest`, `sw.js`, `icons/`: what makes it installable and available offline.
- `scripts/check-links.mjs`: checks every source link (runs automatically on GitHub after each change).

Saved passages and reflections are stored only in each visitor's own browser.

## Coverage

- **Bible:** 100 passages across the Old and New Testaments (King James Version)
- **Taoism:** all 81 chapters of the Tao Te Ching, plus 19 stories from the Zhuangzi
- **Quran:** 100 of the most recited and taught verses and short surahs
- **Buddhism:** 48 from the Dhammapada and 52 from the suttas and Mahayana, Chan/Zen and Pure Land texts
- **Confucianism:** the Four Books: Analects, Mencius, Great Learning and Doctrine of the Mean

## Translations

The Bible is quoted from the King James Version. The Tao Te Ching, Analects and Dhammapada are adapted from James Legge and Max Müller (public domain). The Quran and other sutras are rendered in plain modern English after public-domain translations. Translations are approximate; use the source links to read each passage in context.
