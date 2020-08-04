from Bio import SeqIO
import time
import os
import multiprocessing as mp
import numpy as np
import glob

import Util
import LogicPrep
import Logic
############### start to set env ###############
# WORK_DIR = os.getcwd() + "/"
WORK_DIR = "D:/000_WORK/SangYeon/20200706/WORK_DIR/"

NGS_read_files = "input/NGS_READ/*.txt"
NGS_read_DIR = "input/NGS_READ/"
REF_SEQ = "input/REF_SEQ/200706_hNm2_Reference_Number.txt"

TOTAL_CPU = mp.cpu_count()
MULTI_CNT = int(TOTAL_CPU*0.8)
############### end setting env ################

def multi_processing():
    util = Util.Utils()

    ref_seq_list = util.read_tb_txt_wo_header(WORK_DIR + REF_SEQ)


    for ref_val in ref_seq_list:
        logic_prep = LogicPrep.LogicPreps([ref_val, 0, 0])
        try:
            ngs_read = util.read_tb_txt_wo_header(WORK_DIR + NGS_read_DIR + ref_val[0] + ".txt")
            splited_ngs_read = np.array_split(ngs_read, MULTI_CNT)

            print("total cpu_count : " + str(TOTAL_CPU))
            print("will use : " + str(MULTI_CNT))
            pool = mp.Pool(processes=MULTI_CNT)

            pool_list = pool.map(logic_prep.get_pairwise2_needle_dict_simple, splited_ngs_read)

            merge_dict, _ = logic_prep.merge_multi_dict_from_simple(pool_list)
            result_dict = logic_prep.get_sub_ins_del_list_dict_from_simple(merge_dict)

            util.make_excel_simple(WORK_DIR + "output/multi_p_result_" + ref_val[0], result_dict)
        except FileNotFoundError:
            print(ref_val[0] + ".txt : FileNotFoundError")
            continue

def multi_processing_test():
    util = Util.Utils()
    ref_val = ['76967', 'TTTGACTCATCTCGTCACTACAGACATGCATCGCATACTCTCCCTATGTTCCAGCTTCCTGGGTCTGCAGGTCCAGCCGAGTCGCCAAATAAGTGCCATCTACTCTACC']
    logic_prep = LogicPrep.LogicPreps([ref_val, 0, 0])


    ngs_read = util.read_tb_txt_wo_header(WORK_DIR + NGS_read_DIR + ref_val[0] + ".txt")
    splited_ngs_read = np.array_split(ngs_read, MULTI_CNT)

    print("total cpu_count : " + str(TOTAL_CPU))
    print("will use : " + str(MULTI_CNT))
    pool = mp.Pool(processes=MULTI_CNT)

    pool_list = pool.map(logic_prep.get_pairwise2_needle_dict_simple, splited_ngs_read)

    merge_dict, _ = logic_prep.merge_multi_dict_from_simple(pool_list)
    result_dict = logic_prep.get_sub_ins_del_list_dict_from_simple(merge_dict)

    util.make_excel_simple(WORK_DIR + "output/multi_p_result_" + ref_val[0] + "_" +str(time.perf_counter()), result_dict)





if __name__ == '__main__':
    start_time = time.perf_counter()
    print("start >>>>>>>>>>>>>>>>>>")
    multi_processing()
    # multi_processing_test()
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.perf_counter() - start_time))