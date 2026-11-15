<!-- LTex: language=sv-->
## Frågor

## 1 
> Välj tre olika konstruktioner i koden, till exempel ett villkor, en loop och en funktion med parametrar och return. Förklara hur syntaxen fungerar och vad koden gör.


[`get_server()`](./lagring.py#L95-L107)

```python
# Definera funktion. Tar namn och server. Server kan vara list eller None.
# Default är None. Den returnerar dict eller None.
def get_server(namn, servers: list | None = None) -> dict | None:
    # Läs server endast om det saknas server argument.
    if servers is None:
        servers = parse_servers_json()

    # Hitta och returnera servern (dict)
    for server in servers:
        if server.get("namn") == namn:
            return server

    # I fall servern inte finns returnera None
    return None

```

`get_server()` letar efter en dict med `"namn"` som matchar `namn` parametern. 
Den letar i `servers` listan eller i `INVENTORY_DATAFIL` om inget annat anges. 
Om servern finns så returneras den som en `dict` annars returneras `None` som 
andra funktioner tar hand om.

[Intersection](./meny.py#L207-L227)

```python
# Skapa en ny set datatyp
return_codes = set()
servers = lg.parse_servers_json()
for s in servers:
    return_codes.add(check_server_status(s["namn"]))

# ...

if return_codes & {1, 2}:
    return 1

return 0
```
Den här if-satsen är mer intressant än man skulle tro. `return_codes` är en `set`. 
En set skiljer sig från andra datatyper för att varje värde i en set är unik. 
Enligt instruktionerna ska `--kontrollera` ge exit-code 1 om antalet servrar som 
är "down" är mer, eller lika med, 1. Med andra ord, vi bryr oss inte om hur många 
gånger 1 dök upp, så det passar att ha en set. 

I själva if-satsen så skapar vi en intersection, med en `&` operator, mellan 
`return_codes` och `{1, 2}`. En intersection skapar en ny set som innehåller element som 
finns i båda sets. Till exempel: 
```python
In [1]: {0, 1} & {1, 2}
Out[1]: {1}

In [2]: {0} & {1, 2}
Out[2]: set() # Tom

In [3]: {0, 1, 2} & {1, 2}
Out[3]: {1, 2}
```

I python, den enda intersection som blir `False` är `{0} & {1, 2}`. Koden returnerar 
0 endast om alla servrar är "up".

[`while True`](./meny.py#L181-L192)

```python
while True:
    k_server = input("Vilken server vill du kontrollera? ('q' avbryt): ")
    # qquit() är en liten helper function för att 
    # avbryta  om användare skriver 'q'
    if qquit(k_server):
        return

    k_server = k_server.lower().strip()

    # ser_names declared outside this 
    # snippet.
    if k_server not in ser_names:
        print(f"{k_server} finns inte!")
        continue

    break
```
Den här loopen är en av sex i `meny.py`. While loopar är perfekta 
när man inte vet hur många fel användaren kommer att göra. Den 
här loopen är den kortaste som har alla nyckelord. `input()` tar 
användarens input som sedan omvandlas till små bokstäver och 
tar bort alla "tomma" tecken (" Web01 " blir "web01", t.ex.). 
`ser_names` har alla namn (gjorde det så jag slipper parsa varje gång). 
Om servern inte finns, så körs `continue` som startar om loopen utan att 
koden under den körs. I fall servern finns så fortsätter programmet 
till `break` som avbryter while loopen helt och får resten av funktionen 
att köra. Om användare skrev `q` så körs `return` istället. Den gör 
att programmet lämnar funktionen helt. 

## 2 
> Varför passar en lista med dictionaries för att lagra servrarna? Vilka datatyper har värdena i en server?

[`add_server()`](./lagring.py#L73-L92)

```python
server = {
    "namn": namn,
    "adress": adress,
    "miljo": miljo,
    "roll": roll,
    "status": "unknown",
    "senast_kontrollerad": "",
}
```

En lista passar för att den behåller ordningen på servrarna och är enkel att 
loopa igenom. En dictionary passar för en enskild server eftersom varje värde får 
ett namn i stället för ett index. Om jag hade använt en lista eller tuple för 
servern hade jag behövt komma ihåg att `server[2]` betyder miljö, vilket är lätt 
att blanda ihop. Med en dict skriver jag `server["miljo"]`.

Alla värden i en server är strängar (`str`). Det gäller även `senast_kontrollerad` 
som antingen är en tom sträng `""` (servern är inte kontrollerad ännu) eller en 
formaterad datumsträng. `miljo` och `status` har bara ett begränsat antal tillåtna 
värden:

- `miljo`: `"dev"`, `"test"` eller `"prod"`
- `status`: `"up"`, `"down"` eller `"unknown"`

## 3 
> Varför sparar du data i JSON men exporterar rapporten som CSV?

Jag använder JSON för att spara eftersom datafilen är programmets "arbetsminne" och 
måste kunna läsas tillbaka precis som den skrevs. En server är en dict med flera 
fält, och en lista av dicts motsvarar exakt en JSON-array av objekt. Med `json.load` 
och `json.dump` i [`parse_servers_json()`](./lagring.py#L48-L58) och 
[`add_server()`](./lagring.py#L73-L92) blir konverteringen fram och tillbaka nästan 
gratis, och formatet är strukturerat och maskinläsbart.

CSV använder jag i stället för rapporten eftersom en rapport är något man läser 
eller öppnar i till exempel Excel. Då passar en platt tabell 
med en rubrikrad och en rad per server bättre.

JSON är till för att spara och läsa tillbaka, CSV är till för att visa 
och dela med sig.

## 4 
> Hur är programmet uppdelat i moduler och funktioner? Vilket ansvar har varje fil?

Programmet är uppdelat i fyra moduler, plus en mapp för tester:

- **[`main.py`](./main.py)** – programmets startpunkt. Här ligger 
  `if __name__ == "__main__":` och `argparse` som läser argumenten. `main.py` 
  bestämmer om textmenyn ska startas eller om ett CLI-kommando ska köras.
- **[`meny.py`](./meny.py)** – textmenyn och allt som har med användarens inmatning 
  och utskrift att göra (`visa_alla`, `lagg_till`, `ta_bort`, `kontrollera_en`, ...).
- **[`lagring.py`](./lagring.py)** – all hantering av data: läsa och skriva JSON, 
  lägga till/ta bort/uppdatera servrar och exportera CSV.
- **[`kontroller.py`](./kontroller.py)** – kontrollen av servrar via `ping`.
- **`tests/`** – enhetstester för `lagring` och `kontroller`.

Menyn och CLI-läget använder samma funktioner i 
`lagring.py` och `kontroller.py`. [`kontrollera_en()`](./meny.py#L173-L204) i menyn 
anropar till exempel `check_server_status()` i 
[`kontroller.py`](./kontroller.py#L17-L50), och `python main.py --kontrollera web01` 
i [`main.py`](./main.py#L59-L60) anropar exakt samma funktion. 
Inuti varje modul är funktionerna uppdelade efter uppgift, till 
exempel `get_server()` (hitta en server), `add_server()` (lägga till) och 
`export_csv()` (exportera) i `lagring.py`.

## 5 
> Vilka moduler från standardbiblioteket använder du och till vad?

- `json` – läsa och skriva serverfilen ([`parse_servers_json()`](./lagring.py#L48-L58)).
- `csv` – skriva CSV-rapporten med `csv.DictWriter` ([`export_csv()`](./lagring.py#L126-L158)).
- `os` – läsa miljövariabeln `INVENTORY_DATAFIL` med `os.environ.get()` ([`get_file()`](./lagring.py#L35-L45)).
- `pathlib` – hantera filsökvägar och skapa datafilen om den saknas med `Path`, 
  `exists()` och `write_text()` ([`get_file()`](./lagring.py#L35-L45)).
- `datetime` – hämta aktuellt datum och tid och formatera med `strftime()` 
  ([`get_current_time()`](./lagring.py#L61-L70)).
- `subprocess` – köra `ping` med `subprocess.run()` ([`check_server_status()`](./kontroller.py#L17-L50)).
- `sys` – läsa `sys.argv` och avsluta med rätt exitkod via `sys.exit()` ([`main.py`](./main.py#L41-L63)).
- `argparse` – bygga kommandoradsgränssnittet och hjälptexten ([`main.py`](./main.py#L25-L38)).

Utöver standardbiblioteket använder jag `pytest` för testerna, men det är inte en 
del av själva programmet.

## 6 
> Ge tre exempel på god praxis från din kod och förklara varför de är bra.

1. Ingen duplicerad logik. Kontrollen av en server finns bara på ett ställe, 
[`check_server_status()`](./kontroller.py#L17-L50). Både menyn 
([`kontrollera_en()`](./meny.py#L173-L204)) och CLI-läget ([`main.py`](./main.py#L59-L60)) 
anropar samma funktion.

2. Context managers när filer öppnas. Jag använder `with open(...) as ...` 
överallt där filer läses eller skrivs, till exempel i 
[`parse_servers_json()`](./lagring.py#L48-L58). Det gör att filen stängs 
automatiskt även om något går fel, i stället för att jag måste komma ihåg att 
stänga den själv.

3. Tydliga namn och typannoteringar. Funktioner och variabler har beskrivande 
namn i `snake_case` utan å, ä och ö, till exempel `check_server_status` och 
`senast_kontrollerad`. Dessutom har känsliga funktioner typannoteringar, som 
`get_server(namn, servers: list | None = None) -> dict | None` i 
[`lagring.py`](./lagring.py#L95-L107). Det gör koden lättare att läsa och hjälper 
LSP att hitta misstag tidigt.

## 7 
> Vilka källor och hjälpmedel har du använt och till vad?

- Pythons officiella dokumentation: (docs.python.org) – för att slå upp detaljer 
  i `argparse`, `csv.DictWriter`, `subprocess.run`, `pathlib` och `json`.
- `man ping` / `ping --help`: – för att ta reda på vad flaggorna `-c` och `-W` 
  gör och vilka exitkoder `ping` returnerar.
- AI-verktyg: – jag har använt Gemini och Deepseek för att granska 
  koden, hitta buggar (till exempel en varning om att `None` inte går att indexera) 
  och förklara varför vissa lösningar är bättre än andra. Jag har skrivit och 
  förstått koden själv.
- `pyright` och `pytest`: – för att typkontrollera koden och köra 
  enhetstesterna.
