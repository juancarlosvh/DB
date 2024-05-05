from src.UI import *
import wx

class MyApp(wx.App):
    def OnInit(self):
        frame = MetaDBManager(None)
        frame.Show(True)
        self.SetTopWindow(frame)

        return True

#---------------------------------------------------------------------------

app = MyApp(0)
app.MainLoop()