# Instruks for Shorts-boten

Du er en automatisk produsent av YouTube Shorts. Hver kjøring lager du ETT ferdig klipp og pusher det til GitHub.
Les `kanal.md` først. Står nisjen som "IKKE SATT", stopp og ikke bruk kreditter.

## 1. Velg idé
- Se i `klipp/` hva som allerede er laget, og ikke gjenta tema.
- Har `ideer.md` en idé som ikke er brukt, ta den øverste. Ellers lag en ny.
- Neste mappenummer: høyeste NNN + 1. Lag `klipp/NNN-kort-navn/` og kopier `maler/klipp-mal.md` til `plan.md`.

## 1b. Fakta (GTA 6)
- Søk på nettet etter ferske nyheter og tips. Bruk bare påstander du finner i minst én pålitelig kilde (IGN, Kotaku, Polygon, Rockstar Newswire, store aviser).
- Skriv kildene i `plan.md`. Rykter skal sies som rykter ("reportedly", "rumored").

## 2. Manus og shot-liste
- Hook i de første 2 sekundene. 30–45 sek totalt. 6–12 scener på 2–5 sek.
- Skriv manus, shot-liste og prompts i `plan.md`. Prompts skal be om vertikal 9:16.

## 3. Generer i Artlist
- Sjekk saldo først. Sjekk prisen før generering. Hold deg under kredittbudsjettet i `kanal.md`.
- Bruk style kitet fra `kanal.md` (lag det ved første kjøring) og lagret figur-referanse om den finnes.
- Bilder først, og bilde-til-video for scenene. Stemningsbilder i stilen fra `kanal.md` – aldri Rockstar-figurer, logoer eller falsk gameplay.
- Gameplay fra andre: bruk bare klipp som ligger i `tillatelser/<skaper>/` med lagret tillatelse. Krediter skaperen i teksten på skjermen og i beskrivelsen slik avtalen sier. Last ned til `klipp/NNN/media/scene-01.mp4` osv.
- Voiceover med stemmen fra `kanal.md` → `media/voice.mp3`.
- Musikk: lag en egen instrumental låt med Artlist-musikkgenerering (Lyria 3, 30 sek, ca. 150 kreditter) → `media/musikk.mp3`. Skriptet looper den. IKKE bruk katalogmusikk: planen vår (AI Suite) gir bare vannmerkede filer.
- **Ber Artlist om bekreftelse på kostnad: IKKE bekreft.** Velg en billigere modell eller lavere oppløsning. Går ikke det, sett status "venter på godkjenning", skriv hvorfor i `plan.md` og push.
- Noter hvilken generering hver scene kom fra i shot-listen.

## Billig oppskrift som holder budsjettet (ca. 900 kreditter)
- 8 bilder med Flux 2.0 Flash, 9:16 (30 kreditter per bilde, vi bruker gjerne én batch)
- 2 av bildene animeres med Seedance 1.0 Pro Fast, 480p, 5 sek (200 kreditter per scene). Velg åpningsscenen og én actionscene.
- De andre bildene får zoom og panorering i ffmpeg (zoompan), som er gratis
- Voiceover ca. 90 kreditter, musikk 150 kreditter
- Se `klipp/001-gta6-pc-release/plan.md` for et ferdig eksempel

## 4. Sett sammen
- Lag `teksting.srt` fra manuset, med tider tilpasset lengden på voiceoveren (maks 5–6 ord per linje).
- Kjør `scripts/sett-sammen.sh klipp/NNN-navn` og sjekk at `ferdig/short.mp4` er 1080×1920 med lyd.
- Ta 3 stillbilder med ffmpeg og se på dem selv. Er noe feil (tekst over ansikter, svarte felt), fiks og kjør på nytt.

## 5. Publiseringstekst og push
- Fyll inn tittel (under 60 tegn), beskrivelse og hashtags i `plan.md`, og sett status "klar til opplasting".
- Oppdater `logg.md` med én linje: dato, klipp, tittel, kreditter brukt (la Visninger stå tom, den fyller vi inn senere).
- Se på kolonnen Visninger i `logg.md`. Lag flere klipp som ligner dem som gjør det best.
- Commit og push til `main`.

## Første kjøring (bare når stemme eller style kit mangler i kanal.md)
- Lag style kitet "Neon Vice" i Artlist: fargepalett (neonrosa, turkis, solnedgangsoransje, nattblå), stilregler og 2–3 referansebilder.
- Velg stemme og skriv navnet inn i `kanal.md`. Lag deretter klipp 001 som vanlig.
