
import Logic
class LogicPreps:
    def __init__(self, init_arr):
        self._cpu_cnt = 0
        self.ref_list = init_arr[0]
        self.idx = init_arr[1]
        self.top_n = init_arr[2]

    def get_cnt_cpu(self):
        return self._cpu_cnt

    def set_cnt_cpu(self, cpu_cnt):
        self._cpu_cnt = cpu_cnt

    def get_pairwise2_needle_dict(self, sources, pairwise2_opt_arr):
        logic = Logic.Logics()

        result_dict = {}
        alignments_result_dict = {}
        for i in range(len(sources)):
            tmp_list = []
            alignments_result_list = []
            with open(sources[i], "r") as f:
                print(sources[i])
                print(f.readline())
                while True:
                    tmp_line = f.readline().replace("\n", "")
                    if tmp_line == "":
                        break
                    tmp_arr = tmp_line.split("\t")
                    idx = tmp_arr[0]
                    final_idx = tmp_arr[1]
                    ngs_read = tmp_arr[2]
                    ref_seq = tmp_arr[3]
                    if len(pairwise2_opt_arr) > 1:
                        ngs_read_needle, needle_result, ref_seq_needle, alignments_result = logic.get_pairwise2_needle_result(ngs_read,
                                                                                                           ref_seq,
                                                                                                           pairwise2_opt_arr[
                                                                                                               0],
                                                                                                           pairwise2_opt_arr[
                                                                                                               1],
                                                                                                           pairwise2_opt_arr[
                                                                                                               2])
                    else:  # basic setting
                        ngs_read_needle, needle_result, ref_seq_needle, alignments_result = logic.get_pairwise2_needle_result(ngs_read, ref_seq)
                    tmp_list.append([idx, final_idx, ngs_read_needle, needle_result, ref_seq_needle])
                    alignments_result_list.append([idx, final_idx, alignments_result])

            result_dict[sources[i]] = tmp_list
            alignments_result_dict[sources[i]] = alignments_result_list

        return result_dict, alignments_result_dict

    def get_pairwise2_needle_dict_simple(self, ngs_read_list):
        print("get_pairwise2_needle_dict_ starts ")
        logic = Logic.Logics()

        result_dict = {}
        alignments_result_dict = {}

        fn_name = self.ref_list[0]
        ref_seq = self.ref_list[1]
        for np_arr in ngs_read_list:
            ngs_read = np_arr[0]
            ngs_id = np_arr[1]
            ngs_read_needle, needle_result, ref_seq_needle, alignments_result = logic.get_pairwise2_needle_result(
                ngs_read, ref_seq)
            if fn_name in result_dict:
                result_dict[fn_name].append([ngs_read_needle, needle_result, ref_seq_needle, ngs_id])
            else:
                result_dict.update({fn_name: [[ngs_read_needle, needle_result, ref_seq_needle, ngs_id]]})

            if fn_name in alignments_result_dict:
                alignments_result_dict[fn_name].append([alignments_result])
            else:
                alignments_result_dict.update({fn_name: [[alignments_result]]})


        return result_dict, alignments_result_dict

    """
    :param
        needle_dict = {'D:/000_WORK/YuGooSang_KimHuiKwon/20200609/WORK_DIR/first_excel_output\\result_gDNA_0609.txt':
            [['1', 'Group1,2_RT/20-PBS/7-#Target723'
            , 'AATATATCTTGTGGAAAGGACGAAACACCG--CATACTCGGGCGC-------CGGGGTGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGACCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCACATGCCAGGTGGACGAGTTTTCTTGCTTTTTTTGATACTCTGTCTGTACTACAACGCCCATTTCCGCAAGAAAACTGGTCTACCTGGCATGTTCAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAA'
            , '.|||||||||||||||||||||||||||||  ||| .||   |||       |     ||||||||||||||||||||||||||||||||||||||.||||||||||||||||||||||||||||||||||||||||||||||||.|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'
            , 'TATATATCTTGTGGAAAGGACGAAACACCGCCCAT-TTC---CGCAAGAAAAC-----GTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCACATGCCAGGTAGACgAGTTTTCTTGCTTTTTTTGATACTCTGTCTGTACTACAACGCCCATTTCCGCAAGAAAACTGGTCTACCTGGCATGTTCAGCTTGGCGTAcCgcGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAA', '293', '293', '293', 'O']
            , ['2', 'Group1,2_RT/12-PBS/11-#Target1948'
            , 'TATATATCTTGTGGAAAGGACGAAACACCGAAGTCCGTCAGATTCTATCGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCATACCACGAGATAGAATCTGACGTTTTTTTCGTACTCATATATACATATCTCTAAGTCCGTCAGATTCTATCTGGTGGTATCTCCAGGTGAAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAA'
            , '||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'
            , 'TATATATCTTGTGGAAAGGACGAAACACCGAAGTCCGTCAGATTCTATCGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCATACCACgAGATAGAATCTGACGTTTTTTTCGTACTCATATATACATATCTCTAAGTCCGTCAGATTCTATCTGGTGGTATCTCCAGGTGAAGCTTGGCGTAcCgcGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAA',  '280', '280', '280', 'O']
            , ['3', 'Group1,2_RT/20-PBS/17-#Target833'
            , '-----------------------------------------------------------------------------------------CG-------CTTGAAAAAGTGGCACCGAGTCGGTGCTTACCTCTTTGGATCGTGATCACAATCCTCCAGATGCTTTTTTTCAGATAGCATACTGTATACTGGGCATCTGGAGGATTGTGATCAGGATCCAAAGAGGTAATGAGCTTGGCGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAACGTGCACGTGACACGTTCCAGACCGTACATGCTTACATGGGATGAAGCTTGGCGTAACTAGATCTTGAGACAAATGGCAGTATT'
            , '                                                                                         ||       ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||                                                                                    '
            , 'TATATATCTTGTGGAAAGGACGAAACACCGCATCTGGAGGATTGTGATCGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTACCTCTTTGGATCgTGATCACAATCCTCCAGATGCTTTTTTTCAGATAGCATACTGTATACTGGGCATCTGGAGGATTGTGATCAGGATCCAAAGAGGTAATGAGCTTGGCGTAcCgcGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAA------------------------------------------------------------------------------------', '378', '378', '378', 'O']
            , ['4', 'Group1,2_RT/12-PBS/9-#Target489'
            , 'TATATATCTTGTGGAAAGGACGAAACACCGGCGCGGAACAGGTCG--ATC-TGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCAAGTACCGTTTGATGCCGCTGTTTTTTTCATACACGACACACATCTGAGGTCGTTCACCAGCGGCATCAAAGGGTACTTCATGGCGCATAGCTTGGTGTACCGCGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAA'
            , '||||||||||||||||||||||||||||| |||...|.|||  ||  ||| .||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||.||||||||||||||||||||||||||||||||||||||||||||||||||||||||'
            , 'TATATATCTTGTGGAAAGGACGAAACACC-GCGTTCACCAG--CGGCATCAAGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCAAGTACCgTTTGATGCCGCTGTTTTTTTCATACACGACACACATCTGAGGTCGTTCACCAGCGGCATCAAAGGGTACTTCATGGCGCATAGCTTGGCGTAcCgcGATCTCTACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAA', '281', '281', '281', 'O']
            ]} 
    """
    def get_sub_ins_del_list_dict_by_fnm(self, needle_dict):
        result_dict = {}
        for fnm_key, val_list in needle_dict.items():
            result_dict.update({fnm_key: []})
            for val_arr in val_list:
                read_no = val_arr[0]
                final_index = val_arr[1]
                ngs_read = val_arr[2].upper()
                ref_seq = val_arr[4].upper()
                re_idx = 0
                sub_dict = {}
                ins_dict = {}
                del_dict = {}
                for i in range(len(ngs_read)):
                    if ngs_read[i] != ref_seq[i]:
                        # del
                        if ngs_read[i] == "-":
                            re_idx += 1
                            del_dict.update({re_idx: ref_seq[i]})
                        # ins
                        elif ref_seq[i] == "-":
                            if re_idx in ins_dict:
                                ins_dict[re_idx] += ngs_read[i]
                            else:
                                ins_dict.update({re_idx: ngs_read[i]})
                        # sub
                        else:
                            re_idx += 1
                            sub_dict.update({re_idx: ref_seq[i] + "->" + ngs_read[i]})
                    else:
                        re_idx += 1
                result_dict[fnm_key].append([final_index, sub_dict, ins_dict, del_dict, re_idx, read_no])
        return result_dict

    def get_pairwise2_needle_dict_by_ref_seq(self, ngs_list):
        logic = Logic.Logics()
        result_dict = {}
        print("get_pairwise2_needle_dict_by_ref_seq starts ")
        for val_arr in self.ref_list:
            ref_seq = val_arr[0]
            for ngs_read_arr in ngs_list:
                ngs_read = ngs_read_arr[0]
                ngs_read_needle, needle_result, ref_seq_needle = logic.get_pairwise2_needle_result(ngs_read, ref_seq)
                needle_cnt = needle_result.count('|')
                ins_cnt = ref_seq_needle.count("-")
                del_cnt = ngs_read_needle.count("-")
                needle_tot = len(needle_result)
                sub_cnt = needle_tot - (needle_cnt + del_cnt + ins_cnt)
                if ref_seq in result_dict:
                    result_dict[ref_seq].append([needle_cnt, ins_cnt, del_cnt, sub_cnt, ngs_read])
                    # TODO val_arr 이 너무 많은 경우 TOP_N 갯수 만큼 필터링 추가
                    sorted_list = logic.get_sorted_list_by_idx_ele(result_dict[ref_seq], self.idx)
                    result_dict[ref_seq] = sorted_list[:self.top_n]
                else:
                    result_dict.update({ref_seq: [[needle_cnt, ins_cnt, del_cnt, sub_cnt, ngs_read]]})

        return result_dict

    def merge_multi_dict(self, pool_list):
        merge_dict = {}
        for split_dict in pool_list:
            for ref_seq_key, val_list in split_dict.items():
                if ref_seq_key in merge_dict:
                    merge_dict[ref_seq_key].extend(val_list)
                else:
                    merge_dict.update({ref_seq_key: val_list})
        return merge_dict

    def merge_multi_dict_from_simple(self, pool_list):
        merge_result_dict = {}
        merge_alignments_result_dict = {}
        for pool_tp in pool_list:
            result_dict = pool_tp[0]
            alignments_result_dict = pool_tp[1]
            for fn_key, val_list in result_dict.items():
                if fn_key in merge_result_dict:
                    merge_result_dict[fn_key].extend(val_list)
                else:
                    merge_result_dict.update({fn_key: val_list})

        return merge_result_dict, merge_alignments_result_dict

    def get_sub_ins_del_list_dict_from_simple(self, needle_dict):
        result_dict = {}
        for fnm_key, val_list in needle_dict.items():
            result_dict.update({fnm_key: []})
            for val_arr in val_list:
                ngs_read = val_arr[0].upper()
                ref_seq = val_arr[2].upper()
                ngs_id = val_arr[3]
                re_idx = 0
                sub_dict = {}
                ins_dict = {}
                del_dict = {}
                for i in range(len(ngs_read)):
                    if ngs_read[i] != ref_seq[i]:
                        # del
                        if ngs_read[i] == "-":
                            re_idx += 1
                            del_dict.update({re_idx: ref_seq[i]})
                        # ins
                        elif ref_seq[i] == "-":
                            if re_idx in ins_dict:
                                ins_dict[re_idx] += ngs_read[i]
                            else:
                                ins_dict.update({re_idx: ngs_read[i]})
                        # sub
                        else:
                            re_idx += 1
                            sub_dict.update({re_idx: ref_seq[i] + "->" + ngs_read[i]})
                    else:
                        re_idx += 1

                result_dict[fnm_key].append([sub_dict, ins_dict, del_dict, re_idx, ngs_id])
        return result_dict

