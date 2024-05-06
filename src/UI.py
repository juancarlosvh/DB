import wx
import wx.aui

from src.controller import Controller
from src.config import Config
from src.dbConnect import DBConnect

class MetaDBManager(wx.Frame):
	#instancias
	Controlador = Controller()
	Config = Config()
	connected = None
	#Variables
	is_connected = False
	database_old_selected = ''
	List_tables = []

	def __init__(self,parent):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"MetaDBManager")
		favicon = wx.Icon('src/icons/wxdbmanager_32x32.png',wx.BITMAP_TYPE_PNG, 16,16)
		self.SetIcon(favicon)
		self.SetSize((620,530))
		self.SetTitle("MetaDBManager")
		self.BarraHerramientas()
		self.UI()

		self.Centre()
		self.Show()

		self.CheckConnection()
		self.ArbolLlenado()

	def BarraHerramientas(self):
		self.ToolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY )
		self.Connection_tool = self.ToolBar1.AddTool( wx.ID_ANY, u"tool",wx.Bitmap( u"src/icons/025-settings-1.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.ToolBar1.Realize()

		self.Bind(wx.EVT_TOOL, self.ConnectionManager, self.Connection_tool)
		
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

	def ArbolLlenado(self):
		data = self.connected.return_data("SHOW SCHEMAS","")
		root = self.Arbol.AddRoot('Databases')
		self.Arbol.Expand(root)
		print(data)

		#	def get_databases_list(self,tree,root):
		self.items_database_list = {}

		image_list = wx.ImageList(16, 16)
		img_database = image_list.Add(wx.Image("src/icons/database.png", wx.BITMAP_TYPE_PNG).Scale(16,16).ConvertToBitmap())
		self.img_table    = image_list.Add(wx.Image("src/icons/table.png", wx.BITMAP_TYPE_PNG).Scale(16,16).ConvertToBitmap())

		self.Arbol.AssignImageList(image_list)

		if self.is_connected == True:
			rows = data
			for row in rows:
				item = self.Arbol.AppendItem(root, row[0])
				self.items_database_list[row[0]]=(item)
				# Agregando imagen a los items				
				self.Arbol.SetItemData(item, None)
				self.Arbol.SetItemImage(item, img_database, wx.TreeItemIcon_Normal)
				self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.Arbol)
	
	def OnSelChanged(self,event):
		items =  event.GetItem()
		db_nodo = self.Arbol.GetItemText(items)
		self.item_selected = db_nodo

		if db_nodo != 'Databases':
			if self.check_is_database(items) == 1:
				print(db_nodo)
				self.database_active = db_nodo
				if self.database_old_selected == '':
					self.database_old_selected = db_nodo
					self.object_item = self.items_database_list.get(db_nodo)
				else:
					self.database_old_selected = db_nodo
					self.Arbol.DeleteChildren(self.object_item)
					self.object_item = self.items_database_list.get(db_nodo)

				if self.database_active != '':
					self.add_tables_nodo(self.items_database_list.get(db_nodo), self.Arbol.GetItemText(items))
				self.option_menu = ['New Table', 'Drop DB']
			else:
				self.table_active = db_nodo
				self.option_menu = ['Select','Drop Table','Describe']
		else:
			self.option_menu = ['New DB', 'Refresh']

		self.popupmenu = wx.Menu()
		for text in self.option_menu:
			item = self.popupmenu.Append(-1, text)
			self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)
		self.Arbol.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)
	
	def check_is_database(self,db):
		for value in self.items_database_list.values():
			if value == db:
				return 1
	
	def OnPopupItemSelected(self, event):
		item = self.popupmenu.GetLabel(event.GetId())

	def OnShowPopup(self, event):
		pos = event.GetPosition()
		pos = self.ScreenToClient(pos)
		self.PopupMenu(self.popupmenu, pos)

	def add_tables_nodo(self,root,db_name):
		n = len(self.List_tables)
		if n == 0:
			pass
		else:
			self.List_tables = []

		rows = self.controller.get_tables(self.database_active)
		for row in rows:
			w = self.tree.AppendItem(root,str(row[0]))
			self.List_tables.append(row[0])

			self.tree.SetPyData(w, None)
			self.tree.SetItemImage(w, self.img_table, wx.TreeItemIcon_Normal)
	#Funciones
	def CheckConnection(self):
		data = self.Config.readConfig()

		self.connected = DBConnect(data[0],data[1],data[2],data[3])
		if self.connected.connectiondb() == True:
			self.is_connected = True
		else:
			wx.MessageBox(str(self.connected.connectiondb()), 'Info',wx.OK | wx.ICON_INFORMATION)
			self.ConnectionManager()
	
	def ConnectionManager(self, evt=''):
		NewBD = Dialog_Connection(self)
		NewBD.ShowModal()
		NewBD.Destroy()
		self.CheckConnection()

class Dialog_Connection ( wx.Dialog ):

	controller = Controller()
	config = Config()

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Administrator", pos = wx.DefaultPosition, size = wx.Size( 300,220 ), style = wx.DEFAULT_DIALOG_STYLE )

		datos = self.GetDataConfig()

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Conecction", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		self.m_staticText1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		bSizer1.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"HostName:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		gSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )

		self.txtHostname = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.txtHostname, 0, wx.ALL, 5 )
		self.txtHostname.SetValue(datos[0])

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"UserName:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		gSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.txtUsername = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.txtUsername, 0, wx.ALL, 5 )
		self.txtUsername.SetValue(datos[1])

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Password:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		gSizer1.Add( self.m_staticText4, 0, wx.ALL, 5 )

		self.txtPassword = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.txtPassword, 0, wx.ALL, 5 )
		self.txtPassword.SetValue(datos[2])

		bSizer1.Add( gSizer1, 1, wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.btnSave = wx.Button( self, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.btnSave, 0, wx.ALL, 5 )

		self.btnTest = wx.Button( self, wx.ID_ANY, u"Test", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.btnTest, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer2, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		self.Bind(wx.EVT_BUTTON, self.Save, self.btnSave)
		self.Bind(wx.EVT_BUTTON, self.testingConnection, self.btnTest)

	def GetDataConfig(self):
		data = self.config.readConfig()
		return data

	def testingConnection(self,evt):
		connected = DBConnect(self.txtHostname.GetValue(),self.txtUsername.GetValue(),self.txtPassword.GetValue(),"")
		if connected.connectiondb() == True:
			wx.MessageBox("Testing ok" , 'Info',wx.OK | wx.ICON_INFORMATION)
		else:
			wx.MessageBox(str(connected.connectiondb()), 'Info',wx.OK | wx.ICON_INFORMATION)
		
	def Save(self, evt):
		try:
			msg = self.config.writeConnection(self.txtHostname.GetValue(),self.txtUsername.GetValue(),self.txtPassword.GetValue(),"")
			wx.MessageBox("Correcto" , 'Info',wx.OK | wx.ICON_INFORMATION)
		except:
			wx.MessageBox("Error" , 'Info',wx.OK | wx.ICON_INFORMATION)

class about_panel( wx.Panel ):
	#controller = Controller()

	def __init__(self, parent ):
		wx.Panel.__init__ ( self, parent=parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )