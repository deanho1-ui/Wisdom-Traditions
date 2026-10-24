"""Render podcast episodes to MP3 with Kokoro (open-source text-to-speech) and build the RSS feed.

Runs on GitHub Actions (see .github/workflows/podcast.yml). Only episodes whose script
changed since the last render are re-recorded.
"""
import hashlib, json, os, subprocess, sys, tempfile
from datetime import datetime, timezone, timedelta
from email.utils import format_datetime
from xml.sax.saxutils import escape

import numpy as np
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POD = os.path.join(ROOT, "podcast")
AUDIO = os.path.join(POD, "audio")
SITE = "https://deanho1-ui.github.io/Wisdom-Traditions/"
VOICES = {"A": "af_heart", "B": "am_michael"}
RATE = 24000
VERSION = "1"  # bump to force a full re-render

if not os.path.exists(os.path.join(POD, "episodes.json")):
    print("No episodes.json yet; nothing to record.")
    sys.exit(0)
episodes = json.load(open(os.path.join(POD, "episodes.json")))
manifest_path = os.path.join(POD, "manifest.json")
manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {}
os.makedirs(AUDIO, exist_ok=True)

def ep_hash(ep):
    raw = json.dumps({"v": VERSION, "voices": VOICES, "lines": ep["lines"]}, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

todo = [ep for ep in episodes if manifest.get(ep["id"], {}).get("hash") != ep_hash(ep)
        or not os.path.exists(os.path.join(AUDIO, ep["id"] + ".mp3"))]
print(f"{len(episodes)} episodes, {len(todo)} to render", flush=True)

if todo:
    from kokoro import KPipeline
    pipe = KPipeline(lang_code="a")
    gap = np.zeros(int(RATE * 0.38), dtype=np.float32)
    lead = np.zeros(int(RATE * 0.25), dtype=np.float32)
    for n, ep in enumerate(todo, 1):
        parts = [lead]
        for line in ep["lines"]:
            for res in pipe(line["t"], voice=VOICES[line["s"]], speed=1.0):
                audio = res[2] if isinstance(res, tuple) else res.audio
                if audio is None: continue
                audio = audio.detach().cpu().numpy() if hasattr(audio, "detach") else np.asarray(audio)
                parts.append(audio.astype(np.float32))
            parts.append(gap)
        wav = np.concatenate(parts)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            sf.write(tmp.name, wav, RATE)
        out = os.path.join(AUDIO, ep["id"] + ".mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp.name, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                        "-ac", "1", "-ar", "24000", "-b:a", "56k", out], check=True)
        os.unlink(tmp.name)
        manifest[ep["id"]] = {"hash": ep_hash(ep), "duration": round(len(wav) / RATE), "bytes": os.path.getsize(out),
                              "rendered": datetime.now(timezone.utc).strftime("%Y-%m-%d")}
        print(f"[{n}/{len(todo)}] {ep['id']}: {manifest[ep['id']]['duration']}s", flush=True)

# drop audio for episodes that no longer exist
ids = {ep["id"] for ep in episodes}
for k in list(manifest):
    if k not in ids:
        manifest.pop(k)
        p = os.path.join(AUDIO, k + ".mp3")
        if os.path.exists(p): os.remove(p)
json.dump(manifest, open(manifest_path, "w"), indent=1, sort_keys=True)

# RSS feed (Apple Podcasts / Pocket Casts / Overcast compatible)
order = {"primer": 0, "tradition": 1, "theme": 2}
base = datetime(2026, 10, 25, 12, tzinfo=timezone.utc)
items = []
ordered = sorted(episodes, key=lambda e: (order.get(e["kind"], 9), e["id"] if e["kind"] != "primer" else int(e["ref"])))
for i, ep in enumerate(ordered):
    m = manifest.get(ep["id"])
    if not m: continue
    url = SITE + "podcast/audio/" + ep["id"] + ".mp3"
    dur = m["duration"]
    transcript = "\n\n".join(l["t"] for l in ep["lines"])
    items.append(f"""    <item>
      <title>{escape(ep['title'])}</title>
      <description>{escape(ep['desc'])}</description>
      <content:encoded><![CDATA[<p>{escape(ep['desc'])}</p><p>{escape(transcript).replace(chr(10)*2, '</p><p>')}</p>]]></content:encoded>
      <enclosure url="{url}" length="{m['bytes']}" type="audio/mpeg"/>
      <guid isPermaLink="false">fwt-{ep['id']}</guid>
      <pubDate>{format_datetime(base - timedelta(hours=i))}</pubDate>
      <itunes:duration>{dur // 60}:{dur % 60:02d}</itunes:duration>
      <itunes:episodeType>full</itunes:episodeType>
      <itunes:explicit>false</itunes:explicit>
      <link>{SITE}#learn</link>
    </item>""")
feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Five Wisdom Traditions</title>
    <link>{SITE}</link>
    <atom:link href="{SITE}podcast/feed.xml" rel="self" type="application/rss+xml"/>
    <language>en</language>
    <description>Five-minute conversations on the common principles of the major religions and the most-quoted passages of the Bible, the Tao Te Ching, the Quran, the Buddhist sutras and Confucius: what they meant, how they are used today, and how to live them. Voices are AI-generated with the open-source Kokoro text-to-speech model.</description>
    <itunes:author>Five Wisdom Traditions</itunes:author>
    <itunes:summary>Five-minute conversations on the common principles of the major religions and the most-quoted passages of five wisdom traditions.</itunes:summary>
    <itunes:image href="{SITE}podcast/cover.png"/>
    <image><url>{SITE}podcast/cover.png</url><title>Five Wisdom Traditions</title><link>{SITE}</link></image>
    <itunes:category text="Religion &amp; Spirituality"/>
    <itunes:explicit>false</itunes:explicit>
    <itunes:type>serial</itunes:type>
{chr(10).join(items)}
  </channel>
</rss>
"""
open(os.path.join(POD, "feed.xml"), "w").write(feed)
print("feed items:", len(items))
