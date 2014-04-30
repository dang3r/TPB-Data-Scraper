TPB-Data-Scraper
================
This simple python script allows you to pull torrent data from thepiratebay.org. It is able to retrieve the torrent title, size, date uploaded, uploader name, the number of current leechees and the number of current seeders. 

It utilizes the BeautifulSoup4 library for scraping the data and Python 2.7.X.

Command line arguments are the only form of input for tpbds. There are two formats for specifying what data to pull and output.

1. python ini.py -{s,S,l,L} "NAME" 
2. python ini.py -{m,M,t,T} 

The first format allows you to specify how to sort the data and the search term.
s = sort by lowest number of seeders
S = sort by highest number of seeders
l = sort by lowest number of leeches
L = sort by highest number of Leeches
"Name" = the specified torrent search name

The second format lets you retrieve the current top 100 for the following categories.
m = top 100 SD Movies
M = top 100 HD Movies
t = top 100 SD TV Show
T = top 100 HD TV Shows

After executing the script, the data is outputted to your shell. Redirect to a text file for storage if necessary (ie. python ini.py -s "godel" > sampleout.txt)
