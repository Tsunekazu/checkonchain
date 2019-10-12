#Establish typical charts

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

#Establish a standard set of chart features in __init__
# Font type
# Font sizes
# background colors
# Gridlines


#fig=check_standard_charts(
#       title_data,     =['Chart Title','x-axis', 'Y-Axis-1', 'Y-Axis-2']
#       range_data,     =[[x1,x2],[y1_1,y1_2],[y2_1,y2_2]]
#       type_data,      =['linear','log','log']
#       autorange_data) =[True,True,False] - overrides range

#.subplot_lines_singleaxis(
#.subplot_lines_doubleaxis(
#        loop_data,     =[[a,b,c],[d,e]] where a-c are primary plots, d-e secondary plots
#        x_data,        =[a,b,c,d,e]
#        y_data,        =[a,b,c,d,e]
#        name_data,     =[a,b,c,d,e]
#        color_data,    =[a,b,c,d,e]
#        dash_data,     =[a,b,c,d,e] ('solid','dash','dot')
#        width_data,    =[a,b,c,d,e]
#        opacity_data,  =[a,b,c,d,e]
#        legend_data    =[a,b,c,d,e] (boolean, show legend or not)
#        )


class check_standard_charts():

    def __init__(self,title_data,range_data,type_data,autorange_data):
        self.title_data = title_data #Chart Title , X-Axis, Yaxis-1, Y-axis-2
        self.range_data = range_data # X-axis, Y-axis-1, Y-axis-2
        self.autorange_data = autorange_data
        self.type_data = type_data # X-axis, Y-axis-1, Y-axis-2
        self._background = 'rgb(30,30,30)'
        self._font = 'Raleway'
        self._titlesize = 26
        self._legendsize = 14
        self._axesfontsize = 18
        self._tickfontsize = 14
        self._gridcolor = 'rgb(127,127,127)'
        self._gridwidth = 0.1
        self._zerolinecolor = 'rgb(127,127,127)'


    def subplot_lines_singleaxis(
        self,
        loop_data,
        x_data,
        y_data,
        name_data,
        color_data,
        dash_data,
        width_data,
        opacity_data,
        legend_data
        ):
        
        self._fig = make_subplots(specs=[[{"secondary_y": False}]])
        
        """#######  Add Traces   #######"""
        for i in loop_data[0]:
            self._fig.add_trace(go.Scatter(
                x=x_data[i], 
                y=y_data[i],
                name=name_data[i],
                opacity=opacity_data[i],
                showlegend=legend_data[i],
                line=dict(
                    width=width_data[i],
                    color=color_data[i],
                    dash=dash_data[i]
                    )),
                secondary_y=False)
                
        """#######  Title Block   #######"""
        self._fig.update_layout(
            paper_bgcolor=self._background,
            plot_bgcolor=self._background,
            autosize=True,            
            title=go.layout.Title(
                text=self.title_data[0],
                x=0.5, 
                xref='paper',
                font=dict(
                    family=self._font,
                    size = self._titlesize
                )),
            legend=dict(
                font=dict(
                    family=self._font,
                    size=self._legendsize
                )))
        
        """#######  X-Axis   #######"""
        self._fig.update_xaxes(
            title_text=self.title_data[1],
            type=self.type_data[0],
            range=self.range_data[0],
            title_font=dict(
                family=self._font,
                size=self._axesfontsize
                ),
            tickfont=dict(
                family=self._font,
                size=self._tickfontsize
                ),
            gridcolor=self._gridcolor,
            gridwidth=self._gridwidth,
            zerolinecolor=self._zerolinecolor
            )
        self._fig.update_xaxes(autorange=self.autorange_data[0]) #override range
        

        """#######  Y-Axis-1   #######"""
        self._fig.update_yaxes(
            title_text=self.title_data[2],
            type=self.type_data[1],
            range=self.range_data[1],
            title_font=dict(
                family=self._font,
                size=self._axesfontsize
                ),
            tickfont=dict(
                family=self._font,
                size=self._tickfontsize
                ),
            gridcolor=self._gridcolor,
            gridwidth=self._gridwidth,
            zerolinecolor=self._zerolinecolor,
            secondary_y=False
            )
        self._fig.update_yaxes(autorange=self.autorange_data[1],secondary_y=False) #override range
        
        self._fig.update_layout(template="plotly_dark")
        return self._fig

    def subplot_lines_doubleaxis(
        self,
        loop_data,
        x_data,
        y_data,
        name_data,
        color_data,
        dash_data,
        width_data,
        opacity_data,
        legend_data
        ):

        self._fig = make_subplots(specs=[[{"secondary_y": True}]])
        self._fig.update_layout(template="plotly_dark")
        
        """#######  Add PRIMARY Traces   #######"""
        for i in loop_data[0]:
            self._fig.add_trace(go.Scatter(
                x=x_data[i], 
                y=y_data[i],
                name=name_data[i],
                opacity=opacity_data[i],
                showlegend=legend_data[i],
                line=dict(
                    width=width_data[i],
                    color=color_data[i],
                    dash=dash_data[i]
                    )),
                secondary_y=False)

        """#######  Add SECONDARY Traces   #######"""
        for i in loop_data[1]:
            self._fig.add_trace(go.Scatter(
                x=x_data[i], 
                y=y_data[i],
                name=name_data[i],
                opacity=opacity_data[i],
                showlegend=legend_data[i],
                line=dict(
                    width=width_data[i],
                    color=color_data[i],
                    dash=dash_data[i]
                    )),
                secondary_y=True)
                
        """#######  Title Block   #######"""
        self._fig.update_layout(
            paper_bgcolor=self._background,
            plot_bgcolor=self._background,
            autosize=True,            
            title=go.layout.Title(
                text=self.title_data[0],
                x=0.5, 
                xref='paper',
                font=dict(
                    family=self._font,
                    size = self._titlesize
                )),
            legend=dict(
                font=dict(
                    family=self._font,
                    size=self._legendsize
                )))
        
        """#######  X-Axis   #######"""
        self._fig.update_xaxes(
            title_text=self.title_data[1],
            type=self.type_data[0],
            range=self.range_data[0],
            title_font=dict(
                family=self._font,
                size=self._axesfontsize
                ),
            tickfont=dict(
                family=self._font,
                size=self._tickfontsize
                ),
            gridcolor=self._gridcolor,
            gridwidth=self._gridwidth,
            zerolinecolor=self._zerolinecolor
            )
        self._fig.update_xaxes(autorange=self.autorange_data[0]) #override range

        """#######  Y-Axis-1   #######"""
        self._fig.update_yaxes(
            title_text=self.title_data[2],
            type=self.type_data[1],
            range=self.range_data[1],
            title_font=dict(
                family=self._font,
                size=self._axesfontsize
                ),
            tickfont=dict(
                family=self._font,
                size=self._tickfontsize
                ),
            gridcolor=self._gridcolor,
            gridwidth=self._gridwidth,
            zerolinecolor=self._zerolinecolor,
            secondary_y=False
            )
        self._fig.update_yaxes(autorange=self.autorange_data[1],secondary_y=False) #override range
        
        """#######  Y-Axis-2   #######"""
        self._fig.update_yaxes(
            title_text=self.title_data[3],
            type=self.type_data[2],
            range=self.range_data[2],
            title_font=dict(
                family=self._font,
                size=self._axesfontsize
                ),
            tickfont=dict(
                family=self._font,
                size=self._tickfontsize
                ),
            gridcolor=self._gridcolor,
            gridwidth=self._gridwidth,
            zerolinecolor=self._zerolinecolor,
            secondary_y=True
            )
        self._fig.update_yaxes(autorange=self.autorange_data[2],secondary_y=True) #override range
        
        return self._fig


