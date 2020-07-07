from Bio.SubsMat.MatrixInfo import blosum62
from time import clock
import os

import Util
import LogicPrep
import Logic
############### start to set env ###############
WORK_DIR = os.getcwd() + "/"

INPUT_DIR = "input/*.txt"
# PAIRWISE2_OPT = [blosum62, 10, 0.5]  # basic setting
PAIRWISE2_OPT = []
############### end setting env ################


def pairwise2_main():
    util = Util.Utils()
    logic_prep = LogicPrep.LogicPreps([])

    sources = util.get_files_from_dir(WORK_DIR + INPUT_DIR)

    # TODO adjust options
    needle_dict = logic_prep.get_pairwise2_needle_dict(sources, PAIRWISE2_OPT)

    # util.make_neddle_result_txt(WORK_DIR + "output/pairwise2_neddle_" + str(clock()) + "_", needle_dict)

    result_dict = logic_prep.get_sub_ins_del_list_dict_by_fnm(needle_dict)

    util.make_excel(WORK_DIR + "output/pairwise2_result_" + str(clock()) + "_", result_dict)

def test2():
    ngs_read_needle = "TATATATCTTGTGGAAAGGACGAAACACCAGAAGCTGTACTTCAAAAAAGTT------------------------------------------------------------------------------------------AGTACATTTTTTTCATATCTGCACTCACTCTCTGCTGAAGCTGTACTTCAAAAAATGGATGACATGAAGAAGATAGCTTGGCGTACCGCGATCTCTACTCTACCCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAA"
    needle_result = "||||||||||||||||||||||||||||| ||||||||||||||||||||||                                                                                          |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| ||||||||||||||||||||||||||||||||||||"
    ref_seq_needle = "TATATATCTTGTGGAAAGGACGAAACACCGGAAGCTGTACTTCAAAAAAGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTGTCATCGATTTTTTGAAGTACATTTTTTTCATATCTGCACTCACTCTCTGCTGAAGCTGTACTTCAAAAAATGGATGACATGAAGAAGATAGCTTGGCGTACCGCGATCTCTACTCTA-CCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAA"
    needle_cnt = needle_result.count("|")
    del_cnt = ngs_read_needle.count("-")
    ins_cnt = ref_seq_needle.count("-")
    needle_tot = len(needle_result)
    sub_cnt = needle_tot - (needle_cnt + del_cnt + ins_cnt)
    print(str(needle_cnt))
    print(str(sub_cnt))

def test():
    logic = Logic.Logics()
    aseq = "ATTTAAGGGGCATCGTTTATTTTTTCCCCCCCCTTTGACTCATCTCGTCACTACAGACATGCATCGCATACTCTCCCTATGTTCCAGCTTCCTGGGTCTGCAGGTCCAGCCGAGTCGCCAAATAAGTGCCATCTACTCTACCACTTGTACTTCAGCGGT"
    bseq = "TTTGACTCATCTCGTCACTACAGACATGCATCGCATACTCTCCCTATGTTCCAGCTTCCTGGGTCTGCAGGTCCAGCCGAGTCGCCAAATAAGTGCCATCTACTCTACC"
    align_arr1, align_arr2, align_arr3 = logic.get_pairwise2_needle_result(aseq, bseq)
    print(align_arr1)
    print(align_arr2)
    print(align_arr3)


start_time = clock()
print("start >>>>>>>>>>>>>>>>>>")
# pairwise2_main()
test()
print("::::::::::: %.2f seconds ::::::::::::::" % (clock() - start_time))