<p>Python programa, iš oficialių Vilniaus visuomeninio transporto GTFS duomenų pateikianti išvykimo laikus tiksliau nei visur kitur (stops.lt front-end&#39;as, Trafi, Google Maps). Stotelės pasirenkamos aiškiu ir patogiu būdu. Išvykimo laikai prognozuojami stops.lt sistemos, tačiau pateikiami tiksliu HH:MM:SS formatu. Taip pat pateikiama atvykstančios transporto priemonės talpa, nuokrypis nuo tvarkaraščio bei transporto priemonių garažiniai ir reisų grafikų numeriai.</p>
<h1 id="įdiegimo-instrukcijos">Įdiegimo instrukcijos</h1>
<h2 id="windows">Windows</h2>
<p>1. Įsidiekite Python 3.12 ar naujesnę versiją: <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a></p>
<p>2. Atsidarę Windows terminalą įveskite:</p>
<p>2.1. pip install python</p>
<p>2.2. pip install requests</p>
<p>3. Atsisiųskite programos šaltinio kodą</p>
<p>4. Paleiskite main.py failą</p>
<p>Norėdami atnaujinti, iš naujo parsisiųskite kodą</p>
<h2 id="android">Android</h2>
<p>1. Atsisiųskite F-Droid (ignoruokite klaidinančius perspėjimus apie galimą žalą): <a href="https://f-droid.org/">https://f-droid.org/</a></p>
<p>2. Suteikite leidimą F-Droid įdiegti nežinomas programas</p>
<p>3. Atsisiųskite Termux ir Termux:Widget iš F-Droid parduotuvės</p>
<p>4. Andoid nustatymuose suteikite leidimą programą Termux rodyti ant viršaus</p>
<p>5. Termux aplinkoje įveskite: termux-setup-storage</p>
<p>6. Termux aplinkoje įveskite: termux-change-repo</p>
<p>6.1. Pasirinkite &#39;single mirror&#39;</p>
<p>6.2. Pasirinkite &#39;default&#39;</p>
<p>7. Termux aplinkoje įveskite (pastaba: sutikite su viskuo):</p>
<p>7.1. pkg update</p>
<p>7.2. pkg install python</p>
<p>7.3. pip install requests</p>
<p>7.4. pkg install git bash</p>
<p>7.5. git clone -b challenge <a href="https://github.com/Lanxtot/stops">https://github.com/Lanxtot/stops</a></p>
<p>7.6. mkdir -p /data/data/com.termux/files/home/.shortcuts</p>
<p>7.7. chmod 700 -R /data/data/com.termux/files/home/.shortcuts</p>
<p>7.8. nano ~/.shortcuts/Stops.sh</p>
<p>8. Atidarę failą su nurodyta komanda ir įveskite, užbaigę įvestį išeikite su CTRL+X ir sutikite su viskuo:</p>
<p>8.1. #!/bin/bash</p>
<p>8.2. cd ~/stops</p>
<p>8.3. python3 main.py</p>
<p>9. Įveskite aplinkoje:</p>
<p>9.1. chmod +x ~/.shortcuts/Stops.sh</p>
<p>10. Sukurkite Termux:Widget 1x1 valdiklį pasirinkdami Stops.sh</p>
<p>11. Paleiskite Stops.sh</p>
<p>Norėdami atnaujinti, vėl atlikite 7.5. žingsnį</p>
<h2 id="ios">iOS</h2>
<p>1. Eikite į artimiausią elektronikos parduotuvę</p>
<p>2. Nusipirkite išmanujį įrenginį su Android operacine sistema</p>
<p>3. Toliau sekite instrukcijas skiltyje Android</p>
