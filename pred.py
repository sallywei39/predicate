import sys
import re
from sets import Set
import urllib2
import os

rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE|re.DOTALL)

def find_predicate(device, TREEfile, SUSfile):
  os.system("pdftotext -raw " + device + ".pdf")

  if os.path.getsize(device + '.txt') < 20:
    data = file(device + '.pdf', "rb").read()
    page_num = len(rxcountpages.findall(data))
    os.system ("#!/bin/sh\nSTARTPAGE=1\nENDPAGE=%s\n" % (page_num) + 
    "SOURCE=" + device + ".pdf\nOUTPUT=" + device + ".txt\ntouch $OUTPUT\n" +
    "for i in `seq $STARTPAGE $ENDPAGE`; do\n" + 
    "  convert -monochrome -density 600 $SOURCE\[$(($i - 1 ))\] page.tif\n" +
    "  echo processing page $i\n" +
    "  tesseract page.tif tempoutput -l eng -psm 6\n" +
    "  cat tempoutput.txt >> $OUTPUT\n" +
    "done")

  sumfile = open(device + '.txt')

  '''predicates = re.findall(r"(?:(?:\([Kk]\))|[kK])(?:\s*\d){6}", sumfile.read())'''

  Knumbers = Set()
  SUSfile.write('*' + device + '*\n')
  for line in sumfile:
    printline = 0
    exps = re.findall(r"(?:(?:\([Kk]\))|[kK])(?:\s*\S){6}", line)
    for exp in exps:
      num_digits = len(re.findall(r"\d", exp))
      if num_digits >= 3 and num_digits <= 5:
        printline = 1
      elif num_digits == 6:
        exp = exp.replace("(", "")
        exp = exp.replace(")", "")
        exp = "".join(exp.split())
        if exp.upper() != device:
          Knumbers.add(exp.upper())
    '''
    exps = re.findall(r"[^Kk](?:\s*\S){6}", line)
    for exp in exps:
      num_digits = len(re.findall(r"\d", exp[1:]))
      if num_digits >=5:
        printline = 1
    '''
    if printline == 1:
      SUSfile.write(line)

  TREEfile.write(device + ': ')
  if(len(Knumbers) == 0):
    TREEfile.write("Predicates not found")
  else:
    for Knumber in Knumbers:
      TREEfile.write(Knumber + " ")
  TREEfile.write('\n')

  sumfile.close()


SUMfile = open(sys.argv[1])
TREEfile = open(sys.argv[2], 'w')
SUSfile = open(sys.argv[3], 'w')
TREEfile.write("Device Knumber: Predicates Knumber\n")

for line in SUMfile:
  if line[8] == 'r':
    find_predicate(line[0:7], TREEfile, SUSfile)
  elif line[8] == 'F':
    TREEfile.write(line[0:7] + ": File not found\n")
  elif line[9] == 'u':
    TREEfile.write(line[0:7] + ": Summary not available\n")
  elif line[9] == 't':
    TREEFILE.write(line[0:7] + ": Statment and summary error!\n")

SUMfile.close()
TREEfile.close()
SUSfile.close()
