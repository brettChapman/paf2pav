# paf2pav 

This repository contains instructions for converting a PAF file to a PAV binary matrix for use with [Panache](https://github.com/SouthGreenPlatform/panache)

## Generating the PAF file:

The PAF file is derived from a [PGGB](https://github.com/pangenome/pggb) pangenome graph given an [ODGI](https://github.com/pangenome/odgi) graph or generated from a GFA.

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

##Run the script in this repository with the PAF file to generate a PAV binary matrix tsv file.

```
paf2pav.py -i pangenome.paf -o pangenome_pav.tsv 
```
