# paf2pav - linearising a pangenome graph

This repository contains instructions for linearising a pangenome graph by generating a PAF file and converting it to a PAV binary matrix for use with [Panache](https://github.com/SouthGreenPlatform/panache)

## Generating the PAF file

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

## Generate the PAV binary matrix

Run the script ```paf2pav.py``` in this repository with the PAF file to generate a PAV binary matrix tsv file, formatted to be compatible with Panache.

```
paf2pav.py -i pangenome.paf -o pangenome_pav.tsv
```

## Merging PAV binary matrices across chromosomes

If you have multiple PAV files across different chromosomes you'll need to merge them together.

First, format each PAV file so the headers are consistent, removing unnecessary chromosome names, version numbers etc.

Place the following in a bash script and modify as needed for your data:
```
for i in `ls pangenome_chr*H_pav.tsv`;do
	cat $i | sed 's/Morex_v3_//g' | sed 's/_v1.1_chr[1-9]H//g' | sed 's/_v1_chr[1-9]H//g' | sed 's/_v2_chr[1-9]H//g' > $i.mod.tsv
done
```

Second, run ```merge_pav.py``` from this repository on all the modified PAV files.

```
merge_pav.py -i "*.mod.tsv" -o merged_pangenome_pav_matrix.tsv
```

Third, you may need to filter the PAV binary matrix to retain only variations intersecting with gene regions (using bedtools intersect) and above a certain size to reduce processing overhead by Panache, and remove unnecessary small variants (SNPs and small INDELs) which would be too difficult to see on a large scale.
```
#Filter out variaitons not intersecting with gene regions
bedtools intersect -a merged_pangenome_pav_matrix.tsv -b Morex.gff > merged_pangenome_pav_matrix.overlaps.tsv

#Filter out any variation below 300bp
cat merged_pangenome_pav_matrix.overlaps.tsv | awk '{if (($3-$2) > 199) print $0}' > merged_pangenome_pav_matrix.overlaps.filtered.tsv
```
