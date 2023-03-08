import wx

global class_matrix, GAP_PENALTY, LOCAL_ENABLED, FIRST_RUN
class_matrix = []
GAP_PENALTY = -5
LOCAL_ENABLED = False
FIRST_RUN = True


def read_file(filename):
    """
    Leest een matrix_bestand in. Vervangt ook alle dubbele spaties door
    enkele spaties zodat erop gesplit kan worden.
    :param filename: De bestandsnaam
    :return: file content
    """
    file = open(filename, "r")
    content = file.read()
    content = content.replace("  ", " ")
    file.close()
    return content


def process_matrix(content):
    """
    Zet het matrixbestand om in een dictonary zodat de
    alignment_scores er makkelijk uitgehaald kunnen worden.
    :param content: File content
    :return: De matrix_dict met daarin de alignment_scores
    """
    matrix_dict = {}
    content = content.strip().split("\n")
    index_list = content.pop(0).strip().split(" ")
    for item in index_list:
        matrix_dict[item] = {}
    for line in content:
        line_list = line.strip().split(" ")
        current_target = line_list.pop(0)
        i = 0
        for matrix_value in line_list:
            matrix_dict[index_list[i]][current_target] = matrix_value
            i += 1

    return matrix_dict


def create_class_matrix(seq1, seq2, matrix_dict):
    """
    Loopt door beide sequenties heen en maakt voor elke combi een
    aparte klasse aan. Vervolgens wordt deze klasse toegevoegd aan
    een globale variabele.
    :param seq1: De eerste sequentie
    :param seq2: De tweede sequentie
    :param matrix_dict: De dictonary met de alignment matrix.
    :return:
    """
    colums = list(seq1)
    rows = list(seq2)
    ri = 0
    for row in rows:
        ci = 0
        class_matrix.append([])
        for colum in colums:
            if colum == "-" or row == "-":
                fillin = GAP_PENALTY
            else:
                fillin = matrix_dict[row][colum]
            alignment = Alignment(row, colum, ci, ri,
                                  fillin)
            class_matrix[ri].append(alignment)
            ci += 1
        ri += 1
    return class_matrix


