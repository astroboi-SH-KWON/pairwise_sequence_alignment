from time import clock
import time
import os
import multiprocessing as mp
import numpy as np

import Util
import LogicPrep
import Logic
############### start to set env ###############
WORK_DIR = os.getcwd() + "/"

NGS_read = "input/NGS_read_test.txt"
# NGS_read = "input/NGS_read.txt"
REF_SEQ = "input/Reference_test.txt"
# REF_SEQ = "input/Reference.txt"

PAIRWISE2_OPT = []
TOTAL_CPU = mp.cpu_count()
MULTI_CNT = int(TOTAL_CPU*0.8)
TOP_N = 5
IDX = 0
############### end setting env ################

def multi_processing():
    util = Util.Utils()
    logic = Logic.Logics()

    ngs_read = util.read_tb_txt(WORK_DIR + NGS_read)  # 56k
    ref_seq = util.read_tb_txt(WORK_DIR + REF_SEQ)  # 1200

    logic_prep = LogicPrep.LogicPreps([ref_seq, IDX, TOP_N])

    splited_ngs_read = np.array_split(ngs_read, MULTI_CNT)

    print("total cpu_count : " + str(TOTAL_CPU))
    print("will use : " + str(MULTI_CNT))
    pool = mp.Pool(processes=MULTI_CNT)

    pool_list = pool.map(logic_prep.get_pairwise2_needle_dict_by_res_seq, splited_ngs_read)

    merge_dict = logic_prep.merge_multi_dict(pool_list)
    sorted_dict = logic.sort_dict_top_n_by_idx_ele(merge_dict, IDX, TOP_N)

    util.make_excel_mutil_processing(WORK_DIR + "output/multi_p_result_", sorted_dict)






if __name__ == '__main__':
    start_time = clock()
    # start_time = time.clock_gettime(1)
    print("start >>>>>>>>>>>>>>>>>>")
    multi_processing()
    print("::::::::::: %.2f seconds ::::::::::::::" % (clock() - start_time))
    # print("::::::::::: %.2f seconds ::::::::::::::" % (time.clock_gettime(1) - start_time))