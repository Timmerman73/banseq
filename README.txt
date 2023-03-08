BANSEQ deelopdracht 1 - Tim van der Lee & Lindsey Tichelaar (1126607 & 1130444)

READ ME

Om het programma correct te gebruiken moeten de volgende stappen gevolgd worden:

Voorbereiding
- Zorg dat het bestand 'main.py', 'kimura2.txt' en 'blosum62.txt' in hetzelfde mapje staan.
- Zorg dat 'wxPython' geïnstalleerd is op de computer.


Werking programma
- In de sequentie invoervelden kunnen maximaal 25 tekens worden ingevoerd.

- Er is een radiobox met de opties 'DNA' en 'eiwit'.
	- Als 'DNA' is geselecteerd, kunnen alleen mogelijke DNA basen worden ingevoerd.
	- Als 'eiwit' is geselecteerd, kunnen alleen mogelijke eiwitten worden ingevoerd.
	- Het programma filtert niet-toegestane tekens eruit (afhankelijk van welke optie geselecteerd is).

- Er is een radiobox met de opties 'globaal' of 'lokaal'.
	- Bij 'globaal' laat de matrix ook negatieve getallen zien.
	- Bij 'lokaal' laat de matrix '0' zien waar een negatief getal hoort te staan
	  (in de berekening is dit aangegeven met 'Local Cutoff').

- Om meer informatie te zien over de waardes in de matrix, hover met de muis over de waarde.
	- Dan toont het programma de andere waardes en richting (diagonaal / horizontaal / verticaal).

- Voer twee sequenties in en druk op de 'start' knop om de matrix te creëeren.
