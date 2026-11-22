#!/usr/bin/env bash
# Setter sammen en YouTube Short (1080x1920) fra scener, voiceover, musikk og undertekster.
#
# Bruk: scripts/sett-sammen.sh klipp/001-navn
#
# Forventer i klippmappen:
#   media/scene-01.mp4, scene-02.mp4 ...  (spilles i navnerekkefølge)
#   media/voice.mp3       (valgfri)
#   media/musikk.mp3      (valgfri, dempes under stemmen)
#   teksting.srt          (valgfri, brennes inn)
#   hook.txt              (valgfri, stor tekst øverst de første 3 sek, maks ca. 20 tegn per linje)
# Resultat: ferdig/short.mp4
set -euo pipefail

DIR="${1:?Oppgi klippmappe, f.eks. klipp/001-navn}"
MEDIA="$DIR/media"
OUT="$DIR/ferdig/short.mp4"
mkdir -p "$DIR/ferdig"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

shopt -s nullglob
SCENER=("$MEDIA"/scene-*.mp4)
[ ${#SCENER[@]} -gt 0 ] || { echo "Fant ingen $MEDIA/scene-*.mp4"; exit 1; }

# 1) Normaliser hver scene til 1080x1920, 30 fps, uten lyd
i=0
for s in "${SCENER[@]}"; do
  i=$((i+1))
  ffmpeg -loglevel error -y -i "$s" -an \
    -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p" \
    -c:v libx264 -preset fast -crf 18 "$TMP/n$(printf %02d $i).mp4"
  echo "file '$TMP/n$(printf %02d $i).mp4'" >> "$TMP/liste.txt"
done

# 2) Lim sammen
ffmpeg -loglevel error -y -f concat -safe 0 -i "$TMP/liste.txt" -c copy "$TMP/video.mp4"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$TMP/video.mp4")

# 3) Lyd: stemme + musikk (musikken dukkes under stemmen)
INPUTS=(-i "$TMP/video.mp4")
FILTER=""
MAP_A=()
if [ -f "$MEDIA/voice.mp3" ] && [ -f "$MEDIA/musikk.mp3" ]; then
  INPUTS+=(-i "$MEDIA/voice.mp3" -stream_loop -1 -i "$MEDIA/musikk.mp3")
  FILTER="[2:a]volume=0.35[m];[m][1:a]sidechaincompress=threshold=0.05:ratio=8:release=400[md];[1:a][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1[a]"
  MAP_A=(-map "[a]")
elif [ -f "$MEDIA/voice.mp3" ]; then
  INPUTS+=(-i "$MEDIA/voice.mp3"); FILTER="[1:a]loudnorm=I=-14:TP=-1[a]"; MAP_A=(-map "[a]")
elif [ -f "$MEDIA/musikk.mp3" ]; then
  INPUTS+=(-i "$MEDIA/musikk.mp3"); FILTER="[1:a]afade=t=out:st=$(echo "$DUR-1.5" | bc):d=1.5,loudnorm=I=-14:TP=-1[a]"; MAP_A=(-map "[a]")
fi

# 4) Undertekster (store, sentrert litt under midten – Shorts-stil)
VF="null"
if [ -f "$DIR/teksting.srt" ]; then
  VF="subtitles='$DIR/teksting.srt':force_style='FontName=DejaVu Sans,FontSize=16,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=0,Alignment=2,MarginV=90'"
fi
# Hook-tekst: gul, stor, øverst, synlig fra første bilde i 3 sek
if [ -f "$DIR/hook.txt" ]; then
  VF="$VF,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:textfile='$DIR/hook.txt':fontsize=92:fontcolor=0xFFE600:borderw=8:bordercolor=black:line_spacing=12:x=(w-text_w)/2:y=230:enable='lt(t,3)'"
fi

if [ -n "$FILTER" ]; then
  ffmpeg -loglevel error -y "${INPUTS[@]}" -filter_complex "$FILTER" -map 0:v "${MAP_A[@]}" \
    -vf "$VF" -t "$DUR" -c:v libx264 -preset medium -crf 20 -c:a aac -b:a 192k -movflags +faststart "$OUT"
else
  ffmpeg -loglevel error -y -i "$TMP/video.mp4" -vf "$VF" -c:v libx264 -preset medium -crf 20 -movflags +faststart "$OUT"
fi

echo "Ferdig: $OUT ($(du -h "$OUT" | cut -f1), ${DUR%.*} sek)"
[ "${DUR%.*}" -le 60 ] || echo "Advarsel: over 60 sek – YouTube kan fortsatt godta opptil 3 min, men 60 sek eller mindre er tryggest."
