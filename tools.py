import dash_core_components as dcc
import plotly.graph_objs as go
import plotly

color_list = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)', 
              'rgb(214, 39, 40)', 'rgb(148, 103, 189)', 'rgb(140, 86, 77)', 
              'rgb(227, 119, 194)', 'rgb(127, 127, 127)', 'rgb(188, 189, 34)',
              'rgb((23, 190, 207)']

lineStyle = ['', 'dash', 'dot', 'dashdot']


power_channel =['RF400kHzGenDeliveredPower',
                  'RF400kHzFrequency_AI',
                  'RF400kHzGenDeliveredPower',
                  'RF400kHzGenReflectedPower_AI',
                  'RF400kHzPulseState0DeliveredPower_AI',
                  'RF400kHzPulseState0ReflectedPower_AI',
                  'RF400kHzPulseState0DeliveredPower_AI',
                  'RF400kHzGenDeliveredPower',
                  'RF60MHzFrequency_AI',
                  'RF60MHzGenDeliveredPower',
                  'RF60MHzGenReflectedPower_AI',
                  'RF60MHzPulseState0DeliveredPower_AI',
                  'RF60MHzPulseState0ReflectedPower_AI',
                  'RF60MHzPulseState0DeliveredPower_AI']

temp_panel = [['InnerTopPlateHeaterTemperatureMonitor_AI',
               'InnerTopPlateHeaterTemperatureOutputValue_AI',],
              ['OuterTopPlateHeaterTemperatureMonitor_AI',
               'OuterTopPlateHeaterTemperatureOutputValue_AI',],
              ['ESCCoolantFlow_AI',
               'ESCCoolantSupplyTemperatureMonitor_AI',
               'ESCCoolantReturnTemperatureMonitor_AI',],
              ['InnerUpperElectrode1TemperatureMonitor_AI',
               'InnerUpperElectrode2TemperatureMonitor_AI',
               'InnerUpperElectrode3TemperatureMonitor_AI',
               'InnerUpperElectrode4TemperatureMonitor_AI',
               'InnerUpperElectrodeTemperatureMonitor_AI',],           
              ['ESCTemperatureMonitor1_AI',
               'ESCTemperatureMonitor2_AI',],
              ['HeInnerZoneBacksideFlow_AI',
               'HeOuterZoneBacksideFlow_AI',
               'HeInnerZoneBacksidePressure_AI',
               'HeOuterZoneBacksidePressure_AI',],
              ['TCUCh1TempMonitor_AI',            
               'TCUCh2TempMonitor_AI',
               'TCU2Monitor_AI',],               
               ]

pres_panel = [['ConfinementRingPosition_AI',
               'ConfinementRingAdjustedPosition',],
              ['ForelineManometerAdjustedPressure',
               'ChamberManometer_RawAI',],
              ['ProcessManometer_RawAI',
               'ProcessManometerAdjustedPressure',],              
              ]


lengend_style = dict(orientation='v', font=dict(size=8)) 

