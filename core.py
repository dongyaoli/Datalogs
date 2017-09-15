# -*- coding: utf-8 -*-
#
# Copyright © 2017 Dongyao Li

import re
import pandas as pd
import dateutil.parser as dateparser
import zipfile
import io

class Recipe(object):
    gas_dict = {'Gas1' : 'COS',
                'Gas2' : 'C4F8',
                'Gas3' : 'C4F6',
                'Gas4' : 'CH2F2',
                'Gas5' : 'CHF3',
                'Gas6' : 'Xe',
                'Gas7' : 'O2',
                'Gas8' : 'SON32',
                'Gas9' : 'NotUse',
                'Gas10': 'CF4',
                'Gas11': 'NF3',
                'Gas12': 'SF6',
                'Gas13': 'Ar'}
    
    key_steps = ['ME1', 'ME2', 'ME3', 'OE']
    
    def __init__(self):
        self.num_step = 0
        self.setpoints = None
        self.constants = {}
        self.name = None
    
    def compare(self, recipe):
        '''
        Compare this recipe with a different recipe and output the difference
        '''
        if type(recipe) != Recipe:
            raise TypeError('Must compare with a Recipe')
        
        # Compare set_points
        max_compare_step = min(self.num_step, recipe.num_step)
        extra = set(self.setpoints.columns) - set(recipe.setpoints.columns)
        deficiency = set(recipe.setpoints.columns) - set(self.setpoints.columns)
        if len(extra) > 0:
            for channel in extra:
                print('Recipe ' + self.name + ' has extra channel: ' + channel)
                self.setpoints.drop(channel, axis=1, inplace=True)
        if len(deficiency) > 0:
            for channel in deficiency:
                print('Recipe ' + self.name + ' doesn\'t have channel: ' + channel)
                recipe.setpoints.drop(channel, axis=1, inplace=True)
        
        idx_mask = self.setpoints.index[:max_compare_step] == recipe.setpoints.index[:max_compare_step]
        
        value_mask = self.setpoints.loc[idx_mask] != recipe.setpoints.loc[idx_mask]
        
        unique1 = self.setpoints.loc[idx_mask][value_mask]
        unique1.dropna(axis=1, how='all', inplace=True)
        unique1.dropna(axis=0, how='all', inplace=True)
        
        unique2 = recipe.setpoints.loc[idx_mask][value_mask]
        unique2.dropna(axis=1, how='all', inplace=True)
        unique2.dropna(axis=0, how='all', inplace=True)
        
#        index = pd.MultiIndex.from_product([unique1.columns.values, ['difference', 'purpose']])
        
        setpt_comp = unique1.astype(str) + '/' + unique2.astype(str)
        setpt_diff = pd.DataFrame(columns=unique1.columns)
        for column in unique1.columns:
            try:
                setpt_diff[column] = unique1[column] - unique2[column]
            except:
                continue
        setpt_diff.fillna(0, inplace=True)
        constant_mask = self.constants != recipe.constants
        const_diff = self.constants.loc[constant_mask] + '(' + recipe.constants.loc[constant_mask] + ')'
        return (setpt_diff, const_diff, setpt_comp)
    
    def interpret(self, backbone, drop_column=[]):
        '''
        Interpret the current recipe using the backbone recipe
        '''
        setpt_diff, const_diff, setpt_comp = self.compare(backbone)
        
        if len(setpt_diff) != 0:
            # There is difference in set points
            interpret = pd.DataFrame(columns=setpt_diff.columns)
            interpret.index.name = 'RecipeStepName'
            
            setpt_diff.index = setpt_diff.index.droplevel()
            for step_name in setpt_diff.index.values:
                if step_name in self.key_steps:
                    interpret.loc[step_name] = setpt_diff.loc[step_name]
            for i in interpret.columns.values:
                for keyword in drop_column:
                    if keyword in i:
                        interpret.drop(i, axis=1, inplace=True)
        
            interpret['recipe'] = self.name.split('_')[-1]
    #        interpret['recipe'] = self.name
            interpret.set_index('recipe', append=True, inplace=True)
            interpret = interpret.reorder_levels(['recipe', 'RecipeStepName'])
            interpret = interpret.reindex_axis(sorted(interpret.columns), axis=1)
            
            for i in const_diff.index.values:
                interpret[i] = const_diff.loc[i]
        else:
            interpret = pd.DataFrame()
            interpret = interpret.append(const_diff, ignore_index=True)
            tuples = [(self.name.split('_')[-1], 'All Steps')]       
            interpret.index = pd.MultiIndex.from_tuples(tuples, names=['recipe', 'RecipeStepName'])
        
