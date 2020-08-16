#!/bin/sh

echo $PATH | grep -q "texlive/latest/bin"

if [ $? -eq 0 ]; then
  export PATH=/afs/cern.ch/sw/XML/texlive/latest/bin/x86_64-linux:$PATH
fi

echo ""
echo "Compiling latex"
echo ""

pdflatex DumpPlots.tex 
pdflatex DumpPlots.tex 

cp DumpPlots.pdf  ~/EOS/www/PileUpID_LO_v4.pdf

echo ""
echo "Removing other files"
echo ""
rm -rvf *.aux *.lof *.log *.out *.toc *.nav *.snm
