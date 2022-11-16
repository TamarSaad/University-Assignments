# Tamar Saad 207256991
# Rachel Weinberger 208812628
import os.path
import random
import sys
import re
import math
import numpy as np
from Bio.Seq import Seq
from Bio import SeqIO
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Pool


class SequenceClassifier:
    def __init__(self, pattern_file):
        self.regex_dict = self.__patterns_to_domains(pattern_file)

    def __prosite_to_python(self, pattern_dict):
        # dictionary that translate prosite format to python format
        dic = {"-": None, "x": ".", "(": "{", ")": "}", "{": "[^", "}": "]", "<": "^", ">": "$", ",": ","}
        RE_patterns = {}
        # going through each pattern and domain
        for pattern, domain in pattern_dict.items():
            # check if the format is valid
            if self.__check_prosite_format(pattern):
                # translate the pattern and pair it with its domain
                trans = str(pattern).maketrans(dic)
                re_pattern = str(pattern).translate(trans)
                RE_patterns[re_pattern] = domain
        return RE_patterns

    def __check_prosite_format(self, pattern):
        # create regexes that represent correct prosite format
        occurrences = "(\([\d](,[\d])?\))?"
        prefix = "(<)?"
        suffix = "(>)?"
        amino_group = "(\[[A-Z]*\])"
        amino_single = "[A-Z]"
        amino_any = "x"
        avoid = "(\{[A-Z]*\})"
        correct_format_once = "((" + amino_group + "|" + amino_single + "|" + amino_any + "|" + avoid + ")" + occurrences + ")"
        correct_format_repeat = "((" + amino_group + "|" + amino_single + "|" + amino_any + "|" + avoid + ")" + occurrences + "-)*"
        correct_format = prefix + correct_format_repeat + correct_format_once + suffix

        # check if the pattern is a valid prosite format
        check = re.search(correct_format, pattern)
        # return boolean value
        return check.group() is pattern and re.compile(check.group())

    def __patterns_to_domains(self, pattern_file):
        # initialize empty dictionary
        dict_from_csv = {}
        # read file into dictionary
        try:
            dict_from_csv = pd.read_csv(pattern_file, header=0, index_col=0, squeeze=True).to_dict()
        except ValueError:
            print("File is not in wanted format")
        # turn the prosite regex to python regex
        regex_dict = self.__prosite_to_python(dict_from_csv)
        return regex_dict

    def classify(self, seq_list, csv_file):
        protein_domains = dict()
        # for every protein in the list
        protein_domains["Sequence"] = "Domains"
        for seq in seq_list:
            domains = ""
            flag = False
            # go through each regex
            for reg in self.regex_dict:
                # check if the pattern fits any of the proteins
                if re.search(reg, seq):
                    domains += self.regex_dict[reg] + ";"
                    flag = True
            if not flag:
                domains = "NA"
            if flag:
                domains = domains[:-1]
            protein_domains[seq] = domains
        # turn dictionary into dataframe, and write it to csv file
        df = pd.DataFrame.from_dict(protein_domains, orient='index')
        df.to_csv(csv_file, index=True, header=False)


# define DNA and RNA polymerase
class Polymerase:
    # constructor
    def __init__(self, type, error_rate=0):
        self.type = type
        self.error_rate = error_rate
        # define translation differently for RNA/DNA polymerase
        A_translation = ""
        if type == "RNA":
            A_translation = "U"
        elif type == "DNA":
            A_translation = "T"
        # initialize a dictionary for transcribing
        self.transcribing_dictionary = {"T": "A", "t": "A", "C": "G", "c": "G", "G": "C", "g": "C",
                                        "A": A_translation,
                                        "a": A_translation}

    # this function receive a DNA sequence and translate it to RNA
    def transcribe(self, dna_seq):

        # find the indices of the mutations
        num_of_mutants = math.ceil(self.error_rate * len(dna_seq))
        # locations = np.random.choice(range(1, len(dna_seq)), num_of_mutants)
        locations = random.sample(range(0, len(dna_seq)), num_of_mutants)
        # initialize an empty list
        rna = ""
        # translate the letter according to the dictionary
        for ind, nuc in enumerate(dna_seq):
            if nuc in self.transcribing_dictionary.keys():
                # if we need to insert mutation
                if ind in locations:
                    # create a random mutation. if it's synonym- replace it
                    nucleotides = set(self.transcribing_dictionary.values())  # unique trans dic values
                    nucleotides = list(nucleotides)
                    nucleotides.remove(self.transcribing_dictionary[nuc])
                    mut = np.random.choice(nucleotides)
                    # while mut == self.transcribing_dictionary[nuc]:
                    #     mut = np.random.choice(list(self.transcribing_dictionary.values()))
                    # add the mutation to the sequence
                    rna += mut
                else:
                    rna += self.transcribing_dictionary[nuc]
            else:
                break
        # revers the sequence so it will be 5'-3', and cut the last character to fit the format
        if rna:
            return rna[::-1]
        else:
            return None


