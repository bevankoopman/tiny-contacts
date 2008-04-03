#!/usr/bin/env python
#
# Title:        contacts.py
# Author:       Bevan Koopman <bevan.koopman@gmail.com>
# Created on:   May 7, 2004
#
# Small script for managing list of personal contacts from a contacts text file
#
# Usage: contacts.py [OPTIONS] QUERY1,...,N
#   Options:
#        -h or -help:    diplay usage information
#        -s:             short listing of results (default)
#        -l:             long listing of results
#        -f <file>:      use other contacts file
#        -n:             input new contact
#        -e:             open the contact file using $EDITOR
#        -html:          Translate the contact document to HTML
#        -abook:         output contact to pine address book format
#
# Format of contacts file:
#   - single entry per line
#   - each line: <name>; <email>; <wphone>; <hphone>; <address>
#   - e.g. Bilbo Baggins; bilbo@bagend.middle-earth; ; ; Bag End, Shire, Middle Earth
#
# CVS Details:
# $Source: $
# $Date:  $
# $Revision: $
#==============================================================

import os, sys, string

true = 1
false = 0

style="long"

contactsFile = "/home/bevan/doc/contacts"

def main():
	global contactsFile, style
	
	# print help
	if "-h" in sys.argv or "-help" in sys.argv:
		printUseage()
		return
	# add new contact
	if "-n" in sys.argv:
		addContact()
		return
	# output content as html to stdout
	if "-html" in sys.argv:
		printHTML()
		return
	# output contents as pine address book to stdout
	if "-abook" in sys.argv:
		printABook()
		return
	# edit the file using $EDITOR
	if "-e" in sys.argv:
		os.system("$EDITOR "+contactsFile)
		return
	
	# use different contacts file
	if "-f" in sys.argv:
		try:
			contactsFile = sys.argv[sys.argv.index("-f")+1]
			# remove options from command line args
			del sys.argv[sys.argv.index("-f")+1]
			del sys.argv[sys.argv.index("-f")]
		except IndexError:
			print "Error: No contact file specified"
			printUseage()
	

	# query contacts file
	if len(sys.argv) > 1:
		del sys.argv[0] # remove contact.py from command line args
		if "-s" in sys.argv:
			style = "short"
		query(sys.argv, style)

def query(keywords, style):
	try:
		file = open(contactsFile, "r")
		line = file.readline()
		results = []
		while line != "":
			match = false
			for keyword in keywords:
				if string.find(string.lower(line), keyword) != -1:
					match = true
			if match:
				results.append(parseContact(line))
			line = file.readline()
		file.close()

		# print the results
		for r in results:
			printContact(r, style)
			if style == "long":
				print "--"

		# print number of results
		if len(results) < 1:
			print "No match"
		elif len(results) > 1:
			print `len(results)`+" results found"
	except IOError:
		print "Could not access contacts file: "+contactsFile

def parseContact(line):
	values = string.split(line[:-1], "; ")
	contact = dict(zip(["name", "email", "wphone", "hphone", "address"], values))
	return contact

def printContact(contact, style):
	long = ""
	short = ""
	
	if contact["name"] != "":
		long = long+"Name: "+contact["name"]+"\n"
		short = short+contact["name"]+" | "
	if contact["email"] != "":
		long = long+"Email: "+contact["email"]+"\n"
		short = short+contact["email"]+" | "
	if contact["wphone"] != "":
		long = long+"Phone(W): "+contact["wphone"]+"\n"
		short = short+contact["wphone"]+" | "
	if contact["hphone"] != "":
		long = long+"Phone(H): "+contact["hphone"]+"\n"
		short = short+contact["hphone"]+" | "
	if contact["address"] != "":
		long = long+"Address: "+contact["address"]+"\n"
		short = short+contact["address"]+" | "

	if style == "long":
		print long[:-1]
	else:
		print short[:-3]

def addContact():
	name = raw_input("Name:")
	email = raw_input("Email:")
	wphone = raw_input("Phone(W):")
	hphone = raw_input("Phone(H):")
	address = raw_input("Address:")
	str = name+"; "+email+"; "+wphone+"; "+hphone+"; "+address

	file = open(contactsFile, "a")
	file.write(str+"\n")
	file.close()

def printABook():
	file = open(contactsFile, "r")
	line = file.readline()
	while line != "":
		c = parseContact(line)
		if c["email"] != "":
			fname = string.split(c["name"])[0]
			femail = string.split(c["email"])[0]
			print fname+"\t"+c["name"]+"\t"+femail
		line = file.readline()

def printHTML():
	print '<html>'
	print '<head>'
	print '<title>Contacts</title>'
	print '</head>'
	print '<body>'
	print '<h1>Contacts</h1>'
	print '<table border="1" cellpadding="2" cellspacing="0" width="100%">'
	print '<tr bgcolor="gray">'
	print '<td>Name</td>'
	print '<td>Email</td>'
	print '<td>Phone(W)</td>'
	print '<td>Phone(H)</td>'
	print '<td>Address</td>'
	print '</tr>'
	file = open(contactsFile, "r")
	line = file.readline()
	while line != "":
		values = string.split(line[:-1], "; ")
		print '<tr bgcolor="lightgray" valign="top">'
		for v in values:
			print '<td>'
			if string.strip(v) == "":
				print "&nbsp"
			else:
				print v
			print '</td>'
		print '</tr>'
		line = file.readline()
	print '</table>'
	print '</body>'
	print '</html>'
	print '</body>'

def printUseage():
    print "Usage: contacts.py [OPTIONS] QUERY1,...,N"
    print "   Options:"
    print "\t-h or -help: \tdiplay usage information"
    print "\t-s: \t\tshort listing of results"
    print "\t-l: \t\tlong listing of results (default)"
    print "\t-f <file>: \tuse other contacts file"
    print "\t-n: \t\tinput new contact"
    print "\t-e: \t\topen the contact file using $EDITOR"
    print "\t-html: \t\tTranslate the contact document to HTML"
    print "\t-abook: \toutput contact to pine address book format"

if __name__ == '__main__':
	main()