#loop_data = [[0,1],[2]]
#x_data = [[0,1,2,3,4,5],[0,1,2,3,4,5],[0,1,2,3,4,5]]
#y_data = [[0,1,2,3,4,5],[4,5,0,5,9,5],[-4,-5,0,-5,-9,-5]]
#name_data = ['Bitcoin Market Cap','tap2','secondary']
#color_data = ['rgb(237, 109, 71)','rgb(237, 109, 71)','rgb(237, 109, 71)' ]
#dash_data = ['solid','dash','solid']
#width_data = [2,2,2]
#opacity_data = [1,0.5,1]
#legend_data = [True,True,True]
#title_data = [
#    '<b>Market Capitalisation vs Supply Mined</b>',
#    '<b>Coin Supply Issued</b>',
#    '<b>Coin Market Cap</b>',
#    'secondary Y'
#]
#type_data = ['linear','linear','linear']
#range_data = [[-10,10],[-5,12],[-10,20]]
#autorange_data = [False,False,False]
#
#
#
#fig=check_standard_charts(
#    title_data,
#    range_data,
#    type_data,
#    autorange_data
#    ).subplot_lines_singleaxis(
#        loop_data,
#        x_data,
#        y_data,
#        name_data,
#        color_data,
#        dash_data,
#        width_data,
#        opacity_data,
#        legend_data
#        ).show()
#
#fig=check_standard_charts(
#    title_data,
#    range_data,
#    type_data,
#    autorange_data
#    ).subplot_lines_doubleaxis(
#        loop_data,
#        x_data,
#        y_data,
#        name_data,
#        color_data,
#        dash_data,
#        width_data,
#        opacity_data,
#        legend_data
#        )