#        setpt_diff, const_diff, setpt_comp = self.compare(backbone)
#        setpt_diff.index = setpt_diff.index.droplevel()
#        setpt_diff = setpt_diff.transpose()
#        interpret = pd.DataFrame(index=setpt_diff.index)
#        interpret.columns.name = 'RecipeStepName'
#        recipe = self.name.split('_')[-1]
#        for step_name in setpt_diff.columns.values:
#            if step_name in self.key_steps:
#                interpret[recipe + '_' + step_name] = setpt_diff[step_name]
        return interpret
                
            

class WDLReader(object):
    
    _discard_setpt = ['modified', 'CoFlow1PositionLearned', 
                      'RF400kHzLearnedFrequency', 'RF60MHzLearnedFrequency',
                      'RF400kHzTap', 'RF60MHzTap',
                      'RF400kHzState0LearnedFrequency', 'RF60MHzState0LearnedFrequency',
                      'TGFBulkFlowCenterSetpoint', 'TGFBulkFlowEdgeSetpoint', 
                      'TGFBulkFlowMiddleSetpoint', 'ValveActualPosition',
                      'WAPActualPosition']
    
    def __init__(self, signature=[], exclude=[], catagories={} ):
        self.info = {}
        self.channel_list = {}
        self.data = None
        self.time_line = {}
        self.recipe = Recipe()
        self.signature = signature
        self.exclude = exclude
        self.defected = True
        self.catagory = 'Process'
        self.cata_dic = catagories
        self.file_path = None
        self.parse_lvl = None
        
    def load(self, filePath, true_path=None, parse='full', target=None):
        '''
        parse : str, optional, 'info', 'recipe', 'full'
        '''
        if true_path is None:
            self.file_path = filePath
        else:
            self.file_path = true_path
            
        self.parse_lvl = parse

        parse_stage = 1        
        with zipfile.ZipFile(filePath) as z:
            txt_file = z.open(z.namelist()[0])
            wdl = io.TextIOWrapper(txt_file)           
            for line_count, line in enumerate(wdl, 1):
                # Stage 1: reading process basic info
                if parse_stage == 1:
                    info_list = line.strip().split(':')
                    if info_list[0] == 'machineID':
                        self.info['machineID'] = info_list[1].strip().split('\t')[0]
                        self.info['waferID'] = info_list[2].strip().split('\t')[0]
                        self.info['Recipe'] = info_list[3].strip()
