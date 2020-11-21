## Description :pushpin:
UParser is an XML large file parser written in python 3.7
## Usage :zap:
```bash
python ./XML_uparser.py [ProcessesNb] [WriteLimit] [CopyChunkSize]
```
ProcessesNb
: The maximum number of processes running at the same time

WriteLimit
: The maximum number of lines each process can write at a time

CopyChunkSize
: The input file chunk size given to each processes