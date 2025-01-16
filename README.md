Python programa, iš oficialių Vilniaus visuomeninio transporto GTFS duomenų pateikianti išvykimo laikus tiksliau nei visur kitur (stops.lt front-end'as, Trafi, Google Maps). Stotelės pasirenkamos aiškiu ir patogiu būdu. Išvykimo laikai prognozuojami stops.lt sistemos, tačiau pateikiami tiksliu HH:MM:SS formatu. Taip pat pateikiama atvykstančios transporto priemonės garažinis numeris, grafiko numeris ir nuokrypis nuo tvarkaraščio. Prieinamos ir kitos naudingos funkcijos, pvz. maršrutu kursuojančių transporto priemonių suvestinė.

# Įdiegimo instrukcijos

## Windows

1. Įsidiekite Python 3.12 ar naujesnę versiją: <https://www.python.org/downloads/>
2. Atsidarę Windows terminalą įveskite: pip install requests
3. Atsisiųskite programos šaltinio kodą
4. Paleiskite main.py failą

Norėdami atnaujinti, iš naujo parsisiųskite kodą.

## Android
 
1. Atsisiųskite F-Droid (ignoruokite klaidinančius perspėjimus apie galimą žalą): <https://f-droid.org/>
2. Suteikite leidimą F-Droid įdiegti nežinomas programas
3. Atsisiųskite Termux ir Termux:Widget iš F-Droid parduotuvės
4. Andoid nustatymuose suteikite leidimą programą Termux rodyti ant viršaus
5. Termux aplinkoje įveskite: termux-setup-storage
6. Termux aplinkoje įveskite: termux-change-repo
* Pasirinkite 'single mirror'
* Pasirinkite 'default'
7. Termux aplinkoje įveskite (pastaba: sutikite su viskuo):
* pkg update
* pkg install python
* pip install requests
* pkg install git bash
* git clone https://github.com/Lanxtot/stops
* mkdir -p /data/data/com.termux/files/home/.shortcuts
* chmod 700 -R /data/data/com.termux/files/home/.shortcuts
* nano ~/.shortcuts/Stops
8. Atidarę failą su nurodyta komanda įveskite, užbaigę įvestį išeikite su CTRL+X ir sutikite su viskuo:
* #!/bin/bash
* cd ~/stops
* python3 main.py
10. Sukurkite Termux:Widget 1x1 valdiklį pasirinkdami Stops
11. Paleiskite Stops

Norėdami atnaujinti, Termux bazinėje aplinkoje įveskite:
* cd stops
* git pull .

## iOS

Galima naudotis įsidiegus Linux emuliatorių. Tereikia atsiųsti failus su Git, atverti atsiųstą aplanką ir paleisti failą „main.py“ su Python.

Norėdami atnaujinti, naudokitės Git „pull .“ funkcija.

## Pastabos

Atsisiuntę šią programą galėsite pasirinkti savo operacinę sistemą ir gauti geriausiai pritaikytus bei tiksliausius duomenis.
