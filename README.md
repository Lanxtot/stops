# Aprašymas

**STOPS** – Python programa, iš oficialių Vilniaus visuomeninio transporto GTFS duomenų pateikianti išvykimo laikus tiksliau nei visur kitur (stops.lt front-end'as, Trafi, Google Maps). Stotelės pasirenkamos aiškiu ir patogiu būdu. Išvykimo laikai prognozuojami stops.lt sistemos, tačiau pateikiami tiksliu HH:MM:SS formatu. Taip pat pateikiama atvykstančios transporto priemonės garažinis numeris, grafiko numeris ir nuokrypis nuo tvarkaraščio. Prieinamos ir kitos naudingos funkcijos, pvz. maršrutu kursuojančių transporto priemonių suvestinė.

Toliau rasite įdiegimo instrukcijas. Jei susidursite su klaidomis įdiegę, turėsite patobulinimo pasiūlymu arba norėsite pagalbos su diegimu ar naudojimusi, parašykite pranešimą problemų skiltyje.

# Įdiegimo instrukcijos

Atsisiuntę šią programą galėsite pasirinkti savo operacinę sistemą ir gauti geriausiai pritaikytus bei tiksliausius duomenis.

## Windows

1. Įsidiekite Python 3.12 ar naujesnę versiją: <https://www.python.org/downloads/>
2. Atsidarę Windows terminalą įveskite: pip install requests
3. Atsisiųskite programos šaltinio kodą
4. Paleiskite `main.py` failą

## Android
 
1. Atsisiųskite F-Droid (ignoruokite klaidinančius perspėjimus apie galimą žalą): <https://f-droid.org/>
2. Suteikite leidimą F-Droid įdiegti nežinomas programas
3. Atsisiųskite Termux ir Termux:Widget iš F-Droid parduotuvės
4. Andoid nustatymuose suteikite leidimą programą Termux rodyti ant viršaus
5. Termux aplinkoje įveskite: `termux-setup-storage`
6. Termux aplinkoje įveskite: `termux-change-repo`
* Pasirinkite `single mirror`
* Pasirinkite `default`
7. Termux aplinkoje įveskite (pastaba: sutikite su viskuo):
* `pkg update`
* `pkg install python`
* `pip install requests`
* `pkg install git bash`
* `git clone https://github.com/Lanxtot/stops`
* `mkdir -p /data/data/com.termux/files/home/.shortcuts`
* `chmod 700 -R /data/data/com.termux/files/home/.shortcuts`
* `nano ~/.shortcuts/Stops`
8. Atidarę failą su nurodyta komanda įveskite, užbaigę įvestį išeikite su CTRL+X ir sutikite su viskuo:
* `#!/bin/bash`
* `cd ~/stops`
* `python3 main.py`
10. Sukurkite Termux:Widget 1x1 valdiklį pasirinkdami `Stops`
11. Paleiskite `Stops`

## iOS

Galima naudotis įsidiegus Linux emuliatorių (pvz. Alpine). Tereikia atsiųsti failus su Git, atverti atsiųstą aplanką ir paleisti failą `main.py` su Python.

# Atnaujinimo instrukcijos

## Windows

Paprasčiausiai iš naujo atsiųskite kodą. Galite nukopijuoti ir vietoje tuščių įklijuoti savo senuosius `challenge.csv`, `bugs.txt` failus norėdami išsaugoti sekamas transporto priemones ir atsiliepimus.

PASTABA: nekopijuokite duomenų, jei naujinatės į versiją v2.1 ar naujesnę iš ankstesnės, nei v2.1. Duomenų saugojimo formatas pasikeitė ir senasis nebepalaikomas, todėl prašome įvesti duomenis iš naujo.

## Android ir iOS

Norėdami atnaujinti kodą, atsidarę aplanką su Git (`cd stops`) atlikite šiuos žingsnius:

1. Įveskite `git restore .`

   PASTABA: Žingsnis nebūtinas. Taip ištrinsite išsaugotus duomenis (atsiliepimus, sekamas TP), tačiau užtikrinsite mažesnę nesklandumų riziką, nors ir turėsite iš naujo įvesti duomenis.

2. Įveskite `git pull origin`

# Naudojimo instrukcijos

Ši programa turi kelis skirtingus režimus, kuriais pasiekiami įvairūs duomenys apie Vilniaus miesto visuomeninį transportą. Kitų savivaldybių transporto duomenys yra nepalaikomi, išskyrus vėliau aprašytus atvejus sekimo režime.

Tik atsisiuntę programą turėsite pasirinkti savo operacinę sistemą. Vėliau, įvesties laukelyje, galėsite pasirinkti funkciją/režimą.

Bet kurioje funkcijoje, norėdami išeti iš pasirinkimo, galite įvesti tuščią eilutę.

## Stotelių paieška

Bazinė programos funkcija. Norėdami pasiekti, neturite nieko papildomai įvesti.

* Įvedamas stotelės pavadinimas. Neatsižvelgiama į mažąsias/didžiasias, lietuviškas/nelietuviškas raides. Galima įvesti pavadinimo fragmentą, tuo atveju gali reikėti patikslinti, kuri stotelė turima omenyje. Jei surastų tinkamų variantų bus žymiai per daug, bus prašoma įvesti iš naujo.
* Pasirenkama stotelės kryptis. Stotelėse, kurios turi tik vieną kryptį, šis žingsnis praleidžiamas. Kitu atveju, tenka pasirinkti norimą stotelės kryptį iš pateiktų apibūdinimu. Jeigu apibūdinimai pateikiami netiksliai arba neaiškiai, galite pranešti apie netikslumą įvesdami krypties numerį su `/` (pvz. `1/`).
* Pavaizduojami išvykimo laikai. Nurodomas prognozuojamas laikas sekundžių tikslumu; tuometinis transporto priemonės nuokrypis nuo grafiko; maršruto numeris; maršruto grafiko numeris ir tipas; reiso kryptis; transporto priemonės talpa, garažinis numeris ir modelis.
* Įvedę tuščią eilutę galite atnaujinti išvykimo laikus neieškodami stotelės. Taip pat galite įvesti bet kurią kitą funkciją.

### Paieška pagal kodą

Norėdami surasti stotelę pagal jos stops.lt kodą, įveskite `=`. Tada įvedus norimą kodą bus pateikiami išvykimo laikai.

### Paieška pagal trumpinį

Jeigu nusistatėte stotelės trumpinį, galite jį pasiekti paprasčiausiai įvesdami trumpinio skaitmenį (`1`–`9`). Tada bus iškart pateikiami išvykimo laikai.

## Maršruto paieška

Norėdami pasiekti, įveskite `?`. Norėdami išeiti, įveskite tuščią eilutę.

* Įvedamas maršruto numeris. Troleibusų maršrutai įvedami priekyje prirašius `T`.
* Pateikiama informacija. Nurodomas grafiko numeris ir tipas; transporto priemonės talpa, garažinis numeris, modelis; tuo metu užregistruoto reiso kryptis ir išvykimo laikas iš pradinės stotelės. Jei transporto priemonė tuo metu neturi jokio užregistruoto reiso, dalis informacijos nepateikiama.

## Transporto priemonės paieška

Norėdami pasiekti, įveskite `!`. Norėdami išeiti, įveskite tuščią eilutę.

* Įvedamas transporto priemonės garažinis numeris (tik skaičiai).
* Pateikiama informacija. Nurodomas transproto priemonės modelis, talpa; maršruto numeris; grafiko numeris ir tipas; tuo metu užregistruoto reiso kryptis ir išvykimo laikas iš pradinės stotelės. Jei transporto priemonė tuo metu neturi jokio užregistruoto reiso, dalis informacijos nepateikiama.

## Kelionių sekimas

Norėdami pasiekti, įveskite `-`. Norėdami išeiti, įveskite tuščią eilutę.

Ši funkcija turi keletą tolesnių pasirinkimų, leidžiančių detaliai sekti savo keliones visuomeniniu transportu bei pasinaudotas transporto priemones.

### Kelionės pridėjimas

* Įvedamas norimos užregistruoti transporto priemonės garažinis numeris (šių įmonių: VVT, Transrevis, Kautra, VRAP) arba valstybinis numeris (tinka bet kuris, tačiau transporto priemonės modelis ir talpa nustatomi tik įvedant šių įmonių: VRAP, Šalčininkų AP). 
* Įvedamas pasinaudoto maršruto numeris ir kryptis.

### Modelio arba talpos pridėjimas

* Įvedamas simbolis `+`.
* Įvedamas talpos trumpinys arba transporto priemonės modelio pavadinimas.
* Jei talpa aktuali tiek troleibusams, tiek autobusams, prašoma papildomai patikslinti, kuri transporto rūšis turima omenyje.

### Kelionės ištrynimas

* Įvedamas simbolis `-`.
* Įvedamas norimos trinti užregistruotos kelionės numeris (rodomas kelionių peržiūros režime).

### Kelionių peržiūra

* Įvedamas simbolis `.`.
* Pateikiami užregistruotų kelionių maršrutai ir kryptys; transporto priemonių garažiniai/valstybiniai numeriai, talpos, modeliai.

### Transporto priemonių peržiūra

* Įvedamas simbolis `,`.
* Pateikiamas surūšiuotas pasinaudotų transporto priemonių garažinių/valstybinių numerių, talpų, modelių sąrašas, įskaitant atskirai pridėtus modelius ir talpas. Jei transporto priemonė panaudota kelis kartus, vaizduojamas šauktukas.

## Trumpinių nustatymas

Norėdami pasiekti, įveskite `*`. Norėdami išeiti, įveskite tuščią eilutę.

* Pasirenkamas skaitmuo, kuriam norima priskirti trumpinio funkciją.
* Įvedama norima stotelė ir pasirenkama kryptis (analogiškai stotelių paieškos funkcijai).
* Įvedamas trumpinių sąraše vaizduotinas pavadinimas.

## Atsiliepimų peržiūra

Norėdami pasiekti, įveskite `/`.

Vaizduojami užfiksuoti netikslias kryptis turinčių stotelių kodai. Šia informacija galima pasinaudoti kuriant pranešimą apie klaidą GitHub sistemoje.

## Duomenų atnaujinimas

Norėdami atnaujinti duomenis, įveskite `+`.

## Instrukcijos

Norėdami pamatyti instrukcija programoje, įveskite skaitmenį `0`.

# Legenda

Programoje naudojami įvairūs sutartiniai ženklai.

## Talpa/dydis

* `mk`: mikroautobusai
* `m`: mažos talpos
* `t`: standartinės talpos
* `ti`: pailginti viengubi
* `i`: dvigubi

## Maršruto numeris

* `T`: troleibusų maršrutas
* `*`: reisas alternatyvia trasa

## Grafikas

* `2p`: dviejų pamainų
* `1p`: vienos pamainos
* `pt`: pertraukiamas
* `/`: papildoma informacija – maršrutas, su kuriuo sujungtas grafikas; grafiką aptarnaujantis parkas
