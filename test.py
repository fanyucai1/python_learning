# cython: language_level=3
import subprocess
from cryptography.fernet import Fernet
import os,re

def output(encrypt_file,vcf,chr,pos,ref,alt):
    ########################################################数据库文件
    key = b'NO2GPH6XMyLvIQiKAL44kSkLyw2dL0GvfqqBD97CUBk='
    f = Fernet(key)
    #读取加密文件
    with open(encrypt_file, 'rb') as file:
        encrypted = file.read()
    #解密文件
    decrypted = f.decrypt(encrypted)
    #二进制
    lines=decrypted.decode("utf-8").split("\n")
    #########################################################
    num=0
    for line in lines:
        array=line.strip(",")
        if chr==array[0] and pos==array[1] and ref==array[2] and alt==array[3]:
            num+=1
            print(line)
    if num==0:
        print("Not find corresponding variant.")

def CrossMap(in_vcf,chain,out_vcf):
    cmd="CrossMap.py vcf %s %s %s"%(chain,in_vcf,out_vcf)
    subprocess.check_call(cmd,shell=True)

def select_snp(in_vcf):
    in_vcf = os.path.abspath(in_vcf)
    prefix=""
    if re.search('.vcf$', in_vcf):
        prefix = in_vcf.split("/")[-1].split(".vcf")[0]

    if re.search('.vcf.gz$', in_vcf):
        prefix = in_vcf.split("/")[-1].split(".vcf.gz")[0]
        if re.search('.hard-filtered.vcf.gz$', in_vcf):
            prefix = in_vcf.split("/")[-1].split(".hard-filtered.vcf.gz")[0]

    ###multiallelic sites were split into biallelic records using bcftools norm -m -any
    ###The multi-nucleotide polymorphisms and complex indels were further decomposed into SNPs and simple indels
    ###select snp
    cmd = "bcftools norm -m -any %s -o %s.biallelic_records.vcf && " \
          "vcfdecompose --break-mnps --no-header --no-gzip --break-indels -i %s.biallelic_records.vcf -o %s.format.vcf && " \
          "bcftools view -v snps %s.format.vcf >%s.snp.vcf && rm -rf *biallelic_records.vcf *.format.vcf" % (in_vcf, prefix,prefix,prefix,prefix,prefix)
    subprocess.check_call(cmd, shell=True)


