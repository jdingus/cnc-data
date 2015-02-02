#! /usr/bin/python
from start_stop import create_start_stop
from sqlite_module import write_list_data,initialize_tables

def main():

    start_stop = create_start_stop('data_example.csv')
    data_entries = listdicts_to_listentries(start_stop)
    initialize_tables()
    for item in data_entries:
            write_list_data(item)

def convert_dict_to_commas(dict_in,col_order):
    '''Takes a dictionary and list of col_order to output in  and creates a csv line 
     of the values in the col_order given'''
    list_values = []
    for item in col_order:
        list_values.append(dict_in[item])
    return list_values

def listdicts_to_listentries(list_dicts):
    col_order = ['start_time','stop_time','cnc_id','prog_num','part1_num','part1_suf','part1_qty','part2_num','part2_suf','part2_qty','ref_input','pc_time','tc_time','prog_ct','ref_output']
    list_entries = []
    for ind_dict in list_dicts:
        single_entry = convert_dict_to_commas(ind_dict,col_order)
        list_entries.append(single_entry)
    return list_entries

if __name__ == '__main__':
    main()