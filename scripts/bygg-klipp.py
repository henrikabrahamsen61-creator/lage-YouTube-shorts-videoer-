#!/usr/bin/env python3
"""Bygger scener, undertekster og hook for et klipp, og kjører sett-sammen.sh.

Bruk: python3 scripts/bygg-klipp.py klipp/NNN-navn
Leser klipp/NNN-navn/bygg.json:
  {"manus": "...", "hook": "LINJE 1\\nLINJE 2",
   "scener": ["media/v1.mp4", "klipp/001-.../media/bilder/scene-08.png", ...]}
Videoer (.mp4) klippes, bilder (.png) får zoom. Lengden fordeles likt over scenene,
slik at klippet blir like langt som media/voice.mp3. Undertekstene times etter
pausene i stemmen.
"""
import json, os, re, subprocess, sys

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = os.path.abspath(sys.argv[1]); m = os.path.join(d, "media")
cfg = json.load(open(os.path.join(d, "bygg.json")))

def run(*a): return subprocess.run(a, capture_output=True, text=True)
def varighet(f): return float(run("ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f).stdout)

dur = varighet(os.path.join(m, "voice.mp3")) + 0.3
scener = cfg["scener"]; n = len(scener); L = dur / n
for f in os.listdir(m):
    if re.match(r"scene-\d+\.mp4$", f): os.remove(os.path.join(m, f))
brukt = {}
for i, s in enumerate(scener, 1):
    src = s if os.path.isabs(s) else (os.path.join(d, s) if s.startswith("media/") else os.path.join(ROT, s))
    ut = os.path.join(m, f"scene-{i:02d}.mp4")
    if src.endswith(".mp4"):
        off = 0.0 if src not in brukt else max(0.0, varighet(src) - L)
        brukt[src] = 1
        run("ffmpeg","-loglevel","error","-y","-ss",f"{off:.2f}","-i",src,"-t",f"{L:.3f}","-an","-vf",
            "scale=1080:1920:flags=lanczos,fps=30,format=yuv420p","-c:v","libx264","-preset","fast","-crf","18",ut)
    else:
        fr = int(round(L*30)); z = "min(1+0.0015*on,1.3)" if i % 2 else "max(1.3-0.0015*on,1)"
        run("ffmpeg","-loglevel","error","-y","-loop","1","-i",src,"-vf",
            f"scale=2160:3840,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps=30,format=yuv420p",
            "-frames:v",str(fr),"-c:v","libx264","-preset","fast","-crf","18",ut)

# Undertekster: finn tale-intervaller fra pausene, fordel ord etter antall tegn
st = run("ffmpeg","-i",os.path.join(m,"voice.mp3"),"-af","silencedetect=noise=-30dB:d=0.15","-f","null","-").stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", st)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", st)]
vd = dur - 0.3; tale = []; t = 0.0
for s0, e0 in zip(starts, ends + [vd]*(len(starts)-len(ends))):
    if s0 > t: tale.append((t, s0))
    t = e0
if t < vd: tale.append((t, vd))
total = sum(b-a for a, b in tale)
ord_ = cfg["manus"].split(); biter = [ord_[i:i+4] for i in range(0, len(ord_), 4)]
if len(biter) > 1 and len(biter[-1]) == 1: biter[-2] += biter.pop()
tegn = sum(len(" ".join(b)) for b in biter)
def til_tid(x):  # x = sekunder tale -> faktisk tid
    for a, b in tale:
        if x <= b - a: return a + x
        x -= b - a
    return vd
def ts(t):
    ms = int(round(t*1000)); return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"
srt = []; acc = 0.0
for i, b in enumerate(biter, 1):
    l = total * len(" ".join(b)) / tegn
    srt.append(f"{i}\n{ts(til_tid(acc)+0.02)} --> {ts(til_tid(acc+l))}\n{' '.join(b).upper()}\n"); acc += l
open(os.path.join(d, "teksting.srt"), "w").write("\n".join(srt))
open(os.path.join(d, "hook.txt"), "w").write(cfg["hook"])
print(run(os.path.join(ROT, "scripts", "sett-sammen.sh"), d).stdout.strip())
