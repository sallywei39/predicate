import sys
import re
from sets import Set
import urllib2
import os

def find_predicate(device):
  review_file = 1
  url = "http://www.accessdata.fda.gov/cdrh_docs/reviews/" + device + ".pdf"

  file_name = url.split('/')[-1]
  try:
    u = urllib2.urlopen(url)
  except urllib2.HTTPError, e:
    review_file = 0

  if review_file == 0:
    pdfnum = device[1:3]
    if device[1:3] == "00" or device[1:3] == "01":
      pdfnum = ""
    elif device[1:2] == "0":
      pdfnum = device[2]
    url = "http://www.accessdata.fda.gov/cdrh_docs/pdf" + pdfnum + "/" + device + ".pdf"

    try:
      u = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
      print device + " File not found"
      return
  '''
  f = open(file_name, 'wb')
  meta = u.info()
  file_size = int(meta.getheaders("Content-Length")[0])

  file_size_dl = 0
  block_sz = 8192
  while True:
    buffer = u.read(block_sz)
    if not buffer:
      break
  
    f.write(buffer)
  f.close()
  '''

  print "%s review: %s" % (device, review_file)


PMNfile = open(sys.argv[1])
next(PMNfile)

for line in PMNfile:
  n = 14
  start = line.find('|')
  while start >= 0 and n > 1:
    start = line.find('|', start + 1)
    n -= 1
  end = line.find('|', start + 1)
  if line[start + 1:end] == "Summary":
    if line[0] != 'K' or not (line[1:7]).isdigit():
      print "device Knumber error"
    else:
      find_predicate(line[0:7])
  elif line[start + 1:end] == "Statement":
    print line[0:7] + " Summary not available"
  else:
    print line[0:7] + " Statment and summary error!"

PMNfile.close()