class Alignment:
    def __init__(self, a1, a2, ci, ri, dict_value):
        """
        :param a1: De base/aa die uit seq 1 komt
        :param a2: De base/aa die uit seq 2 komt
        :param ci: De index van de kolommen
        :param ri: De index van de rijen.
        :param dict_value: De waarde die de alignment van a1 en a2
        heeft in de matrix.
        """
        self.a1 = a1
        self.a2 = a2
        self.colum_index = ci
        self.row_index = ri
        self.raw_alignment_score = dict_value
        self.directions = []
        self.inheritance = []
        self.cumulative_score = None
        self.diagonal_values = [None, None, None]
        self.horizontal_values = [None, None, None]
        self.vertical_values = [None, None, None]
        self.cumulative_score = self.calculate_cumalative_score()

    def calculate_cumalative_score(self):  # row, column
        """
        Kijkt naar de 3 mogelijke opties. 
        Kijkt eerst of ze uberhaupt kunnen, bijv bij pos 0,1 kan
        alleen horizontaal.
        Vraagt vervolgens mogelijke waardes op bij de
        calculate_ functions
        :return: De beste alignmentscore 
        """
        possible_values = []
        if LOCAL_ENABLED:
            possible_values.append((0, None, None))
        if self.row_index == 0 and self.colum_index == 0:  # 0,0
            possible_values.append((0, None, None))
        elif self.row_index == 0:  # 0,?
            # First row only horizontal available
            possible_values.append(self.calculate_vertical())
        elif self.colum_index == 0:  # ?,0
            # First colum only vertical available
            possible_values.append(self.calculate_horizontal())
        else:
            # All options available
            possible_values.append(self.calculate_diagonal())
            possible_values.append(self.calculate_horizontal())
            possible_values.append(self.calculate_vertical())

        return self.find_best_alignment(possible_values)

    def find_best_alignment(self, possible_values):
        """
        Vergelijkt de beste matches met elkaar en kiest de beste(n)
        uit om op te slaan.
        Hierbij wordt de richting ook gelijk opgeslagen.
        :param possible_values: Een tabel met de mogelijke waardes
        :return: De cumulatieve waarde van de beste match.
        """
        best_matches = [(-100000, None, None)]
        for Value in possible_values:
            if int(Value[0]) > best_matches[0][0]:
                best_matches = [Value]
            elif int(Value[0]) == best_matches[0][0]:
                if (0, None, None) in best_matches:
                    best_matches = [Value]
                else:
                    best_matches.append(Value)
        for b_match in best_matches:
            self.directions.append(b_match[1])
            self.inheritance.append(b_match[2])
        return int(best_matches[0][0])

    def calculate_diagonal(self):
        """
        Berekent de cumulatieve waarde van de alignment score uit de
        matrix. Samen met de cumulatieve waarde van de cel die er
        diagonaal achter zit.
        :return: cumulatieve_score, Direction, Instantie waar de
        cumulatieve score van wordt geerft.
        """
        inheritance = class_matrix[self.row_index - 1][self.colum_index - 1]
        inher_value = inheritance.request_cumalative_value()
        cuma_score = inher_value + int(self.raw_alignment_score)
        self.diagonal_values = [cuma_score, "DIAGONAL", inheritance]
        return cuma_score, "DIAGONAL", inheritance

    def calculate_horizontal(self):
        """
        Berekent de cumulatieve waarde bij een horizontale jump.
        Doet dit door naar de cel links te kijken en de GAP_PENALTY
        op te tellen bij de cumulatieve score.
        :return: cumulatieve_score, Direction, Instantie waar de
        cumulatieve score van wordt geerft
        """
        inheritance = class_matrix[self.row_index - 1][self.colum_index]
        inher_value = inheritance.request_cumalative_value()
        cuma_score = inher_value + GAP_PENALTY
        self.horizontal_values = [cuma_score, "HORIZONTAL", inheritance]
        return cuma_score, "HORIZONTAL", inheritance

    def calculate_vertical(self):
        """
        Berekent de cumulatieve waarde bij een verticale jump.
        Doet dit door naar de cel boven te kijken en de GAP_PENALTY
        op te tellen bij de cumulatieve score.
        :return: cumulatieve_score, Direction, Instantie waar de
        cumulatieve score van wordt geerft
        """
        inheritance = class_matrix[self.row_index][self.colum_index - 1]
        inher_value = inheritance.request_cumalative_value()
        cuma_score = inher_value + GAP_PENALTY
        self.vertical_values = [cuma_score, "VERTICAL", inheritance]
        return cuma_score, "VERTICAL", inheritance

    def request_cumalative_value(self):
        """
        :return: De cumulatieve score as integer.
        Berekend door self.calculate_cumalative_score()
        """
        return int(self.cumulative_score)

    def get_directions(self):
        """
        :return: Returnt de direction in 1 letter
        (X=nvt, D=diagonal, H=horizontal, V=vertical)
        """
        returnvalue = "X"
        if self.directions != [None]:
            returnvalue = ""
            for direction in self.directions:
                returnvalue = f"{returnvalue}{direction[0]}"
        return returnvalue

    def get_inheritance(self):
        """
        :return: de instantie waar de waardes van zijn ge-erft.
        """
        return self.inheritance

    def get_alignment(self):
        """
        Genereerd het deel van de alignment voor deze klasse.
        Een A gematch met een A wordt dus:
        A
        |
        A
        Verder wordt er rekening gehouden met mismatches.
        Als het om een gap gaat, wordt de sequentie waarin de gap zit
        vervangen door een '-'.
        :return: Alignment lijst met values
        """
        fillin = '!'
        a1 = self.a1
        a2 = self.a2
        if self.directions[0] == "DIAGONAL":
            if self.a1 == self.a2:
                fillin = "|"
            else:
                fillin = "*"
        elif self.directions[0] == "HORIZONTAL" \
                or self.directions[0] == "VERTICAL":
            fillin = " "
            if self.directions[0] == "HORIZONTAL":
                a2 = "-"
            elif self.directions[0] == "VERTICAL":
                a1 = "-"
        else:
            return None
        return [a1, fillin, a2]

    def get_alignment_info(self):
        """
        Genereerd een grote string die wordt displayed voor elk
        paneel in de matrix wanneer hierom gevraagd wordt.
        Hiermee kunnen de andere waardes geinspecteerd worden
        Als een Lokale alignment aanstaat worden hier extra waardes aan
        toegevoegd.
        :return: returnstring
        """
        returnstring = f"""Verplaats de muis over
de panelen in de matrix!
Alignment: {self.a1}{self.a2}
x:{self.row_index}\ny:{self.colum_index}
Kimura/Blosum score: {self.raw_alignment_score}
Matrix score: {self.cumulative_score}
Best direction:\n{self.directions[0]}
{'_'*15}
Diagonal score: {self.diagonal_values[0]}
Horizontal score: {self.horizontal_values[0]}
Vertical score: {self.vertical_values[0]}
"""
        if LOCAL_ENABLED:
            returnstring = f"{returnstring}Local Cutoff: 0"
        return returnstring

    def __gt__(self, other):
        """
        Vergelijkt de cumulatieve scores van 2 klassen met elkaar.
        Dit zodat de klassen vergeleken kunnen worden buiten de klasse
        met behulp van de > operator.
        :param other: een andere instantie van deze klasse
        :return: BOOL True or False
        """
        return self.cumulative_score > other.cumulative_score

    def __repr__(self):
        """
        Voor het printen in lijsten. (Debugging)
        :return:
        """
        return f"xy:{self.row_index}-{self.colum_index}-{self.a1},{self.a2}" \
               f" {','.join(self.directions)}"
        # \t {self.cumulative_score}\t {self.directions}\n"

    def __str__(self):
        """
        Voor het printen van instanties met print(). (Debugging)
        :return:
        """
        return f"Alignment: {self.a1}{self.a2}\t " \
               f"Index: {self.row_index}, {self.colum_index}\t" \
               f"Raw_score: {self.raw_alignment_score}\t " \
               f"Cuma_score: {self.cumulative_score}"


