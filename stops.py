# stops v1.0

import requests
import re
import datetime
import pytz
import time
from bs4 import BeautifulSoup

st=str(input())

while True:

    dict={

        # Stotelės įvedimui, kodai iš GTFS stops.lt duomenų

        # Jei stotelė dvipusė, įvedama:
        #   A-B
        
        # Jei stotelė vienpusė, pakanka įvesti
        #   A

        # Visur išmetamas trumpinys
        #   st.

        # Rašoma pilnais žodžiais, išskyrus vardus, kurių rašoma tik pirma raidė su tašku:
        #   V. Pavardės

        # Trumpintai rašomi ir titulai:
        #   Šv.
        #   Pal.

        # Sąraše pateikiamos ir nenaudojamos stotelės (kadangi stotelė gali būti vėl panaudota ateityje)
        # Jas ir kitas specialias stoteles įvesti naudojami terminai
        #   išlaipinimas
        #   įlaipinimas
        #   laikina
        #   panaikinta
        # Ir kiti, žiūrėti sąrašą

        # Pateikiamos stotelių pavadinimų alternatyvios versijos ir asmeniniai trumpiniai, žiūrėti sąrašą

        # Naujausių ar laikinų stotelių gali trūkti

        'Autobusų parko vartai išlaipinimas': 18,
        'Autobusų parko vartai-Autobusų parkas': 31,
        'Autobusų parko vartai': 32,
        'Žaliasis tiltas-Kalvarijų turgus': 101, 
        'Žaliasis tiltas-Europos aikštė': 101, 
        'Žaliasis tiltas-Lvivo': 101, 
        'Žaliasis tiltas-Lvovo': 101, 
        'ŽTN': 101, 
        'Žaliasis tiltas-Karaliaus Mindaugo tiltas': 102,
        'Žaliasis tiltas-V. Kudirkos aikštė': 102,
        'Žaliasis tiltas-Operos ir baleto teatras': 102,
        'Žaliasis tiltas-J. Tumo-Vaižganto': 102,
        'ŽTS': 102, 
        'Europos aikštė-Kalvarijų turgus': 103, 
        'Europos aikštė-Lvivo': 103, 
        'Europos aikštė-Lvovo': 103, 
        'Europos aikštė-Žaliasis tiltas': 103, 
        'EAE': 103, 
        'Europos aikštė-Nacionalinė dailės galerija': 104, 
        'Europos aikštė-Lietuvos sąjūdžio kelias': 104, 
        'Europos aikštė-Sąjūdžio kelias': 104, 
        'EAW': 104, 
        'Lietuvos sąjūdžio kelias-Nacionalinė dailės galerija': 105, 
        'Lietuvos sąjūdžio kelias-Europos aikštė': 105, 
        'Lietuvos sąjūdžio kelias-Šeškinė': 106, 
        'Lietuvos sąjūdžio kelias-Studentų': 106, 
        'Lietuvos sąjūdžio kelias-Švietimo akademija': 106, 
        'Sąjūdžio kelias-Nacionalinė dailės galerija': 105, 
        'Sąjūdžio kelias-Europos aikštė': 105, 
        'Sąjūdžio kelias-Šeškinė': 106, 
        'Sąjūdžio kelias-Studentų': 106, 
        'Sąjūdžio kelias-Švietimo akademija': 106, 
        'Saltoniškės-Linkmenų': 107, 
        'Saltoniškės-Licėjus': 107, 
        'Studentų-Šeškinė': 108, 
        'Studentų-Lietuvos sąjūdžio kelias': 108, 
        'Studentų-Sąjūdžio kelias': 108, 
        'Studentų-Švietimo akademija': 108,
        'Studentų-Saltoniškės': 108,
        'Lvivo-Rinktinės': 109,
        'Lvivo-Šeimyniškių': 109,
        'Lvivo-Tuskulėnų rimties parkas': 109,
        'Lvivo-Žvejų': 109,
        'Lvivo-Europos aikštė': 110,
        'Lvivo-Žaliasis tiltas': 110,
        'Lvivo-Kalvarijų turgus': 110,
        'Lvovo-Rinktinės': 109,
        'Lvovo-Šeimyniškių': 109,
        'Lvovo-Tuskulėnų rimties parkas': 109,
        'Lvovo-Žvejų': 109,
        'Lvovo-Europos aikštė': 110,
        'Lvovo-Žaliasis tiltas': 110,
        'Lvovo-Kalvarijų turgus': 110,
        'Rinktinės-Šeimyniškių': 111,
        'Šeimyniškių-Vasaros': 112,
        'Šeimyniškių-Tuskulėnų rimties parkas': 112,
        'Šeimyniškių-Šv. Petro ir Povilo bažnyčia': 112,
        'Šeimyniškių-Petro ir Povilo bažnyčia': 112,
        'Nacionalinė dailės galerija-Europos aikštė': 113,
        'Nacionalinė dailės galerija-Lietuvos sąjūdžio kelias': 114,
        'Nacionalinė dailės galerija-Sąjūdžio kelias': 114,
        'Šnipiškės-Linkmenų': 115,
        'Karaliaus Mindaugo tiltas-Žaliasis tiltas': 201,
        'KMTW': 201,
        'Karaliaus Mindaugo tiltas-Operos ir baleto teatras': 201,
        'Karaliaus Mindaugo tiltas-V. Kudirkos aikštė': 201,
        'Karaliaus Mindaugo tiltas-Arkikatedra': 202,
        'Arkikatedra-Bernardinų sodas': 203,
        'Jogailos-V. Kudirkos aikštė': 207,
        'Jogailos': 207,
        'V. Kudirkos aikštė-Žaliasis tiltas': 210,
        'V. Kudirkos aikštė-Karaliaus Mindaugo tiltas': 210,
        'VKAN': 210,
        'V. Kudirkos aikštė-Centro poliklinika': 211,
        'V. Kudirkos aikštė-Islandijos': 211,
        'VKAS': 210,
        'Islandijos-Pamėnkalnio': 212,
        'Islandijos': 212,
        'J. Tumo-Vaižganto-M. K. Čiurlionio': 214,
        'J. Tumo-Vaižganto-Pamėnkalnio': 214,
        'Pamėnkalnio-Centro poliklinika': 215,
        'Pamėnkalnio-Jogailos': 215,
        'Pamėnkalnio-Islandijos': 215,
        'Pamėnkalnio-J. Jasinskio': 216,
        'J. Jasinskio-Liubarto tiltas': 217,
        'J. Jasinskio-Vytauto': 217,
        'J. Jasinskio-Pamėnkalnio': 218,
        'Gedimino prospektas-Studentų': 219,
        'Gedimino prospektas-Saltoniškės': 219,
        'Gedimino prospektas-V. Pietario': 220,
        'Gedimino prospektas-Žemaitės': 220,
        'Gedimino prospektas-Vingis': 220,
        'Gedimino prospektas-Jaunas kaip Vilnius': 220,
        'A. Goštauto-Operos ir baleto teatras': 221,
        'A. Goštauto-Kražių': 221,
        'A. Goštauto-Nepriklausomybės aikštė': 222,
        'Vašingtono aikštė-Gynėjų': 223,
        'Vašingtono aikštė': 223,
        'Kražių-J. Tumo-Vaižganto': 224,
        'Kražių-Operos ir baleto aikštė': 225,
        'Kražių-Lukiškės': 225,
        'J. Tumo-Vaižganto-Kražių': 226,
        'J. Tumo-Vaižganto-Vašingtono aikštė': 226,
        'J. Tumo-Vaižganto-Žaliasis tiltas': 226,
        'Gynėjų-Studentų': 227,
        'Gynėjų-Saltoniškės': 227,
        'Gynėjų': 227,
        'Lukiškės-Kražių': 231,
        'Lukiškės-J. Tumo-Vaižganto': 231,
        'Lukiškės-Vašingtono aikštė': 231,
        'Lukiškės': 231,
        'Operos ir baleto teatras-Kražių': 232,
        'Operos ir baleto teatras-Lukiškės': 232,
        'Operos ir baleto teatras-A. Goštauto': 232,
        'Operos ir baleto teatras-Karaliaus Mindaugo tiltas': 233,
        'Operos ir baleto teatras-Žaliasis tiltas': 233,
        'Operos ir baleto teatras-V. Kudirkos aikštė': 233,
        'Centro poliklinika-MO muziejus': 235,
        'Centro poliklinika-Reformatų': 235,
        'Centro poliklinika': 235,
        'Lukiškės išlaipinimas': 236,
        'A. Tumėno-Studentų': 237,
        'A. Tumėno': 237,
        'Nepriklausomybės aikštė-Verslo trikampis': 238,
        'Nepriklausomybės aikštė-A. Goštauto': 239,
        'Arkikatedra turistiniai': 242,
        'Arkikatedra-V. Kudirkos aikštė': 243,
        'Vokiečių-Reformatų': 244,
        'Vokiečių panaikinta': 245,
        'Rotušė-Vokiečių': 246,
        'Rotušė-Bazilijonų': 247,
        'Rotušė-Gėlių': 247,
        'Verslo trikampis-Nepriklausomybės aikštė': 253,
        'Verslo trikampis-Žemaitės': 254,
        'Verslo trikampis-Jaunas kaip Vilnius': 254,
        'Liubarto tiltas-J. Jasinskio': 301,
        'Liubarto tiltas-Kęstučio': 302,
        'Kęstučio-Liubarto tiltas': 303,
        'Kęstučio-Latvių': 304,
        'Vytauto-D. Dudajevo skveras': 305,
        'Vytauto-Liubarto tiltas': 306,
        'Latvių-Kęstučio': 307,
        'Latvių-Sėlių': 308,
        'D. Dudajevo skveras-Sėlių': 309,
        'D. Dudajevo skveras-Vytauto': 310,
        'Sėlių-Latvių': 311,
        'Sėlių-T. Narbuto': 312,
        'Sėlių-Žvėryno žiedas': 312,
        'Žvėrynas-Sėlių': 313,
        'Žvėrynas-Panorama': 314,
        'Žvėrynas-T. Narbuto': 315,
        'Panorama-Švietimo akademija': 316,
        'Panorama-Žvėrynas': 317,
        'Švietimo akademija-Lietuvos sąjūdžio kelias': 318,
        'Švietimo akademija-Sąjūdžio kelias': 318,
        'Švietimo akademija-Šnipiškės': 318,
        'Švietimo akademija-Studentų': 318,
        'Švietimo akademija-Saltoniškės': 318,
        'Švietimo akademija-Panorama': 319,
        'Švietimo akademija-T. Narbuto': 319,
        'Studentų-A. Goštauto': 320,
        'Studentų-A. Tumėno': 320,
        'Studentų-Gedimino prospektas': 320,
        'Studentų-Nepriklausomybės aikštė': 320,
        'Saltoniškės-Švietimo akademija': 321,
        'Saltoniškės-Studentų': 321,
        'Saltoniškės-Gedimino prospektas': 321,
        'Saltoniškės-Lietuvos sąjūdžio kelias': 321,
        'Saltoniškės-Sąjūdžio kelias': 321,
        'Saltoniškės-Šnipiškės': 321,
        'Šv. Petro ir Povilo bažnyčia-Kalnų parkas': 401,
        'Šv. Petro ir Povilo bažnyčia-Karaliaus Mindaugo tiltas': 401,
        'Šv. Petro ir Povilo bažnyčia-Žvejų': 401,
        'PPBW': 401,
        'PPBS': 401,
        'Šv. Petro ir Povilo bažnyčia-L. Sapiegos': 402,
        'Šv. Petro ir Povilo bažnyčia-Tuskulėnų rimties parkas': 402,
        'Šv. Petro ir Povilo bažnyčia-Tuskulėnai': 402,
        'Šv. Petro ir Povilo bažnyčia-Šeimyniškių': 402,
        'Šv. Petro ir Povilo bažnyčia-Vasaros': 402,
        'Petro ir Povilo bažnyčia-Kalnų parkas': 401,
        'Petro ir Povilo bažnyčia-Karaliaus Mindaugo tiltas': 401,
        'Petro ir Povilo bažnyčia-Žvejų': 401,
        'Petro ir Povilo bažnyčia-L. Sapiegos': 402,
        'Petro ir Povilo bažnyčia-Tuskulėnų rimties parkas': 402,
        'Petro ir Povilo bažnyčia-Tuskulėnai': 402,
        'Petro ir Povilo bažnyčia-Šeimyniškių': 402,
        'Petro ir Povilo bažnyčia-Vasaros': 402,
        'PPBE': 402,
        'PPBN': 402,
        'Kalnų parkas panaikinta': 403,
        'Kalnų parkas-Žvejų': 403,
        'Kalnų parkas-Šv. Petro ir Povilo bažnyčia': 404,
        'Kalnų parkas-Petro ir Povilo bažnyčia': 404,
        'Arkikatedra-Žvejų': 405,
        'Arkikatedra-Karaliaus Mindaugo tiltas': 405,
        'Reformatų-Jogailos': 406,
        'Reformatų-Islandijos': 406,
        'Reformatų-Algirdo': 407,
        'Trakų-Reformatų': 408,
        'Trakų': 408,
        'MO muziejus-Vingriai': 409,
        'MO muziejus-Stotis': 409,
        'MO muziejus-Reformatų': 410,
        'MO muziejus-V. Kudirkos aikštė': 410,
        'MO muziejus-Vokiečių': 410,
        'Vingriai-Gėlių': 411,
        'Vingriai': 411,
        'Gėlių-Stotis': 412,
        'Gėlių-Aguonų': 412,
        'Gėlių': 412,
        'Rūdninkų-MO muziejus': 413,
        'Rūdninkų': 413,
        'R': 413,
        'Aguonų-Vienaragių': 414,
        'Aguonų-Stotis': 415,
        'Aušros vartai-Stotis': 416,
        'AVS': 416,
        'Aušros vartai-Liepkalnis': 416,
        'Aušros vartai-Pelesos': 416,
        'Aušros vartai-Misionierių': 417,
        'Aušros vartai-Gervėčių': 417,
        'AV': 417,
        'Gervėčių-Ramybės': 418,
        'GR': 418,
        'Gervėčių-Aušros vartai 31': 419,
        'GAV': 419,
        'Misionierių-Subačiaus': 420,
        'Misionierių-Užupio': 420,
        'Misionierių-Aušros vartai': 421,
        'Subačiaus-Zarasų': 422,
        'Subačiaus-Balstogės': 422,
        'Subačiaus-Gervėčių': 422,
        'Subačiaus-Misionierių': 423,
        'Subačiaus-Užupio': 423,
        'Drujos-Subačiaus': 424,
        'Drujos-Gervėčių': 424,
        'Drujos-Zarasų': 424,
        'Drujos-Balstogės': 424,
        'Paupio turgus-Riedulių': 425,
        'Užupio-Dailės akademija': 426,
        'UDA': 426,
        'Užupio-Subačiaus': 427,
        'Užupio-Misionierių': 427,
        'U': 427,
        'Vilnios-Užupis': 428,
        'Vilnios-Varpų': 428,
        'Vilnios': 428,
        'Dailės akademija-Bernardinų sodas': 429,
        'Dailės akademija-Užupio': 430,
        'Dailės akademija-Vilnios': 430,
        'Bernardinų sodas-Dailės akademija': 431,
        'Bernardinų sodas-Arkikatedra': 432,
        'Užupis-Bernardinų kapinės': 433,
        'Užupis': 433,
        'Bernardinų kapinės-Bernardinų': 434,
        'Bernardinų kapinės': 434,
        'Bernardinų-Drujos': 435,
        'Bernardinų': 435,
        'Polocko-Drujos': 436,
        'Polocko-Srovės': 436,
        'Polocko-Rudens': 436,
        'Polocko-Gervėčių': 436,
        'Filaretų-Polocko': 437,
        'Krivių-Filaretų': 438,
        'Vasaros-Krivių': 439,
        'Vasaros-Filaretų': 439,
        'Aušros vartai-Bazilijonų': 440,
        'Aušros vartai-Rūdninkų': 440,
        'Aušros vartai-Gelių': 440,
        'Aušros vartai-MO muziejus': 440,
        'Karaliaus Mindaugo tiltas-Kalnų parkas': 441,
        'Karaliaus Mindaugo tiltas-Šv. Petro ir Povilo bažnyčia': 441,
        'Karaliaus Mindaugo tiltas-Petro ir Povilo bažnyčia': 441,
        'KMTE': 441,
        'Gervėčių-Drujos': 443,
        'Gervėčių-Zarasų': 443,
        'Gervėčių-Stotis': 444,
        'Gervėčių-Pelesos': 444,
        'Gervėčių-Aušros vartai 89': 444,
        'Ramybės-Rasų kapinės': 445,
        'Ramybės': 445,
        'Bazilijonų-Rotušė': 446,
        'Rotušė panaikinta': 449,
        'Algirdo-S. Konarskio': 501,
        'Algirdo-M. K. Čiurlionio': 501,
        'Algirdo-Trakų': 502,
        'M. K. Čiurlionio-J. Tumo-Vaižganto': 503,
        'M. K. Čiurlionio-Pamėnkalnio': 503,
        'M. K. Čiurlionio-T. Ševčenkos': 504,
        'M. K. Čiurlionio-S. Konarskio': 505,
        'S. Konarskio-M. K. Čiurlionio': 506,
        'S. Konarskio-Algirdo': 506,
        'S. Konarskio-Vingis': 507,
        'Vingis-S. Konarskio': 508,
        'Vingis-Savanorių prospektas': 509,
        'Vingis-V. Pietario': 509,
        'Vingis-Gedimino prospektas': 509,
        'T. Ševčenkos-M. K. Čiurlionio': 510,
        'T. Ševčenkos-Algirdo': 510,
        'T. Ševčenkos-S. Konarskio': 510,
        'T. Ševčenkos-Vienaragių': 511,
        'T. Ševčenkos-Švitrigailos': 511,
        'Švitrigailos-Vytenio': 512,
        'Švitrigailos': 512,
        'Vytenio-Švitrigailos': 513,
        'Vytenio-Skroblų': 514,
        'Statybininkų-Savanorių prospektas': 515,
        'Statybininkų-V. Pietario': 515,
        'Naugarduko-Vytenio': 516,
        'Naugarduko': 516,
        'Naujamiestis-Statybininkų': 517,
        'Naujamiestis-Savanorių prospektas': 517,
        'Naujamiestis-Skroblų': 517,
        'Naujamiestis-Vienaragių': 518,
        'Vienaragių-Naujamiestis': 519,
        'Vienaragių-Lelija': 519,
        'Vienaragių-T. Ševčenkos': 520,
        'Vienaragių-MO muziejus': 520,
        'Vienaragių-Aguonų': 521,
        'Vienaragių-Stotis': 521,
        'Lelija-Smolensko': 523,
        'Lelija-Amatų': 524,
        'Smolensko-Burbiškės': 525,
        'Smolensko-Lelija': 526,
        'Burbiškės-Skroblų': 527,
        'Burbiškės-Smolensko': 527,
        'Pelesos-Panevėžio': 528,
        'Panevėžio-Dzūkų': 529,
        'Panevėžio-Prūsų': 529,
        'Stotis priemiestiniai': 530,
        'Amatų': 531,
        'Amatų-Vienaragių': 531,
        'Skroblų-Burbiškės': 535,
        'Skroblų-Statybininkų': 536,
        'Skroblų-Naugarduko': 536,
        'Skroblų-Naujamiestis': 536,
        'Stotis X': 546,
        'Stotis S': 547,
        'Stotis atstova': 548,
        'Žemaitės-Statybininkų': 601,
        'Žemaitės': 601,
        'Savanorių prospektas-Gerosios Vilties': 603,
        'Gerosios Vilties-Eigulių': 606,
        'Gerosios Vilties-Vilkpėdės': 606,
        'Gerosios Vilties-Vingio parkas': 606,
        'Gerosios Vilties-Litexpo': 606,
        'Gerosios Vilties-LITEXPO': 606,
        'Gerosios Vilties-Lazdynai': 606,
        'Gerosios Vilties-Savanorių prospektas': 607,
        'Eigulių-Miškiniai': 608,
        'Eigulių-Šiltnamių': 608,
        'Vingio parkas-Giraitės': 609,
        'Vingio parkas-Vingis': 610,
        'Vingio parkas-Jaunas kaip Vilnius': 610,
        'Vingio parkas-Gedimino prospektas': 610,
        'V. Pietario-Vingio parkas': 611,
        'Statybininkų-Naujamiestis': 612,
        'Statybininkų-Skroblų': 612,
        'V. Pietario-Jaunas kaip Vilnius': 615,
        'V. Pietario-Verslo trikampis': 615,
        'Jaunas kaip Vilnius-Žemaitės': 616,
        'Jaunas kaip Vilnius-V. Pietario': 616,
        'Jaunas kaip Vilnius-Verslo trikampis': 617,
        'Jaunas kaip Vilnius-Gedimino prospektas': 617,
        'Linkmenų-Saltoniškės': 701,
        'Linkmenų-Oršos': 702,
        'Kalvarijų turgus-Žaliasis tiltas': 703,
        'Kalvarijų turgus-Europos aikštė': 703,
        'Kalvarijų turgus-B. Laurinavičiaus skveras': 704,
        'Kalvarijų turgus-Trimitų': 704,
        'Žalgirio-Kalvarijų turgus': 705,
        'Žalgirio-Linkmenų': 706,
        'Žalgirio-Kernavės': 706,
        'Giedraičių-Žalgirio': 707,
        'Giedraičių-Apkasų': 707,
        'Giedraičių-Trimitų': 707,
        'Tauragnų-Giedraičių': 708,
        'Pramogų arena-Žalgirio': 709,
        'Pramogų arena-Tauragnų autobusai': 709,
        'Licėjus-Pramogų arena': 710,
        'Žalgirio-Trimitų': 711,
        'Kernavės-Oršos': 712,
        'Kernavės-Krokuvos': 713,
        'Krokuvos-Kernavės': 715,
        'Oršos-Žalgirio': 716,
        'Oršos': 716,
        'Krokuvos-Nacionalinė dailės galerija': 717,
        'Šnipiškės-Krokuvos': 718,
        'J. Kazlausko-Naujakiemio': 801,
        'J. Kazlausko-Baltupiai': 801,
        'Pramogų arena-J. Kazlausko': 802,
        'Tauragnų-Pramogų arena': 803,
        'Pramogų arena-Kareivių': 804,
        'Pramogų arena-Verkių': 804,
        'Pramogų arena-Tauragnų troleibusai': 805,
        'Verkių-Kareivių': 806,
        'Verkių-Pramogų arena': 807,
        'Kareivių-Verkių': 808,
        'Kareivių-Pramogų arena': 808,
        'Kareivių-Žirmūnai': 810,
        'Kareivių-Žirmūnų seniūnija': 811,
        'Kareivių-Valakampių tiltas': 812,
        'Kareivių-Lizdeikos': 812,
        'Autobusų parkas-Žirmūnų seniūnija': 813,
        'Autobusų parkas-Šaltinėlio': 813,
        'Žirmūnų seniūnija-Kareivių': 814,
        'Žirmūnų seniūnija-Autobusų parkas': 815,
        'Žirmūnų seniūnija-Šaltinėlio': 815,
        'Šaltinėlio-Žirmūnų žiedas': 816,
        'Šaltinėlio-Žirmūnų seniūnija': 817,
        'Žirmūnų žiedas išlaipinimas': 818,
        'Žirmūnų žiedas': 818,
        'Valakampių tiltas-Kareivių': 819,
        'Valakampių tiltas-Žirmūnų seniūnija': 819,
        'Valakampių tiltas-Lizdeikos': 820,
        'Valakampių tiltas-Lakštingalų': 820,
        'Žirmūnai-Kareivių': 821,
        'Žirmūnai-Šiaurės miestelis': 822,
        'Verkių-Autobusų parkas': 823,
        'Ozo žiedas-Licėjus': 825,
        'Ozo žiedas': 825,
        'Ozo žiedas panaikinta': 826,
        'Ozo žiedas išlaipinimas': 827,
        'Žirmūnai panaikinta': 828,
        'Trinapolis': 830,
        'Autobusų parkas išlaipinimas': 831,
        'Šiaurės miestelis-Žirmūnai': 901,
        'Šiaurės miestelis-Minties': 902,
        'Šiaurės miestelis-Šilo tiltas': 902,
        'Minties-Šiaurės miestelis': 903,
        'Minties-Šilo tiltas kiti': 903,
        'Minties-Tuskulėnų rimties parkas': 904,
        'Tuskulėnų rimties parkas-Minties': 905,
        'Tuskulėnų rimties parkas-Šeimyniškių': 906,
        'Tuskulėnų rimties parkas-Lvivo': 906,
        'Tuskulėnų rimties parkas-Lvovo': 906,
        'Tuskulėnų rimties parkas-Šv. Petro ir Povilo bažnyčia': 906,
        'Tuskulėnų rimties parkas-Petro ir Povilo bažnyčia': 906,
        'Tuskulėnų rimties parkas-Vasaros': 906,
        'Tuskulėnų rimties parkas-Tuskulėnai': 906,
        'Rinktinės-Lvivo': 907,
        'Rinktinės-Lvovo': 907,
        'Šeimyniškių-Rinktinės': 908,
        'Tuskulėnai-Vasaros': 909,
        'Tuskulėnai-Šv. Petro ir Povilo bažnyčia': 909,
        'Tuskulėnai-Petro ir Povilo bažnyčia': 909,
        'Tuskulėnai-Tuskulėnų rimties parkas': 909,
        'Tuskulėnai-M. Katkaus': 910,
        'M. Katkaus-Tuskulėnai': 911,
        'M. Katkaus-Žalgirio': 912,
        'Trimitų-Mikalojaus Katkaus': 913,
        'Trimitų': 913,
        'B. Laurinavičiaus skveras-Giedraičių': 914,
        'B. Laurinavičiaus skveras-Pramogų arena': 914,
        'B. Laurinavičiaus skveras': 914,
        'Žalgirio-Giedraičių': 915,
        'Giedraičių-Tauragnų': 916,
        'Giedraičių-Ulonų': 916,
        'Apkasų-Žygio': 917,
        'Apkasų-Minties': 918,
        'Minties-Apkasų': 919,
        'Minties-Šilo tiltas 50': 920,
        'P. Lukšio-Šiaurės miestelis': 921,
        'P. Lukšio': 921,
        'Šiaurės miestelis-P. Lukšio kiti': 922,
        'Šiaurės miestelis-J. Galvydžio': 924,
        'Šiaurės miestelis-P. Lukšio autobusai': 925,
        'J. Galvydžio-Ulonų': 926,
        'J. Galvydžio': 926,
        'Ulonų-Šiaurės miestelis': 927,
        'Ulonų-Giedraičių': 928,
        'Ulonų-Herkaus Manto': 928,
        'P. Lukšio išlaipinimas': 929,
        'Saulėtekis-Vilniaus universitetas': 1001,
        'Saulėtekis-VU': 1001,
        'Gedimino technikos universitetas-Vilniaus universitetas': 1002,
        'Vilniaus Gedimino technikos universitetas-Vilniaus universitetas': 1002,
        'VGTU-VU': 1002,
        'Gedimino technikos universitetas-Senoji plytinė': 1003,
        'Vilniaus Gedimino technikos universitetas-Senoji plytinė': 1003,
        'VGTU-Senoji plytinė': 1003,
        'Senoji plytinė-Gedimino technikos universitetas': 1004,
        'Senoji plytinė-Vilniaus Gedimino technikos universitetas': 1004,
        'Senoji plytinė-VGTU': 1004,
        'Senoji plytinė-Plytinės': 1005,
        'Plytinės-Senoji plytinė': 1006,
        'Plytinės-Aukštagiris': 1007,
        'Aukštagiris-Dvarčionių kryžkelė': 1008,
        'Dvarčionių kryžkelė-Lazerių': 1009,
        'Dvarčionių kryžkelė-Baniškės': 1009,
        'Dvarčionys-Lazerių-Dvarčionių kryžkelė': 1011,
        'Lazerių-Dvarčionys': 1012,
        'Lazerių-Juodvarnių': 1012,
        'Lazerių-Dvarčionių kryžkelė': 1013,
        'Baniškės-Kairėnai': 1014,
        'Kairėnai-Paliuliškės': 1015,
        'Paliuliškės-Kairėnai': 1016,
        'Paliuliškės-Lubinų': 1017,
        'Lubinų-Paliuliškės': 1018,
        'Rokantiškės-Lyglaukiai': 1019,
        'Rokantiškės-Anapilio': 1019,
        'Rokantiškės-Klonio': 1019,
        'Rokantiškės-Pagal pareikalavimą': 1019,
        'Rokantiškės': 1019,
        'Vakario-Šiaurės': 1020,
        'Saulėtekis-Lakštingalų': 1021,
        'Saulėtekis-Žuvėdrų': 1021,
        'Vilniaus universitetas-Saulėtekis': 1022,
        'VU-Saulėtekis': 1022,
        'Vilniaus universitetas-Gedimino technikos universitetas': 1023,
        'Vilniaus universitetas-Vilniaus Gedimino technikos universitetas': 1023,
        'VU-VGTU': 1023,
        'Lubinų-Purienų': 1024,
        'Purienų-Galgiai': 1025,
        'Dvarčionys-Lazerių-Baniškės': 1026,
        'Lazerių-Baniškės': 1027,
        'Senoji plytinė išlaipinimas': 1028,
        'Kairėnai-Gvazdikų': 1029,
        'Klonio-Rokantiškės': 1030,
        'Klonio-Rokantiškių sodai': 1031,
        'Juodvarnių-S. Kerbedžio': 1032,
        'Juodvarnių-Lazerių': 1033,
        'S. Kerbedžio-Juodvarnių': 1034,
        'S. Kerbedžio-S. Kairio': 1036,
        'S. Kairio-Pylimėliai': 1038,
        'S. Kairio-S. Kerbedžio': 1039,
        'Moliakalnio-Mileišiškių sodai': 1040,
        'Moliakalnio-Pylimėliai': 1042,
        'Pylimėliai-Moliakalnio': 1043,
        'Pylimėliai-S. Kairio': 1045,
        'Duburio-Uosių sodai': 1046,
        'Sapieginės miškas-Anapilio': 1047,
        'Sapieginės miškas-Viršupio sodai': 1048,
        'Duburio-Kalno': 1049,
        'Duburio-Mažieji Pupojai': 1049,
        'Mažieji Pupojai-Duburio': 1050,
        'Mažieji Popojai-Šiaurės sodai': 1051,
        'Šiaurės sodai-Centrinė': 1054,
        'Šiaurės sodai-Mažieji Pupojai': 1056,
        'Centrinė-Egliškės': 1058,
        'Centrinė-Šiaurės sodai': 1060,
        'Šv. J. Bosko gimnazija-Egliškės': 1062,
        'J. Bosko gimnazija-Egliškės': 1062,
        'Šv. J. Bosko gimnazija': 1062,
        'J. Bosko gimnazija': 1062,
        'Egliškės-Centrinė': 1063,
        'Egliškės-Šv. J. Bosko gimnazija': 1065,
        'Egliškės-J. Bosko gimnazija': 1065,
        'Krivių-Vasaros': 1101,
        'Vasaros-Tuskulėnai': 1102,
        'Vasaros-Tuskulėnų rimties parkas': 1102,
        'Vasaros-Šeimyniškių': 1102,
        'Vasaros-Šv. Petro ir Povilo bažnyčia': 1102,
        'Vasaros-Petro ir Povilo bažnyčia': 1102,
        'L. Sapiegos-Šv. Petro ir Povilo bažnyčia': 1103,
        'L. Sapiegos-Petro ir Povilo bažnyčia': 1103,
        'L. Sapiegos-Vasaros': 1103,
        'L. Sapiegos-Šeimyniškių': 1103,
        'L. Sapiegos-P. Vileišio': 1104,
        'P. Vileišio-L. Sapiegos': 1105,
        'P. Vileišio-Šilo tiltas': 1106,
        'Šilo tiltas-P. Vileišio': 1107,
        'Šilo tiltas-Klinikų': 1108,
        'Klinikų-Šilo tiltas': 1109,
        'Klinikų-Tverečiaus kiti': 1110,
        'Klinikų-Nemenčinės plentas': 1110,
        'Klinikų-Vieversių': 1111,
        'Klinikų-Tverečiaus autobusai': 1112,
        'Tverečiaus-Antakalnis': 1113,
        'Tverečiaus-Klinikų': 1114,
        'Antakalnis-Tverečiaus': 1115,
        'Antakalnis-Klinikų': 1115,
        'Antakalnis-Antakalnio žiedas': 1116,
        'Antakalnis-Nemenčinės plentas': 1116,
        'Nemenčinės plentas-Antakalnis': 1117,
        'Nemenčinės plentas-Antakalnio žiedas': 1117,
        'Antakalnio žiedas-Antakalnis troleibusai': 1118,
        'Antakalnio žiedas troleibusai': 1118,
        'Nemenčinės plentas-Saulėtekis': 1119,
        'Lizdeikos-O. Milašiaus': 1121,
        'Lizdeikos-Kareivių': 1121,
        'Saulėtekis-Nemenčinės plentas': 1122,
        'Saulėtekis-Antakalnio žiedas': 1122,
        'Saulėtekis-Antakalnis': 1122,
        'Lakštingalų-Saulėtekis': 1123,
        'Žolyno-Bistryčios': 1125,
        'Žolyno': 1125,
        'Lyglaukiai-Šilo': 1126,
        'Šilo-Viršupis': 1127,
        'Šilo-Saulės slėnis': 1127,
        'Viršupis-Mildos': 1128,
        'Šilo tiltas-Minties': 1129,
        'Šilo tiltas-Šiaurės miestelis': 1129,
        'Bistryčios-Žolyno': 1130,
        'Bistryčios-Mileišiškės': 1130,
        'BM': 1130,
        'Bistryčios-Vieversių': 1131,
        'Lizdeikos-Antakalnis': 1132,
        'Lizdeikos-Antakalnio žiedas': 1132,
        'Lizdeikos-Nemenčinės plentas': 1132,
        'Žolyno išlaipinimas': 1134,
        'Vieversių-Klinikų': 1136,
        'Vieversių-Bistryčios': 1137,
        'Gvazdikų panaikinta': 1138,
        'Šilo tiltas-V. Grybo': 1139,
        'V. Grybo-Saulės slėnis': 1140,
        'V. Grybo-Šilo tiltas': 1141,
        'Saulės slėnis-Šilo': 1143,
        'Saulės slėnis-Viršupis': 1143,
        'Saulės slėnis-V. Grybo': 1145,
        'Zarasų-Vilnelės': 1201,
        'Zarasų-Subačiaus': 1202,
        'Zarasų-Gervėčių': 1202,
        'Zarasų-Drujos': 1203,
        'Vilnelės-Markučiai': 1204,
        'Vilnelės-Zarasų': 1205,
        'Markučiai-Vilnelės': 1206,
        'Drujos-Srovės': 1207,
        'Drujos-Polocko': 1207,
        'Srovės-Belmontas': 1208,
        'Polocko-Filaretų': 1209,
        'Filaretų-Krivių': 1210,
        'Filaretų-Šv. Petro ir Povilo bažnyčia': 1210,
        'Filaretų-Petro ir Povilo bažnyčia': 1210,
        'Belmontas-Polocko': 1211,
        'Belmontas-Drujos': 1211,
        'Rudens-Belmontas': 1212,
        'Rudens-Polocko': 1212,
        'Rudens-Šaudykla': 1213,
        'Rudens-Lelijų': 1213,
        'Rudens-Pūčkoriai': 1213,
        'Šaudykla-Rudens': 1214,
        'Šaudykla-Mildos': 1215,
        'Mildos-Šaudykla kiti': 1216,
        'Belmontas-Rudens': 1217,
        'Markučiai-Tuputiškės': 1218,
        'Kaukysos': 1219,
        'Pelesos-Stotis 58': 1301,
        'Pelesos-Stadionas': 1302,
        'Pelesos-Stotis kiti': 1303,
        'Stadionas-Pelesos': 1304,
        'Stadionas-Liepkalnis': 1305,
        'Rasų kapinės-Gervėčių': 1306,
        'Rasų kapinės-Dunojaus': 1307,
        'Dunojaus-Rasų kapinės': 1308,
        'Dunojaus-Balstogės': 1308,
        'Dunojaus-Ribiškės': 1309,
        'D': 1309,
        'Ribiškės-Dunojaus': 1310,
        'RD': 1310,
        'Ribiškės-Juodasis kelias': 1311,
        'RJK': 1311,
        'Juodasis kelias-Ribiškės': 1312,
        'Juodasis kelias-Guriai': 1313,
        'Juodasis kelias-Pavilnio regioninis parkas': 1313,
        'Juodasis kelias-Pavilnių regioninis parkas': 1313,
        'Žirnių-Liepkalnis': 1314,
        'Liepkalnis-Stadionas': 1315,
        'Liepkalnis-Aušros vartai': 1315,
        'Liepkalnis-Žirnių kiti': 1316,
        'Perlojos-Merkinės': 1317,
        'Balstogės-Zarasų': 1318,
        'Balstogės-Drujos': 1318,
        'Balstogės-Dunojaus': 1319,
        'Guriai-Juodasis kelias': 1401,
        'GJK': 1401,
        'Guriai-Pavilnio regioninis parkas': 1401,
        'Guriai-Pavilnių regioninis parkas': 1401,
        'Guriai-Pavilnio sodai': 1402,
        'GPS': 1402,
        'Pavilnio sodai-Guriai': 1403,
        'Pavilnio sodai-Garsioji': 1404,
        'Garsioji-Pavilnio sodai': 1405,
        'Garsioji-Grūdų': 1406,
        'Grūdų-Garsioji': 1407,
        'Grūdų-Pavilnys': 1408,
        'Pavilnys-Grūdų': 1409,
        'Pavilnys-Gamtininkų': 1410,
        'P': 1410,
        'Gamtininkų-Pavilnys': 1411,
        'Gamtininkų-Alėja': 1412,
        'Alėja-Gamtininkų': 1413,
        'Alėja-Strelčiukai': 1414,
        'Alėja-Strielčiukai': 1414,
        'Strelčiukai-Alėja': 1415,
        'Strielčiukai-Alėja': 1415,
        'SA': 1415,
        'Strelčiukai-Grigaičiai': 1416,
        'Strielčiukai-Grigaičiai': 1416,
        'SG': 1416,
        'Kinologijos centras-Žirnių': 1417,
        'Minsko plentas-Kinologijos centras': 1418,
        'Sodai-Minsko plentas': 1419,
        'Nemėžis-Sodai': 1420,
        'Žemasis Pavilnys-Žiedų': 1421,
        'Žemasis Pavilnys': 1421,
        'Guriai-P. B. Šivickio': 1422,
        'GPBŠ': 1422,
        'GŠ': 1422,
        'P. B. Šivickio-Ašmenėlės': 1423,
        'P. B. Šivickio-Guriai': 1424,
        'Gurių sodai-Šumsko kryptis': 1425,
        'Gurių sodai-Ašmenėlės': 1426,
        'Gurių sodai-Savičiūnų': 1426,
        'Šumsko kryptis įlaipinimas': 1427,
        'Šumsko kryptis-Šumsko kryptis': 1427,
        'Šumsko kryptis': 1427,
        'Ašmenėlės-P. B. Šivickio': 1428,
        'Ašmenėlės-Gurių sodai': 1429,
        'Ašmenėlės-Savičiūnų': 1429,
        'Žiedų-Žemasis Pavilnys': 1430,
        'Žiedų-Žemoji': 1431,
        'Žemoji-Žiedų': 1432,
        'Žemoji-Tuputiškės': 1433,
        'Tuputiškės-Žemoji': 1434,
        'Tuputiškės-Markučiai': 1435,
        'Pavilnio regioninis parkas-Juodasis kelias': 1436,
        'PG': 1436,
        'PRPG': 1436,
        'Pavilnio regioninis parkas-Kalnėnai': 1437,
        'Pavilnio regioninis parkas-Juodupio': 1437,
        'PJ': 1437,
        'PRPJ': 1437,
        'Pavilnių regioninis parkas-Juodasis kelias': 1436,
        'Pavilnių regioninis parkas-Kalnėnai': 1437,
        'Pavilnių regioninis parkas-Juodupio': 1437,
        'Šumsko kryptis išlaipinimas': 1438,
        'Šumsko kryptis-Gurių sodai': 1439,
        'Šumsko kryptis-9-asis kilometras': 1440,
        'Šumsko kryptis-Devintasis kilometras': 1440,
        'Varpų-Angelo': 1444,
        'Varpų-Užupio gimnazija': 1446,
        'Angelo': 1447,
        'Angelo-Aukštaičių': 1447,
        'Aukštaičių-Užupio': 1448,
        'Aukštaičių-Paupio turgus': 1449,
        'Paupio turgus-Aukštaičių': 1450,
        'Riedulių': 1451,
        'Riedulių-Drujos': 1451,
        'Drujos-Paupio': 1452,
        'Paupio-Paupio turgus': 1453,
        'Paupio': 1453,
        'Naujininkai-Eišiškių plentas': 1501,
        'Naujininkai-Vikingų slėnis': 1501,
        'Naujininkai-Liepynės kapinės': 1501,
        'Naujininkai-Karaimų kapinės': 1501,
        'Naujininkai-Prūsų troleibusai': 1502,
        'Naujininkai išlaipinimas': 1502,
        'Naujininkai troleibusai': 1502,
        'Naujininkai įlaipinimas': 1502,
        'Naujininkai': 1502,
        'Naujininkai-Naujininkai': 1502,
        'Prūsų-Naujininkai': 1503,
        'Prūsų-Vienaragių': 1504,
        'Dzūkų-Rudaminos': 1505,
        'Dzūkų-Panevėžio': 1506,
        'Rudaminos-Merkinės': 1507,
        'Rudaminos-Dzūkų': 1508,
        'Panevėžio-Pelesos': 1509,
        'Merkinės-Perlojos': 1510,
        'Merkinės-Rudaminos': 1511,
        'Perlojos-Liepkalnis': 1512,
        'Žirnių-Vikingų slėnis': 1513,
        'Žirnių-Vikingų': 1513,
        'Žirnių-Naujininkai': 1513,
        'Liepkalnis-Žirnių 58': 1514,
        'Tyzenhauzų-Karaimų kapinės': 1515,
        'Naujininkai-Prūsų autobusai': 1517,
        'Naujininkai-Vienaragių': 1517,
        'Liepkalnis-Perlojos': 1519,
        'Vikingų-Oro uostas': 1520,
        'Vikingų-Vikingų slėnis': 1521,
        'Vikingų-Liepynės kapinės': 1521,
        'Vikingų-Karaimų kapinės': 1521,
        'Vikingų-Žirnių': 1521,
        'Tyzenhauzų-Vikingų': 1522,
        'Tyzenhauzų-Vikingų slėnis': 1522,
        'Vikingų slėnis-Vikingų': 1523,
        'Vikingų slėnis-Naujininkai': 1523,
        'Vikingų slėnis-Karaimų kapinės': 1523,
        'Vikingų slėnis-Liepynės kapinės': 1523,
        'Vikingų slėnis': 1523,
        'Miškiniai-Litexpo': 1601,
        'Miškiniai-LITEXPO': 1601,
        'Miškiniai-Eigulių': 1602,
        'Litexpo-Lazdynai': 1603,
        'LITEXPO-Lazdynai': 1603,
        'Litexpo-Miškiniai': 1604,
        'LITEXPO-Miškiniai': 1604,
        'Litexpo-Gerosios Vilties': 1604,
        'LITEXPO-Gerosios Vilties': 1604,
        'Ąžuolo-Litexpo': 1605,
        'Ąžuolo-LITEXPO': 1605,
        'Ąžuolo-Lazdynai': 1605,
        'Ąžuolo-Riešutų': 1605,
        'Ąžuolo-Ryto': 1606,
        'Ryto-Ąžuolo': 1607,
        'Ryto-Vaivorykštės': 1608,
        'Ryto-Paukščių takas': 1608,
        'Lazdynai-Litexpo': 1609,
        'Lazdynai-LITEXPO': 1609,
        'Lazdynai-Gerosios Vilties': 1609,
        'Lazdynai-Paukščių takas': 1610,
        'Lazdynai-Vaivorykštės': 1610,
        'Lazdynai-Žėručio': 1611,
        'Akacijų-Paukščių takas': 1612,
        'Akacijų-Erfurto': 1613,
        'Akacijų-Šalnos': 1613,
        'Žėručio-Lazdynų seniūnija': 1614,
        'Lazdynų seniūnija-Žėručio': 1615,
        'Lazdynų seniūnija-Oslo': 1616,
        'Lazdynų seniūnija-Lazdynų ligoninė': 1616,
        'Lazdynų seniūnija-Vandenvala': 1616,
        'Lazdynų seniūnija-Pagal pareikalavimą': 1616,
        'Lazdynų seniūnija-Elektrinės': 1616,
        'Erfurto-Lazdynų seniūnija': 1617,
        'Erfurto-Šalnos': 1617,
        'Šalnos-Architektų': 1618,
        'Architektų-Riešutų': 1619,
        'Riešutų-Lazdynai': 1620,
        'Riešutų-Ąžuolo': 1620,
        'Oslo panaikinta': 1621,
        'Oslo-Erfurto': 1622,
        'Oslo-Žaros': 1623,
        'Lazdynų ligoninė-Erfurto': 1624,
        'Lazdynų ligoninė-Vandenvala': 1624,
        'Jonažolių-Oslo': 1625,
        'Lazdynų ligoninė-Šiltnamių': 1626,
        'Jonažolių-Bijūnų': 1627,
        'Jonažolių-Lazdynų ligoninė': 1627,
        'Šiltnamių-Lazdynų ligoninė': 1628,
        'Šiltnamių-Eigulių': 1629,
        'Pakalnučių-Jonažolių': 1630,
        'Pakalnučių': 1630,
        'Bijūnų-Ratilių': 1631,
        'Neužmirštuolių-Bukčiai': 1632,
        'Neužmirštuolių-Užutekio': 1633,
        'Bukčiai-Neužmirštuolių': 1634,
        'Bukčiai': 1634,
        'Paukščių takas-Vaivorykštės': 1635,
        'Paukščių takas-Lazdynai': 1636,
        'Žaros-Lazdynėliai': 1637,
        'Žaros-Oslo': 1638,
        'Lazdynėliai išlaipinimas': 1639,
        'Lazdynai-Ąžuolo': 1640,
        'Lazdynai-Riešutų': 1641,
        'Žėručio-Lazdynai': 1642,
        'Šalnos-Erfurto': 1643,
        'Architektų-Šalnos': 1643,
        'Riešutų-Architektų': 1645,
        'Paukščių takas-Ryto': 1646,
        'Ratilių-Užutekio': 1647,
        'Ratilių-Bijūnų': 1648,
        'Užutekio-Ratilių': 1649,
        'Užutekio-Ungurių': 1650,
        'Bijūnų-Pakalnučių': 1651,
        'Lazdynėliai-Žaros': 1652,
        'Lazdynėliai': 1652,
        'Oslo-Jonažolių': 1653,
        'M. Mironaitės-L. Asanavičiūtės': 1654,
        'Gudeliai-M. Mironaitės': 1655,
        'Gudeliai-Erfurto': 1656,
        'M. Mironaitės-Gudeliai': 1657,
        'Šiltnamių žiedas išlaipinimas': 1658,
        'Šiltnamių žiedas-Pakalnučių': 1659,
        'Bijūnų-Šiltnamių žiedas': 1660,
        'L. Asanavičiūtės-Pasakų parkas': 1661,
        'L. Asanavičiūtės-M. Mironaitės': 1662,
        'Ungurių-Užutekio': 1663,
        'Ungurių': 1663,
        'Lazdynų ligoninė išlaipinimas': 1665,
        'Paukščių takas-Akacijų': 1667,
        'Litexpo įlaipinimas': 1670,
        'LITEXPO įlaipinimas': 1670,
        'Litexpo': 1670,
        'LITEXPO': 1670,
        'Litexpo-Litexpo': 1670,
        'LITEXPO-LITEXPO': 1670,
        'Litexpo išlaipinimas': 1670,
        'LITEXPO išlaipinimas': 1670,
        'Litexpo panaikinta': 1671,
        'LITEXPO panaikinta': 1671,
        'Litexpo vakcinacijos centras': 1672,
        'LITEXPO vakcinacijos centras': 1672,
        'Vakcinacijos centras Litexpo': 1672,
        'Vakcinacijos centras LITEXPO': 1672,
        'Laisvės prospektas-Sietyno': 1702,
        'Laisvės prospektas-T. Narbuto': 1702,
        'Laisvės prospektas-Karoliniškės': 1703,
        'Laisvės prospektas-Karoliniškių poliklinika': 1703,
        'Karoliniškių poliklinika-Ugniagesių': 1704,
        'Karoliniškių poliklinika-Laisvės prospektas': 1705,
        'Karoliniškės-Laisvės prospektas': 1706,
        'Karoliniškės-Televizijos bokštas': 1707,
        'Karoliniškės-Vaivorykštės': 1707,
        'Televizijos bokštas-Laisvės prospektas': 1708,
        'Televizijos bokštas-Vaivorykštės': 1709,
        'Televizijos bokštas-Atminties': 1709,
        'Ugniagesių-Karoliniškių poliklinika': 1710,
        'Ugniagesių-Atminties': 1711,
        'Atminties-Ugniagesių': 1712,
        'Atminties-Vaivorykštės': 1712,
        'Atminties-Televizijos bokštas': 1712,
        'Atminties-Pasakų parkas': 1713,
        'Vaivorykštės-Televizijos bokštas': 1714,
        'Vaivorykštės-Karoliniškės': 1714,
        'Vaivorykštės-Atminties': 1714,
        'Vaivorykštės-Paukščių takas': 1715,
        'Vaivorykštės-Ryto': 1715,
        'Vaivorykštės-Lazdynai': 1715,
        'Pasakų parkas-Atminties': 1716,
        'Pasakų parkas-L. Asanavičiūtės': 1717,
        'T. Narbuto-Žvėrynas': 1718,
        'T. Narbuto-Žvėryno žiedas': 1718,
        'T. Narbuto-Švietimo akademija': 1718,
        'Justiniškės-Rygos': 1801,
        'Rygos-Pal. J. Matulaičio bažnyčia': 1802,
        'Rygos-J. Matulaičio bažnyčia': 1802,
        'Rygos-Viršuliškės': 1802,
        'Pal. J. Matulaičio bažnyčia-Šaulių sąjunga': 1803,
        'J. Matulaičio bažnyčia-Šaulių sąjunga': 1803,
        'Pal. J. Matulaičio bažnyčia-Viršuliškės': 1803,
        'J. Matulaičio bažnyčia-Viršuliškės': 1803,
        'Lūžiai-Justiniškės': 1804,
        'Šaulių sąjunga-Viršuliškės': 1805,
        'Šaulių sąjunga': 1805,
        'Viršuliškės-Pal. J. Matulaičio bažnyčia': 1807,
        'Viršuliškės-J. Matulaičio bažnyčia': 1807,
        'Viršuliškės-Rygos': 1807,
        'Viršuliškės-Spaudos rūmai': 1808,
        'Spaudos rūmai-Viršuliškės': 1809,
        'Spaudos rūmai-Kaukaro': 1810,
        'Spaudos rūmai-Viršilų': 1810,
        'Spaudos rūmai-Sietyno': 1811,
        'Troleibusų parkas-Spaudos rūmai': 1813,
        'Troleibusų parkas': 1813,
        'Kaukaro-Lūžiai': 1815,
        'Kaukaro-Justiniškių žiedas': 1815,
        'Č. Sugiharos-Viršuliškės': 1816,
        'Č. Sugiharos-Ąžuolyno': 1817,
        'Pal. J. Matulaičio bažnyčia-Rygos': 1818,
        'J. Matulaičio bažnyčia-Rygos': 1818,
        'Viršuliškės-Č. Sugiharos': 1819,
        'T. Narbuto-Sietyno': 1820,
        'Viršilų-Piliakalnio': 1841,
        'Viršilų išlaipinimas': 1841,
        'Viršilų': 1841,
        'Ąžuolyno-Č. Sugiharos': 1842,
        'Ąžuolyno-Vaikų kaimas': 1843,
        'Saltoniškės-Šeškinė': 1901,
        'Šeškinė-Ukmergės': 1902,
        'Šeškinė-Šeškinės poliklinika': 1902,
        'Šeškinė-Siesikų': 1902,
        'Šeškinė-Saltoniškės': 1903,
        'Šeškinė-Lietuvos sąjūdžio kelias': 1903,
        'Šeškinė-Sąjūdžio kelias': 1903,
        'Šeškinė panaikinta': 1904,
        'Siesikų-Šeškinės poliklinika': 1905,
        'Siesikų-Saltoniškės': 1905,
        'Siesikų-Vaikų kaimas': 1906,
        'Siesikų-Ąžuolyno': 1906,
        'Siesikų-Buivydiškių': 1906,
        'Vaikų kaimas-Siesikų': 1907,
        'Vaikų kaimas-Buivydiškių': 1908,
        'Buivydiškių-Vaikų kaimas': 1909,
        'Buivydiškių-Dūkštų': 1909,
        'Buivydiškių-Siesikų': 1909,
        'Buivydiškių-Rygos': 1910,
        'Rygos-Buivydiškių': 1911,
        'Rygos-Čiobiškio': 1912,
        'Rygos-Vilniaus rajono poliklinika': 1912,
        'Čiobiškio-Vilniaus rajono poliklinika': 1913,
        'Ukmergės-Dūkštų': 1914,
        'Ukmergės-Šeškinė': 1915,
        'Ukmergės-Šeškinės poliklinika': 1916,
        'Dūkštų-Ukmergės': 1917,
        'Dukštų-Musninkų': 1918,
        'Musninkų-Paberžės 75': 1919,
        'Musninkų-Buivydiškių': 1920,
        'Šeškinės poliklinika-I. Šeiniaus': 1921,
        'Ukmergės-Paberžės': 1922,
        'Šeškinės kalvos-Licėjus': 1923,
        'Gelvonėlio-Šeškinės kalvos': 1924,
        'Gelvonėlio-Gelvonų': 1925,
        'Paberžės-Gelvonėlio': 1926,
        'Paberžės-Gelvonų': 1926,
        'Gelvonų-Gelvonėlio': 1927,
        'Gelvonų-Paberžės': 1927,
        'Gelvonų-Jovaro': 1928,
        'Paberžės-Musninkų': 1929,
        'Šeškinės kalvos-Gelvonėlio': 1930,
        'Šeškinės kalvos-Siesikų': 1931,
        'Šeškinės poliklinika-Ukmergės': 1932,
        'Musninkų-Ukmergės': 1933,
        'Musninkų-Paberžės 48': 1933,
        'Mykolo Romerio universitetas-Ateities': 2001,
        'M. Romerio universitetas-Ateities': 2001,
        'Ateities-Rugių': 2002,
        'Ateities-Kalvarijos': 2002,
        'Kalvarijos-Seminarija': 2003,
        'Kalvarijos-Baltupiai': 2003,
        'Seminarija-Kalvarijos': 2004,
        'Seminarija-Pušynas': 2005,
        'Pušynas-Seminarija': 2006,
        'Pušynas-Baltupiai': 2007,
        'Didlaukio-Baltupiai': 2008,
        'Didlaukio-Ateities': 2009,
        'Baltupiai-Didlaukio': 2010,
        'Baltupiai-Naujakiemio': 2011,
        'Baltupiai-J. Kazlausko': 2011,
        'Naujakiemio-J. Kazlausko': 2012,
        'Naujakiemio-Baltupiai': 2013,
        'J. Kazlausko-Pramogų arena': 2014,
        'Pramogų arena-Licėjus': 2015,
        'Licėjus-Šeškinės kalvos': 2016,
        'Licėjus-Ozo žiedas': 2016,
        'Ateities-Didlaukio': 2017,
        'Baltupiai-Pušynas': 2018,
        'Baltupiai-Kalvarijos': 2018,
        'Ateities': 2019,
        'Ateities įlaipinimas': 2019,
        'Ateities-Ateities': 2019,
        'Ateities išlaipinimas': 2019,
        'P. Vaičaičio-M. Sleževičiaus': 2020,
        'P. Vaičaičio-Visorių sodai': 2021,
        'Visorių sodai-P. Vaičaičio': 2023,
        'Visorių sodai-M. Sleževičiaus': 2024,
        'M. Indriliūno-Visorių sodai': 2025,
        'M. Indriliūno-Mokslininkų': 2026,
        'M. Sleževičiaus-M. Romerio universitetas': 2027,
        'M. Sleževičiaus-Visorių sodai': 2028,
        'Ateities-M. Romerio universitetas': 2101,
        'Ateities-Maumedžių': 2102,
        'Mokyklos-Maumedžių': 2103,
        'Mokyklos-Akademijos': 2104,
        'Bajorų sodai-Chemijos institutas': 2105,
        'Bajorų sodai': 2105,
        'Chemijos institutas-Bajorų sodai': 2106,
        'Akademijos-Mokyklos': 2107,
        'J. Kairiūkščio-Akademijos': 2109,
        'J. Kairiūkščio-Santaros': 2109,
        'J. Kairiūkščio-Vaikų ligoninė': 2109,
        'J. Kairiūkščio-Visoriai': 2110,
        'Visoriai-J. Kairiūkščio': 2111,
        'Visoriai': 2111,
        'Kalvarijos-Rugių': 2112,
        'Kalvarijos-Ateities': 2112,
        'Kalvarijos-Jeruzalė': 2113,
        'Jeruzalė-Kalvarijos': 2114,
        'Jeruzalė-Žaliųjų ežerų': 2115,
        'Jeruzalė-Žaliųjų Ežerų': 2115,
        'Jeruzalė-Santariškės': 2115,
        'Jeruzalė-Molėtų plentas': 2115,
        'Jeruzalė-P. Baublio': 2115,
        'Žaliųjų ežerų-Jeruzalė': 2116,
        'Žaliųjų Ežerų-Jeruzalė': 2116,
        'Molėtų plentas-Žaliųjų ežerų': 2117,
        'Molėtų plentas-Žaliųjų Ežerų': 2117,
        'Molėtų plentas-Akademijos': 2118,
        'Žaliųjų ežerų-Santariškės': 2120,
        'Žaliųjų Ežerų-Santariškės': 2120,
        'Santariškės-Žaliųjų ežerų': 2121,
        'Santariškės-Žaliųjų Ežerų': 2121,
        'Santariškės-Jeruzalė': 2121,
        'Santariškės-Molėtų plentas': 2121,
        'Santariškės-P. Baublio': 2121,
        'Santariškės-Vaikų ligoninė': 2122,
        'Vaikų ligoninė atstova': 2123,
        'P. Baublio-Verkių rūmai': 2127,
        'Verkių rūmai-P. Baublio': 2128,
        'Verkių rūmai-Ežerėliai': 2129,
        'Ežerėliai-Kurklių': 2130,
        'Ežerėliai-Gulbinėlių': 2130,
        'Maumedžių-Ateities': 2131,
        'Maumedžių-Mokyklos': 2132,
        'Chemijos institutas-Akademijos': 2133,
        'Muzikų-Santariškių žiedas': 2134,
        'Muzikų-Vaikų ligoninė': 2135,
        'Santariškių žiedas-Muzikų': 2137,
        'Santariškių žiedas-Vaikų ligoninė': 2137,
        'Santariškių žiedas': 2137,
        'Vaikų ligoninė-Santariškės': 2138,
        'Chemijos institutas-Mokslininkų': 2139,
        'Akademijos-Molėtų plentas': 2141,
        'Akademijos panaikinta': 2142,
        'Akademijos-Geležinio Vilko': 2143,
        'Akademijos-J. Kairiūkščio': 2143,
        'Akademijos-Chemijos institutas': 2144,
        'Geležinio Vilko-Akademijos': 2145,
        'Geležinio Vilko-Skersinės': 2146,
        'Vaikų ligoninė-Muzikų': 2147,
        'Vaikų ligoninė-Santariškių žiedas': 2147,
        'Vaikų ligoninė-Santaros': 2147,
        'Vaikų ligoninė-Geležinio Vilko': 2147,
        'Vaikų ligoninė-J. Kairiūkščio': 2147,
        'Bajorai-Riaubonių': 2148,
        'Mokslininkų-Chemijos institutas': 2149,
        'Mokslininkų-Bajorų miškas': 2150,
        'Mergelės': 2151,
        'Riaubonių-Šaulio': 2152,
        'Riaubonių-Bajorai': 2152,
        'Riaubonių-Daubų': 2152,
        'Riaubonių': 2152,
        'Šaulio-Bajorai': 2153,
        'Bajorų miškas-Bajorai': 2154,
        'Bajorų miškas-Mokslininkų': 2155,
        'Vaikų ligoninė išlaipinimas': 2156,
        'Bajorai-Bajorų miškas': 2157,
        'Šaulio-Mėtų': 2158,
        'Daubų-Bajorai': 2159,
        'Daubų': 2159,
        'Riaubonių panaikinta': 2160,
        'Žvorūnos-Ragės': 2164,
        'Žvorūnos': 2164,
        'Užpalių-Žvorūnos': 2165,
        'Užpalių': 2165,
        'Bubilo-Aitvarų': 2166,
        'Bubilo': 2166,
        'Kryžiokų sodų-Bubilo': 2168,
        'Kryžiokų sodų': 2168,
        'Aitvarų-Užpalių': 2169,
        'Aitvarų': 2169,
        'Ežerėliai-Verkių rūmai': 2201,
        'Naujieji Verkiai-Vaikų darželis': 2202,
        'Naujieji Verkiai': 2202,
        'Vaikų darželis-Naujieji Verkiai': 2204,
        'Vaikų darželis-Naujoji': 2205,
        'Vaikų darželis-Kremplių': 2205,
        'Kremplių-Vaikų darželis': 2206,
        'Kremplių-Naujoji': 2206,
        'Kremplių-Popieriaus': 2207,
        'Popieriaus-Kremplių': 2208,
        'Popieriaus-Kurklių': 2209,
        'Popieriaus-Verkių Riešė': 2209,
        'Kurklių-Ežerėliai': 2210,
        'Kurklių-Verkių Riešė': 2211,
        'Verkių Riešė-Kurklių': 2212,
        'Verkių Riešė-Popieriaus': 2212,
        'Verkių Riešė-Žaliojo Visalaukio': 2213,
        'Staviškės-Naujoji': 2214,
        'Staviškės-Ožkiniai': 2215,
        'Ožkiniai-Staviškės': 2216,
        'Ožkiniai-Ožkinių žiedas': 2217,
        'Ožkinių žiedas-Ožkiniai': 2218,
        'Ožkinių žiedas': 2218,
        'Ragučio-Žaliojo Visalaukio': 2219,
        'Ragučio-Balsiai': 2220,
        'Balsiai-Kryžiokai': 2222,
        'Kryžiokai-Krakiškės': 2223,
        'Naujoji-Staviškės': 2224,
        'Naujoji-Vaikų darželis': 2225,
        'Naujoji-Kremplių': 2225,
        'Naujaneriai-Krakiškės': 2226,
        'Naujaneriai-Krakiškių sodai': 2226,
        'Naujaneriai-Juozapiškės': 2227,
        'Paežerys-Diemedis': 2228,
        'Paežerys-Krakiškių sodai': 2229,
        'Diemedis-Pagubės sodai': 2230,
        'Diemedis-Paežerys': 2231,
        'Gulbinų-Pagubė': 2233,
        'Gulbinų-Pagubės sodai': 2234,
        'Pagubė-Gulbinų': 2235,
        'Pagubė': 2235,
        'Kryžiokai-Balsiai': 2236,
        'Sakališkės-Bireliai': 2237,
        'Krakiškės-Naujaneriai': 2238,
        'Krakiškės-Kryžiokai': 2239,
        'Žvorūnos panaikinta': 2240,
        'Bireliai-Birelių žiedas': 2243,
        'Bireliai-Sakališkės': 2244,
        'Birelių žiedas-Bireliai': 2245,
        'Birelių žiedas': 2245,
        'Juozapiškės-Europos parkas': 2246,
        'Juozapiškės-Skirgiškės': 2246,
        'Juozapiškės-Naujaneriai': 2247,
        'Europos parkas-Skirgiškės': 2248,
        'Europos parkas-Pagal pareikalavimą': 2248,
        'Europos parkas-Juozapiškės': 2248,
        'Europos parkas': 2248,
        'Sakališkės-Ąžuolynas': 2249,
        'Pagubės sodai-Diemedis': 2250,
        'Pagubės sodai-Ąžuolynas': 2251,
        'Pagubės sodai-Gulbinų': 2252,
        'Ąžuolynas-Sakališkės': 2253,
        'Ąžuolynas-Pagubės sodai': 2254,
        'Austėjos-Žaliojo Visalaukio': 2255,
        'Austėjos-Žalčių': 2256,
        'Žalčių-Austėjos': 2257,
        'Žalčių-Laimos': 2258,
        'Balsių mokykla-Laimos': 2259,
        'Balsių mokykla-Žynių': 2259,
        'Balsių mokykla-Kryžiokų sodų': 2259,
        'Balsių mokykla': 2259,
        'Krakiškių sodai-Naujaneriai': 2260,
        'Ragės-Balsiai': 2261,
        'Ragės-Žynių': 2262,
        'Balsiai-Ragučio': 2263,
        'Balsiai-Ragės': 2263,
        'Krakiškių sodai-Paežerys': 2264,
        'Žaliojo Visalaukio-Ragučio': 2265,
        'Žaliojo Visalaukio-Verkių Riešė': 2267,
        'Laimos-Austėjos': 2268,
        'Laimos-Balsių mokykla': 2269,
        'Laimos-Žynių': 2269,
        'Žynių-Balsių mokykla': 2270,
        'Žynių-Laimos': 2270,
        'Žynių-Ragės': 2271,
        'Gulbinėlių-Verkių rūmai': 2272,
        'Gulbinėlių-Raudonės': 2273,
        'Raudonės-Mažieji Gulbinai': 2275,
        'Raudonės-Gulbinėlių': 2276,
        'Mažieji Gulbinai-Pijų': 2277,
        'Mažieji Gulbinai-Raudonės': 2278,
        'Pijų-Padvarės': 2279,
        'Pijų-Mažieji Gulbinai': 2280,
        'Padvarės-Didieji Gulbinai': 2282,
        'Padvarės-Pijų': 2284,
        'Didieji Gulbinai-Padvarės': 2285,
        'Ežerėliai panaikinta': 2286,
        'Žilvičių-Uosių sodai': 2296,
        'Žilvičių-Rokantiškių sodai': 2297,
        'Mileišiškės-Mileišiškių sodai': 2298,
        'Mileišiškės-Bistryčios': 2299,
        'Skirgiškės-Europos parkas': 2300,
        'Skirgiškės-Pagal pareikalavimą': 2300,
        'Skirgiškės-Juozapiškės': 2300,
        'Skirgiškės': 2300,
        'Mildos-Šaudykla 37': 2301,
        'Mildos-Pūčkorių atodanga': 2302,
        'Mildos-Viadukas': 2302,
        'Mildos-Viršupis': 2302,
        'Viršupis-Šilo': 2303,
        'Šilo-Lyglaukiai': 2304,
        'Lyglaukiai-Rokantiškės': 2305,
        'Viadukas-Mildos': 2306,
        'Viadukas-Girininkija': 2307,
        'Girininkija-Viadukas': 2308,
        'Girininkija-Kučkuriškės': 2309,
        'Kučkuriškės-Girininkija': 2310,
        'Kučkuriškės-Užtvankos': 2311,
        'Pūčkorių atodanga-Mildos': 2312,
        'Pūčkorių atodanga-Pūčkoriai': 2313,
        'Pūčkoriai-Pūčkorių atodanga': 2314,
        'Pūčkoriai-Rudens': 2314,
        'Pūčkoriai-S. Batoro': 2315,
        'Pūčkoriai-Lelijų': 2315,
        'S. Batoro-Pūčkoriai': 2316,
        'S. Batoro-Lelijų': 2317,
        'Užtvankos-Kučkuriškės': 2318,
        'Užtvankos-Širšių': 2319,
        'Širšių-Užtvankos': 2320,
        'Širšių-A. Kojelavičiaus': 2321,
        'A. Kojelavičiaus-Širšių': 2322,
        'A. Kojelavičiaus-Dūmų': 2323,
        'A. Kojelavičiaus-Uosių': 2324,
        'Uosių-A. Kojelavičiaus': 2325,
        'Uosių-Palydovo': 2326,
        'Uosių-Paparčių': 2327,
        'Paparčių-Uosių': 2328,
        'Paparčių-Kalno': 2329,
        'Kalno-Paparčių': 2330,
        'Palydovo-Uosių': 2331,
        'Palydovo-Pupojų': 2332,
        'Pupojų-Šiaurės': 2333,
        'Pupojų-Palydovo': 2334,
        'Šiaurės-Pupojų': 2335,
        'Šiaurės-Vakario': 2336,
        'J. Kupalos-A. Kojelavičiaus': 2337,
        'J. Kupalos-Ievų': 2338,
        'Dūmų-A. Kojelavičiaus': 2339,
        'Dūmų-Tremtinių': 2340,
        'Lelijų-S. Batoro': 2341,
        'Lelijų-Pūčkoriai': 2341,
        'Lelijų-Rudens': 2341,
        'Lelijų-Tremtinių': 2342,
        'Ievų-J. Kupalos': 2343,
        'Ievų-Gandrų': 2344,
        'Tremtinių-Dūmų': 2345,
        'Tremtinių-Lelijų': 2345,
        'Tremtinių-Genių': 2346,
        'Tremtinių-Gerovės': 2346,
        'Tremtinių-Pramonės': 2347,
        'Genių-Tremtinių': 2348,
        'Genių-Grigaičiai': 2348,
        'G': 2348,
        'Genių-Respublikinė psichiatrijos ligoninė': 2349,
        'Genių-Psichiatrijos ligoninė': 2349, 
        'GP': 2349, 
        'Grigaičiai-Strelčiukai': 2350,
        'GS': 2350,
        'Grigaičiai-Genių': 2351,
        'Respublikinė psichiatrijos ligoninė-Genių': 2352,
        'Psichiatrijos ligoninė-Genių': 2352,
        'PG': 2352,
        'Respublikinė psichiatrijos ligoninė-Parko': 2353,
        'Psichiatrijos ligoninė-Parko': 2353,
        'PP': 2353,
        'Parko-Respublikinė psichiatrijos ligoninė': 2354,
        'Parko-Psichiatrijos ligoninė': 2354,
        'Parko-Naujosios Vilnios žiedas': 2355,
        'Naujosios Vilnios žiedas-Parko': 2356,
        'Naujosios Vilnios žiedas-Rytų': 2357,
        'Rytų-Naujosios Vilnios žiedas': 2358,
        'Rytų-Linksmoji': 2359,
        'Gandrų-Ievų': 2360,
        'Gandrų-Rugiagėlių': 2361,
        'Pramonės-Tremtinių': 2362,
        'Pramonės-Neries': 2363,
        'Rugiagėlių-Gandrų': 2364,
        'Rugiagėlių-Bičių': 2365,
        'Bičių-Rugiagėlių': 2366,
        'Bičių-Užkiemio': 2367,
        'Neries-Pramonės': 2368,
        'Neries-Naujoji Vilnia': 2369,
        'Linksmoji-Rytų': 2370,
        'Linksmoji-Naujoji Vilnia': 2371,
        'Naujoji Vilnia-Linksmoji': 2372,
        'Naujoji Vilnia-Neries': 2372,
        'Užkiemio-Rugiagėlių': 2373,
        'Užkiemio-Arimų': 2374,
        'Arimų-Užkiemio': 2375,
        'A. Kojelavičiaus-J. Kupalos': 2376,
        'Kalno-Duburio': 2377,
        'Naujosios Vilnios žiedas-Gerviškių': 2378,
        'Naujosios Vilnios žiedas išlaipinimas': 2378,
        'Naujoji Vilnia-Verbų': 2379,
        'Uosių sodai-Duburio': 2391,
        'Uosių sodai-Žilvičių': 2392,
        'Rokantiškių sodai-Žilvičių': 2393,
        'Rokantiškių sodai-Klonio': 2394,
        'Anapilio-Sapieginės miškas': 2395,
        'Anapilio-Rokantiškės': 2396,
        'Viršupio sodai-Sapieginės miškas': 2397,
        'Viršupio sodai-Mileišiškių sodai': 2398,
        'Mileišiškių sodai-Viršupio sodai': 2399,
        'Mileišiškių sodai-Moliakalnio': 2399,
        'Mileišiškių sodai-Mileišiškės': 2400,
        'Eigulių-Gerosios Vilties': 2401,
        'Eigulių-Vilkpėdės': 2401,
        'Eigulių-Vingio parkas': 2401,
        'Burbiškės-Vilkpedės žiedas': 2402,
        'Vilkpėdės-Gerosios Vilties': 2404,
        'Vilkpėdės-Giraitės': 2404,
        'Vilkpėdės-Riovonys': 2405,
        'Riovonys-Vilkpedės': 2406,
        'Riovonys-Pakalniškių': 2407,
        'Pakalniškių-Riovonys': 2408,
        'Pakalniškių-Baldai': 2409,
        'Baldai-Pakalniškių': 2410,
        'Baldai-Žemieji Paneriai': 2411,
        'Sausupio-Baldai': 2412,
        'Sausupio': 2412,
        'Žemieji Paneriai-Vaduvos': 2413,
        'Žemieji Paneriai': 2413,
        'Vaduvos-Valkininkų': 2414,
        'Vaduvos-Fizikos institutas': 2414,
        'Vaduvos-Prekybos bazė': 2414,
        'Vaduvos-Sausupio': 2415,
        'Ūmėdžių-Vaduvos': 2416,
        'Ūmėdžių-Skapiškio': 2416,
        'Ūmėdžių': 2416,
        'Valkininkų-Jankiškių': 2417,
        'Valkininkų-Ūmėdžių 24': 2417,
        'Valkininkų-Ūmėdžių įlaipinimas': 2418,
        'Šaltupio-Jankiškių': 2419,
        'Šaltupio-Titnago': 2420,
        'Titnago-Šaltupio': 2421,
        'Titnago': 2421,
        'Jankiškių-Šaltupio': 2422,
        'Jankiškių-Valkininkų': 2423,
        'Vilkpėdės žiedas-Burbiškės': 2424,
        'Vilkpėdės žiedas': 2424,
        'Vilkpėdės žiedas išlaipinimas': 2425,
        'Meškonių-Gerviškių': 2426,
        'Meškonių išlaipinimas': 2427,
        'Titnago išlaipinimas': 2428,
        'Gerviškių-Meškonių': 2429,
        'Gerviškių-Naujosios Vilnios žiedas': 2431,
        'Riovonių žiedas': 2432,
        'Meškonių pakrovimas': 2433,
        'Skapiškio-Panerių kalvyno': 2434,
        'Panerių kalvyno išlaipinimas': 2435,
        'Panerių kalvyno-Skapiškio': 2436,
        'Panerių kalvyno': 2436,
        'Skapiškio-Vaduvos': 2437,
        'Vaidotai-Šaltinio': 2501,
        'Vaidotai-Pagal pareikalvimą': 2501,
        'Vaidotai-V. A. Graičiūno': 2501,
        'Vaidotai': 2501,
        'Vėjo-Vaidotai': 2502,
        'Vėjo': 2502,
        'Eišiškių plentas-Metalo': 2601,
        'Eišiškių plentas-Naujininkai kiti': 2602,
        'Eišiškių plentas-Dariaus ir Girėno': 2603,
        'Eišiškių plentas-Naujininkai greitieji': 2604,
        'Metalo-Hidrogeologijos': 2605,
        'Metalo-Eišiškių plentas': 2606,
        'Dariaus ir Girėno-F. Vaitkaus': 2607,
        'Dariaus ir Girėno-Oro uostas': 2607,
        'Dariaus ir Girėno-Eišiškių plentas': 2608,
        'Metalo-Geologų': 2609,
        'Metalo panaikinta': 2610,
        'F. Vaitkaus-Oro uostas': 2611,
        'F. Vaitkaus-Dariaus ir Girėno': 2612,
        'Oro uostas-Rodūnios kelias': 2613,
        'Oro uostas-F. Vaitkaus': 2613,
        'Oro uostas-Dariaus ir Girėno': 2613,
        'Oro uostas-Vikingų': 2613,
        'Oro uostas': 2613,
        'Hidrogeologijos-Metalo': 2614,
        'Hidrogeologijos-Verslo': 2615,
        'Geologų-Metalo': 2616,
        'Geologų-Katilinė': 2617,
        'Kirtimai-F. Vaitkaus': 2618,
        'Kirtimai-Rodūnios kelias': 2618,
        'Kirtimai-Oro uostas': 2618,
        'Kirtimai-Tiekimo': 2619,
        'Tiekimo-Kirtimai': 2620,
        'Tiekimo-Kirtimų geležinkelio stotis': 2621,
        'Kirtimų geležinkelio stotis-Tiekimo': 2622,
        'Kirtimų geležinkelio stotis': 2622,
        'Katilinė-Pameistrių': 2623,
        'Verslo-Hidrogeologijos': 2624,
        'Verslo-Dilgynė': 2625,
        'Verslo-Geologų': 2626,
        'Verslo-Tiekimo': 2626,
        'Verslo panaikinta': 2626,
        'Elektros-Dilgynė': 2627,
        'Elektros-Verslo': 2627,
        'Dilgynė-Verslo': 2628,
        'Dilgynė-Elektros': 2628,
        'Dilgynė panaikinta': 2629,
        'Dilgynė-Eišiškių sodai': 2630,
        'Dilgynė-Dieveniškės': 2630,
        'Karaimų kapinės-Žirnių': 2631,
        'Karaimų kapinės': 2631,
        'Žirnių-Kelininkų': 2632,
        'Kelininkų-Šalčininkų kryptis': 2633,
        'Šalčininkų kryptis-Miško parkas': 2634,
        'Miško parkas-Pripetės': 2635,
        'Lydos-Svirno': 2636,
        'Lydos-Pupinė': 2636,
        'Salininkų sodai-Sakalaičių': 2637,
        'Sakalaičių-Pervaža': 2638,
        'Meistrų-Elektros': 2639,
        'Pameistrių-Meistrų': 2640,
        'Paštas-Rodūnios sodų': 2641,
        'Rodūnios kelias-Paštas': 2644,
        'Rodūnios kelias-F. Vaitkaus': 2645,
        'Rodūnios kelias-Oro uostas': 2645,
        'Rodūnios kelias-Kirtimai': 2645,
        'Pupinė-Salininkų sodai': 2646,
        'Pupinė-Lydos': 2647,
        'Rodūnios sodų-Paštas': 2648,
        'Rodūnios sodų': 2648,
        'Paštas-Rodūnios kelias': 2649,
        'Elektros-Meistrų': 2650,
        'Meistrų-Pameistrių': 2651,
        'Katilinė-Geologų': 2652,
        'Pameistrių-Katilinė': 2653,
        'Liepynės kapinės-Karaimų kapinės': 2654,
        'Liepynės kapinės-Žirnių': 2654,
        'Liepynės kapinės': 2654,
        'Pripetės-Lydos': 2655,
        'Pripetės-Miško parkas': 2656,
        'Užusienis-Dieveniškių': 2701,
        'Užusienis': 2701,
        'Eišiškių sodai-Ąžuolijai': 2702,
        'Eišiškių sodai-Dilgynė': 2703,
        'Ąžuolijai-Eišiškių sodai': 2704,
        'Ąžuolijai-Salininkų žiedas': 2705,
        'Salininkų žiedas-Ąžuolijai': 2706,
        'Salininkų žiedas-Mechanikų': 2707,
        'Mechanikų-Salininkų žiedas': 2708,
        'Mechanikų-Salininkai': 2709,
        'Salininkai-J. Stašaičio': 2710,
        'Salininkai-Melioratorių': 2710,
        'Salininkai-Mechanikų kiti': 2711,
        'J. Stašaičio-Salininkai': 2712,
        'Melioratorių-Salininkai': 2712,
        'J. Stašaičio-Vilniaus': 2713,
        'Melioratorių-Vilniaus': 2713,
        'Vilniaus-J. Stašaičio': 2714,
        'Vilniaus-Melioratorių': 2714,
        'Pervaža-Vilniaus': 2715,
        'Pervaža-Avinėlių': 2715,
        'Dieveniškių-Užusienis': 2716,
        'Dieveniškių-Dilgynė': 2717,
        'Salininkų-Kelmijos sodai': 2719,
        'Juodšilių žiedas-2-ieji Juodšiliai': 2720,
        'Juodšilių žiedas-Antrieji Juodšiliai': 2720,
        'Juodšilių žiedas-Avinėlių': 2720,
        'Juodšilių žiedas': 2720,
        'Vokės parkas-Miškinių sodai': 2721,
        '1-ieji Juodšiliai-Miškinių sodai': 2723,
        'Pirmieji Juodšiliai-Miškinių sodai': 2723,
        '1-ieji Juodšiliai-2-ieji Juodšiliai': 2724,
        'Pirmieji Juodšiliai-Antrieji Juodšiliai': 2724,
        'Vokės parkas-Raistelių miškas': 2725,
        'Miškinių sodai-Vokės parkas': 2726,
        'Miškinių sodai-1-ieji Juodšiliai': 2727,
        'Miškinių sodai-Pirmieji Juodšiliai': 2727,
        '2-ieji Juodšiliai-1-ieji Juodšiliai': 2728,
        'Antrieji Juodšiliai-Pirmieji Juodšiliai': 2728,
        '2-ieji Juodšiliai-Avinėlių': 2729,
        'Antrieji Juodšiliai-Avinėlių': 2729,
        '2-ieji Juodšiliai-Juodšilių žiedas': 2729,
        'Antrieji Juodšiliai-Juodšilių žiedas': 2729,
        'Salininkai-Mechanikų 3': 2731,
        'Avinėlių-2-ieji Juodšiliai': 2732,
        'Avinėlių-Antrieji Juodšiliai': 2732,
        'Avinėlių-Juodšilių žiedas': 2732,
        'Avinėlių-Kalviškės': 2732,
        'Avinėlių-Pervaža': 2733,
        'Sakalaičių sodai-Ąžuolijai': 2735,
        'Sakalaičių sodai-Gervėbalės': 2736,
        'Gervėbalės-Sakalaičių sodai': 2737,
        'Gervėbalės-Valakų': 2738,
        'Valakų-Gervėbalės': 2739,
        'Valakų-Vilniaus': 2740,
        'Vokės parkas-Raisteliai': 2741,
        'Fermentų-Fermentų': 2801,
        'Fermentų': 2801,
        'Fermentų-Chemijos': 2802,
        'Fermentų-Vokės': 2802,
        'Fermentų-Kazbėjų žiedas': 2802,
        'Vokės panaikinta': 2803,
        'Vokės-Fermentų': 2804,
        'Vokės-Kazbėjų žiedas': 2804,
        'Vokės-Kazbėjų': 2805,
        'Kazbėjų-Vokės': 2806,
        'Kazbėjų-Vilniaus Pergalė': 2807,
        'Slėnis-V. A. Graičiūno': 2808,
        'Slėnis-Vilniaus Pergalė': 2809,
        'Chemijos panaikinta': 2810,
        'Chemijos-Prekybos': 2811,
        'Prekybos-Chemijos': 2812,
        'Prekybos-Juodšilių': 2813,
        'Juodšilių-Prekybos': 2814,
        'Vilniaus-Pervaža': 2815,
        'Šaltinio-Vaidotai': 2816,
        'Šaltinio-Vėjo': 2816,
        'Šaltinio-Baltoji Vokė': 2817,
        'Pagirių-Juodšilių': 2818,
        'Pagirių-Šaltinio': 2819,
        'Juodšilių-Krantinės': 2820,
        'Juodšilių-Pagirių': 2820,
        'V. A. Graičiūno-Slėnis': 2821,
        'Kazbėjų žiedas-Fermentų': 2822,
        'Kazbėjų žiedas-Vokės': 2822,
        'Kazbėjų žiedas': 2822,
        'Vilniaus Pergalė-Kazbėjų': 2823,
        'Krantinės-Šaltinio': 2824,
        'Vilniaus Pergalė-Slėnis': 2825,
        'Pagal pareikalavimą-V. A. Graičiūno': 2826,
        'Pagal pareikalavimą-Šaltinio': 2827,
        'V. A. Graičiūno-Šaltinio': 2828,
        'V. A. Graičiūno-Pagal pareikalavimą': 2828,
        'Valkininkų-Ūmėdžių kiti': 2901,
        'Fizikos institutas-Lentvario': 2903,
        'Fizikos institutas': 2903,
        'Lentvario-Vaduvos': 2904,
        'Lentvario-Vilijos': 2905,
        'Aukštieji Paneriai-Vilijos-Lentvario': 2906,
        'Galvės-Vilijos': 2908,
        'Galvės panaikinta': 2909,
        'Galvės-Fermentų': 2910,
        'Galvės-Stasylų': 2910,
        'Galvės-Žarijų': 2910,
        'Deguonies-Granito': 2911,
        'Deguonies-Galvės': 2912,
        'Deguonies-Vilijos': 2912,
        'Granito-Deguonies': 2913,
        'Granito': 2913,
        'Žarijų-Šešėlių': 2914,
        'Žarijų-Galvės': 2915,
        'Šešėlių-Liudvinavo': 2916,
        'Šešėlių-Žarijų': 2917,
        'Liudvinavo-Asfalto': 2918,
        'Liudvinavo-Šešėlių': 2919,
        'Asfalto-Liudvinavo': 2920,
        'Asfalto-Liudvinava': 2921,
        'Asfalto-Kulokiškės': 2921,
        'Kulokiškės-Liudvinava': 2922,
        'Kulokiškės-Asfalto': 2922,
        'Kulokiškės-Kauno plentas': 2923,
        'Kulokiškės-Vaduvos': 2923,
        'Kauno plentas-Gariūnai': 2924,
        'Kauno plentas-Kulokiškės': 2925,
        'Gariūnai-Jočionys': 2926,
        'Gariūnai-Plungės': 2926,
        'Gariūnai-Kauno plentas': 2927,
        'Gariūnai-Neravų': 2927,
        'Gariūnai-Vandenvala': 2928,
        'Plungės': 2929,
        'Jočionys-Gariūnai': 2930,
        'Jočionys-Plungės': 2930,
        'Jočionys-Elektrinės': 2931,
        'Elektrinės-Jočionys': 2932,
        'Vandenvala-Gariūnai': 2933,
        'Vandenvala-Erfurto': 2934,
        'Vandenvala-Lazdynų ligoninė': 2934,
        'Liudvinava-Kulokiškės': 2935,
        'Liudvinava-Asfalto': 2935,
        'Liudvinava-Mūrinė Vokė': 2936,
        'Vilijos-Lentvario': 2937,
        'Vilijos-Galvės': 2938,
        'Vilijos-Deguonies': 2938,
        'Prekybos bazė-Neravų': 2939,
        'Prekybos bazė-Vaduvos': 2939,
        'Prekybos bazė-Gariūnų': 2939,
        'Prekybos bazė': 2939,
        'Stasylų-Trakų Vokė': 2940,
        'Stasylų-Galvės': 2941,
        'Elektrinės-Erfurto': 2944,
        'Elektrinės-Pagal pareikalavimą': 2944,
        'Aukštieji Paneriai-Vilijos-Galvės': 2945,
        'Zuikių-Vasarotojų': 2946,
        'Zuikių': 2946,
        'Vasarotojų-Kadugių': 2947,
        'Vasarotojų-Zuikių': 2948,
        'Kadugių-Agrastų': 2949,
        'Kadugių-Vasarotojų': 2950,
        'Vilijos-Aukštieji Paneriai': 2951,
        'Elektrinės laikinoji': 2952,
        'Gariūnų laikinoji': 2953,
        'Kilimų fabrikas-Naujasis Lentvaris': 3000,
        'Naujasis Lentvaris-Žalioji': 3001,
        'Naujasis Lentvaris-Vandenų': 3002,
        'Lentvaris-1-asis Lentvaris': 3003,
        'Lentvaris-Pirmasis Lentvaris': 3003,
        'Kilimų fabrikas-Lentvaris': 3004,
        'Vandenų-Kilimų fabrikas': 3005,
        'Vandenų': 3005,
        'Lentvaris': 3006,
        'Lentvaris Dzūkų': 3006,
        'Lentvaris žiedas': 3006,
        'Lentvaris-Kilimų fabrikas': 3006,
        'Lentvaris-Lentvaris žiedas': 3006,
        'Lentvaris-Lentvaris kiti': 3007,
        'E. Andrė-Trakų Vokė': 3101,
        'E. Andrė-J. Tiškevičiaus': 3101,
        'E. Andrė': 3101,
        'Juodbaliai-E. Pliaterytės': 3102,
        'Juodbaliai-Metropolis': 3103,
        'Daniliškės-Bičiulių': 3104,
        'Gunkliškių-E. Andrė': 3105,
        'Gunkliškių': 3105,
        'Trakų Vokė-Gunkliškių': 3106,
        'Trakų Vokė-Dobūklė': 3106,
        'Trakų Vokė-Dobrovolės': 3106,
        'J. Tiškevičiaus-E. Pliaterytės': 3107,
        'J. Tiškevičiaus-Trakų Vokė': 3108,
        'Trakų Vokė-Stasylų': 3109,
        'Bičiulių-Metropolis': 3110,
        'Bičiulių-Daniliškės': 3111,
        'E. Pliaterytės-J. Tiškevičiaus': 3112,
        'E. Pliaterytės-Juodbaliai': 3113,
        'Metropolis-Bičiulių': 3114,
        'Metropolis-Juodbaliai': 3115,
        'Degučių-Jaunystės': 3116,
        'Degučių-Medkirčių': 3117,
        'Jaunystės-Degučių': 3118,
        'Jaunystės-Vaidotų piliakalnis': 3119,
        'Daniliškės-Medkirčių': 3120,
        'Medkirčių-Daniliškės': 3121,
        'Medkirčių-Degučių': 3122,
        'Vaidotų piliakalnis-Jaunystės': 3123,
        'Vaidotų piliakalnis-Pagiriai': 3124,
        'Lentvario geležinkelio stotis-Račkūnai': 3125,
        'Lentvario geležinkelio stotis-Lentvaris': 3126,
        'Pumpėnų-Taikos': 3201,
        'Pumpėnų': 3201,
        'Taikos-Sūduvių': 3202,
        'Taikos-Medeinos': 3202,
        'Taikos-M. Biržiškos gimnazija': 3203,
        'Taikos-Justiniškės': 3204,
        'M. Biržiškos gimnazija-Atžalyno': 3205,
        'M. Biržiškos gimnazija-Taikos': 3206,
        'Atžalyno-M. Biržiškos gimnazija': 3207,
        'Atžalyno-Šiaurinė': 3208,
        'Justiniškės-Taikos': 3209,
        'Justiniškės-Lūžiai': 3211,
        'Šiaurinė-Atžalyno': 3212,
        'Šiaurinė-Justiniškių žiedas': 3213,
        'Lūžiai-Kaukaro': 3214,
        'Justiniškių žiedas-Šiaurinė': 3216,
        'Justiniškių žiedas-Kaukaro': 3216,
        'Justiniškių žiedas': 3216,
        'Rygos-Justiniškės': 3218,
        'Čiobiškio-Rygos': 3219,
        'Kaukaro-Troleibusų parkas': 3220,
        'Justiniškės-Atžalyno': 3221,
        'Atžalyno-Justiniškės': 3222,
        'Sūduvių-Pumpėnų': 3301,
        'Sūduvių-Medeinos': 3302,
        'Medeinos-Sūduvių': 3303,
        'Medeinos-Pumpėnų': 3303,
        'Medeinos-Skalvių': 3304,
        'Skalvių-Medeinos': 3305,
        'Skalvių-Gabijos': 3305,
        'Skalvių': 3305,
        'Skalvių-Pavilnionių': 3305,
        'Skalvių-Perkūnkiemis': 3305,
        'Skalvių išlaipinimas': 3306,
        'Skalvių žiedas': 3306,
        'Gabijos-Skalvių': 3307,
        'Gabijos-Pašilaičiai': 3308,
        'Perkūnkiemis-Pavilionys': 3309,
        'Deivių-Gedvydžių': 3310,
        'Deivių-Perkūno': 3310,
        'Deivių': 3310,
        'Pašilaičiai-Gabijos': 3311,
        'Pašilaičiai-J. Juzeliūno': 3312,
        'Vilniaus rajono poliklinika-Žemynos': 3313,
        'Vilniaus rajono poliklinika-Čiobiškio': 3314,
        'Vilniaus rajono poliklinika-Rygos': 3314,
        'Žemynos-J. Baltrušaičio': 3315,
        'Žemynos-J. Juzeliūno': 3315,
        'Žemynos-Pašilaičių žiedas': 3315,
        'Žemynos-Kaimelio': 3315,
        'Žemynos-Vilniaus rajono poliklinika': 3316,
        'Perkūnkiemis-Skalvių': 3317,
        'Pavilionys-Perkūnkiemis': 3318,
        'J. Juzeliūno-Pašilaičių žiedas': 3319,
        'J. Juzeliūno-J. Baltrušaičio': 3320,
        'Gedvydžių-J. Baltrušaičio': 3322,
        'S. Lozoraičio-I. Šeiniaus': 3323,
        'Pašilaičių žiedas-Žemynos': 3324,
        'Pašilaičių žiedas': 3324,
        'I. Šeiniaus-Šeškinės poliklinika': 3325,
        'J. Baltrušaičio-S. Lozoraičio': 3326,
        'J. Baltrušaičio-I. Šeiniaus': 3326,
        'J. Baltrušaičio-Fabijoniškės': 3327,
        'J. Baltrušaičio-Takas': 3327,
        'J. Juzeliūno-Pašilaičiai': 3328,
        'J. Baltrušaičio-Kaimelio': 3329,
        'J. Baltrušaičio-Kaimelio žiedas': 3329,
        'Perkūno-Pavilionys': 3331,
        'Perkūno-Gedvydžių': 3332,
        'Perkūno-Deivių': 3332,
        'Pašilaičių žiedas išlaipinimas': 3335,
        'Pavilnionių-Gileikių': 3336,
        'Pavilnionių-Skalvių': 3337,
        'Gileikių-Naujosios Gineitiškės': 3338,
        'Gileikių': 3338,
        'Tvenkinių-Sidaronių': 3403,
        'Sidaronių-Tvenkinių': 3404,
        'Tvenkinių-V. Pociūno': 3405,
        'V. Pociūno-Tvenkinių': 3406,
        'V. Pociūno-Pilaitė': 3407,
        '1-asis paplūdimys-Vaidilutės': 3500,
        'Pirmasis paplūdimys-Vaidilutės': 3500,
        'O. Milašiaus-Valakampių tiltas': 3501,
        'O. Milašiaus': 3501,
        'Lizdeikos-Grybautojų': 3502,
        'Rato-Lizdeikos': 3503,
        '1-asis paplūdimys-Rato': 3504,
        'Pirmasis paplūdimys-Rato': 3504,
        'Vaidilutės-1-asis paplūdimys': 3505,
        'Vaidilutės-Pirmasis paplūdimys': 3505,
        '2-asis paplūdimys-Vaidilutės': 3506,
        'Antrasis paplūdimys-Vaidilutės': 3506,
        'Bruknių-2-asis paplūdimys': 3507,
        'Bruknių-Antrasis paplūdimys': 3507,
        'Meškeriotojų-Svajonių': 3508,
        'Meškeriotojų-Turniškės': 3509,
        'Turniškės-Meškeriotojų': 3510,
        'Turniškės': 3510,
        'Mėlynių-Svajonių': 3511,
        'Mėlynių-Meškeriotojų': 3512,
        'Grybautojų-Mėlynių': 3513,
        'Grybautojų-Žuvėdrų': 3514,
        'Žuvėdrų-Lakštingalų': 3515,
        'Žuvėdrų-Grybautojų': 3516,
        'Lakštingalų-Kiškių': 3518,
        'Kiškių-Lakštingalų': 3519,
        'Kiškių-O. Milašiaus': 3519,
        'Kiškių-Ežerėlių': 3520,
        'Ežerėlių-Kiškių': 3521,
        'Ežerėlių-Nugalėtojų': 3522,
        'Aukštagiris-Plytinės': 3523,
        'Dvarčionių kryžkelė-Aukštagiris': 3524,
        'Baniškės-Lazerių': 3525,
        'Baniškės-Dvarčionių kryžkelė': 3525,
        'Kairėnai-Baniškės': 3526,
        'Gvazdikų-Kairėnai': 3527,
        'Gvazdikų-Žemoji Veržuva': 3528,
        'Žemoji Veržuva-Gvazdikų': 3529,
        'Žemoji Veržuva-Vaguva': 3530,
        'Žemoji Veržuva-Inovacijų pramonės parkas': 3530,
        'Žemoji Veržuva-Vinciūniškės': 3530,
        'Žemoji Veržuva-Pagal pareikalavimą': 3530,
        'Vaguva-Žemoji Veržuva': 3531,
        'Vaguva-Inovacijų pramonės parkas': 3531,
        'Vaguva-Aukštoji Veržuva': 3532,
        'Aukštoji Veržuva-Vaguva': 3533,
        'Aukštoji Veržuva': 3533,
        'Turniškių miškas-Nugalėtojų': 3534,
        'Turniškių miškas-Smėlynė': 3535,
        'Smėlynė-Turniškių miškas': 3536,
        'Smėlynė-Veržuvos': 3537,
        'Veržuvos-Smėlynė': 3538,
        'Veržuvos-Karačiūnai': 3539,
        'Karačiūnai-Smėlynė': 3540,
        'Karačiūnai-Miškas': 3541,
        'Karačiūnai-Šilas': 3541,
        'Šilas-Karačiūnai': 3542,
        'Šilas-J. Biliūno': 3543,
        'Miškas-Balžio': 3544,
        'Miškas-Karačiūnai': 3545,
        'Balžio-Miškas': 3546,
        'Antaviliai-Antavilių žiedas': 3547,
        'Antaviliai-J. Biliūno': 3548,
        'Antavilių žiedas-Antaviliai': 3549,
        'Antavilių žiedas': 3549,
        'J. Biliūno-Antaviliai': 3550,
        'J. Biliūno-Laurų': 3551,
        'Nugalėtojų-Ežerėlių': 3552,
        'Nugalėtojų-Turniškių miškas': 3553,
        'Svajonių-Bruknių': 3554,
        'Balžio žiedas-Balžio': 3558,
        'Balžio žiedas': 3558,
        'Balžio-Balžio žiedas': 3559,
        'Laurų-Šilas': 3560,
        'Laurų': 3560,
        'Vinciūniškės-Žemoji Veržuva': 3561,
        'Vinciūniškės-Pagal pareikalavimą': 3561,
        'Vinciūniškės': 3561,
        'Miškonys': 3562,
        'Lizdeikos-Rato': 3564,
        'Rato-1-asis paplūdimys': 3565,
        'Rato-Pirmasis paplūdimys': 3565,
        'Vaidilutės-2-asis paplūdimys': 3566,
        'Vaidilutės-Antrasis paplūdimys': 3566,
        '2-asis paplūdimys-Bruknių': 3567,
        'Antrasis paplūdimys-Bruknių': 3567,
        'Bruknių-Svajonių': 3568,
        'Svajonių-Meškeriotojų': 3569,
        'Grybautojų-Lizdeikos': 3571,
        'Vismaliukai-Žemoji Veržuva': 3572,
        'Vismaliukai-Vaguva': 3572,
        'Vismaliukai': 3572,
        'Miškadvaris-Vismaliukai': 3574,
        'Miškadvaris': 3574,
        'Inovacijų pramonės parkas-Miškadvaris': 3575,
        'Inovacijų pramonės parkas-Tujų': 3575,
        'Inovacijų pramonės parkas': 3575,
        'Tujų': 3576,
        'Inovacijų pramonės parkas laikina': 3578,
        'Senoji Pilaitė-Pilaitė': 3601,
        'Senoji Pilaitė': 3601,
        'Pilaitė-Smalinės': 3602,
        'Papilėnų-Senoji Pilaitė': 3603,
        'Papilėnų-I. Kanto': 3603,
        'Papilėnų panaikinta': 3604,
        'Tolminkiemio-Papilėnų': 3605,
        'Tolminkiemio-Įsruties': 3605,
        'Tolminkiemio-Karaliaučiaus': 3606,
        'Karaliaučiaus-Tolminkiemio': 3607,
        'Karaliaučiaus-Gilužio': 3608,
        'Gilužio-Karaliaučiaus': 3609,
        'Platiniškės-Kriaučiūnai': 3610,
        'Platiniškės': 3610,
        'Šventapilės-Platiniškės': 3611,
        'Šventapilės': 3611,
        'Bitėnų išlaipinimas': 3612,
        'Bitėnų-Gilužio': 3613,
        'Bitėnų': 3613,
        'Gilužio-Bitėnų': 3614,
        'Kriaučiūnai-Papiškės': 3615,
        'Kriaučiūnai-Padekaniškės': 3616,
        'Papiškės-Vaivadiškės': 3617,
        'Papiškės-Kriaučiūnai': 3618,
        'Vaivadiškės-Karveliškių kapinės': 3619,
        'Vaivadiškės-Karveliškės': 3619,
        'Vaivadiškės-Papiškės': 3620,
        'Gilužio žiedas': 3621,
        'Bitėnų žiedas': 3621,
        'Smalinės-Įsruties': 3622,
        'Įsruties-Pajautos': 3623,
        'Įsruties-Smalinės': 3624,
        'Pajautos-Padekaniškės': 3625,
        'Pajautos-Vėluvos': 3625,
        'Pajautos-Įsruties': 3626,
        'Pajautos-Tolminkiemio': 3626,
        'Pajautos-Bitėnų': 3627,
        'Karaliaučiaus-Pajautos': 3628,
        'Smalinės-Pilaitė': 3629,
        'Senoji Pilaitė-Papilėnų': 3630,
        'Papilėnų-Tolminkiemio': 3631,
        'Padekaniškės-Kriaučiūnai': 3632,
        'Padekaniškės-Pajautos': 3633,
        'Pilaitė-Piliakalnio': 3634,
        'Papilėnų-Pilaitė': 3635,
        'I. Kanto-Taurupės': 3636,
        'I. Kanto-Papilėnų': 3637,
        'Paplūdimio-Pakrantės': 3638,
        'Paplūdimio-Taurupės': 3639,
        'Pakrantės-Paplūdimio': 3640,
        'Taurupės-Paplūdimio': 3641,
        'Taurupės-I. Kanto': 3643,
        'Pakrantės-Trakėnų': 3644,
        'Trakėnų-Gelūžės': 3646,
        'Trakėnų-Pakrantės': 3647,
        'Gelūžės-Obeliškių': 3648,
        'Gelūžės-Trakėnų': 3650,
        'Obeliškių-Vienkiemių': 3652,
        'Obeliškių-Gelūžės': 3653,
        'Vienkiemių-Šventapilės': 3654,
        'Vienkiemių': 3654,
        'Kriaučiūnai-Gavaičių': 3655,
        'Gavaičių-Obeliškių': 3656,
        'Vėluvos-Varnės': 3658,
        'Vėluvos-Padekaniškės': 3659,
        'Varnės-Pergalės': 3660,
        'Varnės-Vėluvos': 3662,
        'Pergalės-Garvės': 3663,
        'Pergalės-Varnės': 3664,
        'Smalinės-Papilėnų': 3665,
        'S. Lozoraičio-J. Baltrušaičio': 3801,
        'Fabijoniškės-Gedvydžių': 3802,
        'Fabijoniškės': 3802,
        'Takas-Sporto gimnazija': 3803,
        'Takas-Kaimelio žiedas': 3803,
        'Takas-J. Juzeliūno': 3803,
        'Takas-J. Baltrušaičio': 3803,
        'Takas-Gedvydžių': 3804,
        'Takas-S. Nėries': 3804,
        'Gedvydžių-Perkūno': 3805,
        'Gedvydžių-Deivių': 3805,
        'Gedvydžių-Takas': 3806,
        'Gedvydžių-Fabijoniškių žiedas': 3807,
        'Fabijoniškių žiedas-Gedvydžių': 3809,
        'Fabijoniškių žiedas-P. Žadeikos': 3810,
        'Fabijoniškių žiedas-Išlaipinimas': 3811,
        'Sporto gimnazija-Takas': 3812,
        'Sporto gimnazija-J. Juzeliūno': 3812,
        'Kaimelio žiedas-Kaimelio': 3813,
        'Sporto gimnazija-P. Žadeikos': 3814,
        'P. Žadeikos-Sporto gimnazija': 3815,
        'P. Žadeikos-Kaimelio žiedas': 3815,
        'P. Žadeikos-L. Giros': 3816,
        'A. Jonyno-Kaimelio': 3817,
        'A. Jonyno-Kaimelio žiedas': 3817,
        'A. Jonyno-L. Giros': 3818,
        'L. Giros-A. Jonyno': 3819,
        'L. Giros-Kaimelio': 3819,
        'L. Giros-P. Žadeikos': 3820,
        'L. Giros-Pamiškė': 3821,
        'L. Giros-M. Romerio universitetas': 3822,
        'M. Romerio universitetas-L. Giros': 3823,
        'Pamiškė-L. Giros': 3824,
        'Pamiškė-S. Stanevičiaus': 3825,
        'S. Stanevičiaus-Pamiškė': 3826,
        'S. Stanevičiaus-Jovaro': 3827,
        'Jovaro-S. Stanevičiaus': 3828,
        'Jovaro-Gelvonėlio': 3829,
        'P. Žadeikos-Fabijoniškių žiedas': 3831,
        'I. Šeiniaus-S. Lozoraičio': 3832,
        'I. Šeiniaus-J. Baltrušaičio': 3832,
        'S. Nėries-Takas': 3833,
        'S. Nėries-L. Zamenhofo': 3834,
        'L. Zamenhofo-M. Lietuvio': 3835,
        'L. Zamenhofo': 3835,
        'L. Zamenhofo-S. Nėries': 3836,
        'M. Lietuvio-S. Nėries': 3837,
        'M. Lietuvio': 3837,
        'M. Lietuvio išlaipinimas': 3838,
        'Kaimelio-J. Juzeliūno': 3839,
        'Kaimelio žiedas-Sporto gimnazija': 3840,
        'Jovaro panaikinta-Fabijoniškių': 3841,
        'Jovaro panaikinta-Gelvonėlio': 3842,
        'Fabijoniškių-Jovaro panaikinta': 3844,
        'Fabijoniškių-Kaimelio': 3846,
        'Fabijoniškių-Kaimelio žiedas': 3846,
        'Kaimelio-Fabijoniškių': 3848,
        'Kaimelio žiedas išlaipinimas': 3890,
        'Mūrinė Vokė-J. Janonio': 3901,
        'Mūrinė Vokė-Gureliai': 3901,
        'J. Janonio-Mūrinė Vokė': 3902,
        'J. Janonio-Bališkės': 3903,
        'Bališkės-J. Janonio': 3904,
        'Bališkės-S. Krasausko': 3905,
        '1-asis Lentvaris-Lentvaris': 3906,
        'Pirmasis Lentvaris-Lentvaris': 3906,
        '1-asis Lentvaris-Mačiuliškių': 3907,
        'Pirmasis Lentvaris-Mačiuliškių': 3907,
        'Raudonbalė-Pagrandos': 3910,
        'Raudonbalė': 3910,
        'Mūrinė Vokė-Liudvinava': 3911,
        'S. Krasausko-Mačiuliškių': 3912,
        'S. Krasausko-Bališkės': 3913,
        'Gureliai-J. Švažo': 3914,
        'Gureliai-Mūrinė Vokė': 3915,
        'Gureliai-J. Janonio': 3915,
        'J. Švažo-Kaimynų': 3917,
        'J. Švažo-Gureliai': 3918,
        'Kaimynų-J. Švažo': 3920,
        'Kaimynų': 3920,
        'Mačiuliškių-1-asis Lentvaris': 3921,
        'Mačiuliškių-Pirmasis Lentvaris': 3921,
        'Mačiuliškių-Bališkės': 3922,
        'Žirnių-Kinologijos centras': 4001,
        'Kinologijos centras-Minsko plentas': 4002,
        'Kelininkų-Žirnių': 4003,
        'Šalčininkų kryptis-Kelininkų': 4004,
        'Miško parkas-Šalčininkų kryptis': 4005,
        'Salininkų sodai-Pupinė': 4006,
        'Sakalaičių-Salininkų sodai': 4007,
        'Pervaža-Sakalaičių': 4008,
        'Svirno-Lydos': 4009,
        'Svirno-Basiukai': 4010,
        'Basiukai-Svirno': 4011,
        'Basiukai-Katiliškės': 4012,
        'Katiliškės-Basiukai': 4013,
        'Katiliškės-Kineliai': 4014,
        'Lydos-Pripetės': 4015,
        'Kalnėnai-Pavilnio regioninis parkas': 4016,
        'Kalnėnai-Pavilnių regioninis parkas': 4016,
        'Kalnėnai-Juodupio': 4016,
        'Juodupio-Kalnėnai': 4017,
        'Juodupio-Pavilnio regioninis parkas': 4017,
        'Juodupio-Pavilnių regioninis parkas': 4017,
        'Juodupio-Airių': 4018,
        'J': 4018,
        'Airių-Savičiūnų': 4019,
        'Kalnėnai-Tautų': 4020,
        'Tautų-Žirnių': 4021,
        'Tautų-Kalnėnai': 4022,
        'Tautų-Pagal pareikalavimą': 4022,
        'Airių-Juodupio': 4024,
        'Savičiūnų-Gurių sodai': 4025,
        'Savičiūnų-Ašmenėlės': 4025,
        'Savičiūnų-Airių': 4026,
        'Kunigiškių-Grigiškių poliklinika': 4102,
        'Šviesos-Kunigiškių': 4103,
        'Salos-Šviesos': 4104,
        'Grigiškių poliklinika-Grigiškių žiedas': 4105,
        'Neravų-Salos': 4106,
        'Neravų': 4106,
        'Kunigiškių-Šviesos': 4107,
        'Kranto-Grigiškių žiedas': 4112,
        'Žalioji-Kranto': 4113,
        'Grigiškių žiedas-Kranto': 4114,
        'Grigiškių žiedas-Kovo 11-osios': 4114,
        'Grigiškių žiedas-Kauno Vokės': 4114,
        'Grigiškių žiedas': 4114,
        'Kranto-Žalioji': 4115,
        'Žalioji-Naujasis Lentvaris': 4116,
        'Valai-Vokės sodai': 4117,
        'Valai': 4117,
        'Grigiškių žiedas išlaipinimas': 4118,
        'Šviesos-Salos': 4119,
        'Salos-Prekybos bazė': 4120,
        'Salos-Kauno plentas': 4120,
        'Kovo 11-osios-Grigiškių poliklinika': 4121,
        'Kovo 11-osios': 4121,
        'Grigiškių poliklinika-Kunigiškių': 4123,
        'Vokės sodai-Kauno Vokės': 4124,
        'Vokės sodai-Valai': 4126,
        'Kauno Vokės-Grigiškių žiedas': 4127,
        'Kauno Vokės-Vokės sodai': 4128,
        'Minsko plentas-Sodai': 4301,
        'Sodai-Nemėžis': 4302,
        'Nemėžis-Daržininkai': 4303,
        'Daržininkai-Posūkis': 4304,
        'Posūkis-Stankutiškės': 4306,
        'Stankutiškės-Sodžiaus': 4307,
        'Stankutiškės-Posūkis': 4308,
        'Stankutiškės-1-asis Didžiasalis': 4308,
        'Stankutiškės-Pirmasis Didžiasalis': 4308,
        'Sodžiaus-Stankutiškės': 4309,
        'Sodžiaus-Skaidiškės': 4310,
        'Skaidiškių žiedas-Sodžiaus': 4311,
        'Skaidiškių žiedas-Skaidiškės': 4312,
        'Skaidiškių žiedas': 4312,
        'Skaidiškės-Skaistės': 4313,
        'Skaidiškės-Sodžiaus': 4314,
        'Skaidiškės-Skaidiškių žiedas': 4314,
        'Skaistės-Skaidiškės': 4315,
        'Skaistės': 4315,
        'Skaidiškės-Draugystės': 4316,
        'Draugystės-Rudamina': 4317,
        'Draugystės-Skaidiškės': 4318,
        'Rudamina panaikinta': 4319,
        'Rudamina priemiestiniai': 4320,
        'Čekėnų-Rudaminos paukštynas': 4321,
        'Čekėnų-Rudamina': 4322,
        'Rudaminos paukštynas-Kineliai': 4323,
        'Rudaminos paukštynas-Čekėnų': 4324,
        'Kineliai-Katiliškės': 4325,
        'Kineliai-Rudaminos paukštynas': 4326,
        'Daržininkai-Nemėžis': 4327,
        'Rudamina-Čekėnų': 4328,
        'Posūkis-Daržininkai': 4329,
        'Rudamina-2-oji Rudamina': 4330,
        'Rudamina-Antroji Rudamina': 4330,
        'Rudaminos žiedas': 4332,
        'Rudamina-Draugystės': 4334,
        'Nemėžis-V. Sirokomlės': 4350,
        'Baltarusių-Ramunių': 4351,
        'Baltarusių': 4351,
        'V. Sirokomlės-Smėlio': 4352,
        'V. Sirokomlės': 4352,
        'Sodybų-Šveicarų': 4353,
        'Sodybų': 4353,
        'Smėlio-Baltarusių': 4354,
        'Smėlio': 4354,
        'Vyturių-Kuprioniškės': 4355,
        'Vyturių': 4355,
        'Minsko plentas panaikinta': 4357,
        'Šveicarų-Vyturių': 4358,
        'Šveicarų': 4358,
        'Ramunių-Sodybų': 4359,
        'Ramunių': 4359,
        'Kalviškės-Kineliai': 4360,
        'Kalviškės-Avinėlių': 4361,
        'Tvenkinių-Buivydiškės': 4401,
        'Buivydiškės-Tvenkinių': 4402,
        'Buivydiškės-Ąžuolų': 4403,
        'Sodų-Zujūnai': 4404,
        'Sodų-Ąžuolų': 4405,
        'Zujūnai-Sodų': 4406,
        'Naujosios Gineitiškės-Senosios Gineitiškės': 4407,
        'Antežeriai-Senosios Gineitiškės': 4408,
        'Antežeriai-Garbės': 4409,
        'Zujūnai-Garbės': 4410,
        'Naujosios Gineitiškės-Pavilnionių': 4411,
        'Senosios Gineitiškės-Antežeriai': 4412,
        'Senosios Gineitiškės-Naujosios Gineitiškės': 4413,
        'Ąžuolų-Buivydiškės': 4414,
        'Ąžuolų-Sodų': 4415,
        'Garbės-Antežeriai': 4416,
        'Garbės-Zujūnai': 4419,
        'Garbės-Pergalės': 4419,
        'Purienų-Lubinų': 4601,
        'Galgiai-Purienų': 4602,
        'Galgiai-Vakario': 4603,
        'Vakario-Galgiai': 4604,
        'Rytų-Karklėnų': 4605,
        'Gerovės-Tremtinių': 4606,
        'Karklėnų-Žvirblių': 4608,
        'Karklėnų-Rytų': 4610,
        'Žvirblių-Gerovės': 4612,
        'Žvirblių-Karklėnų': 4613,
        'Gerovės-Žvirblių': 4615,
        '2-osios Bukiškės-Bukiškių': 4901,
        'Antrosios Bukiškės-Bukiškių': 4901,
        '1-osios Bukiškės-Durpynas': 4902,
        'Pirmosios Bukiškės-Durpynas': 4902,
        'Liepų-Mėtų': 4905,
        'Liepų': 4905,
        'Aušros-Liepų': 4907,
        'Aušros': 4907,
        'Mėtų-Šaulio': 4910,
        'Mėtų-Aušros': 4911,
        'Pavilionys-Medelynas': 5001,
        'Pavilionys-Tarandė': 5001,
        'Pavilionys-Perkūno': 5002,
        'Medelynas-Bukiškių': 5003,
        'Medelynas-Pavilionys': 5004,
        'Bukiškių-Medelynas': 5005,
        'Tarandė-Medelynas': 5006,
        'Tarandė-T. Žebrausko': 5007,
        'Laidagaliai-T. Žebrausko': 5009,
        'Laidagaliai': 5009,
        'T. Žebrausko-Tarandė': 5011,
        'Pagrandos-Laidagaliai': 5013,
        'Pagrandos': 5013,
        'Kelmiškių-Raudonbalė': 5014,
        'Kelmiškių': 5014,
        'Bukiškių-1-osios Bukiškės': 5015,
        'Bukiškių-Pirmosios Bukiškės': 5015,
        'T. Žebrausko-Kelpių': 5016,
        'Kelpių-J. Kamarausko': 5018,
        'Kelpių': 5018,
        'J. Kamarausko-Gegliškių': 5019,
        'J. Kamarausko': 5019,
        'Gegliškių-Kelmiškių': 5020,
        'Gegliškių': 5020,
        'Didžioji Riešė-Kooperatyvo': 5101,
        'Kooperatyvo-Beržų': 5102,
        'Kooperatyvo-Alyvų': 5102,
        'Riešės gimnazija-Ežero': 5103,
        'Riešės gimnazija-Beržų': 5104,
        'Vanaginė-Vanaginės žiedas': 5106,
        'Vanaginė-Prašiškės': 5107,
        'Raisteliai-Baltoji Vokė': 5108,
        'Raisteliai-Panerių miškas': 5109,
        'Raisteliai-Raistelių miškas': 5109,
        'Baltoji Vokė-Raisteliai': 5110,
        'Baltoji Vokė-Krantinės': 5111,
        'Baltoji Vokė-Durpių': 5111,
        'Žemieji Pagiriai-Pagiriai': 5112,
        'Žemieji Pagiriai-1-ieji Pagiriai': 5113,
        'Žemieji Pagiriai-Pirmieji Pagiriai': 5113,
        'Pagiriai-Žemieji Pagiriai': 5114,
        'Pagiriai-Vaidotų piliakalnis': 5114,
        'Pagiriai': 5114,
        'Skersinės-Geležinio Vilko': 5115,
        'Skersinės-Santaros': 5115,
        'Skersinės-Vaikų ligoninė': 5115,
        'Skersinės-Prašiškės': 5116,
        'Ąžuolijai-Panerių miškas': 5117,
        'Margirio-Baltoji Vokė': 5118,
        'Margirio-Raisteliai': 5118,
        'Gulbinai-Riešė': 5119,
        'Gulbinai-Vanaginė': 5120,
        'Alyvų-Kalinas': 5121,
        'Alyvų-Didžioji Riešė': 5122,
        'Margirio-Agrastų': 5123,
        'Agrastų-Margirio': 5124,
        'Agrastų-Kadugių': 5124,
        'Agrastų': 5124,
        'Kiparisų-Vanaginės žiedas': 5125,
        'Kiparisų-Samanų': 5126,
        'Samanų-Kiparisų': 5127,
        'Samanų-Lauko': 5128,
        'Lauko-Samanų': 5129,
        'Lauko-Kaštonų': 5130,
        'Kaštonų-Lauko': 5131,
        'Kaštonų-Kooperatyvo': 5132,
        'Pirmieji Pagiriai-Žemieji Pagiriai': 5133,
        '1-ieji Pagiriai-Žemieji Pagiriai': 5133,
        'Pirmieji Pagiriai-Durpių': 5134,
        '1-ieji Pagiriai-Durpių': 5134,
        'Beržų-Didžioji Riešė': 5135,
        'Kelmijos sodai-Raistelių miškas': 5136,
        'Kelmijos sodai-Salininkai': 5137,
        'Durpių-Baltoji Vokė': 5138,
        'Durpių-Pirmieji Pagiriai': 5139,
        'Durpių-1-ieji Pagiriai': 5139,
        'Riešė-Raudondvaris': 5141,
        'Rugių-Ateities': 5142,
        'Rugių-Kalvarijos': 5143,
        'Karveliškių kapinės-Vaivadiškės': 5144,
        'Karveliškės-Vaivadiškės': 5144,
        'Karveliškių kapinės': 5144,
        'Karveliškės': 5144,
        'Raistelių miškas-Raisteliai': 5145,
        'Raistelių miškas-Vokės parkas': 5145,
        'Raistelių miškas-Kelmijos sodai': 5146,
        'Žalgirio išlaipinimas': 5147,
        'Kalinas-Didieji Gulbinai': 5148,
        'Didieji Gulbinai-Kalinas': 5149,
        'Kalinas-Alyvų': 5150,
        'Žvėryno žiedas-T. Narbuto': 5151,
        'Žvėryno žiedas-Sėlių': 5151,
        'Žvėryno žiedas': 5151,
        'Bazilijonų-Aušros vartai': 5153,
        'B': 5153,
        'Lazdynų ligoninė-Oslo': 5158,
        'Lazdynų ligoninė': 5158,
        'Kaimelio-A. Jonyno': 5159,
        'Grigaičiai-Karklėnai': 5160,
        'GK': 5160,
        'Jaunimo-Grigaičių žiedas': 5161,
        'Jaunimo-Karklėnai': 5162,
        'Grigaičių žiedas-Jaunimo': 5163,
        'Piliakalnio-Pilaitė': 5164,
        'Piliakalnio-V. Pociūno': 5164,
        'Piliakalnio-Sietyno': 5165,
        'Sietyno-Spaudos rūmai': 5166,
        'Sietyno-Piliakalnio': 5167,
        'Sietyno-Laisvės prospektas': 5176,
        'Autobusų parkas-Verkių': 5177,
        'Kuprioniškės-Minsko plentas': 5178,
        'Kuprioniškės': 5178,
        'Girinaičių-Karačiūnai': 5179,
        'Girinaičių-Miškas': 5180,
        'Trimitų-Herkaus Manto': 5181,
        'Žvejų-Rinktinės': 5182,
        'Žvejų-Lvivo': 5182,
        'Žvejų-Lvovo': 5182,
        'Žvejų-Arkikatedra': 5183,
        'Žvejų-Karaliaus Mindaugo tiltas': 5183,
        'Rinktinės-Herkaus Manto': 5184,
        'Herkaus Manto-Žygio': 5185,
        'Herkaus Manto-Rinktinės': 5186,
        'Žygio-Ulonų': 5187,
        'Žygio-Tauragnų': 5187,
        'Žygio': 5187,
        'Rinktinės-Žvejų': 5188,
        'Erfurto-Oslo': 5189,
        'Erfurto-Vandenvala': 5189,
        'Sietyno-T. Narbuto': 5190,
        'Prašiškės-Skersinės': 5191,
        'Beržų-Riešės gimnazija': 5192,
        'Erfurto-Akacijų': 5193,
        'Karklėnai-Jaunimo': 5194,
        'Karklėnai-Grigaičiai': 5195,
        'KG': 5195,
        'Giraitės-Vilkpėdės': 5196,
        'Giraitės-Vingio parkas': 5197,
        'Prašiškės-Vanaginė': 5198,
        'Panerių miškas-Raisteliai': 5199,
        'Panerių miškas-Ąžuolijai': 5200,
        'Kooperatyvo-Kaštonų': 5201,
        'Kooperatyvo-Didžioji Riešė': 5202,
        'Vanaginės žiedas-Vanaginė': 5206,
        'Vanaginės žiedas-Kiparisų': 5206,
        'Vanaginės žiedas': 5206,
        'Mažoji Riešė-Ežero': 5207,
        'Mažoji Riešė-Bendoriai': 5208,
        'Bendoriai-Mažoji Riešė': 5209,
        'Bendoriai-Bendorėliai': 5210,
        'Bendorėliai-Bendoriai': 5211,
        'Bendorėliai-Klevinė': 5212,
        'Klevinė-Bendorėliai': 5213,
        'Klevinė-Durpynas': 5214,
        'Durpynas-Klevinė': 5215,
        'Durpynas-2-osios Bukiškės': 5216,
        'Durpynas-Antrosios Bukiškės': 5216,
        'Ežero-Mažoji Riešė': 5217,
        'Ežero-Riešės gimnazija': 5218,
        '9-asis kilometras-Šumsko kryptis': 5219,
        'Devintasis kilometras-Šumsko kryptis': 5219,
        '9-asis kilometras-Slėnis': 5221,
        'Devintasis kilometras-Slėnis': 5221,
        'Slėnis-9-asis kilometras': 5223,
        'Slėnis-Devintasis kilometras': 5223,
        'Slėnis-Grigaičių žiedas': 5224,
        'Naujosios Vilnios sankryža-Slėnis': 5225,
        '2-asis Didžiasalis-Grigaičių žiedas': 5226,
        'Antrasis Didžiasalis-Grigaičių žiedas': 5226,
        'Grigaičių žiedas-Naujosios Vilnios sankryža': 5227,
        '2-asis Didžiasalis-1-asis Didžiasalis': 5228,
        'Antrasis Didžiasalis-Pirmasis Didžiasalis': 5228,
        'Naujosios Vilnios sankryža-2-asis Didžiasalis': 5230,
        'Naujosios Vilnios sankryža-Antrasis Didžiasalis': 5230,
        '1-asis Didžiasalis-Stankutiškės': 5231,
        'Pirmasis Didžiasalis-Stankutiškės': 5231,
        '1-asis Didžiasalis-2-asis Didžiasalis': 5232,
        'Pirmasis Didžiasalis-Antrasis Didžiasalis': 5232,
        'Juodšiliai-Valčiūnai': 5300,
        'Juodšiliai-Šiaudinė': 5300,
        'Juodšiliai-Avinėlių': 5301,
        'Juodšiliai-Kalviškės': 5301,
        'Juodšiliai-1-ieji Juodšiliai': 5301,
        'Juodšiliai-Pirmieji Juodšiliai': 5301,
        'Valčiūnai-Valčiūnai II': 5302,
        'Valčiūnai-Terešiškės': 5302,
        'Valčiūnai-Šiaudinė': 5303,
        'Valčiūnai-Juodšiliai': 5303,
        'Terešiškės': 5304,
        'Jašiūnai': 5305,
        'Trakų autobusų stotis': 6000,
        'Kaimelis-Račkūnai': 6001,
        'Kaimelis-Trakų autobusų stotis': 6002,
        'Račkūnai-Lentvario kryžkelė': 6003,
        'Račkūnai-Kaimelis': 6004,
        'Lentvario kryžkelė-Dobūklė': 6005,
        'Lentvario kryžkelė-Račkūnai': 6006,
        'Dobūklė-Trakų Vokė': 6007,
        'Dobūklė-Lentvario kryžkelė': 6008,
        'Liudvinavos laikina-Mūrinė Vokė': 6009,
        'Liudvinavos laikina-Ižos laikina': 6010,
        'Ižos laikina-Liudvinavos laikina': 6011,
        'Ižos laikina-Žarijų laikina': 6012,
        'Žarijų laikina-Ižos laikina': 6013,
        'Žarijų laikina-Žarijų': 6014
        }
    
    # Dėl techninių priežasčių stotelių kodai su 'a' ir 'b' bei dviprasmybės (ta pati jungtis, kelios stotelės) pateikiami apačioje

    # Iškilus dviprasmybėms bus papildomai paprašoma pasirinkti

    if st=='Žaliasis tiltas laikina' or st=='ŽTL':
        stop='0101b'
    elif st=='Akreditacijos biuras':
        stop='0237a'
    elif st=='Medijų centras':
        stop='0237b'
    elif st=='Prezidentūra':
        stop='0242a'
    elif st=='Vokiečių-Rotušė' or st=='Vokiečių':
        stop='0245a'
    elif st=='Vokiečių-Reformatų':
        stop='0245b'
    elif st=='Šv. Petro ir Povilo bažnyčia laikina' or st=='Petro ir Povilo bažnyčia laikina':
        print('Šeimyniškių ar L. Sapiegos?')
        st=str(input())
        if st=='L. Sapiegos' or st=='Šv. Petro ir Povilo bažynčia laikina-L. Sapiegos':
            stop='0401a'
            st='Šv. Petro ir Povilo bažynčia laikina-L. Sapiegos'
        if st=='Šeimyniškių' or st=='Šv. Petro ir Povilo bažynčia laikina-Šeimyniškių':
            stop='0402a'
            st='Šv. Petro ir Povilo bažynčia laikina-Šeimyniškių'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Šv. Petro ir Povilo bažynčia laikina-L. Sapiegos' or st=='Petro ir Povilo bažynčia laikina-L. Sapiegos':
        stop='0401a'
    elif st=='Šv. Petro ir Povilo bažynčia laikina-Šeimyniškių' or st=='Petro ir Povilo bažynčia laikina-Šeimyniškių':
        stop='0402a'
    elif st=='Kalnų parkas laikina' or st=='Kalnų parkas-Karaliaus Mindaugo tiltas':
        stop='0403a'
    elif st=='Gervėčių-Aušros vartai':
        print('31 ar 89?')
        st=str(input())
        if st=='31' or st=='Gervėčių-Aušros vartai 31':
            stop='0419'
            st='Gervėčių-Aušros vartai 31'
        if st=='89' or st=='Gervėčių-Aušros vartai 89':
            stop='0444'
            st='Gervėčių-Aušros vartai 89'
        else:
            print('BLOGAI ĮVESTA')
    if st=='Rotušė-Gėlių' or st=='Rotušė-Rūdninkų':
        stop='0449a'
    elif st=='Laikina-Naujamiestis':
        stop='0519a'
    elif st=='Vienaragių-Naujininkai' or st=='Vienaragių-Prūsų':
        stop='0522a'
    elif st=='Burbiškės panaikinta':
        stop='0527a'
    elif st=='Stotis':
        print('Kokia raidė?')
        st=str(input())
        if st=='A' or st=='Stotis A':
            stop='0530a'
            st='Stotis A'
        elif st=='B' or st=='Stotis B':
            stop='0530b'
            st='Stotis B'
        elif st=='C' or st=='Stotis C':
            stop='0530c'
            st='Stotis C'
        elif st=='D' or st=='Stotis D':
            stop='0530d'
            st='Stotis D'
        elif st=='E' or st=='Stotis E':
            stop='0530e'
            st='Stotis E'
        elif st=='F' or st=='Stotis F':
            stop='0530f'
            st='Stotis F'
        elif st=='G' or st=='Stotis G':
            stop='0530g'
            st='Stotis G'
        elif st=='H' or st=='Stotis H':
            stop='0530h'
            st='Stotis H'
        elif st=='I' or st=='Stotis I':
            stop='0530i'
            st='Stotis I'
        elif st=='J' or st=='Stotis J':
            stop='0530j'
            st='Stotis J'
        elif st=='P' or st=='Stotis P':
            stop='0530p'
            st='Stotis P'
        elif st=='S' or st=='Stotis S':
            stop='0547'
            st='Stotis S'
        elif st=='W' or st=='Stotis W':
            stop='0547w'
            st='Stotis W'
        elif st=='X' or st=='Stotis X':
            stop='0546'
            st='Stotis X'
        elif st=='Z' or st=='Stotis Z':
            stop='0530z'
            st='Stotis Z'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Stotis-Rūdninkų':
        print('Troleibusai, Autobusai ar 89?')
        st=str(input())
        if st=='Troleibusai' or st=='troleibusai' or st=='Stotis A':
            stop='0530a'
            st='Stotis A'
        if st=='89' or st=='Stotis E':
            stop='0530e'
            st='Stotis E'
        if st=='Autobusai' or st=='autobusai' or st=='Stotis J':
            stop='0530j'
            st='Stotis J'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Stotis-Pelesos':
        print('B, C, G, ar I?')
        st=str(input())
        if st=='B' or st=='Stotis B':
            stop='0530b'
            st='Stotis B'
        if st=='C' or st=='Stotis C':
            stop='0530c'
            st='Stotis C'
        if st=='G' or st=='Stotis G':
            stop='0530g'
            st='Stotis G'
        if st=='I' or st=='Stotis I':
            stop='0530i'
            st='Stotis I'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Stotis-Aguonų':
        print('D, F, H, ar I?')
        st=str(input())
        if st=='D' or st=='Stotis D':
            stop='0530d'
            st='Stotis D'
        if st=='F' or st=='Stotis F':
            stop='0530f'
            st='Stotis F'
        if st=='H' or st=='Stotis H':
            stop='0530h'
            st='Stotis H'
        if st=='I':
            stop='0530i'
            st='Stotis I'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Stotis-Bazilijonų':
        stop='0530e'
        st='Stotis E'
    elif st=='Stotis A':
        stop='0530a'
    elif st=='Stotis B':
        stop='0530b'
    elif st=='Stotis C':
        stop='0530c'
    elif st=='Stotis D':
        stop='0530d'
    elif st=='Stotis E':
        stop='0530e'
    elif st=='Stotis F':
        stop='0530f'
    elif st=='Stotis G':
        stop='0530g'
    elif st=='Stotis H':
        stop='0530h'
    elif st=='Stotis I':
        stop='0530i'
    elif st=='Stotis J':
        stop='0530j'
    elif st=='Stotis P':
        stop='0530p'
    elif st=='Stotis l':
        stop='0530z'
    elif st=='Stotis W':
        stop='0547w'
    elif st=='Savanorių prospektas-Vingis' or st=='Savanorių prospektas-Žemaitės' or st=='Savanorių prospektas-Naujamiestis':
        stop='0602a'
    elif st=='Paėmimo':
        stop='0609a'
    elif st=='Išleidimo':
        stop='0609b'
    elif st=='Pramogų arena-Tauragnų':
        print('Autobusai ar Troleibusai?')
        st=str(input())
        if st=='Autobusai' or st=='autobusai' or st=='Pramogų arena-Tauragnų autobusai':
            stop='0709'
            st='Pramogų arena-Tauragnų autobusai'
        if st=='Troleibusai' or st=='troleibusai' or st=='Pramogų arena-Tauragnų troleibusai':
            stop='0805'
            st='Pramogų arena-Tauragnų troleibusai'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Minties-Šilo tiltas':
        print('50 ar Kiti?')
        st=str(input())
        if st=='Kiti' or st=='kiti' or st=='Minties-Šilo tiltas':
            stop='0903'
            st='Minties-Šilo tiltas'
        if st=='50' or st=='Minties-Šilo tiltas 50':
            stop='0920'
            st='Minties-Šilo tiltas 50'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='B. Laurinavičiaus skveras laikina' or st=='Broniaus Laurinavičiaus skveras laikina' :
        stop='0914b'
    elif st=='Šiaurės miestelis-Povilo Lukšio':
        print('30 ir 33 ar Kiti?')
        st=str(input())
        if st=='Kiti' or st=='kiti' or st=='Šiaurės miestelis-Povilo Lukšio':
            stop='0922'
            st='Šiaurės miestelis-Povilo Lukšio'
        if st=='30' or st=='33' or st=='30 ir 33' or st=='Autobusai' or st=='autobusai' or st=='Šiaurės miestelis-Povilo Lukšio autobusai':
            stop='0925'
            st='Šiaurės miestelis-Povilo Lukšio autobusai'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Dvarčionys-Lazerių':
        print('Dvarčionių kryžkelė ar Baniškės?')
        st=str(input())
        if st=='Dvarčionių kryžkelė' or st=='Dvarčionys-Lazerių-Dvarčionių kryžkelė':
            stop='1011'
            st='Dvarčionys-Lazerių-Dvarčionių kryžkelė'
        if st=='Baniškės' or st=='Dvarčionys-Lazerių-Baniškės':
            stop='1026'
            st='Dvarčionys-Lazerių-Baniškės'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Klinikų-Tverečiaus':
        print('Žolyno ar Antakalnio gatvėje?')
        st=str(input())
        if st=='Antakalnio' or st=='Antakalnio gatvėje' or st=='Klinikų-Tverečiaus kiti':
            stop='1110'
            st='Klinikų-Tverečiaus kiti'
        if st=='Žolyno' or st=='Žolyno gatvėje' or st=='Klinikų-Tverečiaus autobusai':
            stop='1112'
            st='Klinikų-Tverečiaus autobusai'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Antakalnio žiedas-Antakalnis':
        print('Autobusai ar Troleibusai?')
        st=str(input())
        if st=='Troleibusai' or st=='troleibusai' or st=='Antakalnio žiedas-Antakalnis troleibusai':
            stop='1118'
            st='Antakalnio žiedas-Antakalnis troleibusai'
        if st=='Autobusai' or st=='autobusai' or st=='Antakalnio žiedas-Antakalnis autobusai':
            stop='1118a'
            st='Antakalnio žiedas-Antakalnis autobusai'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Antakalnio žiedas autobusai':
        stop='1118a'
    elif st=='Antakalnio žiedas-Antakalnis autobusai':
        stop='1118a'
    elif st=='Antakalnio žiedas-Nemenčinės plentas':
        stop='1118a'
    elif st=='Antakalnio žiedas-Lizdeikos':
        stop='1118c'
    elif st=='Šilo panaikinta':
        stop='1127a'
    elif st=='Pelesos-Stotis':
        print('58 ar Kiti?')
        st=str(input())
        if st=='58' or st=='Pelesos-Stotis 58':
            stop='1301'
            st='Pelesos-Stotis 58'
        if st=='Kiti' or st=='kiti' or st=='Pelesos-Stotis kiti':
            stop='1303'
            st='Pelesos-Stotis kiti'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Liepkalnis-Žirnių':
        print('58 ar Kiti?')
        st=str(input())
        if st=='Kiti' or st=='kiti' or st=='Pelesos-Stotis kiti':
            stop='1317'
            st='Pelesos-Stotis kiti'
        if st=='58' or st=='Pelesos-Stotis 58':
            stop='1514'
            st='Pelesos-Stotis 58'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Pavilnio laikinoji':
        stop='1435a'
    elif st=='Naujininkai-Prūsų':
        print('Troleibusai ar Autobusai?')
        st=str(input())
        if st=='Troleibusai' or st=='troleibusai' or st=='Naujininkai-Prūsų troleibusai':
            stop='1502'
            st='Naujininkai-Prūsų troleibusai'
        if st=='Autobusai' or st=='autobusai' or st=='Naujininkai-Prūsų autobusai':
            stop='1517'
            st='Naujininkai-Prūsų autobusai'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Musninkų-Paberžės':
        print('75 ar 87?')
        st=str(input())
        if st=='87' or st=='Musninkų-Paberžės 87':
            stop='1919'
            st='Musninkų-Paberžės 87'
        if st=='75' or st=='Musninkų-Paberžės 75':
            stop='1933'
            st='Musninkų-Paberžės 75'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Mildos-Šaudykla':
        print('37 ar Kiti?')
        st=str(input())
        if st=='Kiti' or st=='Mildos-Šaudykla kiti':
            stop='1216'
            st='Mildos-Šaudykla kiti'
        if st=='37' or st=='Mildos-Šaudykla 37':
            stop='2301'
            st='Mildos-Šaudykla 37'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Lazdynėliai panaikinta':
        stop='1652a'
    elif st=='Bajorai':
        stop='2105a'
    elif st=='Bajorų žiedas':
        stop='2105a'
    elif st=='Bajorai panaikinta':
        stop='2105a'
    elif st=='Chemijos institutas panaikinta':
        stop='2106a'
    elif st=='Žaliųjų Ežerų panaikinta':
        stop='2119a'
    elif st=='P. Baublio-Žaliųjų Ežerų' or st=='P. Baublio-Žaliųjų ežerų':
        stop='2125b'
    elif st=='P. Baublio panaikinta':
        stop='2127a'
    elif st=='Santariškių žiedas išlaipinimas':
        stop='2136a'
    elif st=='Geležinio Vilko panaikinta-Akademijos':
        stop='2145a'
    elif st=='Geležinio Vilko panaikinta-Skersinės':
        stop='2146a'
    elif st=='Daubų panaikinta':
        stop='2153a'
    elif st=='Bajorai-Šaulio':
        stop='2157a'
    elif st=='Baniškių-Ivaniškės':
        stop='2375a'
    elif st=='Baniškių-Užkiemio':
        stop='2375b'
    elif st=='A. Kojelavičiaus panaikinta':
        stop='2376a'
    elif st=='Polocko kryptis-Viktariškės':
        stop='2380regio'
    elif st=='Polocko kryptis-Verbų':
        stop='2381regio'
    elif st=='Viktariškės-Lyta':
        stop='2382regio'
    elif st=='Viktariškės-Polocko kryptis':
        stop='2383aregio'
    elif st=='Lyta-Mickūnai':
        stop='2384regio'
    elif st=='Lyta-Viktariškės':
        stop='2385regio'
    elif st=='Mickūnai' or st=='Mickūnai-Lyta':
        stop='2386regio'
    elif st=='Verbų-Polocko kryptis':
        stop='2387regio'
    elif st=='Verbų-Naujoji Vilnia':
        stop='2388regio'
    elif st=='Burbiškės-Eigulių':
        stop='2402a'
    elif st=='Burbiškės-Miškiniai':
        stop='2402a'
    elif st=='Burbiškės-Šiltnamių':
        stop='2402a'
    elif st=='Vaduvos-Skapiškio':
        stop='2414e'
    elif st=='Vaduvos-Jankiškių':
        stop='2414e'
    elif st=='Valkininkų-Ūmėdžių':
        print('24, Įlaipinimas ar Kiti?')
        st=str(input())
        if st=='24' or st=='Valkininkų-Ūmėdžių 24':
            stop='2417'
            st='Valkininkų-Ūmėdžių 24'
        if st=='Įlaipinimas' or st=='įlaipinimas' or st=='Valkininkų-Ūmėdžių įlaipinimas':
            stop='2418'
            st='Valkininkų-Ūmėdžių įlaipinimas'
        if st=='Kiti' or st=='kiti' or st=='Valkininkų-Ūmėdžių kiti':
            stop='2901'
            st='Valkininkų-Ūmėdžių kiti'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Eišiškių plentas-Naujininkai':
        print('Eišiškių ar Dariaus ir Girėno?')
        st=str(input())
        if st=='Eišiškių' or st=='Eišiškių plentas-Naujininkai kiti':
            stop='2602'
            st='Eišiškių plentas-Naujininkai kiti'
        if st=='Dariaus ir Girėno' or st=='Eišiškių plentas-Naujininkai greitieji':
            stop='2604'
            st='Eišiškių plentas-Naujininkai greitieji'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Oro uostas a':
        stop='a2613'
    elif st=='Oro uostas b':
        stop='a2613b'
    elif st=='Oro uostas išlaipinimas':
        stop='2613b'
    elif st=='Oro uostas c':
        stop='a2613c'
    elif st=='Oro uostas parkingas':
        stop='2613c'
    elif st=='Salininkai-Mechanikų':
        print('3 ar Kiti?')
        st=str(input())
        if st=='Kiti' or st=='kiti' or st=='Salininkai-Mechanikų kiti':
            stop='2711'
            st='Salininkai-Mechanikų kiti'
        if st=='3' or st=='Salininkai-Mechanikų 3':
            stop='2731'
            st='Salininkai-Mechanikų 3'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Fermentų-Galvės' or st=='Fermentų-Deguonies':
        stop='2802a'
    elif st=='Chemijos-Fermentų':
        stop='2810a'
    elif st=='Aukštieji Paneriai-Vilijos':
        print('Galvės ar Lentvario?')
        st=str(input())
        if st=='Lentvario' or st=='Aukštieji Paneriai-Vilijos-Lentvario':
            stop='2906'
            st='Aukštieji Paneriai-Vilijos-Lentvario'
        if st=='Galvės' or st=='Aukštieji Paneriai-Vilijos-Galvės':
            stop='2945'
            st='Aukštieji Paneriai-Vilijos-Galvės'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Dobrovolės išlaipinimas':
        stop='2941a'
    elif st=='Dobrovolės':
        stop='2941b'
    elif st=='Lentvaris-Lentvaris':
        print('Dzūkų ar Vilniaus?')
        st=str(input())
        if st=='Dzūkų' or st=='Lentvaris-Lentvaris žiedas':
            stop='3006'
            st='Lentvaris-Lentvaris žiedas'
        if st=='Vilniaus' or st=='Lentvaris-Lentvaris':
            stop=''
            st='Lentvaris-Lentvaris'
        else:
            print('BLOGAI ĮVESTA')
    elif st=='Bratoniškės-Skirgiškės':
        stop='3008regio'
    elif st=='Bratoniškės-SB Pavasaris':
        stop='3009regio'
    elif st=='Skalvių panaikinta':
        stop='3305a'
    elif st=='Pavilnionių panaikinta':
        stop='3306a'
    elif st=='Meškeriotojų panaikinta':
        stop='3509a'
    elif st=='Veržuvos laikina':
        stop='3539a'
    elif st=='Šilas-Karačiūnai laikina' or st=='Šilas-Girinaičių laikina':
        stop='3542a'
    elif st=='Šilas-J. Biliūno laikina':
        stop='3543a'
    elif st=='Pagal pareikalavimą' or st=='Pagal pareikalavimą-Kalnėnai':
        stop='4022a'
    elif st=='Nemėžis-Laikina':
        stop='4305a'
    elif st=='Laikina' or st=='Laikina-V. Sirokomlės':
        stop='4305b'
    elif st=='V. Sirokomlės-Baltarusių':
        stop='4305c'
    elif st=='Rudaminos laikina-Draugystės':
        stop='4319a'
    elif st=='Rudaminos laikina-Čekėnų':
        stop='4320a'
    elif st=='Rudaminos laikina-Rudaminos žiedas':
        stop='4320b'
    elif st=='Rudaminos laikina-Rudamina' or st=='Rudaminos laikina':
        stop='4320c'
    elif st=='Rudaminos kapinės išlaipinimas':
        stop='4333a'
    elif st=='Rudaminos kapinės-Rudaminos mokykla':
        stop='4333b'
    elif st=='Tarandė-Kelpių' or st=='Tarandė laikina':
        stop='5007a'
    elif st=='Kelpių-T. Žebrausko' or st=='Kelpių-Tarandė' or st=='Kelpių laikina':
        stop='5018a'
    elif st=='J. Kamarausko-Kelpių' or st=='J. Kamarausko laikina':
        stop='5019a'
    elif st=='Baltoji Vokė panaikinta-Durpių':
        stop='5110a'
    elif st=='Baltoji Vokė panaikinta-Pagirių' or st=='Baltoji Vokė panaikinta-Juodšilių' or st=='Baltoji Vokė panaikinta-Raisteliai':
        stop='5111a'
    elif st=='Karveliškių kapinės išlaipinimas':
        stop='5144a'
    elif st=='Rinktinės panaikinta':
        stop='5188a'

    # Galimybė įvesti stotelės kodą rankiniu būdu

    elif st=='input': 
        stop=str(input())
        st=stop

    else:
        stop=str(dict.get(st)).zfill(4)

    # Transporto duomenų rinkimas - 1 dalis
    # Iš išvykimų puslapio

    base="https://www.stops.lt/vilnius/departures2.php?stopid="
    if st=='Žaliasis tiltas laikina' or st=='ŽTL':
        url="https://www.stops.lt/vilnius/departures2.php?stopid=0101b"
        # Ši nesąmonė yra pataisymas nežinia iš ko kylančios problemos
    else:
        url=base+stop
    
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    text=soup.get_text()
    t=text.splitlines()
    try:
        t.pop(0)
    except IndexError:
        print('NEEGZISTUOJANTI STOTELĖ')

    # Duomenų rūšiavimas

    rusis=[]
    marsrutas=[]
    laikas=[]
    nrblokas=[] 
    nr=[]
    kiti=[]
    kryptis=[]
    modelis=[]
    variantas=[]
    for i in range(len(t)):
        try:
            a,b,c,d,e,f,g,h=t[i].split(',')
            rusis.append(a)
            marsrutas.append(b)
            variantas.append(c)
            laikas.append(d)
            nrblokas.append(e)
            kryptis.append(f)
        except ValueError:
            pass

    # Atskiriamas garažinis numeris ir transporto priemonės savybės (pvz. žemagrindis) - DAŽNAI NURODYTOS KLAIDINGAI!

    for i in range(len(nrblokas)):
        nr.append(re.findall(r'[0-9]+',nrblokas[i])[0])
        try:
            kiti.append(re.findall(r'[D-U|W-l]+',nrblokas[i])[0])
        except IndexError:
            kiti.append('')

    # Rankiniu būdu tikrinamas autobuso modelis pagal garažinį numerį
    
    # Naujai paleidžiant transporto priemones modelis iš anksto nebūna įvestas (išskyrus atvejus, kai jau žinoma, kokius garažiniai numeriai bus paskirti, pvz. SOR troleibusai)

    # Gali pasitaikyti netikri techniniai autobusai su tariamu garažiniu numeriu 'TEST T02', jų garažinis išeitų 02, juos vertėtų ignoruoti

    for i in range(len(nr)):
        if int(nr[i])>=555 and int(nr[i])<=586:
            mod='Altas Novus Cityline'
        elif int(nr[i])>=700 and int(nr[i])<=709:
            mod='Volvo 7700A'
        elif int(nr[i])<=729:
            mod='Volvo 7700'
        elif int(nr[i])>=740 and int(nr[i])<=749:
            mod='Volvo 7700A'
        elif int(nr[i])<=769:
            mod='Volvo 7700'
        elif int(nr[i])<=779:
            mod='Volvo 7700A'
        elif int(nr[i])<=799:
            mod='Volvo 7700'
        elif int(nr[i])>=923 and int(nr[i])<=929:
            mod='Peugeot Boxer'
        elif int(nr[i])<=931:
            mod='Citroen Jumper'
        elif int(nr[i])<=949:
            mod='MAN A21 Lions City NL273 CNG'
        elif int(nr[i])<=968:
            mod='Solaris Urbino III 12 CNG'
        elif int(nr[i])==969:
            mod='Castrosua Tempus Hybrid'
        elif int(nr[i])<=989:
            mod='Castrosua City Versus CNG'
        elif int(nr[i])<=999:
            mod='Neoplan Centroliner N4421'
        elif int(nr[i])>=1101 and int(nr[i])<=1136:
            mod='Škoda 14Tr'
        elif int(nr[i])<=1399:
            mod='Škoda 9Tr'
        elif int(nr[i])<=1599:
            mod='Škoda 14Tr'
        elif int(nr[i])<=1604:
            mod='Škoda 15Tr'
        elif int(nr[i])<=1649:
            mod='Škoda 14Tr'
        elif int(nr[i])>=1651 and int(nr[i])<=1673:
            mod='Škoda 14TrM'
        elif int(nr[i])<=1718:
            mod='Solaris Trollino II 15 AC'
        elif int(nr[i])<=1720:
            mod='MAZ-ETON T203 Amber'
        elif int(nr[i])<=1761:
            mod='Solaris Trollino IV 12'
        elif int(nr[i])>=1770 and int(nr[i])<=1860:
            mod='Škoda 32Tr SOR'
        elif int(nr[i])>=2101 and int(nr[i])<=2136:
            mod='Škoda 14Tr'
        elif int(nr[i])<=2399:
            mod='Škoda 9Tr'
        elif int(nr[i])<=2599:
            mod='Škoda 14Tr'
        elif int(nr[i])<=2604:
            mod='Škoda 15Tr'
        elif int(nr[i])<=2649:
            mod='Škoda 14Tr'
        elif int(nr[i])>=2651 and int(nr[i])<=2673:
            mod='Škoda 14TrM'
        elif int(nr[i])<=2718:
            mod='Solaris Trollino II 15 AC'
        elif int(nr[i])<=2720:
            mod='MAZ-ETON T203 Amber'
        elif int(nr[i])<=2761:
            mod='Solaris Trollino IV 12'
        elif int(nr[i])>=2770 and int(nr[i])<=2860:
            mod='Škoda 32Tr SOR'
        elif int(nr[i])>=3006 and int(nr[i])<=3009:
            mod='MAN A23 NG313'
        elif int(nr[i])>=3015 and int(nr[i])<=3020:
            mod='MAN A23 Lions City GL NG313'
        elif int(nr[i])>=3030 and int(nr[i])<=3039:
            mod='MAN A21 Lions City NL273'
        elif int(nr[i])>=3101 and int(nr[i])<=3125:
            mod='Solaris Urbino IV 12'
        elif int(nr[i])>=4007 and int(nr[i])<=4012:
            mod='MAN A23 NG313'
        elif int(nr[i])>=4018 and int(nr[i])<=4026:
            mod='MAN A23 Lions City GL NG313'
        elif int(nr[i])>=4030 and int(nr[i])<=4034:
            mod='MAN A21 Lions City NL273'
        elif int(nr[i])>=4101 and int(nr[i])<=4138:
            mod='Solaris Urbino IV 12'
        elif int(nr[i])<=4175:
            mod='Solaris Urbino IV 18'
        elif int(nr[i])<=4198:
            mod='MAN A23 Lions City G NG313 CNG'
        elif int(nr[i])>=4501 and int(nr[i])<=4537:
            mod='Solaris Urbino IV 12'
        elif int(nr[i])>=4541 and int(nr[i])<=4550:
            mod='Anadolu Isuzu Novociti Life'
        elif int(nr[i])<=4575:
            mod='Solaris Urbino IV 18'
        elif int(nr[i])<=4602:
            mod='MAN A23 Lions City G NG313 CNG'
        elif int(nr[i])>=4611 and int(nr[i])<=4615:
            mod='Karsan Jest Electric'
        elif int(nr[i])>=4637 and int(nr[i])<=4661:
            mod='MAN A23 Lions City G NG273 LPG'
        elif int(nr[i])>=7001 and int(nr[i])<=7072:
            mod='Anadolu Isuzu Citibus'
        elif int(nr[i])==7073:
            mod='Anadolu Isuzu Citiport 12'
        elif int(nr[i])==7074:
            mod='Anadolu Isuzu Citibus'
        elif int(nr[i])<=7080:
            mod='MAN A21 Lions City NL313 CNG'
        elif int(nr[i])>=8001 and int(nr[i])<=8050:
            mod='Scania Citywide LFA'
        else:
            mod='NEĮVESTAS MODELIS'
        modelis.append(mod)

    # Transporto duomenų rinkimas - 2 dalis
    # iš GPS puslapio

    # Paimami dabartiniai kiekvienos transporto priemonės vėlavimo laikai

    # Laikai pastoviai kaitaliojasi, gali neatitikti realybės arba planuojamo išvykimo vėlavimo
    # Šie duomenys atitinka dabartinę vėlavimo būseną, ne skirtumą tarp planuojamo ir numatomo faktinio išvykimo
  
    url="https://www.stops.lt/vilnius/gps_full.txt"
    response=requests.get(url)
    soup=BeautifulSoup(response.content,'html.parser')
    text=soup.get_text()
    t=text.splitlines()
    t.pop(0)
    nr2=[]
    velavimas=[]
    velavimas2=[]
    pliusminus=[]

    for i in range(len(nr)):
        velavimas2.append(0)
        pliusminus.append(0)

    for i in range(len(t)):
        a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p=t[i].split(',')
        nr2.append(d)
        velavimas.append(j)

    for i in range(len(nr)):
        for j in range(len(nr2)):
            if nr[i]==nr2[j]:
                try:
                    velavimas2[i]=velavimas[j]
                    if int(velavimas2[i])<0:
                        velavimas2[i]=str(abs(int(velavimas2[i])))
                        pliusminus[i]='-'
                    elif int(velavimas2[i])>0:
                        pliusminus[i]='+'
                    else:
                        pliusminus[i]=' '
                    velavimas2[i]=datetime.datetime.fromtimestamp(int(velavimas2[i])).strftime("%M:%S")
                except IndexError:
                    # Kai transporto priemonė vykdo atstovą, vėlavimas gali būti nerodomas
                    pass


    for i in range(len(velavimas2)):
        if velavimas2[i]==0:
            velavimas2[i]='     '
            pliusminus[i]=' '
        
    # Spausdinamas dabartinis laikas orientavimuisi

    print('Laikas',datetime.datetime.now().strftime("%H:%M:%S")) 

    # Spausdinami transporto priemonių išvykimo laikai (valanda į priekį)

    for i in range(len(rusis)):
        # Apskaičiojamas numatomo išvykimo laikas

        # Skaičius '3' dalyje 'int(laikas[i])-3*3600' perstumia laiką valandomis, jį gali reikėti kaitalioti į '2' ar pan. dėl stops nemokėjimo dorotis su laiko juostomis
        
        l=datetime.datetime.fromtimestamp(int(laikas[i])-3*3600).strftime("%H:%M:%S")

        # Išskiriami tam tikri variantiniai maršrutų reisai pridedant 'A' raidę (kaip seniau įprastai žymėti iki 2013 m.)
        # Išskiriami tie variantiniai reisai, kuriais kursuojantys autobusai beveik nepereidinėja iš įprastų reisų

        if marsrutas[i]=='9' and (variantas[i]=='a1-b1' or variantas[i]=='b1-a1' or variantas[i]=='d-b' or variantas[i]=='b2-d'):
            marsrutas[i]='9A'
        if marsrutas[i]=='33' and (variantas[i]=='a1-b1' or variantas[i]=='b1-a1'):
            marsrutas[i]='33A'

        # Išvykimo laikai spausdinami su nustatytais tarpais siekiant padorios lygiuotės 

        if rusis[i]=='bus' or rusis[i]=='expressbus' or rusis[i]=='nightbus':
            print(f'{l:<10} {pliusminus[i]:<1}{velavimas2[i]:<7} {marsrutas[i].upper():<4}{kryptis[i]:<30} {modelis[i]:<32} {nr[i]:<4} {kiti[i]}')
        elif rusis[i]=='trol':
            print(f'{l:<10} {pliusminus[i]:<1}{velavimas2[i]:<7} T{marsrutas[i]:<3}{kryptis[i]:<30} {modelis[i]:<32} {nr[i]:<4} {kiti[i]}')

    # Laikai naujinami kas 10 sekundžių
    
    time.sleep(45)
    print(st)
