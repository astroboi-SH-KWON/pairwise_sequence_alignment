
from time import clock
import os

import Util
import LogicPrep
############### start to set env ###############
# WORK_DIR = os.getcwd() + "/"
WORK_DIR = "D:/000_WORK/YuGooSang/20200622/WORK_DIR/"

INPUT_DIR = "input/*.txt"
PAIRWISE2_OPT = []

PATH_SPLIT = "/input"
############### end setting env ################

def pairwise2_main():
    util = Util.Utils()
    logic_prep = LogicPrep.LogicPreps([[], 0, 0])

    sources = util.get_files_from_dir(WORK_DIR + INPUT_DIR)

    needle_dict, alignments_result_dict = logic_prep.get_pairwise2_needle_dict(sources, PAIRWISE2_OPT)

    result_dict = logic_prep.get_sub_ins_del_list_dict_by_fnm(needle_dict)

    util.make_txt_needle_result(WORK_DIR + "output/pairwise2_needle_result_", alignments_result_dict, PATH_SPLIT)
    util.make_excel(WORK_DIR + "output/pairwise2_result_", result_dict)



start_time = clock()
print("start >>>>>>>>>>>>>>>>>>")
pairwise2_main()
print("::::::::::: %.2f seconds ::::::::::::::" % (clock() - start_time))