def temperature_panel(wdl_list):
    
    fig_list = []
    
    # Figure 1
    plot_idx = 0
    label=True
    row = len(temp_panel[plot_idx])
    fig = plotly.tools.make_subplots(rows=row, cols=1, 
                                     specs=[[{}], [{}]],
                                     subplot_titles=temp_panel[plot_idx],
                                     shared_xaxes=True)
    titles = []
    for i in range(len(temp_panel[plot_idx])):
        channel = temp_panel[plot_idx][i]
        titles.append(channel)
        for j in range(len(wdl_list)):
            color = color_list[j % len(color_list)]
            wdl = wdl_list[j]       
            y_trace = wdl.data[(channel, 'value')]
            trace = go.Scatter( x = wdl.data[(channel, 'time')]/1000,
                                y = y_trace,
                                legendgroup = wdl.info['Recipe'],
                                mode = 'lines',
                                line = dict(width = 1, 
                                            color=color),
                                name = wdl.info['Recipe'],
                                text = wdl.info['Recipe'],
                                hoverinfo='y+text',
                                showlegend=label
                                )
            fig.append_trace(trace, i+1, 1)
        label = False
    fig['layout']['legend']=lengend_style                                            
    fig_list.append(dcc.Graph(id='InnerTopPlate',
                              figure=fig,
                              style={'width':'33%'}))
    
    # Figure 2
    plot_idx = 1
    label=True
    row = len(temp_panel[plot_idx])
    fig = plotly.tools.make_subplots(rows=row, cols=1, 
                                     subplot_titles=temp_panel[plot_idx],
                                     shared_xaxes=True)
    titles = []
    for i in range(len(temp_panel[plot_idx])):
        channel = temp_panel[plot_idx][i]
        titles.append(channel)
        for j in range(len(wdl_list)):
            color = color_list[j % len(color_list)]
            wdl = wdl_list[j]       
            y_trace = wdl.data[(channel, 'value')]
            trace = go.Scatter( x = wdl.data[(channel, 'time')]/1000,
                                y = y_trace,
                                legendgroup = wdl.info['Recipe'],
                                mode = 'lines',
                                line = dict(width = 1, 
                                            color=color),
                                name = wdl.info['Recipe'],
                                text = wdl.info['Recipe'],
                                hoverinfo='y+text',
                                showlegend=label
                                )
            fig.append_trace(trace, i+1, 1)
        label = False
    fig['layout']['legend']=lengend_style                                           
    fig_list.append(dcc.Graph(id='OuterTopPlate',
                              figure=fig,
                              style={'width':'33%'}))
    
    # Figure 3
    plot_idx = 2
    label=True
    row = len(temp_panel[plot_idx])
    fig = plotly.tools.make_subplots(rows=row, cols=1,                                 
                                     subplot_titles=temp_panel[plot_idx],
                                     shared_xaxes=True)
    for i in range(len(temp_panel[plot_idx])):
        channel = temp_panel[plot_idx][i]
        for j in range(len(wdl_list)):
            color = color_list[j % len(color_list)]
            wdl = wdl_list[j]       
            y_trace = wdl.data[(channel, 'value')]
            trace = go.Scatter( x = wdl.data[(channel, 'time')]/1000,
                                y = y_trace,
                                legendgroup = wdl.info['Recipe'],
                                mode = 'lines',
                                line = dict(width = 1, 
                                            color=color),
                                name = wdl.info['Recipe'],
                                text = wdl.info['Recipe'],
                                hoverinfo='y+text',
                                showlegend=label
                                )
            fig.append_trace(trace, i+1, 1)
        label = False
    fig['layout']['legend']=lengend_style                                           
    fig_list.append(dcc.Graph(id='ESCCool',
                              figure=fig,
                              style={'width':'33%'}))
    
    # Figure 4
    plot_idx = 3
    label=True
    column = len(temp_panel[plot_idx])
    fig = plotly.tools.make_subplots(rows=1, cols=column, 
                                     subplot_titles=['iUET_Avg', 'iUET_1', 'iUET_2',
                                                     'iUET_3', 'iUET_4'],
                                     shared_yaxes=True)
    for i in range(len(temp_panel[plot_idx])):
        channel = temp_panel[plot_idx][i]
        for j in range(len(wdl_list)):
            color = color_list[j % len(color_list)]
            wdl = wdl_list[j]       
            y_trace = wdl.data[(channel, 'value')]
            trace = go.Scatter( x = wdl.data[(channel, 'time')]/1000,
                                y = y_trace,
                                legendgroup = wdl.info['Recipe'],
                                mode = 'lines',
                                line = dict(width = 1, 
                                            color=color),
                                name = wdl.info['Recipe'],
                                text = wdl.info['Recipe'],
                                hoverinfo='y+text',
                                showlegend=label
                                )
            if channel == 'InnerUpperElectrodeTemperatureMonitor_AI':
                fig.append_trace(trace, 1, 1)
            else:
                fig.append_trace(trace, 1, i+2)
        label = False
    fig['layout']['legend']=lengend_style                                         
    fig_list.append(dcc.Graph(id='iUET',
                              figure=fig,
                              style={'width':'100%'}))
    
    # Figure 5
    plot_idx = 4
    label=True
    row = len(temp_panel[plot_idx])
    fig = plotly.tools.make_subplots(rows=row, cols=1,                                 
                                     subplot_titles=temp_panel[plot_idx],
                                     shared_xaxes=True)
    for i in range(len(temp_panel[plot_idx])):
        channel = temp_panel[plot_idx][i]
        for j in range(len(wdl_list)):
            color = color_list[j % len(color_list)]
            wdl = wdl_list[j]       
            y_trace = wdl.data[(channel, 'value')]
            trace = go.Scatter( x = wdl.data[(channel, 'time')]/1000,
                                y = y_trace,
                                legendgroup = wdl.info['Recipe'],
                                mode = 'lines',
                                line = dict(width = 1, 
                                            color=color),
                                name = wdl.info['Recipe'],
                                text = wdl.info['Recipe'],
                                hoverinfo='y+text',
                                showlegend=label
                                )
            fig.append_trace(trace, i+1, 1)
        label = False
    fig['layout']['legend']=lengend_style                                        
    fig_list.append(dcc.Graph(id='ESCTemp',
                              figure=fig,
                              style={'width':'33%'}))
    
    # Figure 6
    plot_idx = 5
    label=True
    fig = plotly.tools.make_subplots(rows=2, cols=2,                                 
                                     subplot_titles=['HeIFlow', 'HeOFlow',
                                                     'HeIPress', 'HeOPress'],
                                     shared_xaxes=True)
    for i in range(len(temp_panel[plot_idx])):
        channel = temp_panel[plot_idx][i]
        for j in range(len(wdl_list)):
            color = color_list[j % len(color_list)]
            wdl = wdl_list[j]       
            y_trace = wdl.data[(channel, 'value')]
            trace = go.Scatter( x = wdl.data[(channel, 'time')]/1000,
                                y = y_trace,
                                legendgroup = wdl.info['Recipe'],
                                mode = 'lines',
                                line = dict(width = 1, 
                                            color=color),
                                name = wdl.info['Recipe'],
                                text = wdl.info['Recipe'],
                                hoverinfo='y+text',
                                showlegend=label
                                )
            fig.append_trace(trace, i//2 + 1, i%2 + 1)
        label = False
    fig['layout']['legend'] = lengend_style                                         
    fig_list.append(dcc.Graph(id='HeFlow',
                              figure=fig,
                              style={'width':'33%'}))
    
    # Figure 7
    plot_idx = 6
    label=True
    row = len(temp_panel[plot_idx])
    fig = plotly.tools.make_subplots(rows=row, cols=1,                                 
                                     subplot_titles=temp_panel[plot_idx],
                                     shared_xaxes=False)
    for i in range(len(temp_panel[plot_idx])):
        channel = temp_panel[plot_idx][i]
        for j in range(len(wdl_list)):
            color = color_list[j % len(color_list)]
            wdl = wdl_list[j]       
            y_trace = wdl.data[(channel, 'value')]
            trace = go.Scatter( x = wdl.data[(channel, 'time')]/1000,
                                y = y_trace,
                                legendgroup = wdl.info['Recipe'],
                                mode = 'lines',
                                line = dict(width = 1, 
                                            color=color),
                                name = wdl.info['Recipe'],
                                text = wdl.info['Recipe'],
                                hoverinfo='y+text',
                                showlegend=label
                                )
            fig.append_trace(trace, i+1, 1)
        label = False
    fig['layout']['legend'] = lengend_style                                           
    fig_list.append(dcc.Graph(id='TCUTemp',
                              figure=fig,
                              style={'width':'33%'}))
    
#    label = False
#    
#        if not noted[plot_idx]:              
#            annotations.append(dict(xref='paper', x=0.1, y=y_trace[0],
#                                    xanchor='left', yanchor='middle',
#                                    text= channel,
#                                    font=dict(family='Arial',
#                                              size=15,),
#                                    showarrow=True))
#            fig_list[plot_idx].figure['layout']['annotations'] = annotations
#    fig_list[plot_idx].figure['layout']['legend']=dict(orientation='h')
#    noted[plot_idx] = True
#    
#    
#    
#    fig_list = [dcc.Graph(id='InnerTopPlate',
#                          figure=dict(data=[], layout={}),
#                          style={}),
#                dcc.Graph(id='OutTopPlate',
#                          figure=dict(data=[], layout={}),
#                          style={}),
#                dcc.Graph(id='InEleTemp',
#                          figure=dict(data=[], layout={}),
#                          style={}),
#                dcc.Graph(id='ESCCool',
#                          figure=dict(data=[], layout={}),
#                          style={}),
#                dcc.Graph(id='ESCTemp',
#                          figure=dict(data=[], layout={}),
#                          style={}),
#                dcc.Graph(id='He',
#                          figure=dict(data=[], layout={}),
#                          style={}),
#                dcc.Graph(id='TCUTemp',
#                          figure=dict(data=[], layout={}),
#                          style={}),
#                ]
#    noted = [False for _ in range(len(fig_list))]
#    
#    for i in range(len(wdl_list)):
#        wdl = wdl_list[i]
#        color = color_list[i % len(color_list)]
#        
#        # Figure 1
#        plot_idx = 0
#        label=True
#        annotations = []
#        for j in range(len(temp_panel[plot_idx])):
#            channel = temp_panel[plot_idx][j]
#            
#            y_trace = wdl.data[(channel, 'value')]
#            trace = go.Scatter( x = wdl.data[(channel, 'time')]/1000,
#                                y = y_trace,
#                                legendgroup = wdl.info['Recipe'],
#                                mode = 'lines',
#                                line = dict(width = 1, 
#                                            color=color, 
#                                            dash=lineStyle[j%len(lineStyle)]),
#                                name = wdl.info['Recipe'],
#                                text = wdl.info['Recipe'],
#                                hoverinfo='y+text',
#                                showlegend=label
#                                )
#            fig_list[plot_idx].figure['data'].append(trace)
#            label = False
#        
#            if not noted[plot_idx]:              
#                annotations.append(dict(xref='paper', x=0.1, y=y_trace[0],
#                                        xanchor='left', yanchor='middle',
#                                        text= channel,
#                                        font=dict(family='Arial',
#                                                  size=15,),
#                                        showarrow=True))
#                fig_list[plot_idx].figure['layout']['annotations'] = annotations
#        fig_list[plot_idx].figure['layout']['legend']=dict(orientation='h')
#        noted[plot_idx] = True
#        
#        
#        # Figure 2
#        plot_idx = 1
#        label=True
#        annotations = []
#        for j in range(len(temp_panel[plot_idx])):
#            channel = temp_panel[plot_idx][j]
#            
#            y_trace = wdl.data[(channel, 'value')]
#            trace = go.Scatter( x = wdl.data[(channel, 'time')]/1000,
#                                y = y_trace,
#                                legendgroup = wdl.info['Recipe'],
#                                mode = 'lines',
#                                line = dict(width = 1, 
#                                            color=color, 
#                                            dash=lineStyle[j%len(lineStyle)]),
#                                name = wdl.info['Recipe'],
#                                text = wdl.info['Recipe'],
#                                hoverinfo='y+text',
#                                showlegend=label
#                                )
#            fig_list[plot_idx].figure['data'].append(trace)
#            label = False
#        
#            if not noted[plot_idx]:              
#                annotations.append(dict(xref='paper', x=0.1, y=y_trace[0],
#                                        xanchor='left', yanchor='middle',
#                                        text= channel,
#                                        font=dict(family='Arial',
#                                                  size=15,),
#                                        showarrow=True))
#                fig_list[plot_idx].figure['layout']['annotations'] = annotations
#        fig_list[plot_idx].figure['layout']['legend']=dict(orientation='h')
#        noted[plot_idx] = True
#        
#        
#        # Figure 3
#        
#        plot_idx = 2
#        label=True
#        annotations = []
#        for j in range(len(temp_panel[plot_idx])):
#            channel = temp_panel[plot_idx][j]
#            
#            y_trace = wdl.data[(channel, 'value')]
#            trace = go.Scatter( x = wdl.data[(channel, 'time')]/1000,
#                                y = y_trace,
#                                legendgroup = wdl.info['Recipe'],
#                                mode = 'lines',
#                                line = dict(width = 1, 
#                                            color=color, 
#                                            dash=lineStyle[j%len(lineStyle)]),
#                                name = wdl.info['Recipe'],
#                                text = wdl.info['Recipe'],
#                                hoverinfo='y+text',
#                                showlegend=label
#                                )
#            fig_list[plot_idx].figure['data'].append(trace)
#            label = False
#        
#            if not noted[plot_idx]:              
#                annotations.append(dict(xref='paper', x=0.1, y=y_trace[0],
#                                        xanchor='left', yanchor='middle',
#                                        text= channel,
#                                        font=dict(family='Arial',
#                                                  size=15,),
#                                        showarrow=True))
#                fig_list[plot_idx].figure['layout']['annotations'] = annotations
#        fig_list[plot_idx].figure['layout']['legend']=dict(orientation='h')
#        noted[plot_idx] = True
#        
#        # Figure 4
#        plot_idx = 3
#        label=True
#        annotations = []
#        for j in range(len(temp_panel[plot_idx])):
#            channel = temp_panel[plot_idx][j]
#            if channel == 'InnerUpperElectrodeTemperatureMonitor_AI':
#                ch_name = 'iUET_avg'
#                size = 2    
#                width = 2
#                plot_style = None
#                plot_mode = 'line'
#            else:
#                ch_name = 'iUET_' + channel[19]
#                size = 0.9
#                width = 0.9
#                plot_style = 'dash'
#                plot_mode = 'markers'
#            y_trace = wdl.data[(channel, 'value')]
#            trace = go.Scatter( x = wdl.data[(channel, 'time')]/1000,
#                                y = y_trace,
#                                legendgroup = wdl.info['Recipe'],
#                                mode = plot_mode,
#                                marker = dict(size = size,
#                                                color = color),
##                                mode = 'lines',
#                                line = dict(width = width, 
#                                            color=color),
#                                name = wdl.info['Recipe'],
#                                text = ch_name,
#                                hoverinfo='y+text',                                
#                                showlegend=label
#                                )
#            fig_list[plot_idx].figure['data'].append(trace)
#            label = False
#        fig_list[plot_idx].figure['layout']['legend']=dict(orientation='h')
#        noted[plot_idx] = True
#    
#        # Figure 5
#        plot_idx = 4
#        label=True
#        annotations = []
#        for j in range(len(temp_panel[plot_idx])):
#            channel = temp_panel[plot_idx][j]
#            
#            y_trace = wdl.data[(channel, 'value')]
#            trace = go.Scatter( x = wdl.data[(channel, 'time')]/1000,
#                                y = y_trace,
#                                legendgroup = wdl.info['Recipe'],
#                                mode = 'lines',
#                                line = dict(width = 1, 
#                                            color=color, 
#                                            dash=lineStyle[j%len(lineStyle)]),
#                                name = wdl.info['Recipe'],
#                                text = wdl.info['Recipe'],
#                                hoverinfo='y+text',
#                                showlegend=label
#                                )
#            fig_list[plot_idx].figure['data'].append(trace)
#            label = False
#        
#            if not noted[plot_idx]:              
#                annotations.append(dict(xref='paper', x=0.1, y=y_trace[0],
#                                        xanchor='left', yanchor='middle',
#                                        text= channel,
#                                        font=dict(family='Arial',
#                                                  size=15,),
#                                        showarrow=True))
#                fig_list[plot_idx].figure['layout']['annotations'] = annotations
#        fig_list[plot_idx].figure['layout']['legend']=dict(orientation='h')
#        noted[plot_idx] = True
    
    return fig_list

#@app.callback(
#    Output('temperature_panel', 'children'),
#    [Input('parsing_status', 'children'),
#     Input('select_wdl', 'value'),
#     Input('svd_wdl', 'children')])
#def update_temp_graph(parsing_done, wdl_list, svd_wdl):
#    
#    if wdl_list is not None:
#        try:
#            with open(svd_wdl, 'rb') as f:
#                existing_wdl = pickle.load(f)
#        except:
#            existing_wdl = {}
#        
#        position = ['left', 'right']
#        num_plot = len(temp_panel)
#        fig_list = [dcc.Graph(id='temp' + str(i), 
#                              figure=dict(data=[], layout={}),
#                              style={'width': '50%'}) 
#                    for i in range(num_plot)]
#
#        for i in range(len(wdl_list)):
#            wdl_path = wdl_list[i]
#            color = color_list[i % len(color_list)]
#            if wdl_path in existing_wdl:
#                wdl = existing_wdl[wdl_path]
#            else:
#                wdl = WDLReader()
#                wdl.load(wdl_path, parse='full')
#                existing_wdl[wdl_path] = wdl
#
#            for j in range(num_plot):
#                try:
#                    section = temp_panel[j]
#                    for channel in section:
#                        trace = go.Scatter(
#                                        x = wdl.data[(channel, 'time')]/1000,
#                                        y = wdl.data[(channel, 'value')],
#                                        legendgroup = channel,
#                                        mode = 'lines',
#                                        line = dict(width = 1, color=color),
#                                        name = wdl.info['Recipe'],
#                                        text = channel,
#                                        hoverinfo='text',
#                                        )
#                        fig_list[j].figure['data'].append(trace)
#                    
#                    fig_list[j].figure['layout']['legend']=dict(orientation='h')
#                    fig_list[j].style.update(float=position[j%2])
#                except:
#                    continue
#        return fig_list
#    else:
#        return None



class LamPE(object):
    channel_OI = ['InnerTopPlateHeaterTemperatureMonitor_AI',
                  'InnerTopPlateHeaterTemperatureOutputValue_AI',
                  'OuterTopPlateHeaterTemperatureMonitor_AI',
                  'OuterTopPlateHeaterTemperatureOutputValue_AI',
                  'InnerUpperElectrode1TemperatureMonitor_AI',
                  'InnerUpperElectrode2TemperatureMonitor_AI',
                  'InnerUpperElectrode3TemperatureMonitor_AI',
                  'InnerUpperElectrode4TemperatureMonitor_AI',
                  'InnerUpperElectrodeTemperatureMonitor_AI',
                  'ESCCoolantFlow_AI',
                  'ESCCoolantSupplyTemperatureMonitor_AI',
                  'ESCCoolantReturnTemperatureMonitor_AI',
                  'ESCTemperatureMonitor1_AI',
                  'ESCTemperatureMonitor2_AI',
                  'HeInnerZoneBacksideFlow_AI',
                  'HeOuterZoneBacksideFlow_AI',
                  'HeInnerZoneBacksidePressure_AI',
                  'HeOuterZoneBacksidePressure_AI',
                  'TCU2Monitor_AI',
                  'TCUCh1TempMonitor_AI',
                  'TCUCh1InletFlowMonitor_AI',
                  'TCUCh1OutletFlowMonitor_AI',
                  'TCUCh2TempMonitor_AI',
                  'TCUCh2InletFlowMonitor_AI',
                  'TCUCh2OutletFlowMonitor_AI',
                  'ConfinementRingPosition_AI',
                  'ConfinementRingAdjustedPosition',
                  'ForelineManometerAdjustedPressure',
                  'ChamberManometer_RawAI',
                  'ProcessManometer_RawAI',
                  'ProcessManometerAdjustedPressure',
                  'ESCBasePlateBiasCurrent_AI',
                  'ESCBasePlateBiasVoltage_AI',
                  'ESCBaseplateTemperature_AI',
                  'ESCCenterTapBiasVoltage_AI',
                  'RF60MHzFrequency_AI',
                  'RF60MHzGenDeliveredPower',
                  'RF60MHzGenReflectedPower_AI',
                  'RF60MHzPulseState0DeliveredPower_AI',
                  'RF60MHzPulseState0ReflectedPower_AI',
                  'RF60MHzPulseState0DeliveredPower_AI',
                  'RF400kHzFrequency_AI',
                  'RF400kHzGenDeliveredPower',
                  'RF400kHzGenReflectedPower_AI',
                  'RF400kHzPulseState0DeliveredPower_AI',
                  'RF400kHzPulseState0ReflectedPower_AI',
                  'RF400kHzPulseState0DeliveredPower_AI',
                  'Gas_1_Flow_AI',
                  'Gas_1_Reference_Flow_AI',
                  'Gas_2_Flow_AI',
                  'Gas_2_Reference_Flow_AI',
                  'Gas_3_Flow_AI',
                  'Gas_3_Reference_Flow_AI',
                  'Gas_4_Flow_AI',
                  'Gas_4_Reference_Flow_AI',
                  'Gas_5_Flow_AI',
                  'Gas_5_Reference_Flow_AI',
                  'Gas_6_Flow_AI',
                  'Gas_6_Reference_Flow_AI',
                  'Gas_7_Flow_AI',
                  'Gas_7_Reference_Flow_AI',
                  'Gas_8_Flow_AI',
                  'Gas_8_Reference_Flow_AI',
                  'Gas_9_Flow_AI',
                  'Gas_9_Reference_Flow_AI',
                  'Gas_10_Flow_AI',
                  'Gas_10_Reference_Flow_AI',
                  'Gas_11_Flow_AI',
                  'Gas_11_Reference_Flow_AI',
                  'Gas_12_Flow_AI',
                  'Gas_12_Reference_Flow_AI',
                  'Gas_13_Flow_AI',
                  'Gas_13_Reference_Flow_AI',
                  'IB1Value',
                  'IB2Value',
                  'IB3Value',
                  'IB4Value',
                  'IB5Value',
                  'IB6Value'
                 ]
    
    recipe_interpret = ['ProcessManometerAdjustedPressure',
                      'ESCCoolantReturnTemperatureMonitor_AI',
                      'RF400kHzGenDeliveredPower',
                      'RF400kHzPulseState0DeliveredPower_AI',
                      'RF60MHzGenDeliveredPower',
                      'RF60MHzPulseState0DeliveredPower_AI',
                      'RFPulseDutyCycleSetpoint',
                      'RFPulseRepetitionRateSetpoint',
                      'Gas_1_Flow_AI',
                      'Gas_2_Flow_AI',
                      'Gas_3_Flow_AI',
                      'Gas_4_Flow_AI',
                      'Gas_5_Flow_AI',
                      'Gas_6_Flow_AI',
                      'Gas_7_Flow_AI',
                      'Gas_8_Flow_AI',
                      'Gas_9_Flow_AI',
                      'Gas_10_Flow_AI',
                      'Gas_11_Flow_AI',
                      'Gas_12_Flow_AI',
                      'Gas_13_Flow_AI',
                      ]
    def __init__(self, power_channel, gas_channel ):
        self.power_channel = power_channel
        
        self.gas_channel = gas_channel
#    
#    def inspection(wdl_list):
#        