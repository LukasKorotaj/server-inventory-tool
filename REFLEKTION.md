<!-- LTeX: language=sv-->
## När ska man spara?
Generellt skulle jag säga att det är smidigare för 
användaren att ändringarna sparas direkt än senare. 
Man behöver inte tänka på att spara manuellt och 
ändringar syns direkt. Om man vill kontrollera och 
lista direkt efteråt så kan man det.

Anledningen till att visa program inte gör det 
är att riskerna överväger fördelarna. I Server 
Inventory Tool så är dessa risker inte så stora. Det 
största problemet med att ändringar sparas direkt är 
att det är svårt att ångra ändringarna. I en bank 
så skulle det vara ett problem om någon kunde radera massa 
konto utan att kunna ångra det. I fall då man vill ha 
både direktsparande och möjligheten att ångra sig 
så måste man ha en historik av alla ändringar vilket 
ökar komplexiteten av programmet. I vårt fall så finns 
det inte så många destruktiva saker man kan göra i programmet. 
Det mest destruktiva är möjligheten att ta bort en server. 
Om det är en production server så får man ett confirm meddelande. 
Även om användaren lyckas ta bort en prod server så är det inte 
så mycket data man förlorar. Det blir jobbigt men det går att lägga 
till den igen ganska fort.

Ett annat fall då det kan bli jobbigt att spara direkt är om vårt program 
skulle skicka tusentals requests eller skriva i en fil väldigt många 
gånger under en kort tid. Jag har varit i fall då någon service 
skrev så många loggar att min dator var långsam eftersom I/O var så stor. 
Server Inventory Tool har inte dessa problem. Om man har 1000 servrar och 
vill kontrollera alla så är det inte så farligt.

Jag tycker att det är bättre att spara efter varje ändring eftersom 
det inte finns någon bra anledning till att inte göra det.

## Använda `subprocess` och `ping` istället för ren python
Varför ska man återuppfinna hjulet? Subprocess och ping är 
battle-tested och det är, i princip, omöjligt att skriva en bättre 
version själv. [Ping](https://en.wikipedia.org/wiki/Ping_(networking_utility)) är 
43 år gammal, den gör en sak och gör den bra. Mänskligheten är baserad på att 
dela information. Om alla skulle lära sig allt själva så skulle vi fortfarande 
jaga med stenar och pinnar. Även om man, av någon superspecifik anledning, vill 
göra sin egen ping så är python sista språket man använder.

## `-o /dev/null` istället för `--out-null`
I [`check_webserver_status()`](./kontroller.py#L16-L52) funktionen så använder 
`curl` kommando en `-o /dev/null` flagga. Den gör att textblocket som `curl` 
returnerar försvinner (på grund av att man skickar den till `/dev/null`). 
Man *behöver* inte använda den. Min första lösning tog hela `stdout` från 
kommando output, delade upp den till en `list[bytes]` genom att 
splittra den vid varje `\n` (newline) och ta sista elementet, som var HTTP-statuskoden.
Problemet med den lösningen var att man kunde inte lita på att det fanns en 
newline framför statuskoden.

```
$ curl -s -w "%{http_code}" https://wiki.archlinux.org/title/Main_page | tail -2
</body>
</html>200
```
I fallet övan skulle min lösning returnera `"</html>200"` vilket är fel.

Lösningen jag hittade var `-o /dev/null`. Där så skickar curl allt den fick från 
webbplatsen till `/dev/null`. Så det enda man får när man kör kommandot är statuskoden.
```
$ curl -s -o /dev/null -w "%{http_code}" https://wiki.archlinux.org/title/Main_page
200
```

Dock, när jag kollade på dokumentationen, under `--output` så såg jag att 
det finns en option till, `--out-null`, som gör samma sak, men bättre, 
för att den fungerar på system som inte håller sig till POSIX (windows). 
Främsta anledningen dock var att den såg bättre ut. 

Jag bytte till den och den fungerade. Men när jag läste vidare på manpage så 
har jag sett att den är ny sedan versionen `8.16.0`. Min version är `8.23.0` 
men jag har ett operativsystem som kör nyaste versionen av alla paket. Vilket 
är annorlunda från de flesta. På [repology.org](https://repology.org/project/curl/versions) 
går det att se vilken version av `curl` olika distros har. Om man har `Ubuntu < 26` eller 
`Fedora < 44` så känner curl inte igen flaggan `--out-null`, eftersom operativsystemet har en 
gammal version av curl. Så jag bytte tillbaka till `-o /dev/null` så jag är 
säker att du kan köra programmet :). Nackdelen är att `-o /dev/null` inte är 
portabel till Windows (där enheten heter `nul`), men jag prioriterar att 
kommandot fungerar på äldre versioner av `curl`.

## Hoppa över Boilerplate
I [`menu_loop()`](./meny.py#L266-L289) så använder jag en lista av listor, 
[`option_function`](./meny.py#L238-L247). Listorna innehåller två element: 
En sträng som anger namn till funktionen som kommer att visas i menyn och 
en funktion som ska köras när användaren väljer. Jag gör det så att jag 
inte behöver tänka på siffror i menyn. Alternativet är en `match` med 
9 cases (8 + `_`). En `match` fungerar, tills man vill ändra ordningen på 
något eller lägga till en ny funktion i mitten. Man borde inte göra 
datorns jobb. Datorn är bra på att repetera och människor är bra på att tänka.

`match` finns av en anledning. Om man endast har fyra options, till exempel, 
och man vet att antalet inte kommer att ändras så är det bäst att ha en `match case`. 
Det finns ingen "rätt" eller "fel", men kod kan vara fin eller ful.
