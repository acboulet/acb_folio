# import biopython
from Bio.Seq import Seq
from Bio.SeqUtils import GC
import pandas as pd

def primer_main(cDNA, target_residue, mutant_codon):
    """
    Function: 
        Function will generate the list of potential primers when generating mutants
        The function will calculate all primers that have a Tm between 78 and 82
        It will then remove any that start or end with a AT
        It will then remove any duplicates from the list
    Input:
        :param cDNA: String with cDNA sequence where mutant is desired
        :param target_residue: Amino acid residue that is being targeted for mutation
        :param mutant_codon: Mutation that you wanted to replace the target residue
    Output:
        Returns a tuple containing the following information:
            index0: record of all recommended primers including they following keys:
                'GC': GC% of primer as integer
                'seq': Primer sequence as a string
                'Tm': Calculated Tm
                'bp': Length of the given primer as integer
            index1: target codon in string format
            index2: mutant_codon in string format

    """

    # pull out the first attempt at a primer which would be +/- 6 codonsfrom the target
    # The required +2 means it will accept the entire target codon
    cDNA = cDNA.strip().lower()
    cDNA = ''.join(cDNA.split()) # Process the cDNA by making all lower, and remove all whitespace
    print(cDNA)
    start_bp = (target_residue-1)*3
    codon = cDNA[start_bp : start_bp+3]
    # Calculates number of mutations designed to be inserted
    no_mutations = 0
    for bp in range(3):
        if codon[bp] != mutant_codon[bp]:
            no_mutations +=1
    
    primer = cDNA[start_bp-18 : start_bp+3+18]
    mut_primer = primer[:18] + mutant_codon + primer[21:]
    mut_primer = Seq(mut_primer)
    result = Tm_calc(mut_primer, no_mutations)
    result2 = check_lockdown(result)
    cleaned_result2 = remove_duplicates(result2)
    # Converting using BioSeq for easier analysis
    codon = Seq(codon)
    endo_codon = [str(codon), str(Seq.translate(codon))]
    mut_codon = Seq(mutant_codon)
    mutated_codon = [str(mut_codon), str(Seq.translate(mut_codon))]
    return(cleaned_result2, endo_codon, mutated_codon)


# generate a list of every primer sequence that has a Tm between 78 and 82
def Tm_calc(sequence, mutations, good_primers = None):
    """
    Function:
        This function is designed to find possible SDM primers for a given mutagenesis sequence
        Generates a list of all primers within a given sequence that have a Tm between 78 and 82
        Will use the Strategene formula to calculaate the Tm
    Input:
        :param sequence: Sequence to be searched where the mutant codon is in the center
        :param mutations: Number of mutations planned to be inserted (up to 3)
        :param good_primers: Recursive variable to store primers through multiple calls
    Output:
        Returns a list of records containing the following information:
            'GC': GC% of primer as integer
            'seq': Primer sequence as a string
            'Tm': Calculated Tm
            'bp': Length of the given primer as integer

    """
    if good_primers == None:
        good_primers = []
    primer_GC = GC(sequence)
    Tm = 81.5 + (0.41 * primer_GC) - (675 / ((len(sequence)) - mutations))
    # If the Tm drops too low then this is a base case
    if Tm < 78:
        return good_primers
    # First recursive case is the Tm falls in appropriate range
    # An inventory will be added to primer database
    # And the script will then test chopping the primer down from each end recursively
    elif Tm <= 82:
        primer_db = {}
        primer_db['GC'] = round(primer_GC, 1)
        primer_db['rev'] = str(sequence.reverse_complement())
        primer_db['seq'] = str(sequence)
        primer_db['Tm'] = round(Tm, 2)
        primer_db['bp'] = len(sequence)
        good_primers.append(primer_db)
        good_primers = Tm_calc(sequence[1:], mutations, good_primers)
        good_primers = Tm_calc(sequence[:-1], mutations, good_primers)
    # If Tm is above 82, then it will chop a bp off either end of the sequence
    else:
        good_primers = Tm_calc(sequence[1:-1], mutations, good_primers)
    return good_primers


def check_lockdown(primer_list):
    """
    Function:
        Searches through a list of SDM primers and removes any that don't adhere to the GC lockdown rule.
        This means that the primer sequence must begin and end with a 'GC' base pair
    Input:
        :param primer_list: List of primers output from the Tm_calc function
    Output:
        :return: New list of primers in same format as Tm_calc function
    """
    best_primers = []
    for primer in primer_list:
        if primer['seq'][0] in 'gc' and primer['seq'][-1] in 'gc':
            best_primers.append(primer)
    return best_primers

