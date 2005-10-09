#!/usr/bin/env python
#-*- coding: iso-8859-1 -*-

## gui.py ( gui program )
## Copyright © 2005 Viallard Anthony, homer242@gmail.com

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

# python
import exceptions, os

# wxpython
import wx

# me
import utils
from upsite import *

## GLOBAL
pwdProject = ""
configFile = "_upsite" # pickle structure

projectOpen = False
projectModif = False
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
def showInfo(parent, message, titre) :
	dg = wx.MessageDialog(parent, message, titre, style=wx.ICON_INFORMATION|wx.OK)
	dg.ShowModal()
	dg.Destroy()
	
def showError(parent, message, titre) :
	dg = wx.MessageDialog(parent, message, titre, style=wx.ICON_ERROR|wx.OK)
	dg.ShowModal()
	dg.Destroy()
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################	
class DialogConfig(wx.Dialog) :
	def __init__(self, parent, title) :
		wx.Dialog.__init__(self, parent, -1, title)
		
		# sizer
		topSizer = wx.BoxSizer(wx.VERTICAL)
		formSizer = wx.GridSizer(cols=2)
		
		# input
		self.inputFtpHost = wx.TextCtrl(self, -1)
		self.inputFtpPort = wx.TextCtrl(self, -1, "21")
		self.inputFtpUser = wx.TextCtrl(self, -1)
		self.inputFtpPass = wx.TextCtrl(self, -1, style=wx.TE_PASSWORD)
		self.inputFtpPwd = wx.TextCtrl(self, -1)
		
		# sizer
		formSizer.Add(wx.StaticText(self, -1, "Ip serveur ftp : "), 0, wx.ALL, 5)
		formSizer.Add(self.inputFtpHost, 0, wx.ALL, 5)
		formSizer.Add(wx.StaticText(self, -1, "Port serveur ftp : "), 0, wx.ALL, 5)
		formSizer.Add(self.inputFtpPort, 0, wx.ALL, 5)
		formSizer.Add(wx.StaticText(self, -1, "Login : "), 0, wx.ALL, 5)
		formSizer.Add(self.inputFtpUser, 0, wx.ALL, 5)
		formSizer.Add(wx.StaticText(self, -1, "Mot de passe : "), 0, wx.ALL, 5)
		formSizer.Add(self.inputFtpPass, 0, wx.ALL, 5)
		formSizer.Add(wx.StaticText(self, -1, "Repertoire dépot : "), 0, wx.ALL, 5)
		formSizer.Add(self.inputFtpPwd, 0, wx.ALL, 5)
		
		topSizer.Add(formSizer, 0, wx.ALL, 5)
		topSizer.Add(self.CreateButtonSizer(wx.CANCEL|wx.OK), 0, wx.ALIGN_CENTER|wx.ALL, 5)
		
		self.SetSizer(topSizer)
		topSizer.Fit(self)
	
	def getFtpHost(self) :
		return self.inputFtpHost.GetValue()
		
	def getFtpPort(self) :
		return int(self.inputFtpPort.GetValue())
		
	def getFtpUser(self) :
		return self.inputFtpUser.GetValue()
		
	def getFtpPass(self) :
		return self.inputFtpPass.GetValue()
		
	def getFtpPwd(self) :
		return self.inputFtpPwd.GetValue()
		