# define ribosome
class Ribosome:
    # constructor
    def __init__(self, genetic_code, start_codons):
        self.genetic_code = genetic_code
        self.start_codons = start_codons

    # turn RNA sequence to the biggest protein available
    def synthesize(self, rna_seq):
        # calls to translate
        protein = self.translate(rna_seq)
        if protein:
            return protein
        else:
            return None

    # this function receives rna sequence and returns the codons of the longest reading frame
    def translate(self, rna_seq):
        # initialize the biggest protein with empty string
        max_protein = ""
        # go through every nucleotide and look for start codon (AUG)
        for i in range(len(rna_seq)):
            if rna_seq[i:i + 3] in self.start_codons:
                # initialize the protein we will go through
                protein = ""
                # go through each codon and add it to the protein. stop in stop codon or at the end of the sequence
                for j in range(i, len(rna_seq) - 2, 3):
                    codon = rna_seq[j:j + 3]
                    # check for stop codon
                    if not self.genetic_code[codon]:
                        i += 4
                        break
                    else:
                        # add the codon to the protein
                        protein += self.genetic_code[codon]
                # when the protein is done, check if it's bigger than the biggest protein, and replace it if so
                if len(protein) > len(max_protein):
                    max_protein = protein
        return max_protein


class Cell:
    # constructor
    def __init__(self, name, genome, num_copies, genetic_code, start_codons, division_rate):
        self.name = name
        self.genome = []
        self.genome.append(genome)
        # input check
        if type(num_copies) is int and num_copies > 0:
            self.num_copies = num_copies
        self.genetic_code = genetic_code
        self.start_codons = start_codons
        # input check
        if type(division_rate) is int and division_rate > 1:
            self.division_rate = division_rate
        # initialize RNA+DNA polymerases
        self.RNA_Polymerase = Polymerase("RNA", 0)
        self.DNA_Polymerase = Polymerase("DNA", 0)
        # initialize Ribosome
        self.Ribosome = Ribosome(genetic_code, start_codons)

    # define a printing method
    def __str__(self):
        return "<" + str(self.name) + ", " + str(self.num_copies) + ", " + str(self.division_rate) + ">"

    # returns a list of n identical cells, while n is the division rate
    def mitosis(self):
        return self * self.division_rate

    # define the * operator
    def __mul__(self, num):
        cells = [self]
        return cells * num

    # return 2 cells: one identical to the original, one with the complimentary genome. both with n/2 genome copies
    def meiosis(self):
        if self.num_copies % 2 != 0:
            return None
        new_cell = Cell(self.name, self.genome, (self.num_copies / 2), self.genetic_code, self.start_codons,
                        self.division_rate)
        # find the complementary strands of the genome
        comp_genome = []
        for seq in self.genome:
            comp_genome.append(self.DNA_Polymerase.transcribe(seq))
            # define the complementary cell
        new_comp = Cell(self.name, comp_genome, self.num_copies / 2, self.genetic_code, self.start_codons,
                        self.division_rate)
        return [new_cell, new_comp]

    # this function find microsatellites in repeats of 3-6
    def find_srr(self, dna_seq):
        # flag to know if there are satellites
        satellites = {}
        # looking for microsatellites in increasing sizes of nucleotides
        for size_of_match in range(1, 7):
            # looking for satellite in different reading frames
            for i in range(len(dna_seq) - (len(dna_seq) % size_of_match)):
                count = 1  # number of repeats
                # checking for repeats
                for j in range(i, len(dna_seq) - (len(dna_seq) % size_of_match), size_of_match):
                    # if the sequences are the same- increase the counter
                    if dna_seq[j: j + size_of_match] == dna_seq[j + size_of_match: j + 2 * size_of_match]:
                        count += 1
                    else:
                        # if the sequences are different and there are more than 3 repeats- add it to the dictionary
                        if count >= 3:
                            satellite = dna_seq[j: j + size_of_match]
                            # if the satellite exists already- check if the count is bigger
                            if satellite in satellites.keys():
                                if count <= satellites[satellite]:
                                    break
                            # if the satellite didn't exist/the count is smaller- update the dictionary
                            satellites[satellite] = count
                        break
            size_of_match += 1
        if satellites:
            sat_list = ""
            for satellite, count in sorted(satellites.items(), key=lambda t: t[0]):
                sat_list += satellite + "," + str(count) + ";"
            return sat_list[:-1]
        else:
            return None

    # returns tuple for every strand. each tuple contains: satellites, RNA transcribe, translated protein
    def repertoire(self):
        list_of_tuples = []
        for sequence in self.genome:
            # find the satellites
            satellites = self.find_srr(sequence)
            if not satellites:
                satellites = "No simple repeats in DNA sequence"
            # find RNA transcribe
            rna_seq = self.RNA_Polymerase.transcribe(sequence)
            # find the biggest protein available
            protein = self.Ribosome.synthesize(rna_seq)
            if not protein:
                protein = "Non-coding RNA"
            seq = (satellites, rna_seq, protein)
            # returns list of tuples
            list_of_tuples.append(seq)
        return list_of_tuples


