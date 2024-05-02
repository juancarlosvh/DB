import wx
from src.controller import Controller

class MetaDBManager(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"MetaDBManager", pos = wx.DefaultPosition, size = wx.Size( 522,432 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        favicon = wx.Icon('src/img/wxdbmanager_32x32.png',wx.BITMAP_TYPE_PNG, 16,16)
        self.SetIcon(favicon)
        self.SetSize((620,530))
        self.SetTitle("MetaDBManager")
        self.Centre()
        self.Show()
