# check how many rows are in covid vars
wc -l covid.txt
# count the munber of covid vars thst are in whole genes
intersectBed -u -a covid.txt -b whole_gene.txt | wc -l
# find how many exons intersect with introns
intersectBed -wa -a exons.txt -b introns.txt | wc -l
# remove doplicates
intersectBed -wa -a exons.txt -b introns.txt | sort | uniq | wc -l
# save the results as a file
intersectBed -wa -a exons.txt -b introns.txt | sort | uniq > exons_introns_intersection.txt
# create a file of exons_introns_intersection with the CDS
intersectBed -wa -a exons_introns_intersection.txt -b CDS.txt | sort | uniq > ei_CDS_intersection.tx
# count the number of results
wc -l ei_CDS_intersection.txt
# find the number of ei_CDS_intersection after merging
bedtools sort -i ei_CDS_intersection.txt | bedtools merge | wc -l
# save the results to a file
bedtools sort -i ei_CDS_intersection.txt | bedtools merge > merge_ei_CDS.txt
#find the intersection between merge_ei_CDS and covid vars
intersectBed -a covid.txt -b merge_ei_CDS.txt > covid_marge_ei_CDS.txt
# find the number of covid and marge_ei_CDS intersection
wc -l covid_marge_ei_CDS.txt
# print the first 20 lines of covid_marge_ei_CDS
head -n 20 covid_marge_ei_CDS.txt