# inherit class from cell
class ProkaryoticCell(Cell):
    # constructor
    def __init__(self, genome):
        prokaryotic_genetic_code = {
            'AUA': 'I', 'AUC': 'I', 'AUU': 'I', 'AUG': 'M',
            'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACU': 'T',
            'AAC': 'N', 'AAU': 'N', 'AAA': 'K', 'AAG': 'K',
            'AGC': 'S', 'AGU': 'S', 'AGA': 'R', 'AGG': 'R',
            'CUA': 'L', 'CUC': 'L', 'CUG': 'L', 'CUU': 'L',
            'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCU': 'P',
            'CAC': 'H', 'CAU': 'H', 'CAA': 'Q', 'CAG': 'Q',
            'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGU': 'R',
            'GUA': 'V', 'GUC': 'V', 'GUG': 'V', 'GUU': 'V',
            'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCU': 'A',
            'GAC': 'D', 'GAU': 'D', 'GAA': 'E', 'GAG': 'E',
            'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGU': 'G',
            'UCA': 'S', 'UCC': 'S', 'UCG': 'S', 'UCU': 'S',
            'UUC': 'F', 'UUU': 'F', 'UUA': 'L', 'UUG': 'L',
            'UAC': 'Y', 'UAU': 'Y', 'UAA': None, 'UAG': None,
            'UGC': 'C', 'UGU': 'C', 'UGA': 'U', 'UGG': 'W'}
        start_codons = ("AUG", "GUG", "UUG")
        division_rate = 4
        num_copies = 1
        # calls parent's constructor
        super().__init__("ProKaryoticCell", genome, num_copies, prokaryotic_genetic_code, start_codons, division_rate)


# inherit class from cell
class EukaryoticCell(Cell):
    # constructor
    def __init__(self, name, genome, division_rate):
        standard_genetic_code = {
            'AUA': 'I', 'AUC': 'I', 'AUU': 'I', 'AUG': 'M',
            'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACU': 'T',
            'AAC': 'N', 'AAU': 'N', 'AAA': 'K', 'AAG': 'K',
            'AGC': 'S', 'AGU': 'S', 'AGA': 'R', 'AGG': 'R',
            'CUA': 'L', 'CUC': 'L', 'CUG': 'L', 'CUU': 'L',
            'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCU': 'P',
            'CAC': 'H', 'CAU': 'H', 'CAA': 'Q', 'CAG': 'Q',
            'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGU': 'R',
            'GUA': 'V', 'GUC': 'V', 'GUG': 'V', 'GUU': 'V',
            'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCU': 'A',
            'GAC': 'D', 'GAU': 'D', 'GAA': 'E', 'GAG': 'E',
            'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGU': 'G',
            'UCA': 'S', 'UCC': 'S', 'UCG': 'S', 'UCU': 'S',
            'UUC': 'F', 'UUU': 'F', 'UUA': 'L', 'UUG': 'L',
            'UAC': 'Y', 'UAU': 'Y', 'UAA': None, 'UAG': None,
            'UGC': 'C', 'UGU': 'C', 'UGA': None, 'UGG': 'W'}
        start_codons = "AUG"
        num_copies = 2
        # calls parent's constructor
        super().__init__(name, genome, num_copies, standard_genetic_code, start_codons, division_rate)


