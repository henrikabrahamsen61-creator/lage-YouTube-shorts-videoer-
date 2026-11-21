# GTA 6 Shorts med Artlist + Claude

Her ligger alt vi lager: idéer, manus, prompts, valg av musikk og lyd, og ferdige klipp.

## Arbeidsflyt (ett klipp)

| Steg | Hva | Hvem |
|---|---|---|
| 1. Idé | Du gir tema/nisje, jeg lager 3–5 vinkler med en sterk *hook* | Du + Claude |
| 2. Manus | 30–60 sek manus: hook (0–2 s) → innhold → avslutning/CTA | Claude |
| 3. Shot-liste | Hver scene får sin prompt (9:16, 3–8 sek) | Claude |
| 4. Generering | Bilder/video i Artlist. Video lages først som 480p-utkast, så rendres de beste i 1080p (sparer kreditter) | Claude via Artlist |
| 5. Lyd | Voiceover (Artlist-stemme eller din klonede stemme), musikk fra Artlist-katalogen, lydeffekter | Claude via Artlist |
| 6. Sammensetting | `scripts/sett-sammen.sh` limer scener + voice + musikk + teksting til 1080×1920 | Claude |
| 7. Publisering | Tittel, beskrivelse, hashtags ligger i `plan.md` | Du laster opp |

## Mappestruktur

```
maler/klipp-mal.md     ← mal for hvert nytt klipp
klipp/NNN-navn/        ← ett klipp per mappe
  plan.md              ← idé, manus, shot-liste, prompts, musikk, status
  teksting.srt         ← undertekster
  media/               ← nedlastede filer (ikke i git, se under)
  ferdig/              ← ferdig short
scripts/sett-sammen.sh ← ffmpeg-skript for å lage ferdig video
tillatelser/           ← skriftlige tillatelser for gameplay fra andre + mal for forespørsel
```

## Tips for best resultat

- **Hooken avgjør alt.** De første 1–2 sekundene må vise noe overraskende eller stille et spørsmål.
- **Fast stil = gjenkjennelig kanal.** Vi lager et *style kit* i Artlist (farger, stil, referansebilder) som brukes på alle genereringer.
- **Faste figurer.** Har kanalen en karakter/maskot, lagrer vi den som referanse så den ser lik ut i alle klipp.
- **Korte scener.** 2–4 sek per klipp holder tempoet oppe i Shorts.
- **Teksting alltid på.** De fleste ser Shorts uten lyd.
- **Lisens:** Planen vår (AI Suite) dekker AI-generert innhold. Musikk fra katalogen lastes ned med vannmerke, så vi lager egen AI-musikk.

## Store filer

Videofiler kan bli større enn GitHubs grense på 100 MB per fil. Derfor ignoreres `media/` (råfiler).
Ferdige shorts i `ferdig/` blir committet så lenge de er under ~90 MB, og det er de normalt (60 sek 1080p ≈ 20–50 MB).
I `plan.md` noterer vi hvilken Artlist-generering hver scene kom fra, så råfilene kan hentes på nytt.
