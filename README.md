# paf2pav - linearising a pangenome graph

This repository contains instructions for linearising a pangenome graph by generating a PAF file and converting it to a PAV binary matrix for use with [Panache](https://github.com/SouthGreenPlatform/panache)

## Generating the PAF file:

The PAF file is derived from a pangenome graph generated using [PGGB](https://github.com/pangenome/pggb). An [ODGI](https://github.com/pangenome/odgi) graph or  GFA graph is expected. 

```
reference_prefix='Morex'
odgi build -g pangenome.gfa -o pangenome.og

#Obtain all query paths except the reference
odgi paths -i pangenome.og -L | grep -v ${reference_prefix} > query_paths.txt

#Obtain the reference path name
reference=$(odgi paths -i pangenome.og -L | grep ${reference_prefix})

#Generate the PAF file with a single reference path and multiple query paths
odgi untangle -t 10 -i pangenome.og -Q query_paths.txt -r ${reference} -p > pangenome.paf
```

## Generate the PAV binary matrix given the PAF file

Run the script ```paf2pav.py``` in this repository with the PAF file to generate a PAV binary matrix tsv file, formatted to be compatible with Panache.

```
paf2pav.py -i pangenome.paf -o pangenome_pav.tsv
```