# inherit from EukaryoticCell
class NeuronCell(EukaryoticCell):
    # constructor
    def __init__(self, genome):
        division_rate = 2
        # calls parent's constructor
        super().__init__("NeuronCell", genome, division_rate)


# inherit from EukaryoticCell
class StemCell(EukaryoticCell):
    def __init__(self, genome):
        division_rate = 3
        # calls parent's constructor
        super().__init__("StemCell", genome, division_rate)


# inherit from stem cell
class MutantCell(StemCell):
    def __init__(self, genome, num_mutations=0, error_rate=0.05):
        # call father's constructor
        super().__init__(genome)
        # override the name
        self.name = "MutantCell"
        # default mutation rate is 1:20
        self.DNA_Polymerase.error_rate = error_rate
        self.RNA_Polymerase.error_rate = 0
        # initialize num of muts to 0
        self.num_of_mutations = num_mutations
        self.num_of_new_mutations_per_generation = self.calculate_num_of_muts_per_generation()

    def calculate_num_of_muts_per_generation(self):
        num_of_new_mutations_per_generation = 0
        for g in self.genome:
            num_of_new_mutations_per_generation += math.ceil(len(g) * self.DNA_Polymerase.error_rate)
        return num_of_new_mutations_per_generation

    # returns a list of n identical cells, while n is the division rate
    def mitosis(self):
        # get a list of mutants
        mutants = self * self.division_rate
        mutants[0] = self
        return mutants

    # define the * operator
    def __mul__(self, num):
        # create mutant genome
        t_genome = self.get_mutant_genome()
        # check if the number of mutations is under 10
        if self.num_of_mutations + self.num_of_new_mutations_per_generation > 10:
            # create cancer cell
            mutant = CancerCell(t_genome,
                                num_mutations=self.num_of_mutations + self.num_of_new_mutations_per_generation,
                                error_rate=self.DNA_Polymerase.error_rate)
        else:
            # create mutant cell
            mutant = MutantCell(t_genome,
                                num_mutations=self.num_of_mutations + self.num_of_new_mutations_per_generation,
                                error_rate=self.DNA_Polymerase.error_rate)

        # def the number of mutations the cell has
        cells = [mutant]
        return cells * num

    def get_mutant_genome(self):
        # t_genome = []
        complement = None
        for dna in self.genome:
            complement = Seq(self.DNA_Polymerase.transcribe(dna))
            # t_genome.append(str(complement.reverse_complement()))
            complement = str(complement.reverse_complement())
        return complement


class CancerCell(MutantCell):
    def __init__(self, genome, num_mutations, error_rate=0.05):
        super().__init__(genome, num_mutations, error_rate=error_rate)
        self.division_rate = 10
        self.name = "CancerCell"


# factory to initialize each cell
class CellFactory:
    def create_cell_object(self, name, genome):
        if name == "NeuronCell":
            return NeuronCell(genome)
        if name == "StemCell":
            return StemCell(genome)
        if name == "ProkaryoticCell":
            return ProkaryoticCell(genome)
        if name == "MutantCell":
            return MutantCell(genome)
        if name == "CancerCell":
            return CancerCell(genome, num_mutations=10)
        else:
            raise AssertionError(name)


# check if the input sequences are valid as genome
def is_genome_valid(sequences):
    genome = ("A", "T", "G", "C",)
    for seq in sequences:
        matched_list = [characters in genome for characters in seq.upper()]
        assert all(matched_list), "Invalid input " + seq


def cells_divisions(cell, divisions_num, max_cell_num):
    divs = 0
    num_of_cells = 1
    cells = [cell]
    # while we didn't do maximum num of divisions:
    while divs < int(divisions_num):
        # go through each cell in the list
        for c in range(num_of_cells):
            # if we will not exceed from the max number of cells- do mitosis
            # the -1 is because we exclude the cell that actually is going through mitosis
            if len(cells) <= max_cell_num - (cells[c].division_rate - 1):
                # adding the new cells to the list, excluding the original cell that actually did mitosis
                cells += (cells[c].mitosis()[1:])
            else:  # we have the max number of cells and can exit both loops
                break
        # after all the cells went through mitosis once- we increase the number of divisions
        divs += 1
        num_of_cells = len(cells)
    return cells


