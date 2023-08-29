"""
Alternative if no need to copy activities in a new DB
"""
import pprint
import json
import random
from logging import getLogger
from pathlib import Path
import typing
import bw2data
import bw2data as bd
import openpyxl
import pandas as pd
from bw2data.backends import Activity
from bw2data.errors import UnknownObject
from ast import literal_eval
from enbios2.generic.files import DataPath
from projects.seed.Data.const import data_path
getLogger("peewee").setLevel("ERROR")

#data_path = DataPath("temp/seeds")
processors_path = data_path / 'base_file_simplified.xlsx'

calliope = data_path / 'flow_out_sum_modified.csv'
dict_path = data_path / 'enbios_input_3.json'
tree_path=data_path / 'tree_mod.json'
tree_path_2=data_path / 'tree_mod2.json'
dict_gen=data_path/'dict_names.json'
data = openpyxl.load_workbook(processors_path)
processors = data.active
bd.projects.set_current('ecoinvent')
database = bd.Database('cutoff_3.9.1_default')

print(bd.projects.dir)




# Scenarios_cool

def get_scenario(df):
    """
    Iters through 1 scenario of the data.csv (scenarios data), storing basic data in a dictionary
    Gets like
    activities : {
        alias : [
        unit,
        amount]
    }

    :param df:
    :return:
    """
    scenario = {}


    for index, row in df.iterrows():
        other_stuff = []
        alias = row['aliases']
        flow_out_sum = (row['flow_out_sum'])
        unit = row['units']
        other_stuff.append(unit)
        other_stuff.append(flow_out_sum)

        scenario[alias] = other_stuff
    return scenario






def generate_scenarios(calliope_data, smaller_vers=False):
    """
    Iterate through the data from calliope (data.csv, output results...)
        -Create new columns, such as alias

    :param calliope_data:
    :param smaller_vers: BOOL, if true, a small version of the data for testing gets produced
    :return:
    """


    cal_dat = pd.read_csv(calliope_data, delimiter=',')
    cal_dat['aliases'] = cal_dat['techs'] + '__' + cal_dat['carriers'] + '___' + cal_dat['locs'] # Use ___ to split the loc for the recognision of the activities
    scenarios = cal_dat['scenarios'].unique().tolist()
    if smaller_vers:  # get a small version of the data
        scenarios = scenarios[:3]

    cooler_dooper = {}

    for scenario in scenarios:
        df = cal_dat[cal_dat['scenarios'] == scenario]
        stuff = get_scenario(df)
        cooler_dooper[scenario] = {}
        cooler_dooper[scenario]['activities'] = stuff

    # GENERATE KEYS FOR THE SCENARIOS

    scens = random.choice(list(cooler_dooper.keys()))  # select a random scenario from the list
    print(f'techs from scenario {scens} chosen')
    acts=list(cooler_dooper[scens]['activities'].keys())


    # Generate a code-region alias name dictionary to create the hierarchy

    general={}
    for act in set(acts):
        act_key=act.split('___')[0]
        if act_key not in general.keys():
            elements_to_append=[]
            for act2 in set(acts):
                act_key2=act2.split('___')[0]
                if act_key2 == act_key:
                    elements_to_append.append(act2)
            general[act_key]=elements_to_append


    with open(dict_gen, 'w') as file:
        json.dump(general, file, indent=4)





    return cooler_dooper,acts


def generate_activities(*args) ->dict:
    processors = pd.read_excel(processors_path, sheet_name='BareProcessors simulation')

    activities_cool = {}
    for index, row in processors.iterrows():
        code = str(row['BW_DB_FILENAME'])

        print('im parsing', str(row['Processor']), code)
        try:
            act = database.get_node(code)

        except UnknownObject:
            print(row['Processor'], 'has an unknown object')
            pass

        name = act['name']
        unit = act['unit']
        alias = str(row['Processor']) + '__' + str(row['@SimulationCarrier'])
        print(alias)

        activities_cool[alias] = {
            'name': name,
            'code': code,
        }
    pprint.pprint(activities_cool)
    # CALL THE FUNCTION HERE
    activities={}
    pass
    for element  in args:
        print('ELEMTNT IS ',element)
        new_element=element.split('___')[0] #This should match the name
        for key in activities_cool.keys():
            if new_element==key:

                new_code=activities_cool[key]['code']
                activities[element]={
                    "id":{
                        'code':new_code
                    }

                }

    print('#THE DICTIONARY IS')
    pprint.pprint(activities)
    return activities

