#!/usr/bin/env python3
"""Henter offentlig YouTube-statistikk for kanalen og skriver innsikt/youtube-api.md og .json.

Krever miljøvariabelen YOUTUBE_API_KEY (YouTube Data API v3).
Bruk: python3 scripts/hent-statistikk.py
"""
import json, os, sys, urllib.parse, urllib.request
from datetime import datetime, timezone

KANAL = "UCSkrhplI0A121BXm6pd4Q6g"  # @vicehexdispatch
KEY = os.environ.get("YOUTUBE_API_KEY")
if not KEY:
    sys.exit("YOUTUBE_API_KEY mangler. Sesjonen må startes på nytt etter at variabelen er lagt inn.")

def api(sti, **p):
    p["key"] = KEY
    url = f"https://www.googleapis.com/youtube/v3/{sti}?" + urllib.parse.urlencode(p)
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)

kanal = api("channels", part="statistics,contentDetails,snippet", id=KANAL)["items"][0]
opplastinger = kanal["contentDetails"]["relatedPlaylists"]["uploads"]

ids, token = [], None
while True:
    p = dict(part="contentDetails", playlistId=opplastinger, maxResults=50)
    if token: p["pageToken"] = token
    side = api("playlistItems", **p)
    ids += [i["contentDetails"]["videoId"] for i in side["items"]]
    token = side.get("nextPageToken")
    if not token: break

videoer = []
for i in range(0, len(ids), 50):
    for v in api("videos", part="statistics,snippet,contentDetails", id=",".join(ids[i:i+50]))["items"]:
        s = v["statistics"]
        videoer.append(dict(
            id=v["id"], tittel=v["snippet"]["title"], publisert=v["snippet"]["publishedAt"],
            varighet=v["contentDetails"]["duration"],
            visninger=int(s.get("viewCount", 0)), likes=int(s.get("likeCount", 0)),
            kommentarer=int(s.get("commentCount", 0))))
videoer.sort(key=lambda v: v["publisert"], reverse=True)

nå = datetime.now(timezone.utc)
data = dict(hentet=nå.isoformat(), kanal=dict(
    navn=kanal["snippet"]["title"],
    abonnenter=int(kanal["statistics"].get("subscriberCount", 0)),
    visninger=int(kanal["statistics"].get("viewCount", 0)),
    videoer=int(kanal["statistics"].get("videoCount", 0))), videoer=videoer)

os.makedirs("innsikt", exist_ok=True)
json.dump(data, open("innsikt/youtube-api.json", "w"), ensure_ascii=False, indent=2)

k = data["kanal"]
linjer = [f"# YouTube-statistikk fra API ({k['navn']})", "",
          f"Hentet: {nå:%Y-%m-%d %H:%M} UTC. Offentlige tall fra YouTube Data API. "
          "Viewed vs. swiped away og visningstid finnes ikke her.", "",
          f"**Kanal:** {k['abonnenter']} abonnenter, {k['visninger']} visninger, {k['videoer']} videoer", "",
          "| Publisert | Video | Visninger | Likes | Kommentarer |", "|---|---|---:|---:|---:|"]
for v in videoer:
    linjer.append(f"| {v['publisert'][:10]} | [{v['tittel']}](https://youtube.com/shorts/{v['id']}) | "
                  f"{v['visninger']} | {v['likes']} | {v['kommentarer']} |")
open("innsikt/youtube-api.md", "w").write("\n".join(linjer) + "\n")
print("\n".join(linjer))
