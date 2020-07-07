from Bio import pairwise2
from Bio.SubsMat.MatrixInfo import blosum62

import Util

class Logics:
    def __init__(self):
        self.tmp = ""

    """
    by using the BLOSUM62 matrix, together with a gap open penalty of 10 and a gap extension penalty of 0.5 (using globalds)
    """
    def get_pairwise2_needle_result(self, asequence, bsequence, matrx=blosum62, gap_open_penalty=10, extension_penalty=0.5):
        alignments = pairwise2.align.globalds(asequence.upper().replace(" ", ""), bsequence.upper().replace(" ", ""), matrx, -gap_open_penalty,
                                              -extension_penalty)
        alignments_result = pairwise2.format_alignment(*alignments[0])
        align_arr = alignments_result.split("\n")
        return align_arr[0], align_arr[1], align_arr[2], alignments_result

    def get_del_idx_seq(self, idx_key, del_dict, del_seq):
        if idx_key in del_dict:
            return self.get_del_idx_seq(idx_key + 1, del_dict, del_seq + del_dict[idx_key])
        else:
            return idx_key - 1, del_seq

    def get_sub_idx_seq(self, idx_key, sub_dict, seq_arr):
        sub_seq_from = seq_arr[0]
        sub_seq_to = seq_arr[1]
        if idx_key in sub_dict:
            sub_seq_from_char = sub_dict[idx_key].split("->")[0]
            sub_seq_to_char = sub_dict[idx_key].split("->")[1]
            return self.get_sub_idx_seq(idx_key + 1, sub_dict, [sub_seq_from + sub_seq_from_char, sub_seq_to + sub_seq_to_char])
        else:
            return idx_key - 1, sub_seq_from, sub_seq_to

    def get_sorted_list_by_idx_ele(self, data_list, idx):
        sorted_list = []
        for tmp_list in sorted(data_list, key=lambda tmp_list: tmp_list[idx], reverse=True):
            sorted_list.append(tmp_list)
        return sorted_list

    def sort_dict_top_n_by_idx_ele(self, input_dict, idx, top_n):
        result_dict = {}
        for ref_seq_key, val_list in input_dict.items():
            soted_list = self.get_sorted_list_by_idx_ele(val_list, idx)
            result_dict.update({ref_seq_key: soted_list[:top_n]})
        return result_dict