def find_highest_cuma_score():
    """
    Vindt de alignment met de hoogste score.
    Alleen van toepassing op lokale alignments.
    Zijn er 2 beste scores dan, pakt hij de eerste die gevonden wordt.
    :return: Best scoring class
    """
    current_best = class_matrix[0][0]
    for row in class_matrix:
        for instance in row:
            if instance > current_best:
                current_best = instance
    return current_best


def calculate_traceback():
    """
    Berekent de traceback van de alignment.
    Er wordt standaard begonnen bij de waarde rechtsonder.
    Tenzij LOCAL_ENABLED == True. Dan wordt de hoogste waarde gebruikt
    Vervolgens volgt hij de eerste inheritance van elke instantie.
    Deze instantie wordt toegevoegd aan de traceback.
    Dit gaat door tot:
    Bij een lokale alignment de waarde van het paneel 0 is.
    Bij een niet lokale alignment de instantie linksboven bereikt is.

    Wordt de alignment gestopt? dan wordt de waarde waardoor die stopte
    Niet meegenomen
    :var class_matrix: Globale variable class_matrix met daarin de
    klassen.
    :return: De traceback lijst. Wordt eerst omgedraaid zodat de
    laatste instantie ook achteraan staat.
    """
    instance_list = [class_matrix[-1][-1]]  # startinstance
    traceback = []
    terminated = False
    if LOCAL_ENABLED:
        instance_list = [find_highest_cuma_score()]

    while not terminated:
        if LOCAL_ENABLED and instance_list[0].request_cumalative_value() == 0:
            break
        elif not LOCAL_ENABLED and instance_list[0] == class_matrix[0][0]:
            break
        traceback.append(instance_list)
        inheritance = instance_list[0].get_inheritance()
        instance_list = inheritance

    return traceback[::-1]


