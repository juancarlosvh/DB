import wx
import wx.aui

from src.controller import Controller

class MetaDBManager(wx.Frame):
	is_connected = False
	Controlador = Controller()

	def __init__(self,parent):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"MetaDBManager")
		favicon = wx.Icon('src/img/wxdbmanager_32x32.png',wx.BITMAP_TYPE_PNG, 16,16)
		self.SetIcon(favicon)
		self.SetSize((620,530))
		self.SetTitle("MetaDBManager")
		self.BarraHerramientas()
		self.UI()

		self.Centre()
		self.Show()

		self.CheckConnection()

	def BarraHerramientas(self):
		self.ToolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY )
		self.Connection_tool = self.ToolBar1.AddTool( wx.ID_ANY, u"tool",wx.Bitmap( u"src/img/025-settings-1.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.ToolBar1.Realize()

		self.Bind(wx.EVT_TOOL, self.conection_manager, self.Connection_tool)
		

	def UI(self):
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		VerticalSizerPrincipal = wx.BoxSizer( wx.VERTICAL )

		self.Splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		#self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )

		self.PanelArbol = wx.Panel( self.Splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		VSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.Arbol = wx.TreeCtrl( self.PanelArbol, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
		VSizer1.Add( self.Arbol, 1, wx.ALL|wx.EXPAND, 5 )


		self.PanelArbol.SetSizer( VSizer1 )
		self.PanelArbol.Layout()
		VSizer1.Fit( self.PanelArbol )
		self.PanelNoteBook = wx.Panel( self.Splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		VSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.NoteBook = wx.aui.AuiNotebook( self.PanelNoteBook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_DEFAULT_STYLE )

		VSizer2.Add( self.NoteBook, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel1 = wx.Panel( self.NoteBook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		
		self.NoteBook.AddPage( about_panel(self.NoteBook), u"WxDBManager")
		
		self.PanelNoteBook.SetSizer( VSizer2 )
		self.PanelNoteBook.Layout()
		VSizer2.Fit( self.PanelNoteBook )
		self.Splitter.SplitVertically( self.PanelArbol, self.PanelNoteBook, 151 )
		VerticalSizerPrincipal.Add( self.Splitter, 1, wx.EXPAND, 5 )


		self.SetSizer( VerticalSizerPrincipal )

	#Funciones
	def conection_manager(evt,self):
		print("Connection")
	
	def CheckConnection(self):
		m = self.Controlador.initConection()
		wx.MessageBox(str(m), 'Info',wx.OK | wx.ICON_INFORMATION)

class about_panel( wx.Panel ):
	#controller = Controller()

	def __init__(self, parent ):
		wx.Panel.__init__ ( self, parent=parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )