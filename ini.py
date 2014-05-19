#!/usr/bin/python
from bs4 import BeautifulSoup
from urllib2 import urlopen
import sys, types

############
# Constants
############
baseURL = "http://thepiratebay.se" 
baseURLSearch = "http://thepiratebay.se/search/"
topSeed = "/0/7/0"
bottomSeed = "/0/8/0"
topLeech = "/0/9/0"
bottomLeech = "/0/10/0"
top100HDMovies = "/top/207"
top100HDTV = "/top/208"
top100SDTV = "/top/205"
top100SDMovies = "/top/201"
replaceChar = "%20"
clformat1 = 'python ini.py -{s,S,l,L} "NAME" '
clformat2 = 'python ini.py -{m,M,t,T} '
clist1 = [ '-s','-S','-l','-L']
clist2 = [ '-m','-M','-t','-T']
url = ''
opt = ''

#################
#DS and Functions
#################

# Holds torrent information
class tpbdata:
	title =""
	desc = ""
	user = ""
	seed = ""
	leech = ""
	date = ""
	size = ""

# Prints all torrent information
def printAll(datalist):
        for index,foo in enumerate(datalist):
            print "[INDEX] " , index
            print "[TITLE] " + foo.title.encode('utf8')
            print "[SEED] " + foo.seed.encode('utf8')
            print "[LEECH]" + foo.leech.encode('utf8')
            print "[SIZE]"  + foo.size.encode('utf8')
            print "[DATE]" + foo.date.encode('utf8')
            print "[USER] " + foo.user.encode('utf8') + "\n"

#Adds all torrents on specified page to the datalist
def addPageLinks(soup,datalist):
    for base in soup.findAll("div" , {"class" : "detName"}):
		try:
			temp = tpbdata()
			temp.title = base.a.contents[0]
			# Seperate the general info from csv format
			listDesc = base.parent.font.contents[0].split(',')
		#	print temp.title, listDesc
			temp.size = listDesc[1].replace("Size",'')
			temp.date = listDesc[0].replace("Uploaded ","") 
			temp.seed = base.parent.find_next_siblings()[0].string
			temp.leech= base.parent.find_next_siblings()[1].string
			temp.desc = base.parent.font.contents[0]
			temp.user = base.parent.font.a.contents[0]
		except AttributeError:
			temp.user = 'Anonymous'
		datalist.append(temp)

#Find the line numbers
def findLineNumbers():
   lastPage = 1
   for divCenter in soup.findAll("div", {"align" : "center"}):
    for line in divCenter.children:
        if line != '\n' and line != ' ':
            lineNum = line.string
            if  lineNum is not None and ('xa0' not in repr(lineNum) or '1\\'in repr(lineNum)):
                lastPage = int(lineNum)
   return lastPage

#Add all the torrents from all the specified pages
def addAllPageLinks(lastPage): 
	try:
		if arglen == 2:
			soup = BeautifulSoup(urlopen(url))
			addPageLinks(soup,datalist)
		elif arglen == 3:	
			for pages in range(0,lastPage):
				# Convert to list to replace the page no. char
				optlist = list(opt)
				optlist[1] = pages
				optstring = ''.join([str(i) for i in optlist])
				tempurl = baseURLSearch + sys.argv[2] + optstring
				soup =  BeautifulSoup(urlopen(tempurl))
				addPageLinks(soup,datalist)
	except:
		print "Error occured when mining the page links. Links might not exist"
		sys.exit()

def endProgram():
	print "Enter in one of the valid formats BELOW"
	print clformat1
	print clformat2
	sys.exit()

#####################
# Main Body of Script
#####################

arglen = len(sys.argv)

if arglen == 3 and sys.argv[1] in clist1 and isinstance(sys.argv[2], basestring):
	opt = ""
	if sys.argv[1] == '-s':
		opt = bottomSeed
	elif sys.argv[1] == '-S':
		opt = topSeed
	elif sys.argv[1] == '-l':
		opt = bottomLeech
	elif sys.argv[1] == '-L':
		opt = topLeech
	url = baseURLSearch + sys.argv[2].replace(' ',replaceChar) + opt
elif arglen == 2 and sys.argv[1] in clist2:
	if sys.argv[1] == '-m':
		opt = top100SDMovies
	elif sys.argv[1] == '-M':
		opt = top100HDMovies
	elif sys.argv[1] == '-t':
		opt = top100SDTV
	elif sys.argv[1] == '-T':
		opt = top100HDTV
	url = baseURL + opt	
else:
	endProgram()

#Construct the initial soup object
soup = BeautifulSoup(urlopen(url))

#Construct the array of torrent links
datalist = []

# Assume minimum 1 page
#lastPage = 1
print url
#Find all page numbers and add their data to list
pagenum = findLineNumbers()
#print pagenum
addAllPageLinks(pagenum)

# Output scraped data
printAll(datalist)
