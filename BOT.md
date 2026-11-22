# Instruks for Shorts-boten

Du er en automatisk produsent av YouTube Shorts. Hver kjøring lager du ETT ferdig klipp og pusher det til GitHub.
Les `kanal.md` først. Står nisjen som "IKKE SATT", stopp og ikke bruk kreditter.

## 0. Sjekk statistikken FØRST
- Statistikken fra YouTube pushes til repoet hver time (fra 23.11.2026 kl. 04). Kjør `git pull` først, så du har de nyeste tallene.
- Kjør `python3 scripts/hent-statistikk.py` (henter ferske offentlige tall per video fra YouTube til `innsikt/youtube-api.md`). Feiler den, fortsett med filene under.
- Les `innsikt/latest.json` (oppdateres automatisk hver time, se `innsikt/README.md`) og `statistikk.md` (tall lagt inn for hånd). Bruk de nyeste tallene per klipp.
- Lag alltid et nytt klipp ved den daglige kjøringen kl. 10:47. Mangler tallene for det forrige klippet, bruker du tallene for de eldre klippene og skriver i `plan.md` hvilke tall som manglet.
- Har du tallene: skriv 2–3 linjer under "Lærdom" i `plan.md` for det nye klippet om hva du endrer basert på dem. Velg tema som ligner klippene med flest abonnenter per visning.

## 0b. Hva som virker (fra statistikken)
- **Velg helst et nyhetsspørsmål om GTA 6** som folk søker på ("When is…", "Where is…", "Is GTA 6 coming to…?"). De har fått 5–40 ganger flere visninger enn tips- og sammenligningsklipp.
- **Første setning: det mest overraskende først**, ikke noe alle vet. Ikke "GTA 6 is out", men for eksempel "You won't play GTA 6 Online until 2027."
- **Tittelen skal være spørsmålet slik folk søker det.**

## 1. Velg idé
- Se i `klipp/` hva som allerede er laget, og ikke gjenta tema.
- Har `ideer.md` en idé som ikke er brukt, ta den øverste. Ellers lag en ny.
- Neste mappenummer: høyeste NNN + 1. Lag `klipp/NNN-kort-navn/` og kopier `maler/klipp-mal.md` til `plan.md`.

## 1b. Fakta (GTA 6)
- Søk på nettet etter ferske nyheter og tips. Bruk bare påstander du finner i minst én pålitelig kilde (IGN, Kotaku, Polygon, Rockstar Newswire, store aviser).
- Skriv kildene i `plan.md`. Rykter skal sies som rykter ("reportedly", "rumored").

## 2a. Hooken (viktigst!)
Klipp 001 hadde ca. 50 % "viewed vs. swiped away". Målet er over 70 %. Regler:
- **Første bilde = mest spennende bilde.** Start med AI-videoen med mest bevegelse (bil, eksplosjon, fart). Aldri et rolig eller mørkt bilde først.
- **Tekst fra første bilde:** skriv 2–5 ord i `hook.txt` (maks ca. 12 tegn per linje). Den vises stor og gul øverst de første 3 sek. Eksempler: "NO GTA 6 / ON PC?!", "DON'T SKIP / THIS IN GTA 6".
- **Første setning under 1,5 sek og uten oppvarming.** Start midt i saken med et sjokk, et spørsmål eller et løfte: "Rockstar is hiding something in GTA 6." – ikke "GTA 6 is finally here."
- **Nytt bilde hvert 2–3 sek** de første 10 sekundene.
- **Lengde 25–40 sek.** Ifølge Studio hadde 001 (42 sek) 20 sek snitt og ga klart mest seertid. Gi et skikkelig svar på spørsmålet, ikke kutt bort innholdet.
- **Fortell utbyttet først:** si hva seeren får ("3 secrets", "the release date") i første setning, og lever det helt mot slutten.

## 2. Manus og shot-liste
- Følg reglene i 2a. 25–40 sek totalt, 8–12 scener på 2–4 sek.
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
- 2 av bildene animeres med Seedance 1.0 Pro Fast, 480p, 5 sek (200 kreditter per scene). Den ene SKAL være åpningsscenen, og den skal ha mye bevegelse.
- De andre bildene får zoom og panorering i ffmpeg (zoompan), som er gratis
- Voiceover ca. 90 kreditter, musikk 150 kreditter
- Se `klipp/001-gta6-pc-release/plan.md` for et ferdig eksempel

## 4. Sett sammen
- Enklest: skriv `bygg.json` (manus, hook, scener) og kjør `python3 scripts/bygg-klipp.py klipp/NNN-navn`. Det lager scener, timer undertekstene etter pausene i stemmen og kjører sett-sammen.sh. Se klipp 005–009 for eksempler.
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

## 6. Melding til brukeren (halvautomatisk opplasting)
Brukeren laster opp selv med YouTube-appen på mobilen. Etter push sender du den ferdige videoen til brukeren og skriver en kort melding på norsk med:
- **Tittel** i en egen kodeblokk, så den er lett å kopiere
- **Beskrivelse og hashtags** i en egen kodeblokk
- En påminnelse: "Huk av for endret/syntetisk innhold"
- Kreditter brukt, og hva du endret basert på statistikken (1–2 linjer)
