set -e
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo ""${last_command}" command filed with exit code $?."' EXIT

WANTED_DIR=/home/alu/aluguest/Project2022_Renana_Or/Ex4Genomics/

# download
fastq-dump --gzip -X 1000000 -O $WANTED_DIR --split-files SRR12765536; #control 
fastq-dump --gzip -X 1000000 -O $WANTED_DIR --split-files SRR12765537; #control 

# summarize FastQC command
fastqc -o ${WANTED_DIR} ${WANTED_DIR}"SRR12765536_1.fastq.gz" ${WANTED_DIR}"SRR12765536_2.fastq.gz" ${WANTED_DIR}"SRR12765537_1.fastq.gz" ${WANTED_DIR}"SRR12765537_2.fastq.gz"
/home/alu/kobish/MULTIQC/multiqc/multiqc --in_dir  $WANTED_DIR --out_dir $WANTED_DIR
# download reference genome - chr7.
wget 'ftp://hgdownload.cse.ucsc.edu/goldenPath/hg38/chromosomes/chr7.fa.gz' -O chr7.fa.gz
zcat chr7.fa.gz > chr7.fa
bwa index "chr7.fa"
#alignment bwa 
bwa-0.7.4 mem ${WANTED_DIR}"/chr7.fa" ${WANTED_DIR}"/SRR12765536_1.fastq.gz" ${WANTED_DIR}"/SRR12765536_2.fastq.gz"  > SRR12765536.sam
bwa-0.7.4 mem ${WANTED_DIR}"/chr7.fa" ${WANTED_DIR}"/SRR12765537_1.fastq.gz" ${WANTED_DIR}"/SRR12765537_2.fastq.gz"  > SRR12765537.sam
#check files - % mapped
samtools flagstat SRR12765536.sam
samtools flagstat SRR12765537.sam
#SAM to BAM
samtools-1.9 view -Sb "SRR12765536.sam" > "SRR12765536.bam"
samtools-1.9 view -Sb "SRR12765537.sam" > "SRR12765537.bam"
# remove unmapped reads
samtools-1.9 view -b -F 4 "SRR12765536.bam"  | samtools-1.9 sort > "SRR12765536_noUnmappad.bam"
samtools-1.9 view -b -F 4 "SRR12765537.bam"  | samtools-1.9 sort > "SRR12765537_noUnmappad.bam"
# create vcf files
samtools-1.9 mpileup -f ${WANTED_DIR}"/chr7.fa" -O -v -u "SRR12765536_noUnmappad.bam" > ${WANTED_DIR}"/SRR12765536.vcf"
samtools-1.9 mpileup -f ${WANTED_DIR}"/chr7.fa" -O -v -u "SRR12765537_noUnmappad.bam" > ${WANTED_DIR}"/SRR12765537.vcf"
# the real command vcf
bcftools-1.8 mpileup -Ov -f ${WANTED_DIR}"/chr7.fa" "SRR12765536_noUnmappad.bam" | bcftools-1.8 call -mv -o ${WANTED_DIR}"/SRR12765536.vcf"
bcftools-1.8 mpileup -Ov -f ${WANTED_DIR}"/chr7.fa" "SRR12765537_noUnmappad.bam" | bcftools-1.8 call -mv -o ${WANTED_DIR}"/SRR12765537.vcf"

# statistics
bcftools-1.8 stats ${WANTED_DIR}"/SRR12765536.vcf" > stats36.txt
bcftools-1.8 stats ${WANTED_DIR}"/SRR12765537.vcf" > stats37.txt
# A2G, C2T
cat SRR12765536.vcf  | awk '!/^ *#/ {print $0}' | awk '($4 == "A" && $5 == "G")||($4 == "C" && $5 == "T") {print $0}' > SRR12765536edit.vcf
cat SRR12765537.vcf  | awk '!/^ *#/ {print $0}' | awk '($4 == "A" && $5 == "G")||($4 == "C" && $5 == "T") {print $0}' > SRR12765537edit.vcf
# convert vcf to bed
vcf2bed < "SRR12765536edit.vcf" > "SRR12765536edit_bed.txt"
vcf2bed < "SRR12765537edit.vcf" > "SRR12765537edit_bed.txt"
# intersection with 5 chosengenes
intersectBed -a SRR12765536edit_bed.txt -b chosengenes
intersectBed -a SRR12765537edit_bed.txt -b chosengenes
# intersection with clinVar snp table
intersectBed -a SRR12765536edit_bed.txt -b clinVar
intersectBed -a SRR12765537edit_bed.txt -b clinVar
