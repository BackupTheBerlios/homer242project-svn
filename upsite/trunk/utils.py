#!/usr/bin/env python
#-*- coding: iso-8859-1 -*-

## utils.py ( util fonctions )
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

import re, os

def getEndPwd(pwd) :
	sep = os.sep 
	if sep == "\\" :
		sep = "\\\\"
		
	reg = ".*"+sep+"([^"+sep+"]+)$"
	reg_c = re.compile(reg)
	result = re.search(reg_c, pwd)
	if result and result.group(1) :
		return result.group(1)
	else :
		return pwd
		
		
def getRestPwd(pwdstart, pwdend) :
	return pwdend.lstrip(pwdstart)
	