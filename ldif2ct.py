#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Title:        ldif2ct.py
# Author:       Bevan Koopman <bevan.koopman@gmail.com>
# Created on:   March 30, 2008
#
# Small script converting a LDIF addressbook to contacts format. Prints
# the output to stdout.
#
# Usage: ldif2ct.py LDIF_FILE
#
#==============================================================

import sys, os

class Ldif2ct:
	def __init__(self, ldifFile):
		contacts = []
		contact = {}
		fh = open(ldifFile)
		for line in fh:
			split = line.split(":", 2)
			if len(split) > 1:
				contact[split[0].strip().lower()] = split[1].strip()
			else:
				contacts.append(Contact(contact))
				contact = {}
		
		fh.close()

		for c in contacts:
			if c.isPerson():
				print c.getName()+"; "+c.getMail()+"; "+c.getWPhone()+"; "+c.getHPhone()+"; "
				
class Contact:
	def __init__(self, data):
		self.data = data

	def isPerson(self):
		return ("givenname" in self.data) and ("sn" in self.data)

	def getName(self):
		if self.isPerson():
			return self.data["givenname"]+" "+self.data["sn"]

	def getMail(self):
		if "mail" in self.data:
			return self.data["mail"]
		else:
			return ""
	
	def getHPhone(self):
		numbers = ""
		if "mobile" in self.data:
			numbers = self.data["mobile"]
		if "homephone" in self.data:
			numbers = numbers + ", " + self.data["homephone"]
		return numbers		
	
	def getWPhone(self):
		if "telephonenumber" in self.data:
			return self.data["telephonenumber"]
		else:
			return ""

def main():
	# checks args
	if len(sys.argv) < 2:
		print "No ldif file supplied"
		printUsage()
	elif not os.path.exists(sys.argv[1]):
		print "No such ldif file: "+sys.argv[1]
	else:
		lp = Ldif2ct(sys.argv[1])

def printUsage():
	print "Usage: ldif2ct ldif-file"

main()
