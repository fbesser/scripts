#!/usr/bin/env python

# Copyright (c) 2018 Florian Besser

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import urllib3
import csv
import time
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


felder = ["lblKitaname",
          "lblTraegerName",
          "lblTraegerart",
          "lblStrasse",
          "lblOrt",
          "lblTelefon",
          "HLinkEMail",
          "lblPaedSchwerpunkte",
          "lblPaedAnsaetze",
          "lblMehrsprachigkeit",
          "lblThemSchwerpunkte"]
# Plaetze GridViewPlatzstrukturen
# <div>
# 		<table class="seninn c1" rules="all" id="GridViewPlatzstrukturen" style="width:100%;border-collapse:collapse;" cellspacing="0" border="1">
# 			<tbody><tr align="left">
# 				<th scope="col">angeboten</th><th scope="col">unter 3 Jahre</th><th scope="col">über 3 Jahre</th><th scope="col">frühestes Aufnahmealter in Monaten</th><th scope="col">Altersmischung</th>
# 			</tr><tr class="odd">
# 				<td>43</td><td>20</td><td>23</td><td>12</td><td>&nbsp;</td>
# 			</tr>
# 		</tbody></table>
# 	</div>
# maxplatz unter3 ueber3 falter mischung

kita_baseurl = "https://www.berlin.de/sen/jugend/familie-und-kinder/kindertagesbetreuung/kitas/verzeichnis/"
kitaverz = "https://www.berlin.de/sen/jugend/familie-und-kinder/kindertagesbetreuung/kitas/verzeichnis/ListeKitas.aspx?Sort=Ortsteil"


def make_soup(url):
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    return BeautifulSoup(r.data, 'html.parser')


def check_ingredient(soup, ingredient):
    try:
        feld = soup.find(id=ingredient).text
    except:
        feld = " "
    
    return feld


def main():
    verzeichnis = make_soup(kitaverz)

    kitalinks = verzeichnis.find_all(id=re.compile("^DataList_Kitas_HLinkKitaName_"))

    outputFile = open('output.csv', 'w', newline='')
    outputWriter = csv.writer(outputFile)
    outputWriter.writerow(["Name", "Traeger", "traegerart", "Strasse", "Ort",
                           "Telefon", "EMail", "P. Schwerpunkte", "P. Ansatz",
                           "Thematischer Schwerpunkt", "Sprache"])
    # 2 Links aus dem Verzeichnis zum testen
    #kitalinks = ["https://www.berlin.de/sen/jugend/familie-und-kinder/kindertagesbetreuung/kitas/verzeichnis/KitaDetailsNeu.aspx?ID=%20493229", "https://www.berlin.de/sen/jugend/familie-und-kinder/kindertagesbetreuung/kitas/verzeichnis/KitaDetailsNeu.aspx?ID=%20472129"]
    
    for link in kitalinks:
        url = kita_baseurl + link.get('href').replace(' ','%20')
        
        # Test abruf der zwei links
        kita = make_soup(url)
        
        outputWriter.writerow(list(
            map(lambda x: check_ingredient(kita, x), felder)))
        print(url)
        time.sleep(2)

    outputFile.close()


if __name__ == '__main__':
    main()