def get_different_proteins_from_cells(cells):
    proteins = []
    for cell in cells:
        for sequence in cell.genome:
            # rep = cell.repertoire()
            rna_seq = cell.RNA_Polymerase.transcribe(sequence)
            # find the biggest protein available
            cell_proteins = cell.Ribosome.synthesize(rna_seq)
            if not cell_proteins:
                cell_proteins = "Non-coding RNA"
            proteins += [cell_proteins]
    proteins = np.array(proteins)
    unique_proteins = np.unique(proteins)
    unique_proteins = np.delete(unique_proteins, np.where(unique_proteins == "Non-coding RNA"))
    return unique_proteins


def get_most_mutant_cell(mutant_cells):
    most_mutant = None
    muts_num = 0
    for cell in mutant_cells:
        if cell.num_of_mutations > muts_num:
            most_mutant = cell
            muts_num = cell.num_of_mutations
    return most_mutant


def get_genome_from_fasta(fastaFile):
    GenomicSequences = []
    # records = list(SeqIO.parse(fastaFile, "fasta"))
    # for r in records:
    #    genome.append(r.seq)
    for record in SeqIO.parse(fastaFile, "fasta"):
        GenomicSequences.append(record.seq)
    return GenomicSequences


"""
this function gets a sequence and returns a df that contains the number of cancer cells,
mutant cells and different proteins, as a function of different error rates and divisions numbers
"""
def get_results(seq):
    # initialize a list of error rates
    error_rates = np.arange(0.05, 0.5, 0.05)
    error_rates = np.concatenate(([0.01], error_rates, [0.5]))
    # initialize a list of divisions number
    division_numbers = range(1, 6)
    # initialize an empty dataframe
    df = pd.DataFrame(
        columns=['division_number', 'error_rate', 'number_of_cancer_cells', 'number_of_mutant_cells',
                 'number_of_proteins'])
    # go through each division number
    for div_num in division_numbers:
        # go through each error rate
        for error_rate in error_rates:
            # initialize a mutant cell
            mut_cell = MutantCell(str(seq), error_rate=error_rate)
            # get all the cells after mitosis
            cells = cells_divisions(mut_cell, div_num, float('inf'))
            # get number of cancer cells
            cancer_cells_num = len([c for c in cells if c.name == "CancerCell"])
            # number of mutant cells
            mutant_cell_num = len(cells) - cancer_cells_num
            # get a list of the different proteins
            proteins = get_different_proteins_from_cells(cells)
            df = df.append({'division_number': div_num, 'error_rate': error_rate,
                            'number_of_cancer_cells': cancer_cells_num, 'number_of_mutant_cells': mutant_cell_num,
                            'number_of_proteins': len(proteins)}, ignore_index=True)
    return df


# option number 1 for the combined graphs- linear graphs
"""
def create_combined_graphs(data_df, sequences):
    # the different options for x axis
    x_axes = ["division_number", "error_rate"]
    # go through each kind of x axis
    for ind, x in enumerate(x_axes):
        # initialize a new plot
        plt.figure()
        curves = []
        # create a curve for each sequence
        for num, seq in enumerate(sequences):
            # get the relevant data of the current sequence from the df
            data_df_seq = data_df[data_df['Sequence'].str.contains(str(seq))]
            y_axis = data_df_seq['number_of_proteins']
            x_axis = data_df_seq[x]
            curves.append(x_axis)
            plt.plot(x_axis, y_axis, label=("seq " + str(num + 1)))
        plt.xlabel(x)
        plt.ylabel('number_of_proteins')
        title = "number of proteins as a function of " + x
        plt.title(title)
        plt.legend()
        plt.savefig("exercise4_207256991_208812628_" + title + ".png")
"""