def remove_duplicates(primer_list):
    """
    Function:
        Searches through a list of SDM primers generated by Tm_calc function and removes any duplicates
    Input:
        :param primer_list: List of primers output from the Tm_calc function
    Output:
        :return: New list of primers in same format as Tm_calc function
    """
    cleaned_primers = []
    for item in primer_list:
        not_found = True
        for primer in cleaned_primers:
            if item['seq'] == primer['seq']:
                not_found = False
        if not_found:
            cleaned_primers.append(item)
    return cleaned_primers


if __name__ == "__main__":
    # accept the following
    # Seq is Paul_Pic2
    sequence = 'ATGGAGTCCAATAAACAACCACGTAAAATCCAATTATATACGAAAGAGTTTTATGCCACATGTACCTTAGGTGGTATAATTGCGTGCGGTCCAACACATTCTTCGATCACTCCACTAGATCTTGTCAAATGTAGGCTACAGGTCAATCCCAAGTTGTATACTTCAAACTTACAAGGGTTCCGTAAGATTATAGCTAATGAAGGCTGGAAGAAAGTATACACTGGGTTTGGTGCTACATTCGTCGGATATTCGCTACAAGGTGCAGGTAAGTATGGTGGTTATGAGTATTTCAAGCATTTGTATTCTAGTTGGTTAAGTCCTGGTGTCACTGTGTACTTGATGGCCTCAGCGACCGCTGAATTCCTCGCTGATATCATGTTGTGCCCATTTGAAGCTATTAAAGTGAAACAGCGGACTACTATGCCGCCCTTTTGCAATAACGTTGTTGATGGATGGAAAAAAATGTATGCAGAAAGTGGAGGTATGAAAGCATTTTATAAAGGTATTGTTCCCCTATGGTGCAGACAGATTCCTTACACAATGTGTAAGTTTACCTCATTCGAAAAAATTGTTCAAAAAATATACAGTGTTTTACCTAAAAAGAAAGAAGAAATGAACGCATTACAGCAAATATCAGTCAGTTTTGTAGGTGGTTATCTGGCAGGTATATTATGTGCTGCAGTCTCACATCCTGCAGACGTTATGGTTTCCAAGATCAATAGCGAAAGAAAGGCCAACGAGTCCATGTCTGTAGCCTCTAAAAGAATATATCAAAAAATTGGCTTTACTGGGTTGTGGAATGGGTTAATGGTGAGAATTGTCATGATCGGTACTTTGACAAGTTTCCAATGGCTAATTTACGATTCGTTCAAGGCTTATGTAGGCTTACCAACCACCGGTTAG '
    # HsSCO1
    sequence = """ATGGCGATGCTGGTCCTAGTACCCGGACGAGTTATGCGGCCTCTGGGTGGCCAACTTTGGCGCTTCTTGC
CTCGCGGACTCGAGTTTTGGGGCCCAGCCGAGGGGACTGCGAGAGTCTTGCTGAGGCAGTTCTGCGCGCG
GCAAGCGGAGGCGTGGCGTGCCTCGGGGCGCCCTGGCTATTGCCTGGGAACCCGGCCCCTCAGCACTGCG
AGGCCGCCACCCCCGTGGTCGCAGAAGGGCCCCGGAGACTCCACGCGCCCCTCGAAGCCCGGGCCTGTTT
CCTGGAAGTCTTTAGCAATCACATTTGCTATTGGAGGAGCTTTACTGGCTGGAATGAAGCACGTCAAGAA
AGAAAAGGCAGAGAAGTTAGAGAAGGAACGGCAGCGACACATCGGCAAGCCTTTACTTGGGGGACCGTTT
TCCCTCACAACTCATACTGGGGAGCGTAAAACTGACAAGGACTACTTGGGTCAGTGGTTATTGATTTATT
TTGGCTTCACTCATTGCCCTGATGTCTGTCCAGAAGAACTAGAAAAGATGATTCAAGTCGTGGATGAAAT
AGATAGCATTACAACTCTGCCAGATCTAACTCCACTTTTCATCAGCATTGACCCAGAGAGGGACACAAAA
GAAGCCATCGCAAATTATGTGAAAGAATTTTCTCCCAAACTGGTTGGCTTGACTGGCACGAGAGAAGAGG
TCGATCAAGTGGCCAGAGCATACAGAGTGTATTACAGCCCTGGCCCCAAGGACGAAGATGAAGACTACAT
AGTGGATCACACAATAATAATGTACTTGATTGGACCAGATGGTGAGTTTCTAGATTATTTTGGCCAGAAC
AAGAGGAAGGGAGAAATAGCTGCTTCAATTGCCACACACATGAGGCCATACAGAAAAAAGAGCTAG"""
    target_residue = 294
    mutant_codon = 'ATG'
    result3 = primer_main(sequence, target_residue, mutant_codon)
    #df = pd.DataFrame.from_records(result3[0])
    #print(df.head)
    for item in result3[0]:
        print(item)
    print(result3[1])
    print(result3[2])