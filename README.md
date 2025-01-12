Python programa, iš oficialių Vilniaus visuomeninio transporto GTFS duomenų pateikianti išvykimo laikus tiksliau nei visur kitur (stops.lt front-end'as, Trafi, Google Maps). Stotelės pasirenkamos aiškiu ir patogiu būdu. Išvykimo laikai prognozuojami stops.lt sistemos, tačiau pateikiami tiksliu HH:MM:SS formatu. Taip pat pateikiama atvykstančios transporto priemonės talpa, nuokrypis nuo tvarkaraščio bei transporto priemonių garažiniai ir reisų grafikų numeriai.

# Įdiegimo instrukcijos

## Windows

1. Įsidiekite Python 3.12 ar naujesnę versiją: <https://www.python.org/downloads/>
2. Atsidarę Windows terminalą įveskite:
2.1. pip install python
2.2. pip install requests
3. Atsisiųskite programos šaltinio kodą
4. Paleiskite main.py failą
Norėdami atnaujinti, iš naujo parsisiųskite kodą

## Android

1. Atsisiųskite F-Droid (ignoruokite klaidinančius perspėjimus apie galimą žalą): <https://f-droid.org/>
2. Suteikite leidimą F-Droid įdiegti nežinomas programas
3. Atsisiųskite Termux ir Termux:Widget iš F-Droid parduotuvės
4. Andoid nustatymuose suteikite leidimą programą Termux rodyti ant viršaus
5. Termux aplinkoje įveskite: termux-setup-storage
6. Termux aplinkoje įveskite: termux-change-repo
6.1. Pasirinkite 'single mirror'
6.2. Pasirinkite 'default'
7. Termux aplinkoje įveskite (pastaba: sutikite su viskuo):
7.1. pkg update
7.2. pkg install python
7.3. pip install requests
7.4. pkg install git bash
7.5. git clone -b challenge https://github.com/Lanxtot/stops
7.6. mkdir -p /data/data/com.termux/files/home/.shortcuts
7.7. chmod 700 -R /data/data/com.termux/files/home/.shortcuts
7.8. mkdir -p /data/data/com.termux/files/home/.shortcuts/tasks
7.9. chmod 700 -R /data/data/com.termux/files/home/.shortcuts/tasks
7.10. nano ~/.shortcuts/Stops.sh
8. Atidarę failą su nurodyta komanda ir įveskite, užbaigę įvestį išeikite su CTRL+X ir sutikite su viskuo: 
8.1. #!/bin/bash
8.2. cd ~/repo
8.3. git pull
8.4. ./stops.sh
9. Įveskite aplinkoje:
9.1. chmod +x ~/.shortcuts/Stops.sh
10. Sukurkite Termux:Widget 1x1 valdiklį pasirinkdami Stops.sh
11. Paleiskite Stops.sh
Norėdami atnaujinti, vėl atlikite 7.5. žingsnį

## iOS

1. Eikite į artimiausią elektronikos parduotuvę
2. Nusipirkite išmanujį įrenginį su Android operacine sistema
3. Toliau sekite instrukcijas skiltyje Android
