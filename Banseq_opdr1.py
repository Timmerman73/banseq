import wx


class Startscherm(wx.Panel):
    """Hierin worden alle functies aangeroepen."""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.knoppenMaken()
        self.setFont()
        self.hoverAlignment()
        self.settingsBoxMaken()
        self.knoppenBinden()

    """In deze functie worden alle knoppen en teksten aangemaakt."""
    def knoppenMaken(self):
        self.cell = wx.Panel(self)  # Dit is het blauwe vlak
        self.titel = wx.StaticText(self, -1, "Sequenties alignen")
        optie = ["DNA", "Eiwit"]
        uitvoering = ["Lokaal", "Globaal"]
        self.radiobox_optie = wx.RadioBox(self, -1, "DNA of eiwit?",
                                          wx.DefaultPosition, wx.DefaultSize,
                                          optie, 1, wx.RA_SPECIFY_COLS)
        self.radiobox_uitvoering = wx.RadioBox(self, -1, "Lokaal of globaal?",
                                               wx.DefaultPosition,
                                               wx.DefaultSize, uitvoering, 1,
                                               wx.RA_SPECIFY_COLS)
        self.seq_tekst1 = wx.StaticText(self, -1, "Sequentie 1")
        self.seq_tekst2 = wx.StaticText(self, -1, "Sequentie 2")
        self.invoer_seq1 = wx.TextCtrl(self, -1)
        self.invoer_seq2 = wx.TextCtrl(self, -1)
        self.startknop = wx.Button(self, -1, "Start")

        # self.gap_tekst = wx.StaticText(self, -1, "Gap Penalty")
        # self.spintekst = wx.StaticText(self, -1, "-5")
        # self.gap_penalty = wx.SpinButton(self, -1)
        # self.gap_penalty.SetRange(-100, 100)
        # self.gap_penalty.SetValue(-5)

        self.traceback_tekst = wx.StaticText(self, -1, "Traceback")
        self.traceback = wx.StaticText(self, -1, "***Hier komt de traceback***")  # Nog invoegen
        self.alignment_tekst = wx.StaticText(self, -1, "Alignment")
        self.alignment = wx.StaticText(self, -1, "***Hier komt alignment1***"
                                                 "\n***Hier komt alignment2***")  # Nog invoegen

        # Deze nog invullen met de goede waardes.
        self.alignment_duo = wx.StaticText(self, -1, "Alignment: xx")
        self.index = wx.StaticText(self, -1, "Index: x,y")
        self.diagonal_score = wx.StaticText(self, -1, "Diagonal = x")
        self.horizontal_score = wx.StaticText(self, -1, "Horizontal = x")
        self.vertical_score = wx.StaticText(self, -1, "Vertical = x")

        # Deze weghalen aan het einde
        self.test = wx.StaticText(self, -1, "ATGCGGATTCA\n|-|****-|*|\nA GTAAG TAA")

    """Hierin wordt de tekst van de Spinbutton opgevraagd.
    def onSpin(self, event):
        self.spintekst.SetLabel(str(event.GetPosition()))
    """

    """Hierin wordt het Fonttype van alle tekst aangepast.
    De titel heeft zijn eigen font. De rest heeft een general font.
    De alignment font wordt een apart lettertype, omdat de tekens dan
    recht onder elkaar uitgelijnd staan."""
    def setFont(self):
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
        # self.spintekst.SetFont(general_font)
        # self.gap_tekst.SetFont(general_font)
        self.traceback_tekst.SetFont(general_font)
        self.traceback.SetFont(general_font)
        self.alignment_tekst.SetFont(general_font)
        self.alignment.SetFont(general_font)
        self.alignment_duo.SetFont(general_font)
        self.index.SetFont(general_font)
        self.diagonal_score.SetFont(general_font)
        self.horizontal_score.SetFont(general_font)
        self.vertical_score.SetFont(general_font)
        alignmentfont = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.test.SetFont(alignmentfont)

    """
    def calculations(self):
        # Diagonal
        *berekening*
        
        # Horizontal
        *berekening *
        
        # Vertical
        *berekening *
    """

    """Hier worden de startknop en Spinbutton voor Gap-Penalty
    gebonden. Daarna gaan deze door naar de functies onStart en
    onSpin om uitgevoerd te worden."""
    def knoppenBinden(self):
        self.startknop.Bind(wx.EVT_BUTTON, self.onStart)
        # self.gap_penalty.Bind(wx.EVT_SPIN, self.onSpin)

    """Hierin worden de knoppen uitgevoerd. Er wordt gekeken naar de
    Radiobuttons van DNA/eiwit en Lokaal/Globaal."""
    def onStart(self, event):
        label = self.startknop.GetLabel()
        optie = self.radiobox_optie.GetStringSelection()
        uitvoering = self.radiobox_uitvoering.GetStringSelection()
        """
        if optie == "DNA":
            letters = self.base_dict  # Voor de base + score opties een dictionairy maken
                                        # of iets waaruit je de scores kan halen
        elif optie == "Eiwit":
            letters = self.amino_dict # Voor de amino's + score opties een dictionairy maken
                                        # of iets waaruit je de scores kan halen

        if uitvoering == "Globaal":
            # De gehele sequentie van elk eiwit of DNA molecuul --> bij ons: max 25.
            # Kan negatieve getallen bevatten.
            # Alignment bouwen: begint rechtsonder naar linksboven.
            # Stopt pas als linksboven bereikt is.

        elif uitvoering == "Lokaal":
            # Kijkt naar regionen met de hoogste overeenkomst tussen twee sequenties.
            # Bevat alleen positieve getallen (is iets negatief, dat voer je ‘0’ in).
            # Alignment bouwen: begint bij de hoogste getal en gaat naar linksboven.
            # Stopt wanneer er een 0 is bereikt (deze 0 hoort niet bij de alingment.

        """
    """ Hover Alignment en de twee Mouse functies zorgen ervoor
    dat je met je muis kan hoveren over een cell / panel en daarvan
    de waarde op kan vragen."""
    def hoverAlignment(self):
        self.color = self.cell.GetBackgroundColour()
        self.cell.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
        self.cell.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)

    def onMouseOver(self, event):
        # mouseover changes colour of button
        self.cell.SetBackgroundColour('Blue')
        event.Skip()
        self.cell.Refresh()

    def onMouseLeave(self, event):
        # mouse not over button, back to original colour
        self.cell.SetBackgroundColour(self.color)
        event.Skip()
        self.cell.Refresh()


    """Hierin worden alle boxen gemaakt. Eerst de box met alle settings
    en als laatste in 'totalbox' wordt de alignment eraan toegevoegd."""
    def settingsBoxMaken(self):
        optiebox = wx.BoxSizer(wx.VERTICAL)
        # spinbox = wx.BoxSizer(wx.VERTICAL)
        seqbox = wx.BoxSizer(wx.VERTICAL)
        alignment_infobox = wx.BoxSizer(wx.VERTICAL)
        alignmentbox = wx.BoxSizer(wx.VERTICAL)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer()
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        leeg = wx.Panel(self)
        totalbox = wx.BoxSizer()

        """Keuzeboxen: DNA/Eiwit en Lokaal/Globaal"""
        optiebox.Add(self.radiobox_optie, 2, wx.EXPAND)
        optiebox.Add(self.radiobox_uitvoering, 2, wx.EXPAND)

        """Spinbutton box met alles wat erbij hoort
        spinbox.Add(self.gap_tekst, 0, wx.EXPAND)
        spinbox.Add(self.spintekst, 0, wx.CENTER)
        spinbox.Add(self.gap_penalty, 0, wx.CENTER)
        """

        """Invoerboxen voor sequentie 1 en 2"""
        seqbox.Add(self.seq_tekst1, 0, wx.EXPAND)
        seqbox.Add(self.invoer_seq1, 1, wx.EXPAND)
        seqbox.Add(self.seq_tekst2, 0, wx.EXPAND)
        seqbox.Add(self.invoer_seq2, 1, wx.EXPAND)

        """Informatiebox over matrix, hier staat welke basen alignen,
        wat de coordinaten daarvan zijn en wat de DHV scores zjjn."""
        alignment_infobox.Add(self.alignment_duo, 0, wx.EXPAND)  # alignment_tekst (bijv. AA / CT)
        alignment_infobox.Add(self.index, 0, wx.EXPAND)  # index (coordinaten/positie, bijv. 2,5)
        alignment_infobox.Add(self.diagonal_score, 0, wx.EXPAND)  # Diagonal score
        alignment_infobox.Add(self.horizontal_score, 0, wx.EXPAND)  # Horizontal score
        alignment_infobox.Add(self.vertical_score, 0, wx.EXPAND)  # Vertical score

        """Box met traceback en optimale alignment"""
        #alignmentbox.Add()  # Matrix
        alignmentbox.Add(self.test, 3, wx.EXPAND)
        alignmentbox.Add(self.cell, 1, wx.EXPAND)  # Dit is het blauwe vlak
        alignmentbox.Add(self.traceback_tekst, 0, wx.EXPAND)
        alignmentbox.Add(self.traceback, 1, wx.EXPAND)  # Traceback in letters (bijv. AGCTAGC)
        alignmentbox.Add(self.alignment_tekst, 0, wx.EXPAND)
        alignmentbox.Add(self.alignment, 1, wx.EXPAND)  # Alignment seq1 en seq2

        """Alles combineren"""
        vbox1.Add(optiebox, 3, wx.EXPAND)
        # vbox1.Add(spinbox, 1, wx.ALIGN_LEFT)

        hbox1.Add(vbox1, 1, wx.EXPAND)
        hbox1.Add(alignment_infobox, 1, wx.EXPAND)

        vbox2.Add(self.titel, 0, wx.EXPAND)
        vbox2.Add(hbox1, 2, wx.EXPAND)
        vbox2.Add(seqbox, 1, wx.EXPAND)

        totalbox.Add(vbox2, 5, wx.EXPAND)
        totalbox.Add(leeg, 1, wx.EXPAND)
        totalbox.Add(alignmentbox, 10, wx.EXPAND)
        # totalbox.Add(self.startknop, 1, wx.EXPAND)

        self.SetSizer(totalbox)
        return totalbox

    """
    def alignmentBoxMaken(self):
        # 25x25 max length (seq1 x seq2)
        #
        lengte_seq1 = len(self.invoer_seq1.GetValue()[:25])
        lengte_seq2 = len(self.invoer_seq2.GetValue()[:25])

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add()  # Add dit^ alles in een box
        return box
        """

    def traceback_path(self):
        path = wx.Panel()
        path.SetBackgroundColour("Blue")
        box = wx.BoxSizer()
        box.Add(path, 1, wx.EXPAND)
        self.SetSizer(box)
        return box


if __name__ == "__main__":
    class Scherm(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent, title="BANSEQ", size=(800, 600))
            self.paneel = Startscherm(self)
            self.Show(True)


    app = wx.App()
    Scherm(None)
    app.MainLoop()

"""
Vragen om 2 sequenties --> alignment maken
Eisen:
- Alignment moet globaal of lokaal uitgevoerd kunnen worden
- Programma werkt voor DNA en eiwitten
- Lengte = max 25 posities, langer? --> afkappen
- Alles moet op 1 scherm te zien zijn met daarin:
- Gemaakte matrix met:
    - Berekende waarden van elke positie
    - Traceback
    - Alignment
- Wijziging in sequentie ook op scherm tonen
- Gebruiker kan voor elke waarde van elke positie in de matrix de andere (berekende) waarden opvragen.
    Dit zijn de berekende waarden in het dynamisch model die niet de maximum score geven.
- Als de gebruiker kiest voor een eiwit, dan wordt gebruik gemaakt van de blosum62 scoringsmatrix.
    Bij een DNA sequentie wordt er gebruik gemaakt van de kimura 2 parameter distance matrix.
"""