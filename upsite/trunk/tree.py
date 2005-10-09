#!/usr/bin/env python
#-*- coding: iso-8859-1 -*-

## tree.py ( Tree Data Structure )
## version 0.hu
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

class Tree :
	def __init__(self, rootObj) :
		self.rootItem = Node(rootObj)
		
class Node :
	""" 
	Un noeud 
	============
	Contient 0, 1 ou plusieurs liens vers d'autres noeuds ou feuilles (une feuille est un noeud sans fils)
	"""
	def __init__(self, obj) :
		self.__object = obj
		self.__father = None
		self.__d = []
		
	def Get(self) :
		return self.__object
	
	def Set(self, obj) :
		self.__object = obj

	def GetFather(self) :
		return self.__father
		
	def __SetFather(self, node) :
		self.__father = node
		
	def Add(self, node) :
		node.__SetFather(self)
		self.__d.append(node)
	
	def GetChilds(self) :
		return self.__d
		
	#~ def GetChild(self, name) :
		#~ for node in self.__d :
			#~ if node.GetName() == name :
				#~ return node
		#~ return None
		
	def IsLeaf(self) :
		return len(self.__d) == 0
	
	def IsTrueNode(self) :
		return len(self.__d) > 0
		