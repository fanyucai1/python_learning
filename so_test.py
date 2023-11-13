# Copyright 2023 Illumina Inc, San Diego, CA
# yucai.fan@illumina.com

import os
import test
import argparse
import subprocess
import re


parser=argparse.ArgumentParser("")
parser.add_argument("-v","--vcf",help="vcf file",required=True)
parser.add_argument("-d","--db",help="directory contains database",required=True)
parser.add_argument("-o","--outdir",help="output directory",default=os.getcwd())
parser.add_argument("-p","--prefix",help="prefix of output")
parser.add_argument("-v","--version",help="reference version",choices=['hg19','hg38'])
parser.add_argument("-c","--chain")
args=parser.parse_args()

#############################################
if not os.path.exists(args.outdir):
    subprocess.check_call("mkdir -p %s"%(args.outdir),shell=True)

args.vcf=os.path.abspath(args.vcf)
if re.search('.vcf$', args.vcf):
    args.prefix = args.vcf.split("/")[-1].split(".vcf.gz")[0]

if re.search('.vcf.gz$',args.vcf):
    args.prefix = args.vcf.split("/")[-1].split(".vcf.gz")[0]
    if re.search('.hard-filtered.vcf.gz$',args.vcf):
        args.prefix=args.vcf.split("/")[-1].split(".hard-filtered.vcf.gz")[0]
#############################################
### online liftover:     https://www.ensembl.org/Homo_sapiens/Tools/AssemblyConverter

###format vcf using( 1-10297148-ATT-A(GRCh38)) https://primad.basespace.illumina.com
out=args.outdir+"/"+args.prefix

###Liao W W, Asri M, Ebler J, et al. A draft human pangenome reference[J]. Nature, 2023, 617(7960): 312-324.
if os.system('which vcfdecompose')!=0 and os.system('which bcftools')!=0:
    print("please install software:\n\nRTG Tools link:https://github.com/RealTimeGenomics/rtg-tools/releases")
    print("bcftools:http://www.htslib.org/download/")

###multiallelic sites were split into biallelic records using bcftools norm -m -any
cmd="bcftools norm -m -any %s -o %s.biallelic_records.vcf"%(args.vcf,out)
subprocess.check_call(cmd,shell=True)

###The multi-nucleotide polymorphisms and complex indels were further decomposed into SNPs and simple indels
cmd="vcfdecompose --break-mnps --no-header --no-gzip --break-indels -i %s -o %s.format.vcf"%(args.vcf,out)
subprocess.check_call(cmd,shell=True)

infile=open("%s.format.vcf"%(out),"r")
for line in infile:
    line = line.strip()
    if not line.startswith("#"):
        array=line.split("\t")
        chr=array[0]
        pos=array[1]
        ref=args[3]
        all=args[4]
        test.output(args.database,args.chr,args.pos,args.ref,args.alt)

def liftover(in_vcf,chain,reference,version,outdir):
    cmd="java -jar picard.jar LiftoverVcf I=input.vcf O=lifted_over.vcf CHAIN=b37tohg38.chain REJECT=rejected_variants.vcf R=reference_sequence.fasta"