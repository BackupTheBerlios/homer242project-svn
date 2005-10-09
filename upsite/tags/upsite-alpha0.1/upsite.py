#!/usr/bin/env python
#-*- coding: iso-8859-1 -*-

## upsite.py ( main program )
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
import sys, os
import pickle
from ftplib import FTP

# wxpython
import wx

# xml
from xml.dom.minidom import parse

# exception
import exceptions

#
import gui
from tree import *
from utils import *

__appname__ = "upSite"
__appversion__ = "0.1"

##############################################################################

class File :
	def __init__(self, name, modtimestamp) :
		self.name = name
		self.modtimestamp = modtimestamp

class Dir :
	def __init__(self, pwd) :
		self.pwd = pwd
		
class Project :
	def __init__(self, projectFile) :
		self.projectFile = projectFile
		self.fileTree = None
		
		self.ftphost = ""
		self.ftpport = 21
		self.ftpuser = ""
		self.ftppass = ""
		self.ftppwd = ""
		
	def openProject(self) :
		# on ouvre le fichier
		f = open(self.projectFile, 'rb') # b=> binaire
		
		project = pickle.load(f) # vive pickle !
		
		self.fileTree = project.fileTree
		self.ftphost = project.ftphost
		self.ftpport = project.ftpport
		self.ftpuser = project.ftpuser
		self.ftppass = project.ftppass
		self.ftppwd = project.ftppwd
	
		f.close()
		
	def saveProject(self) :
		f = open(self.projectFile, 'w+b')
		
		pickle.dump(self, f)
		
		f.close()
		
	def createProject(self, dirItem) :
		self.fileTree = Tree(dirItem)
		
	def addFiles(self, files) :
		pass
		
	def addDir(self, pwd) :
		# pour l'instant, on enregistre direct dans la racine
		# aller hop, on parcours le dossier
		self.__sub_addDir(self.fileTree.rootItem, pwd)
		
	def __sub_addDir(self, treeNode, pwd) :
		for nom in os.listdir(pwd):
			chemin = os.path.join(pwd,nom)
			if os.path.isfile(chemin):
				treeNode.Add( Node( File(nom, 0) ) )
			elif os.path.isdir(chemin):
				nodeDir = Node(Dir(chemin))
				treeNode.Add(nodeDir)
				self.__sub_addDir(nodeDir, chemin)
		
	def upload(self) :
		"""
		Fonction d'upload. Compare les dates de modifications
		"""
		# connexion au serveur ftp
		self.ftpd = FTP()
		self.ftpd.connect(self.ftphost, self.ftpport)
		self.ftpd.login(self.ftpuser, self.ftppass)
		
		self.__openFtpDir(self.ftppwd)
		# let's rock !
		self.__sub_upload(self.fileTree.rootItem)
		
		self.ftpd.quit()
		
		# on sauvegarde les modifs
		self.saveProject()
		
	def __sub_upload(self, treeNode) :
		# on parcours l'arbre
		for node in treeNode.GetChilds() :
			if node.IsLeaf():
				# on compare la date
				file = node.Get()
				fileName = treeNode.Get().pwd + os.sep + file.name
				lastModts = os.stat(fileName)[7]
				if lastModts > file.modtimestamp :
					print "Upload -> " + fileName
					# upload ftp !
					f = open(fileName, 'rb') # on ouvre le fichier pour le transfert
					# on change de repertoire sur le ftp
					self.__openFtpDir(self.ftppwd+getRestPwd(self.fileTree.rootItem.Get().pwd, treeNode.Get().pwd))
					self.ftpd.storbinary("STOR "+file.name, f)
					file.modtimestamp = lastModts
				continue
			else :
				# repertoire
				self.__sub_upload(node)
	
	def __createFtpDir(self, pwd) :
		self.ftpd.cwd("/")
		ftppwd = pwd.lstrip("/")
		for folder in ftppwd.split('/') :
			try :
				self.ftpd.cwd(folder)
			except :
				self.ftpd.mkd(folder)
				self.ftpd.cwd(folder)
				
	def __openFtpDir(self, pwd) :
		pwd = pwd.replace("\\", "/") # encore windows qui fait chier !
		#~ print pwd
		self.__createFtpDir(pwd)
		
##############################################################################
class ReadConfig :
	lastproject = ""
	
	def __init__(self, filename) :
		self.filename = filename
		
	def readXml(self) :
		self.doc = parse(self.filename)
		ElemDB = self.doc.documentElement.getElementsByTagName("history")[0]
		
		self.lastproject = ElemDB.getAttribute("lastproject")
		
	def writeXml(self, lastProject="") :
		f = file(self.filename, "w")
		
		f.write("<configuration>\n")
		f.write("\t<history lastproject=\""+str(lastProject)+"\" />\n")
		f.write("</configuration>\n")
			
		f.close()
		
		
if __name__ == "__main__" :

	class GApp(wx.App) :
		def OnInit(self) :
		## global variables
			global __appname__, __appversion__
			self.appname = __appname__
			self.appversion = __appversion__
		
			## lecture du fichier de configuration
			## par defaut :
			##      host = localhost
			##      port = 5432
			##      database = lanmanager
			##      user = 
			##      password = 
			conf = ReadConfig("configuration.xml")
			try :
				conf.readXml()
			except exceptions.Exception, detail:
				dg = wx.MessageDialog(None, "Impossible de charger la configuration (une erreur se trouve dans le fichier configuration.xml !)\nErreur : %s \n\nVoulez-vous remettre à defaut le fichier de configuration ?" % detail, "Erreur", style=wx.ICON_ERROR|wx.YES_NO)
				if dg.ShowModal() == wx.ID_YES :
					conf.writeXml()
				else :
					dg.Destroy()
					sys.exit(1)
				dg.Destroy()
	
			## si tout vas bien, on lance l'application graphique
			if conf.lastproject :
				project = Project(conf.lastproject)
				frame = gui.MainFrame(self, project)
			else :
				frame = gui.MainFrame(self)
			frame.Show(True)
			self.SetTopWindow(frame)
			return True

	## on lance l'application
	app = GApp(False)
	## mainLoop
	app.MainLoop()
