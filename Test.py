from time import clock
import os

import Util
import LogicPrep
############### start to set env ###############
WORK_DIR = os.getcwd() + "/"

INPUT_DIR = "input/*.txt"
############### end setting env ################


def pairwise2_main():
    util = Util.Utils()
    logic_prep = LogicPrep.LogicPreps()

    sources = util.get_files_from_dir(WORK_DIR + INPUT_DIR)

    needle_dict = logic_prep.get_pairwise2_needle_dict(sources)

    result_dict = logic_prep.get_sub_ins_del_list_dict_by_fnm(needle_dict)

    util.make_excel(WORK_DIR + "output/pairwise2_result_", result_dict)

start_time = clock()
print("start >>>>>>>>>>>>>>>>>>")
# main()
pairwise2_main()
print("::::::::::: %.2f seconds ::::::::::::::" % (clock() - start_time))