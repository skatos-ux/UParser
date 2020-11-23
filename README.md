## Description :pushpin:
UParser is an XML large file parser written in python 3.7

<img src="https://img.shields.io/badge/stability-stable-success"
     alt="stability badge"
     style="float: left; margin-right: 10px;" 
/>
<img src="https://img.shields.io/badge/unitary--tests-work--in--progress-lightgrey"
     alt="unitary-tests badge"
     style="float: left; margin-right: 10px;" 
/>

## Usage :zap:
```bash
python ./XML_uparser.py [-p ProcessesNb] [-m WriteLimit] [-n OutFileNb] outDir tag inputFile
```
ProcessesNb
: The maximum number of processes running at the same time (default: 12)

WriteLimit
: The maximum number of lines each process can write at a time (default: 200)

OutFileNb
: The maximum number of output files (default: 200)

outDir
: the output directory

tag
: The tag to retrieve

inputFile
: The path to the input file

## Examples :books:
```bash
python ./XML_uparser.py -p 12 -m 200 -c 200 splits <author> dblp.xml
```
{ 12, 200, 200 } is my optimum configuration running : 
- i7 8cores
- 8Go RAM
- HDD

Parsing takes approximately between 10 and 40 seconds to parse ~3Go

```bash
python ./XML_uparser.py -p 12 -m 200 -c 200 splits <author> dblp.xml
python ./XML_uparser.py splits <author> dblp.xml
```
