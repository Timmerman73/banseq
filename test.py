import wx


class Panel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        self.__global_vars()
        self.__widget_builder()
        eindbox = self.__box_Builder()
        self.SetSizer(eindbox)

    def __global_vars(self):
        pass

    def __widget_builder(self):
        pass

    def __box_Builder(self):
        box = wx.BoxSizer()

        return box


if __name__ == "__main__":
    class Scherm(wx.Frame):
        def __init__(self, parent, id, title):
            wx.Frame.__init__(self, parent, id, title, size=(410, 480))
            framebox = wx.BoxSizer()
            xbox = wx.BoxSizer(wx.HORIZONTAL)
            for x in "ATGATGATG":
                ybox = wx.BoxSizer(wx.VERTICAL)
                for y in "ATGCATGCATGC":

                    ybox.Add(self.Create_Panel_with_text(f"{x}{y}"),1,wx.EXPAND)
                xbox.Add(ybox,1,wx.EXPAND)


            framebox.Add(xbox, 1, wx.EXPAND | wx.ALL)
            self.SetSizer(framebox)
            self.__knoppenBinden()
            self.Show()

        def Create_Panel_with_text(self,text):
            panel = Panel(self)
            panel.SetWindowStyle(wx.SIMPLE_BORDER)
            text = wx.StaticText(panel,-1,text)
            hbox = wx.BoxSizer()
            hbox.Add(text,1,wx.CENTER)
            vbox = wx.BoxSizer(wx.VERTICAL)
            vbox.Add(hbox,1,wx.CENTER)
            panel.SetSizer(vbox)
            return panel

        def __knoppenBinden(self):
            pass

        def onButton(self, event):
            pass


    app = wx.App()
    Scherm(None, -1, "")
    app.MainLoop()