"""
this function creates a plot for each sequence:
x axis: error rate
y axis: divisions number
size+color of points: number of proteins
"""
# option number 2 to combined graphs: scatter plots
def create_combined_graphs_2(data_df, sequences):
    # go through each kind of x axis
    for ind, seq in enumerate(sequences):
        # initialize a new plot
        plt.figure()
        # get the data of one sequence
        data_df_seq = data_df[data_df['Sequence'].str.contains(str(seq))]
        # set the axes
        x_axis = data_df_seq["error_rate"]
        y_axis = data_df_seq["division_number"]
        # number of proteins
        prot_num = data_df_seq['number_of_proteins']
        # create scatter plot:
        # define the sizes and colors to represent the number of protein
        plt.scatter(x_axis, y_axis, c=prot_num, cmap='viridis', s=prot_num, alpha=0.7)
        # labels and titles
        plt.xlabel("error rate")
        plt.ylabel("division number")
        title = f"sequence {ind+1} protein number ~ division number and error rate"
        plt.suptitle(f"sequence {seq}")
        plt.title("number of proteins is represented by size and color")
        plt.colorbar()
        plt.savefig("exercise4_207256991_208812628_" + title + ".png")


# gets the required plots: a plot for number of proteins, number of mutant cells
# and number of cancer cells as a function of error rate
def get_graphs_per_seq(sequences):
    # read the csv file we created
    data_df = pd.read_csv('exercise4_207256991_208812628.csv', sep=',')
    # keep only the rows of division_number = 5
    data_df_max_divs = data_df[data_df['division_number'].astype(str).str.contains('5')]
    plot_num = 1
    # go through each sequence
    for ind, seq in enumerate(sequences):
        # keep only the data for this sequence
        data_df_seq = data_df_max_divs[data_df_max_divs['Sequence'].str.contains(str(seq))]
        # define the x axis as error rate
        x_axis = data_df_seq['error_rate']
        # define the different options for y axis
        y_axes = ["number_of_cancer_cells", "number_of_mutant_cells", "number_of_proteins"]
        # go through each option
        for y in y_axes:
            # define a specific plot and clear it from previous plots
            plt.figure(plot_num)
            # define the y axis
            y_axis = data_df_seq[y]
            plt.plot(x_axis, y_axis)
            # create labels
            plt.xlabel('error_rate')
            plt.ylabel(y)
            plt.title(str(seq))
            # save the plot
            plt.savefig("exercise4_207256991_208812628_" + f"seq_{ind+1}_" + y + ".png")
            plot_num += 1
            plt.clf()
    # create_combined_graphs(data_df, sequences)
    # create the combined graphs
    create_combined_graphs_2(data_df, sequences)


def main():
    random.seed(1)
    # input checkups
    assert len(sys.argv) == 2, "Wrong number of inputs"
    fastaFile = sys.argv[1]
    assert os.path.isfile(fastaFile), "input is not a file " + fastaFile
    name, extension = os.path.splitext(fastaFile)
    assert extension == ".fa", "input must be fasta file " + fastaFile
    # get list of the sequences from the input fasta file
    # get the sequences names from the file
    seqs = []
    seq_names = []
    for seq_record in SeqIO.parse(fastaFile, "fasta"):
        seqs.append(str(seq_record.seq))
        seq_names.append(seq_record.id)
    sequences = pd.DataFrame(list(zip(seq_names, seqs)), columns=['Name', 'Seq'])

    # check input sequences
    is_genome_valid(seqs)

    # initialize the results dataframe
    df = pd.DataFrame(
        columns=['Sequence', 'division_number', 'error_rate', 'number_of_cancer_cells', 'number_of_mutant_cells',
                 'number_of_proteins'])
    # go through each sequence
    for index, seq in sequences.iterrows():
        # create an iterable list of the sequence for the map function
        # it's just a list with the same sequence 3 times
        itr_seq = [seq["Seq"]] * 3
        # create 3 processes
        with Pool(3) as p:
            # the output is a list of 3 dataframes, one from each process
            results = p.map(get_results, itr_seq)
        # calculate the average result
        results = (results[0] + results[1] + results[2]) / 3
        # create a list with the sequence name, for the csv file
        seq_list = [seq['Name']] * len(results.index)
        # insert the list to the dataframe in the first column
        results.insert(0, "Sequence", seq_list)
        # concatenate the results dataframe to the df of all the sequences
        df = pd.concat([df, results])
    # save results to csv
    df.to_csv('exercise4_207256991_208812628.csv', index=False)
    # create the required graphs
    get_graphs_per_seq(sequences['Name'])


if __name__ == "__main__":
    main()