#                        print(self.info['Recipe'])
                        if len(self.signature) == 0:
                            self.defected = False
                        else:
                            for keyword in self.signature:
                                if keyword in self.info['Recipe']:
                                    self.defected = False
                            if not self.defected and target is not None:
                                on_target = False
                                for keyward in target:
                                    if keyward in self.info['Recipe']:
                                        on_target = True
                                        break        
                                self.defected = not on_target
                                      
                        if self.defected:
                            break
                        for keyword in self.exclude:
                            if keyword in self.info['Recipe']:
                                self.defected = True
                                break
                        for cata, keyword in self.cata_dic.items():
                            if keyword in self.info['Recipe']:
                                self.catagory = cata                        
                            
                        self.recipe.name = info_list[3].strip()
                    elif len(info_list) == 2:
                        key, content = info_list
                        self.info[key] = content.strip()
                    elif info_list[0] == 'Start':
                        start_t, end_t = line.strip().split('\t')
                        self.info['Start Time'] = dateparser.parse(start_t.split('(')[-1][:-1])
                        self.info['End Time'] = dateparser.parse(end_t.split('(')[-1][:-1])
                        parse_stage = 2
                # Stage 2: reading channel info
                elif parse_stage == 2:
                    if self.parse_lvl == 'info':
                        break
                    channel_info = re.split('\W+', line.strip())
                    if len(channel_info) > 3:
                        if channel_info[2] == 'name':
                            self.channel_list[channel_info[3]] = int(channel_info[6])
                        elif channel_info[2] == 'channels':
                            self.info['Number of Channels'] = int(channel_info[3])
                        elif channel_info[2] == 'steps':
                            self.recipe.num_step = int(channel_info[3])
                            parse_stage = 3                            
                # Stage 3: reading recipe set_points
                elif parse_stage == 3:
                    recipe_info = line.strip().split('\t')
                    if recipe_info[0].isdigit():
                        step_no = int(recipe_info[0])
                        self.recipe.setpoints.loc[step_no] = recipe_info
                        if step_no == self.recipe.num_step:
                            time_table = pd.DataFrame(columns=['catagory', 'unit', 'SetTime', 'Step'])
                            self.recipe.setpoints.set_index('Step', inplace=True)
                            for label in self._discard_setpt:
                                if label in self.recipe.setpoints.columns.values:
                                    self.recipe.setpoints.drop(label, axis=1, inplace=True)                            
                            for column in self.recipe.setpoints:
                                self.recipe.setpoints[column] = pd.to_numeric(self.recipe.setpoints[column], errors='ignore')                   
                            parse_stage = 4  
                    elif recipe_info[0] == 'Step':
                        self.recipe.setpoints = pd.DataFrame(columns=recipe_info)
                # Stage 4: reading time setting for each step and included in recipe
                elif parse_stage == 4:
                    time_info = line.strip().split('\t')
                    if len(time_info) == 4:
                        time_series = pd.Series(time_info, index=['catagory', 'unit', 'SetTime', 'Step'])
                        time_table = time_table.append(time_series, ignore_index=True)
                    elif time_info[0] == 'Hardware Calibration Begin':
                        set_time = time_table.groupby('catagory').get_group('SET_TIME')
                        set_time['Step'].apply(int)
                        set_time.set_index('Step', inplace=True)
                        self.recipe.setpoints = pd.concat([self.recipe.setpoints, 
                                                           set_time['SetTime']], 
                                                            axis=1, join='inner')
                        self.recipe.setpoints.reset_index(inplace=True)
                        self.recipe.setpoints.set_index(['Step', 'RecipeStepName'], inplace=True)
                        self.recipe.setpoints.drop('SetTime',  axis=1, inplace=True)
#                        if 'RecipeStepName' in self.recipe.setpoints.columns.values:
#                                self.recipe.setpoints.set_index('RecipeStepName', inplace=True)
                    elif time_info[0] == 'Recipe Constants Begin':
                        parse_stage = 5
                    elif time_info[0] == 'Unable to write COMPLEX STEP data to log.  KeyNotFoundError  Key not found: #subsequence':
                        '''this is when recipe is not written inside the datalog'''
                        parse_stage = 6
                # Stage 5: reading recipe constant and included in recipe
                elif parse_stage == 5:
                    constant_info = line.strip().split()
                    if line.strip() == 'Recipe Constants End':
                        parse_stage = 6
                        self.recipe.constants = pd.Series(self.recipe.constants)
                    elif len(constant_info) == 1:
                        self.recipe.constants[constant_info[0]] = 'None'
                    else:
                        self.recipe.constants[constant_info[0]] = ' '.join(constant_info[1:])
                # Stage 6: reading value of each channel vs. time
                elif parse_stage == 6:
                    if self.parse_lvl == 'recipe':
                        break
                    if line.strip() == 'HistoricalData:':
                        channel_name = wdl.readline().strip().split('\t')
                        columns = pd.MultiIndex.from_product([channel_name, ['time', 'value']])
                        self.data = pd.read_csv(filePath, sep='\s+',
                                                na_values='---',
                                                names=columns,
                                                index_col=False,
                                                skiprows=line_count+2)
                        break