def calculate_alignment(traceback):
    """
    Berekent de gehele alignment met behulp van de traceback.
    Zet al deze strings netjes in één grote string.
    :param traceback:
    :return: De alignment string
    """
    endstring = ""
    for i in range(len(traceback[0][0].get_alignment())):
        for a_item in traceback:
            alignment = a_item[0].get_alignment()
            endstring = f"{endstring}{alignment[i]}"
        endstring += "\n"
    return endstring


def main(seq1="ATGC", seq2="ATGC", dna=False, aa=False):
    """
    De main: deze functie roept alle andere functies aan die nodig
    zijn voor het alignment algoritme. (Dus niet voor wx)
    :param seq1: de 1ste sequentie (str)
    :param seq2: de 2de sequentie (str)
    :param dna: is het DNA Bool
    :param aa: is het aa Bool
    :return: None
    """
    dna_matrix_dict = process_matrix(read_file("kimura2.txt"))
    aa_matrix_dict = process_matrix(read_file("blosum62.txt"))
    if dna:
        create_class_matrix(seq1, seq2, dna_matrix_dict)
    elif aa:
        create_class_matrix(seq1, seq2, aa_matrix_dict)
    else:
        raise Exception("NO DNA OR AA SET")


class Startscherm(wx.Panel):
    def __init__(self, parent):
        """
        Roept alle functies aan die nodig zijn voor het WX scherm.
        :param parent: De parent voor het WX paneel.
        """
        wx.Panel.__init__(self, parent)
        self.matrixlist = []
        self.knoppenMaken()
        self.setFont()
        self.settingsBoxMaken()
        self.knoppenBinden()

    def knoppenMaken(self):
        """
        Hierin worden alle knoppen en (tekst)panelen aangemaakt.
        Ook staan hierin de Lokaal/Globaal en DNA/Eiwit opties.
        """
        self.titel = wx.StaticText(self, -1, "Sequenties alignen")
        optie = ["DNA (AGCT)", "Eiwit (ARNDCQEGHILKMFPSTWYV)"]
        uitvoering = ["Globaal", "Lokaal"]
        self.radiobox_optie = wx.RadioBox(self, -1, "DNA of eiwit?",
                                          wx.DefaultPosition, wx.DefaultSize,
                                          optie, 1, wx.RA_SPECIFY_COLS)
        self.radiobox_uitvoering = wx.RadioBox(self, -1, "Globaal of lokaal?",
                                               wx.DefaultPosition,
                                               wx.DefaultSize, uitvoering, 1,
                                               wx.RA_SPECIFY_COLS)
        self.seq_tekst1 = wx.StaticText(self, -1, "Sequentie 1 (0/25)")
        self.seq_tekst2 = wx.StaticText(self, -1, "Sequentie 2 (0/25)")
        self.invoer_seq1 = wx.TextCtrl(self, -1)
        self.invoer_seq2 = wx.TextCtrl(self, -1)
        self.invoer_seq1.SetMaxLength(25)
        self.invoer_seq2.SetMaxLength(25)
        self.startknop = wx.Button(self, -1, "Start")
        self.alignment_tekst = wx.StaticText(self, -1, "Alignment")
        self.alignment_tekst.Hide()
        self.alignment = wx.StaticText(self, -1, "")  # Nog invoegen

        self.alignment_info = wx.StaticText(self, -1, "Houd de muis boven \n"
                                                      "een paneel in de "
                                                      "matrix!")

    def create_panel(self, text, matrix_parent=None):
        """
        Maakt een paneel met daarop gecentreerde text.
        Geeft deze ook een extra atribuut: de parent van de matrix.
        Elk Paneel wordt ook toegevoegd aan self.matrixlist.
        Dit zodat de traceback er later doorheen kan loopen.
        :param text: De text die op het paneel komt te staan
        :param matrix_parent: De parent uit class_matrix
        :return:
        """
        panel = wx.Panel(self)
        panel.SetWindowStyle(wx.SIMPLE_BORDER)
        panel.matrix_parent = matrix_parent
        text = wx.StaticText(panel, -1, text)
        hbox = wx.BoxSizer()
        hbox.Add(text, 1, wx.CENTER)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, 1, wx.CENTER)
        panel.SetSizer(vbox)
        self.matrixlist.append(panel)
        return panel

    def matrix_builder(self, seq1, seq2):
        """
        Bouwt een matrix met behulp van de 2 sequenties en de waardes
        in class_matrix.
        Er wordt eerst telkens de sequentie toegevoegd en later de
        waardes van de matrix.
        Hierdoor krijg je een nette matrix.
        :param seq1: De 1ste sequentie
        :param seq2: de 2de sequentie
        :return: De boxsizer met daarin de matrix
        """
        xbox = wx.BoxSizer(wx.HORIZONTAL)
        fb = wx.BoxSizer(wx.VERTICAL)
        fb.Add(self.create_panel(" "), -1, wx.EXPAND)
        for align in seq1:
            fb.Add(self.create_panel(str(align)), -1, wx.EXPAND)
        xbox.Add(fb, 1, wx.EXPAND)
        for row in class_matrix:
            ybox = wx.BoxSizer(wx.VERTICAL)
            index = class_matrix.index(row)
            ybox.Add(self.create_panel(str(seq2[index])), 1, wx.EXPAND)
            for instance in row:
                ybox.Add(self.create_panel(str(instance.
                                               request_cumalative_value()),
                                           instance), 1, wx.EXPAND)
            xbox.Add(ybox, 1, wx.EXPAND)
        return xbox

    def setFont(self):
        """
        Hierin wordt het Fonttype van alle tekst aangepast.
        De titel heeft zijn eigen font. De rest heeft een general font.
        De alignment font wordt een apart lettertype, omdat de tekens
        dan recht onder elkaar uitgelijnd staan.
        """
        titelfont = wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.titel.SetFont(titelfont)
        general_font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.radiobox_uitvoering.SetFont(general_font)
        self.radiobox_optie.SetFont(general_font)
        self.seq_tekst1.SetFont(general_font)
        self.seq_tekst2.SetFont(general_font)
        self.invoer_seq1.SetFont(general_font)
        self.invoer_seq2.SetFont(general_font)
        self.startknop.SetFont(general_font)
        self.alignment_tekst.SetFont(general_font)
        self.alignment_info.SetFont(general_font)
        alignmentfont = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.alignment.SetFont(alignmentfont)

    def knoppenBinden(self):
        """
        Deze functie bindt alle events aan de functies, zodat wx deze
        op tijd uitvoerd.
        :return: None
        """
        self.startknop.Bind(wx.EVT_BUTTON, self.onStart)
        self.invoer_seq1.Bind(wx.EVT_TEXT_PASTE, self.onPaste)
        self.invoer_seq2.Bind(wx.EVT_TEXT_PASTE, self.onPaste)
        self.invoer_seq2.Bind(wx.EVT_CHAR, self.onCharEnter)
        self.invoer_seq1.Bind(wx.EVT_CHAR, self.onCharEnter)
        self.radiobox_optie.Bind(wx.EVT_RADIOBOX, self.onModeSwitch)
        self.Bind(wx.EVT_SIZE, self.updateLayout)

    def onCharEnter(self, event):
        """
        Wordt uitgevoerd elke keer dat de user een character invoert.
        Checkt of deze ingevoerd kan worden.
        Bij DNA kan alleen ACGT en bij eiwit alleen
        ARNDCQEGHILKMFPSTWYV.
        Verder kunnen de keycodes [8, 127, 314, 316, 3, 22, 24, 1]
        altijd. Dit zijn de backspace, delete, de pijltjestoetsen
        en Ctrl + C/X/V/A.
        Als een character mag, wordt het event.Skip() aangeroepen en
        wordt het door wx ingetypt.
        Is het lowercase? Dan wordt het geconverteerd naar uppercase
        door 32 van de keycode af te halen en dit vervolgens op de
        juiste plek te inserten.
        De characters die ingetypt mogen worden, is afhankelijk van
        de modus DNA of eiwit.
        :param event: Event Object Gegeven door wxpython
        :return: None
        """
        panel = self.FindWindowById(event.GetId())
        mode = self.radiobox_optie.GetStringSelection()
        defkeycodes = [8, 127, 314, 316, 3, 22, 24, 1]
        # [BACKSPACE, DELETE, ARROW_LEFT,
        # ARROW_RIGHT, CTRL+C, CTRL+V, CTRL+X, CTRL+A]
        if mode == "DNA (AGCT)":
            comparestring = "AGCT"
        elif mode == "Eiwit (ARNDCQEGHILKMFPSTWYV)":
            comparestring = "ARNDCQEGHILKMFPSTWYV"
        cs_l = comparestring.lower()
        comparestring += cs_l
        keycodes = [ord(c) for c in comparestring]
        keycodes = keycodes + defkeycodes
        kc_l = [ord(c) for c in cs_l]
        keycode = event.GetKeyCode()
        if keycode in keycodes:
            if keycode in kc_l and keycode not in defkeycodes:
                text_list = list(panel.GetValue())
                if len(text_list) < 25:
                    converted_keycode = keycode - 32
                    ins_point = panel.GetInsertionPoint()
                    text_list.insert(ins_point, chr(converted_keycode))
                    text = "".join(text_list)
                    panel.SetValue(text)
                    panel.SetInsertionPoint(ins_point+1)
            else:
                event.Skip()
        wx.CallAfter(self.trackSeqLen)

    def onPaste(self, event):
        """
        Wordt aangeroepen door wx als CTRL + V gebruikt wordt
        Leest de clipboard in en filterd alle text die niet mag
        en voegt dit toe op de juiste plek.
        Als de clipboard te lang is, wordt deze afgekapt.
        Bijv. staan er al 5 characters en wordt er een seq van 25 lang
        geplakt, dan worden de eerste 20 letter toegevoegd.
        :param event: wx.EventObject
        :return: None
        """
        panel = self.FindWindowById(event.GetId())
        clipbord = wx.TheClipboard
        text_list = list(panel.GetValue())
        remaining_char = 25 - len(text_list)
        if clipbord.Open() and remaining_char > 0:
            text = wx.TextDataObject()
            clipbord.GetData(text)
            ins_point = panel.GetInsertionPoint()
            text = text.GetText().upper()
            text = self.onModeSwitch(None, text)
            text = text[0:remaining_char]
            text_list.insert(ins_point, text)
            text = "".join(text_list)
            panel.SetValue(text)
            panel.SetInsertionPoint(ins_point+len(text))
        wx.CallAfter(self.trackSeqLen)

    def trackSeqLen(self):
        """
        Update de tekstlabel zodat de lengte van de sequentie
        ijgehouden wordt.
        :return: None
        """
        seq1 = self.invoer_seq1.GetValue()
        seq2 = self.invoer_seq2.GetValue()
        self.seq_tekst1.SetLabel(f"Sequentie 1 ({len(seq1)}/25)")
        self.seq_tekst2.SetLabel(f"Sequentie 2 ({len(seq2)}/25)")
        self.seq_tekst1.Refresh()
        self.seq_tekst2.Refresh()

    def onModeSwitch(self, event, input=None):
        """
        Deze functie heeft 2 modussen:
        Modus 1: WX
        Wordt de functie aangeroepen door wx. omdat de radiobox
        van selection wisselt. Dan wordt de inputvelden gecheckt en
        characters die er niet horen worden verwijderd.

        Modus 2: MANUAL
        Wordt de functie handmatig aangeroepen dan wordt er input
        meegegeven.
        In plaats van dat de inputvelden gefilterd worden, wordt de
        opgegeven string gefilterd. Vervolgens wordt deze gereturned.
        :param event: wx.EventObject
        :param input: De input als de functie niet door
        WX wordt aangeroepen
        :return: filteredstring if input != None
        """
        mode = self.radiobox_optie.GetStringSelection()
        if mode == "DNA (AGCT)":
            comparestring = "AGCT"
        elif mode == "Eiwit (ARNDCQEGHILKMFPSTWYV)":
            comparestring = "ARNDCQEGHILKMFPSTWYV"
        if input is None:
            comparestring += "|"
            stringvalue = f"{self.invoer_seq1.GetValue()}|" \
                          f"{self.invoer_seq2.GetValue()}"
        else:
            stringvalue = input
        filteredstring = ''
        for i in stringvalue:
            if i in comparestring:
                filteredstring += i
        if input is None:
            filteredlist = filteredstring.split("|")
            self.invoer_seq1.SetValue(filteredlist[0])
            self.invoer_seq2.SetValue(filteredlist[1])
        else:
            return filteredstring

    def updateLayout(self, event):
        """
        Update de layout van het scherm als het van grootte veranderd.
        Dit zodat het scherm er netjes uit blijft zien.
        :param event: unused wx.EventObject
        :return: None
        """
        if not FIRST_RUN:
            self.matrix.Layout()
        self.Layout()
        self.Refresh()

    def onStart(self, event):
        """
        Deze functie roept alle andere funcies aan.
        Het wordt aangeroepen als er op de startknop wordt gedrukt.
        Wordt de fucntie voor een tweede keer aangeroepen, dan wordt
        eerst de alignmentbox lostgemaakt en de vorige matrix
        wordt verwijderd.
        Vervolgens worden alle variabelen die het algoritme gebruikt
        worden gereset, zodat het opnieuw kan beginnen.
        Verder wordt ook de input gefilterd (just in case).
        Dan worden de instellingen opgehaald.
        Vervolgens worden de functies aangeroepen die de matrix maken
        en op het scherm zetten.
        :param event: wx.EventObject
        """
        self.onModeSwitch(None)
        seq1, seq2 = f"-{self.invoer_seq1.GetValue()}", \
                     f"-{self.invoer_seq2.GetValue()}"
        if len(seq1) > 1 and 1 < len(seq2):
            global FIRST_RUN
            if FIRST_RUN:
                FIRST_RUN = False
            else:
                self.matrix.Clear(delete_windows=True)
                self.totalbox.Remove(self.alignmentbox)
                self.Refresh()
                self.Layout()
            dna = False
            protein = False
            global class_matrix
            class_matrix = []
            self.matrixlist = []

            optie = self.radiobox_optie.GetStringSelection()
            uitvoering = self.radiobox_uitvoering.GetStringSelection()
            global LOCAL_ENABLED
            if uitvoering == "Globaal":
                LOCAL_ENABLED = False
            elif uitvoering == "Lokaal":
                LOCAL_ENABLED = True
            if optie == "DNA (AGCT)":
                dna = True
            elif optie == "Eiwit (ARNDCQEGHILKMFPSTWYV)":
                protein = True

            main(seq1, seq2, dna, protein)
            self.alignment_box(seq1, seq2)
            self.create_matrix_interactivity()
            self.updateLayout(None)

    def create_matrix_interactivity(self):
        """
        Doet 2 dingen:
        Geeft de panelen in de matrix een rode kleur als ze in de
        traceback zitten.
        Verder wordt de hover functie gebonden aan elk paneel.
        Dit zodat wanneer de muis eroverheen hovered, er een functie
        aangeroepen wordt die extra info laat zien.
        :return: None
        """
        traceback = calculate_traceback()
        self.alignment.SetLabel(calculate_alignment(traceback))
        self.alignment.Refresh()
        for panel in self.matrixlist:
            panel.Bind(wx.EVT_ENTER_WINDOW, self.matrix_hover_enter)
            tb = [trace[0] for trace in traceback]
            if panel.matrix_parent in tb:
                panel.SetBackgroundColour('Red')
                panel.Refresh()

    def matrix_hover_enter(self, evt):
        """
        Zoekt uit boven welk paneel de muis staat.
        Past vervolgens de self.alignment_info aan zodat de
        info over dit paneel zichtbaar wordt.
        :param evt: wx.EventObject
        :return: None
        """
        panel = self.FindWindowById(evt.GetId())
        if panel.matrix_parent is not None:
            string_to_set = panel.matrix_parent.get_alignment_info()
            self.alignment_info.SetLabel(string_to_set)
            self.alignment_info.Refresh()

    def settingsBoxMaken(self):
        """
        Hierin worden alle boxen gemaakt. Eerst de box met alle
        settings en als laatste in 'totalbox' wordt de alignment
        eraan toegevoegd.
        """
        optiebox = wx.BoxSizer(wx.VERTICAL)
        seqbox = wx.BoxSizer(wx.VERTICAL)
        alignment_infobox = wx.BoxSizer(wx.VERTICAL)

        vbox1, vbox2 = wx.BoxSizer(wx.VERTICAL), wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer()
        leeg = wx.Panel(self)
        self.totalbox = wx.BoxSizer()

        """Keuzeboxen: DNA/Eiwit en Lokaal/Globaal"""
        optiebox.Add(self.radiobox_optie, 1, wx.EXPAND)
        optiebox.Add(self.radiobox_uitvoering, 1, wx.EXPAND)

        """Invoerboxen voor sequentie 1 en 2"""
        seqbox.Add(self.seq_tekst1, 0, wx.EXPAND)
        seqbox.Add(self.invoer_seq1, 1, wx.EXPAND)
        seqbox.Add(self.seq_tekst2, 0, wx.EXPAND)
        seqbox.Add(self.invoer_seq2, 1, wx.EXPAND)

        """
        Informatiebox over matrix, hier staat welke basen alignen,
        wat de coordinaten daarvan zijn en wat de D/H/V scores zjjn.
        """
        alignment_infobox.Add(self.alignment_info, 1, wx.EXPAND)

        """
        Hier wordt alles gecombineerd tot één box
        """
        hbox1.Add(optiebox, 2, wx.EXPAND)
        hbox1.Add(alignment_infobox, 1, wx.EXPAND)

        vbox2.Add(self.titel, 0, wx.EXPAND)
        vbox2.Add(hbox1, 2, wx.EXPAND)
        vbox2.Add(seqbox, 2, wx.EXPAND)
        vbox2.Add(self.startknop, 1, wx.EXPAND)

        self.totalbox.Add(vbox2, 5, wx.EXPAND)
        self.totalbox.Add(leeg, 1, wx.EXPAND)
        self.SetSizer(self.totalbox)

    def alignment_box(self, seq1, seq2):
        """
        :param seq1: sequentie 1 in de matrix
        :param seq2: sequentie 2 in de matrix
        Functie maakt de box met traceback en optimale alignment
        """
        leeg = wx.Panel(self)
        self.alignmentbox = wx.BoxSizer(wx.VERTICAL)
        self.matrix = self.matrix_builder(seq1, seq2)
        self.alignmentbox.Add(self.matrix, 10, wx.EXPAND)
        self.alignmentbox.Add(leeg, 1, wx.EXPAND)
        self.alignmentbox.Add(self.alignment_tekst, 0, wx.EXPAND)
        self.alignment_tekst.Show()
        self.alignmentbox.Add(self.alignment, 3, wx.EXPAND)
        self.totalbox.Add(self.alignmentbox, 10, wx.EXPAND)


if __name__ == "__main__":
    class Scherm(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent, title="BANSEQ Tim van der Lee"
                                                  " & Lindsey Tichelaar",
                              size=(800, 600))
            self.paneel = Startscherm(self)
            self.Maximize()
            self.Show(True)

    app = wx.App()
    Scherm(None)
    app.MainLoop()
