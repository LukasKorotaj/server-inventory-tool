<!-- LTex: language=sv-->
# Server Inventory Tool

Ett litet kommandoradsverktyg för att hålla ordning på servrar: lägga till och ta
bort dem, kontrollera om de svarar på ping, spara dem i JSON mellan körningarna och
exportera en CSV-rapport. Verktyget kan användas på två sätt: via en interaktiv
textmeny eller direkt från kommandoraden.

## Funktioner

- Håller reda på servrar med `namn`, `adress`, `miljo`, `roll`, `status` och `senast_kontrollerad`.
- Sparar alla servrar i en JSON-fil som läses in vid start och uppdateras vid varje ändring.
- Kontrollerar om en server (eller alla) svarar på ping.
- Exporterar alla servrar till en CSV-rapport med rubrikrad.
- Kan användas både via en textmeny och via argument på kommandoraden.

## Krav

- **Python 3.10 eller senare**. Testat med [`vermin`](https://github.com/netromdk/vermin).

## Kom igång

```bash
git clone https://github.com/LukasKorotaj/server-inventory-tool.git
cd server-inventory-tool
```

Projektet innehåller redan en `servrar.json` med exempeldata, så det går att köra
direkt. Om filen saknas skapas den automatiskt som en tom lista.

## Meny

Starta utan argument:

```bash
python main.py
```

Menyn visas i en loop och innehåller:

1. Visa alla servrar
2. Visa servrar i en viss miljö
3. Lägg till en server
4. Ta bort en server
5. Kontrollera en server
6. Kontrollera alla servrar
7. Exportera som CSV
8. Avsluta

Skriv siffran för ditt val. Ogiltiga val ger ett meddelande och menyn visas igen.
Vid inmatning av namn, miljö och adress kan du skriva `q` för att avbryta. När du
tar bort en server i miljön `prod` måste du bekräfta borttagningen extra.

## CLI

| Kommando | Beskrivning |
|---|---|
| `python main.py` | Startar textmenyn. |
| `python main.py --lista` | Skriver ut alla servrar och avslutar. |
| `python main.py --lista --miljo prod` | Skriver bara ut servrar i miljön `prod`. |
| `python main.py --kontrollera web01` | Kontrollerar servern `web01`. |
| `python main.py --kontrollera-alla` | Kontrollerar alla servrar. |
| `python main.py --export` | Skapar en CSV-rapport. |
| `python main.py --help` | Visar hjälptexten. |

`--miljo` får bara användas tillsammans med `--lista` och accepterar `dev`, `test`
eller `prod`.

## Exitkoder

| Kod | Betydelse |
|---|---|
| `0` | Allt gick bra. |
| `1` | Minst en server är nere, eller servern i `--kontrollera` finns inte. |
| `2` | Felaktig kombination av argument, till exempel `--miljo` utan `--lista`. |

## Miljövariabel

Vilken JSON-fil som används styrs av miljövariabeln `INVENTORY_DATAFIL`. Om
variabeln inte är satt används standardvärdet `servrar.json` i projektets rot.

```bash
INVENTORY_DATAFIL=/tmp/mina_servrar.json python main.py --lista
```

## CSV-rapporter

Rapporter sparas i katalogen `rapporter/` och filnamnet innehåller datum och tid:

```text
rapporter/inventering_2026-11-15_1337.csv
```

Katalogen skapas automatiskt om den inte finns. Filen har en rubrikrad med alla
fält och en rad per server.

## Projektstruktur

```text
server-inventory-tool/
├── main.py         ← startpunkt, läser argument med argparse och kör CLI-läget
├── meny.py         ← textmenyn och dess funktioner
├── lagring.py      ← läser och sparar JSON samt exporterar CSV
├── kontroller.py   ← kontrollerar om servrar svarar på ping
├── servrar.json    ← sparad serverdata
├── tests/          ← enhetstester (pytest)
├── .gitignore      ← ignorerar __pycache__/ och rapporter/
├── REDOGORELSE.md  ← skriftlig redogörelse
└── REFLEKTION.md   ← skriftlig reflektion (VG)
```

Ansvarsfördelning:

- **`main.py`** – programmets startpunkt. Parsar kommandoradsargument med `argparse`
  och anropar antingen menyn (`meny.menu_loop()`) eller rätt CLI-funktion.
- **`meny.py`** – textmenyn, all inmatning från användaren och utskrift av servrar.
- **`lagring.py`** – all hantering av datafilen: läsa/skriva JSON, lägga till, ta
  bort och uppdatera servrar samt exportera CSV.
- **`kontroller.py`** – ping-kontrollen via `subprocess.run()`. Både menyn och
  CLI-läget använder samma funktion, så logiken finns bara på ett ställe.
- **`tests/`** – enhetstester för lagring och kontroll.

## Tester
Tester kräver `pytest` vilken inte är en del av python standard library. 
Allting testas inte. Jag ville mest prova hur man anväder `pytest`.

```bash
python -m pytest
```