def tree_last_level(df,*args):
    """

    :param df:
    :param names: comes from generate scenarios. List of unique aliases
    :return:
    """


    # TODO: modify here to adapt the alias
    new_rows=[]

    for index,row in df.iterrows():
        processor=row['Processor']

        for element in args:
            cop=element.split('___')[0]
            if cop == processor:
                new_row=row.copy()
                new_row['Processor']=element

                new_rows.append(new_row)

    df = pd.concat([df] +new_rows, ignore_index=True)


    last_level_list=[]
    # return a list of dictionaries
    parents=list(df['ParentProcessor'].unique())

    for parent in parents:
        last_level = {}

        df3=df[df['ParentProcessor']==parent]
        childs=df3['Processor'].unique().tolist()
        last_level[parent]=childs
        last_level_list.append(last_level)
    return last_level_list



def generate_dict(df,list_pre):
    """
    Pass a list of the lower level and the dataframe of the present
    Returns a list of the dictionary


    :param df:
    :param list:
    :return:
    """
    parents=df['ParentProcessor'].unique().tolist()
    list_branches=[]
    pass
    for parent in parents:
        branch={}
        df_parent=df[df['ParentProcessor']==parent]
        branch[parent]={}

        for _,row in df_parent.iterrows():
            child_df=row['Processor']
            for element in list_pre:
                if child_df in element:

                    branch[parent][child_df]=element[child_df]
        list_branches.append(branch)


    return list_branches


def hierarchy(data,*args):
    df=pd.read_excel(data, sheet_name='parents')
    df2=pd.read_excel(data,sheet_name='BareProcessors simulation')


    # Do some changes to match the regions and aliases

    df2['Processor']=df2['Processor']+'__'+df2['@SimulationCarrier']  # Mark, '__' for carrier split

    #start by the last level of parents
    levels=df['Level'].unique().tolist()
    last_level_parent=int(levels[-1].split('-')[-1])
    last_level_processors='n-' + str(last_level_parent+1)
    df2['Level']=last_level_processors
    df=pd.concat([df,df2[['Processor','ParentProcessor','Level']]],ignore_index=True,axis=0)

    levels = df['Level'].unique().tolist()

    list_total=[]

    for level in reversed(levels):
        df_level=df[df['Level']==level]

        if level==levels[0]:
            break
        elif level==levels[-1]:

            last=tree_last_level(df_level,*args)
            global last_list
            last_list=last

        else:

            df_level=df[df['Level']==level]
            list_2=generate_dict(df_level,last_list)
            last_list=list_2
            list_total.append(list_2)

    dict_tree=list_total[-1]
    a=dict_tree[-1]
    with open(tree_path,'w') as file:
        json.dump(a,file, indent=4)



    return dict_tree[-1]





enbios2_methods = {
    'ozone depletion potential (ODPinfinite)': ('ReCiPe 2016 v1.03, midpoint (H)',
                                                'ozone depletion',
                                                'ozone depletion potential (ODPinfinite)'),
    'agricultural land occupation (LOP)': ('ReCiPe 2016 v1.03, midpoint (H)',
                                           'land use',
                                           'agricultural land occupation (LOP)'),
    'surplus ore potential (SOP)': ('ReCiPe 2016 v1.03, midpoint (H)',
                                    'material resources: metals/minerals',
                                    'surplus ore potential (SOP)'),
    'global warming potential (GWP1000)': ('ReCiPe 2016 v1.03, midpoint (H)',
                                           'climate change',
                                           'global warming potential (GWP1000)')
}



enbios2scenarios,activ_names = generate_scenarios(calliope, smaller_vers=True)
hope_final_acts=generate_activities(*activ_names)
print(activ_names)


hierarchy=hierarchy(processors_path,*activ_names)


with open(dict_gen, 'r') as second_file:
    second_dict = json.load(second_file)

def print_all_list_values(hierarchy_dict):
    # 1 look for the list

    for value in hierarchy_dict.values():

        if isinstance(value, list):
            print("Lista encontrada:", value)

            values_copy = value[:]
            value.clear()

            print(values_copy)
            for element in values_copy:

                for key,val in second_dict.items():
                    if element==key:
                        print(element, 'is equal to', key)
                        list_names=second_dict[key]

                        # 3. Include the new names
                        for name in list_names:
                            print(name)
                            value.append(name)



        elif isinstance(value, dict):
            print_all_list_values(value)

    with open(tree_path_2, 'w') as file:
            json.dump(hierarchy_dict, file, indent=4)

print_all_list_values(hierarchy)






enbios2_data = {
    "bw_project": 'ecoinvent',
    "activities": hope_final_acts,
    "hierarchy" : hierarchy,
    "methods": enbios2_methods,
    "scenarios": enbios2scenarios
}

with open(dict_path, 'w') as gen_diction:
    json.dump(enbios2_data, gen_diction, indent=4)
pass

print(activ_names)
# We're assuming that one scenario includes all the possible technologies




