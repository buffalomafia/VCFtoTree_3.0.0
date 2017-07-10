#! /bin/bash

## load/download the reference sequence from the given address
## load/download the vcf file specified by the user
## then build the alignment, or further build the tree

## Usage: ./otheranimals.sh refaddress vcfaddress chr start end num treebuild


## address for the reference sequence,  in XX.fa.gz
refaddress=$1
## address for your vcf file.
vcfaddress=$2

## change this to your chromosome number
chr=$3
## change this to the start position of your region
start=$4
## change this to the end position of your region
end=$5
## How many species do you have?
num=$6

## Do you want to build the tree?
treebuild=$7

echo "The region of your interest: chr"$chr":"$start"-"$end". Have fun!"

mkdir ../../../VCFtoTree_Output_otherSpecies

## prepare reference sequence for your chosen chromosome
if [[ $refaddress == *"http://"* ]]
then
    /usr/local/bin/wget $refaddress > chr$chr.fa.gz
else
    mv $refaddress > chr$chr.fa.gz
fi

gunzip -c chr$chr.fa.gz > chr$chr.fa
/usr/local/bin/samtools faidx chr$chr.fa
/usr/local/bin/samtools faidx chr$chr.fa chr$chr:$start-$end > REF_chr$chr.START$start.END$end.fa

ref=REF_chr$chr.START$start.END$end.fa

## prepare vcf file for the given region
if [[ $vcfaddress == *"http://"* ]]
then
    /usr/local/bin/wget $vcfaddress > chr$chr.vcf.gz
else
    mv $vcfaddress > chr$chr.vcf.gz
fi

/usr/local/bin/tabix -h -f chr$chr.vcf.gz
/usr/local/bin/tabix -h -f chr$chr.vcf.gz $chr:$start-$end > otherAnimal_chr$chr.START$start.END$end.vcf

vcffile=otherAnimal_chr$chr.START$start.END$end.vcf


## building the alignment
python Code/vcf2fasta_otheranimals.py $vcffile $ref $start $end $num ALI_otherAnimals.fa log.txt &
wait

echo "vcftofasta has run."

## Tree building

## TO BE CHANGED ACCORDING TO THE FINAL GUI

## If use FastTree
## If the user need to compile it:
gcc -DUSE_DOUBLE -O3 -finline-functions -funroll-loops -Wall -o FastTree FastTree.c -lm
chmod +x Code/FastTree
Code/FastTree -gtr -gamma -nt ALI_otherAnimals.fa > ALI_otherAnimals.newick &
wait

## If use RAxML
python Code/fas2phy.py ALI_otherAnimals.fa ALI_otherAnimals.phy
chmod +x Code/raxmlHPC-PTHREADS-SSE3
Code/raxmlHPC-PTHREADS-SSE3 -T 2 -n YourRegion -s ALI_otherAnimals.phy -mGTRGAMMA -p 235 -N 2 &
wait
mv RAxML_bestTree.YourRegion RAxML_bestTree.YourRegion.newick &
wait

## finishing up:
shopt -s extglob
mv !(VCFtoTree.py|README.md|Code) ../../../VCFtoTree_Output/
open ../../../VCFtoTree_Output/

echo "All done, Erica is a genius."