class MainFrame(wx.Frame) :
	# id
	IDMENU_NEWPROJ = wx.NewId()
	IDMENU_OPENPROJ = wx.NewId()
	IDMENU_SAVEPROJ = wx.NewId()
	IDMENU_QUIT = wx.NewId()
	IDMENU_ADDFILES = wx.NewId()
	IDMENU_ADDDIR = wx.NewId()
	IDMENU_UPLOAD = wx.NewId()
	
	IDTB_NEWPROJ = wx.NewId()
	IDTB_OPENPROJ = wx.NewId()
	IDTB_RECPROJ =wx.NewId()
	IDTB_ADDFILESPROJ = wx.NewId()
	IDTB_UPLOADPROJ = wx.NewId()
	
	def __init__(self, main, lastProject = None) :
		wx.Frame.__init__(self, None, -1, str(main.appname) + " v" + str(main.appversion), 
			size=(230, 320))

		self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE));
		
		# sizer
		topSizer = wx.BoxSizer(wx.HORIZONTAL)
		
		# menu
		self.menubar = wx.MenuBar()
		
		filemenu = wx.Menu()
		filemenu.Append(self.IDMENU_NEWPROJ, "Nouveau projet")
		filemenu.Append(self.IDMENU_OPENPROJ, "Ouvrir projet")
		filemenu.Append(self.IDMENU_SAVEPROJ, "Sauvegarder projet")
		filemenu.Append(self.IDMENU_QUIT, "Quitter")
		
		projmenu = wx.Menu()
		#~ projmenu.Append(self.IDMENU_ADDDIR, "Ajouter un dossier")
		#~ projmenu.Append(self.IDMENU_ADDFILES, "Ajouter fichiers")
		projmenu.Append(self.IDMENU_UPLOAD, "Uploader")
		
		self.menubar.Append(filemenu, "Fichier")
		self.menubar.Append(projmenu, "Projet")
		
		self.SetMenuBar(self.menubar)
		
		# toolbar
		self.toobar = self.CreateToolBar()
		
		tsize = (16,16)
		new_bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
		open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
		rec_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
		up_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DIR_UP, wx.ART_TOOLBAR, tsize)
		add_bmp = wx.ArtProvider.GetBitmap(wx.ART_ADD_BOOKMARK, wx.ART_TOOLBAR, tsize)
		
		self.toobar.AddSimpleTool(self.IDTB_NEWPROJ, new_bmp, "Nouveau projet")
		self.toobar.AddSimpleTool(self.IDTB_OPENPROJ, open_bmp, "Ouvrir projet")
		self.toobar.AddSimpleTool(self.IDTB_RECPROJ, rec_bmp, "Enregistrer projet")
		self.toobar.AddSeparator()
		self.toobar.AddSimpleTool(self.IDTB_ADDFILESPROJ, add_bmp, "Ajouter fichiers au projet")
		self.toobar.AddSimpleTool(self.IDTB_UPLOADPROJ, up_bmp, "Uploader projet")
		
		self.toobar.Realize()
		
		# tree
		self.tree = wx.TreeCtrl(self, -1)
		self.tree.AddRoot("projet")
		
		# chargement arbre
		if lastProject :
			self.project = lastProject
			try :
				self.project.openProject()
				self.populateWxTree() # on charge le projet
				projectOpen = True
			except IOError, detail :
				showError(self, "Impossible d'ouvrir le fichier projet !\nDetail : %s" % detail, "Erreur !")
			except :
				showError(self, "Impossible de charger le fichier de configuration du projet !", "Erreur !")
				
		# event
		self.Bind(wx.EVT_MENU, self.OnQuit, id=self.IDMENU_QUIT)
		self.Bind(wx.EVT_TOOL, self.OnNewProject, id=self.IDTB_NEWPROJ)
		self.Bind(wx.EVT_MENU, self.OnNewProject, id=self.IDMENU_NEWPROJ)
		self.Bind(wx.EVT_TOOL, self.OnOpenProject, id=self.IDTB_OPENPROJ)
		self.Bind(wx.EVT_MENU, self.OnOpenProject, id=self.IDMENU_OPENPROJ)
		self.Bind(wx.EVT_TOOL, self.OnRecProject, id=self.IDTB_RECPROJ)
		self.Bind(wx.EVT_MENU, self.OnRecProject, id=self.IDMENU_SAVEPROJ)
		self.Bind(wx.EVT_MENU, self.OnAddDir, id=self.IDMENU_ADDDIR)
		self.Bind(wx.EVT_TOOL, self.OnAddFiles, id=self.IDTB_ADDFILESPROJ)
		self.Bind(wx.EVT_MENU, self.OnAddFiles, id=self.IDMENU_ADDFILES)
		self.Bind(wx.EVT_TOOL, self.OnUpProject, id=self.IDTB_UPLOADPROJ)
		self.Bind(wx.EVT_MENU, self.OnUpProject, id=self.IDMENU_UPLOAD)
		
		self.tree.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnTreeRightClick) # for msw
		self.tree.Bind(wx.EVT_RIGHT_UP, self.OnTreeRightClick) # for gtk
		
		# sizer
		topSizer.Add(self.tree, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
		
		self.SetSizer(topSizer)

	def OnQuit(self, event) :
		self.Destroy()
	
	def OnNewProject(self, event) :
		# où se trouve le projet ?
		dlg = wx.DirDialog(self, "Choisissez le repertoire où se trouve le projet : ", style=wx.DD_DEFAULT_STYLE)
		if dlg.ShowModal() == wx.ID_OK :
			projectPath = Dir(dlg.GetPath())
			dlg.Destroy()
		else :
			dlg.Destroy()
			return
			
		# la configuration ftp
		dlg = DialogConfig(self, "Configuration FTP")
		if dlg.ShowModal() == wx.ID_OK :
			ftpHost = dlg.getFtpHost()
			ftpPort = dlg.getFtpPort()
			ftpUser = dlg.getFtpUser()
			ftpPass = dlg.getFtpPass()
			ftpPwd = dlg.getFtpPwd()
			dlg.Destroy()
		else :
			dlg.Destroy()
			return
		
		# où enregistrer le fichier de configuration ?
		dlg = wx.FileDialog(self, message="Sauvegarder le fichier de configuration du projet ... ",
			defaultFile="_upsite", style=wx.SAVE)
		
		if dlg.ShowModal() == wx.ID_OK :
			configFileProject = dlg.GetPath()
			
			# on ouvre le fichier (try ?)
			f = open(configFileProject, 'w')
			f.write("\n") # on écrit un truc
			f.close()
			
			# on sauvegarde dans le fichier xml l'endroit où se trouve ce fichier de configuration
			conf = ReadConfig("configuration.xml")
			conf.writeXml(configFileProject)
			
			# 
			self.project = Project(configFileProject)
			self.project.createProject(projectPath)
			self.project.ftphost = ftpHost
			self.project.ftpport = ftpPort
			self.project.ftpuser = ftpUser
			self.project.ftppass = ftpPass
			self.project.ftppwd = ftpPwd
			
			self.project.addDir(projectPath.pwd)
			
			self.populateWxTree()
		
		dlg.Destroy()
		
	def OnOpenProject(self, event) :
		# où est le fichier ?
		dlg = wx.FileDialog(self, message="Ouvrir le projet ... ",
			defaultFile="_upsite", style=wx.OPEN|wx.CHANGE_DIR)
		
		if dlg.ShowModal() == wx.ID_OK :
			path = dlg.GetPath()
			
			self.project = Project(path)
			self.project.openProject()
			
			self.populateWxTree()
		
		dlg.Destroy()
	
	def OnRecProject(self, event) :
		self.project.saveProject()
		
	def OnAddDir(self, event) :
		pass
		
	def OnAddFiles(self, event) :
		pass
		
	def OnUpProject(self, event) :
		self.project.upload()
		
	def OnTreeRightClick(self, event) :
		pass
		#~ menu = wx.Menu()
	
		#~ self.PopupMenu(menu, wx.DefaultPosition)
		#~ menu.Destroy()
	
	def OnPopupAdd(self, event) :
		pass
		
	def OnPopupDel(self, event) :
		pass
		
	def LoadFilesTree(self) :
		# chargement du fichier de configuration du site
		#~ if True : #try :
		self.project.openProject()
		#~ except Exception, detail :
			#~ # erreur ... oui
			#~ showError(self, "Erreur : Impossible de lire le fichier xml '%s', une erreur a été trouvé ! \nDetail : %s" % (self.project.projectFile, detail), "Erreur !")
			#~ return -1
			
		self.tree.Hide()
		
		# on fait le ménage
		self.tree.DeleteAllItems()
		
		# on explore et on ajoute
		self.__sub_loadFilesTree(self.project.fileTree.rootItem, self.tree.GetRootItem())
			
		self.tree.Expand(self.tree.GetRootItem())
		
		self.tree.Show()
		
	def __sub_loadFilesTree(self, treeNode, pwdParentNode) :
		child = self.tree.AppendItem(treeNode.GetName(), utils.getEndPwd(treeNode.GetName()))
		
		files = []
		for fileintree in treeNode.GetChilds :
			if fileintree.IsLeaf() :
				files.append(fileintree.GetName())
			else :
				self.__sub_loadFilesTree(fileintree, child)
				
		for file in files :
			self.tree.AppendItem(child, file)
			
		#~ for nom in os.listdir(pwdStr):
			#~ chemin = os.path.join(pwdStr,nom)
			#~ if os.path.isfile(chemin):
				#~ if nom != configFile :
					#~ files.append(nom)
			#~ elif os.path.isdir(chemin):
				#~ self.__sub_loadFilesTree(chemin, child)
		
	def populateWxTree(self) :
		self.tree.Hide()
		
		# on fait le ménage
		self.tree.DeleteAllItems()
		
		# on parcours l'arbre (objet python)
		rootItem = self.project.fileTree.rootItem
		
		self.__sub_populateWxTree(self.tree.GetRootItem(), rootItem)
		
		# expand
		self.tree.Expand(self.tree.GetRootItem())
		
		self.tree.Show()
		
	def __sub_populateWxTree(self, wxTreeNode, treeNode) :
		# on a affaire à un repertoire
		child = self.tree.AppendItem(wxTreeNode, getEndPwd(treeNode.Get().pwd))
		
		files = []
		for fileintree in treeNode.GetChilds() :
			if fileintree.IsLeaf() :
				files.append(fileintree.Get().name)
			else :
				self.__sub_populateWxTree(child, fileintree)
				
		for file in files :
			self.tree.AppendItem(child, file)
			