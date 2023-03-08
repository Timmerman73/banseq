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
            self.paneel = Panel(self)
            framebox.Add(self.paneel, 1, wx.EXPAND | wx.ALL)
            self.SetSizer(framebox)
            self.__knoppenBinden()
            self.Show()

        def __knoppenBinden(self):
            pass

        def onButton(self, event):
            pass


    app = wx.App()
    Scherm(None, -1, "")
    app.MainLoop()
