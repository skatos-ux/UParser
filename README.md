## Description :pushpin:
UParser is an XML large file parser written in python 3.7
## Usage :zap:
```bash
python ./XML_uparser.py [-p ProcessesNb] [-m WriteLimit] [-c CopyChunkSize] tag inputFile
```
ProcessesNb
: The maximum number of processes running at the same time (default: 12)

WriteLimit
: The maximum number of lines each process can write at a time (default: 200)

CopyChunkSize
: The input file chunk size given to each processes (default: 200)

Tag
: The tag to retrieve

inputFile
: The path to the input file
## Examples :books:
```bash
python ./XML_uparser.py -p 12 -m 200 -c 200 <author> dblp.xml
```
{ 12, 200, 200 } is my optimum configuration running : 
- i7 8cores
- 8Go RAM
- HDD

Parsing takes approximately between 10 and 40 seconds to parse ~3Go

```bash
python ./XML_uparser.py -p 12 -m 200 -c 200 <author> dblp.xml
python ./XML_uparser.py <author> dblp.xml
```