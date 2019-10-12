#Plot up ground displacement curves

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default = "browser"


'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Overview of the code

1. Takes set of displacment curves output from 3DEC (and saved as csv)
        Assumes column titles are Step | Y-Axis | Step | Y-Axis etc
2. Decomposes into x, y, z and resolved (r) components are converts to mm (x1000)
3. Set of sub-functions isolates out specific monitoring points for each structure
        as well as whether x, y, z or some user defined combination is important
4. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''

class Displacement():
        
        def __init__(self,df_csv):
                self.df_csv = df_csv.fillna(method='ffill') #remove NAs
                self.rows = len(self.df_csv.index)
                self.cols = len(self.df_csv.columns)
                #print(self.cols)

        def create_disp_df(self):
                #setup df variable to avoid manipulating the raw input df
                df_csv_mod = pd.DataFrame()
                df_csv_mod = self.df_csv

                #Drop unnecessary columns (duplicate step cols for each plot)
                for i in range (0,int(self.cols/2-1)): # to --> 131
                        _str_drop = str('Step.')+ str((i+1))
                        df_csv_mod = df_csv_mod.drop(columns=_str_drop)
                _index = df_csv_mod['Step'] #set first column to be the index
                _index = _index.values.tolist()

                
                #setup variables and empty dataframes
                _columns = ['Step']
                _data_x = pd.DataFrame()
                _data_y = pd.DataFrame()
                _data_z = pd.DataFrame()
                _data_r = pd.DataFrame()
                _data_lat = pd.DataFrame()
                
                #First set the first column to Step number
                _data_x[[0]] = df_csv_mod.iloc[0:self.rows,[0]]
                _data_y[[0]]=_data_z[[0]]=_data_r[[0]]=_data_lat[[0]]=_data_x[[0]] 
                for i in range (1,int(self.cols/2-1),3): #to --> 132
                        _string = 'pt_' + str(int((i+2)/3))
                        _columns.append(_string)
                        _data_x[[i]] = df_csv_mod.iloc[0:self.rows,[i]]
                        _data_y[[i]] = df_csv_mod.iloc[0:self.rows,[i+1]]
                        _data_z[[i]] = df_csv_mod.iloc[0:self.rows,[i+2]]
                        _data_r[[i]] = ((_data_x[[i]]**2+_data_y[[i]]**2+_data_z[[i]]**2)**0.5)
                        _data_lat[[i]] = ((_data_x[[i]]**2+_data_y[[i]]**2)**0.5)
                

                #Set column names to monitoring points
                _data_x.columns=_data_y.columns=_data_z.columns=_data_r.columns=_data_lat.columns=_columns
                #Set Step to be index
                _data_x.set_index('Step',inplace=True)
                _data_y.set_index('Step',inplace=True)
                _data_z.set_index('Step',inplace=True)
                _data_r.set_index('Step',inplace=True)
                _data_lat.set_index('Step',inplace=True)
        

                #Record into separate dataframes for x, y, z and resolved
                #Convert into mm (Assumed 3DEC outputs in m)
                self._data_x = _data_x*1000
                self._data_y = _data_y*1000
                self._data_z = _data_z*1000
                self._data_r = _data_r*1000
                self._data_lat = _data_lat*1000

                return {
                        'x':self._data_x,
                        'y':self._data_y,
                        'z':self._data_z,
                        'r':self._data_r,
                        'lat':self._data_lat
                }
        '''---------------------------------------------------'''
        def fourpts_disp(self): #Four OG points around the shaft
                response = self.create_disp_df()
                fourpts=pd.DataFrame()
                fourpts[0] = response['y'].iloc[:,0]
                fourpts[1] = response['x'].iloc[:,1]
                fourpts[2] = response['z'].iloc[:,2]
                fourpts[3] = response['x'].iloc[:,3]
                fourpts.columns = ['Shaft_Major','Shaft_Minor','Tunnel_Crown','Tunnel_Sidewall']
                return fourpts
        def fourpts_S1(self): #Four OG points around the shaft
                response = self.create_disp_df()
                response = response['x']/1e9
                response = response.iloc[:,:4]
                response.columns = ['Shaft_Major','Shaft_Minor','Tunnel_Crown','Tunnel_Sidewall']
                return response
        def fourpts_S2(self): #Four OG points around the shaft
                response = self.create_disp_df()
                response = response['y']/1e9
                response = response.iloc[:,:4]
                response.columns = ['Shaft_Major','Shaft_Minor','Tunnel_Crown','Tunnel_Sidewall']
                return response.iloc[:,:4]
        def fourpts_S3(self): #Four OG points around the shaft
                response = self.create_disp_df()
                response = response['z']/1e9
                response = response.iloc[:,:4]
                response.columns = ['Shaft_Major','Shaft_Minor','Tunnel_Crown','Tunnel_Sidewall']
                return response
        '''---------------------------------------------------'''
        def funnel(self):
                response = self.create_disp_df()
                response = response['x']
                return response.iloc[:,4:20]
        def funnel_slab(self):
                response = self.create_disp_df()
                response = response['z']
                return response.iloc[:,20:24]
        def funnel_crown(self):
                response = self.create_disp_df()
                response = response['z']
                return response.iloc[:,9:16]
        def funnel_sidewalls(self):
                response = self.create_disp_df()
                response = response['lat']
                response = response[list(response.iloc[:,4:10]) + list(response.iloc[:,15:21])]
                return response
        '''---------------------------------------------------'''
        def tunnel(self):
                response = self.create_disp_df()
                response = response['r']
                return response.iloc[:,24:40]
        def tunnel_slab(self):
                response = self.create_disp_df()
                response = response['z']
                return response.iloc[:,40:44]
        def tunnel_crown(self):
                response = self.create_disp_df()
                response = response['z']
                return response.iloc[:,29:36]
        def tunnel_sidewalls(self):
                response = self.create_disp_df()
                response = response['lat']
                response = response[list(response.iloc[:,24:30]) + list(response.iloc[:,35:41])]
                return response
        '''---------------------------------------------------'''

# Pull in supported displacement csv
dfn_sup_disp_csv = pd.read_csv(r'C:\Users\james.care\Documents\_coding_projects\3DEC\SS_MTS\dfn_sup_disp.csv')
dfn_sup_disp_csv.columns


dfn_disp = Displacement(dfn_sup_disp_csv).create_disp_df()
dfn_disp['z'].columns

dfn_mon_pts_coords = pd.read_csv(r'C:\Users\james.care\Documents\_coding_projects\3DEC\SS_MTS\dfn_mon_pts_coords.csv')
dfn_mon_pts_coords




data_set=dfn_disp['z']
dfn_disp['z']

sort_list = [19,20,21,22,23,24,25,18,26,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61]
color_data = ['#e54d6f','#e14f70','#de5172','#db5473','#d85675','#d55977','#d25b78','#ce5e7a','#cb607b','#c8637d','#c5657f','#c26880','#bf6a82','#bc6c84','#b86f85','#b57187','#b27488','#af768a','#ac798c','#a97b8d','#a67e8f','#a28091','#9f8392','#9c8594','#998895','#968a97','#938c99','#908f9a','#8c919c','#89949e','#86969f','#8399a1','#809ba2','#7d9ea4','#79a0a6','#76a3a7','#73a5a9','#70a7ab','#6daaac','#6aacae','#67afaf','#63b1b1','#60b4b3','#5db6b4','#5ab9b6','#57bbb8','#54beb9','#51c0bb','#4dc3bc','#4ac5be','#47c7c0','#44cac1','#41ccc3','#3ecfc5','#3bd1c6','#37d4c8','#34d6c9','#31d9cb','#2edbcd','#2bdece','#28e0d0','#25e3d2']

data_set.columns.values[61]
fig=go.Figure()
for i in sort_list:#range(0,len(data_set.columns)):
    line_name = data_set.columns.values[i]
    fig.add_trace(go.Scattergl(
            x=data_set.index, 
            y=data_set[str(line_name)],
            mode='lines',
            name=line_name,
            line=dict(color=color_data[i])
        ))
fig.update_xaxes(
        title_text="<b>Step</b>",
        title_font=dict(family='Times New Roman',size=18),
        tickfont=dict(family='Times New Roman',size=14),
        gridcolor='rgb(127,127,127)',
        gridwidth=0.1
        )
fig.update_yaxes(
        title_text="<b>Total Displacement (mm)</b>",
        title_font=dict(family='Times New Roman',size=18),
        tickfont=dict(family='Times New Roman',size=14),
        gridcolor='rgb(127,127,127)',
        gridwidth=0.1
        )
fig.update_layout(
    title=go.layout.Title(
            text="<b>DFN Supported Displacement</b>",
            x=0.5, xref='paper',
            font=dict(family='Times New Roman',size = 26)
            ),
        paper_bgcolor='rgb(39,40,34)',
        plot_bgcolor='rgb(39,40,34)',
        autosize=True,
    #width = 1000,
    #height = 500
)
fig.update_layout(template="plotly_dark")
fig.show()
































mon_pts_coords = pd.read_csv(r'C:\Users\james.care\Documents\_coding_projects\3DEC\SS_MTS\dfn_mon_pts_coords.csv')

'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CONTINUUM
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
#Displacement Suite
cont_unsup_disp = pd.read_csv(r'C:\Users\james.care\Documents\_coding_projects\3DEC\SS_MTS\cont_unsup_disp.csv')
cont_unsup_disp = Displacement(cont_unsup_disp)

cont_sup_disp = pd.read_csv(r'C:\Users\james.care\Documents\_coding_projects\3DEC\SS_MTS\cont_sup_disp.csv')
cont_sup_disp = Displacement(cont_sup_disp)

#Stress Suite
cont_unsup_stress = pd.read_csv(r'C:\Users\james.care\Documents\_coding_projects\3DEC\SS_MTS\cont_unsup_stress.csv')
cont_unsup_stress = Displacement(cont_unsup_stress)

cont_sup_stress = pd.read_csv(r'C:\Users\james.care\Documents\_coding_projects\3DEC\SS_MTS\cont_sup_stress.csv')
cont_sup_stress = Displacement(cont_sup_stress)


'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DISCONTINUUM
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
#Displacement Suite
discont_unsup_disp = pd.read_csv(r'C:\Users\james.care\Documents\_coding_projects\3DEC\SS_MTS\discont_unsup_disp.csv')
discont_unsup_disp = Displacement(discont_unsup_disp)

discont_sup_disp = pd.read_csv(r'C:\Users\james.care\Documents\_coding_projects\3DEC\SS_MTS\discont_sup_disp.csv')
discont_sup_disp = Displacement(discont_sup_disp)

#Stress Suite
discont_unsup_stress = pd.read_csv(r'C:\Users\james.care\Documents\_coding_projects\3DEC\SS_MTS\discont_unsup_stress.csv')
discont_unsup_stress = Displacement(discont_unsup_stress)

discont_sup_stress = pd.read_csv(r'C:\Users\james.care\Documents\_coding_projects\3DEC\SS_MTS\discont_sup_stress.csv')
discont_sup_stress = Displacement(discont_sup_stress)


'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DFN
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
#Displacement Suite
#dfn_unsup_disp = pd.read_csv(r'C:\Users\james.care\Documents\_coding_projects\3DEC\SS_MTS\discont_unsup_disp.csv')
#dfn_unsup_disp = Displacement(discont_unsup_disp)

dfn_sup_disp = pd.read_csv(r'C:\Users\james.care\Documents\_coding_projects\3DEC\SS_MTS\dfn_sup_disp.csv')
dfn_sup_disp = Displacement(dfn_sup_disp).create_disp_df()
#Stress Suite
#dfn_unsup_stress = pd.read_csv(r'C:\Users\james.care\Documents\_coding_projects\3DEC\SS_MTS\discont_unsup_stress.csv')
#dfn_unsup_stress = Displacement(discont_unsup_stress)
#
#dfn_sup_stress = pd.read_csv(r'C:\Users\james.care\Documents\_coding_projects\3DEC\SS_MTS\discont_sup_stress.csv')
#dfn_sup_stress = Displacement(discont_sup_stress)


'''Plot as a line chart
Setup data_set with parameters
cont OR discont
sup OR unsup
'blank', _slab, _crown, _sidewalls

EXAMPLE
data_set = cont_unsup_funnel_sidewalls().loc[5000:]
data_set = discont_sup_tunnel_crown().loc[5000:]
'''

'''%%%%%%%%%%%%%%%%%%%% PLOT DISPLACEMENTS %%%%%%%%%%%%%%%%%%%%'''
#cont_disp = cont_unsup_disp.fourpts_disp()#.loc[5000:]
#dis_disp = discont_unsup_disp.fourpts_disp()#.loc[5000:]
'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''


data_set = dfn_sup_disp
fig=go.Figure()
for i in range(0,len(data_set.columns)):
    line_name = data_set.columns.values[i]
    fig.add_trace(go.Scattergl(x=data_set.index, y=data_set[str(line_name)],
        mode='lines',
        name=line_name))
fig.update_xaxes(title_text="Step")
fig.update_yaxes(title_text="Total Displacement (mm)")
fig.update_layout(
    title=go.layout.Title(
            text="<b>Continuum Unsupported Displacement</b>",
            x=0.5,
            xref='paper'
    ),
    autosize=False,
    width = 1000,
    height = 500
)
fig.show()


'''%%%%%%%%%%%%%%%%%%%% PLOT Major Principle Stress %%%%%%%%%%%%%%%%%%%%'''
data_set = cont_unsup_stress.fourpts_S1().loc[5000:]
'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''

fig=go.Figure()
for i in range(0,len(data_set.columns)):
    line_name = data_set.columns.values[i]
    fig.add_trace(go.Scattergl(x=data_set.index, y=data_set[str(line_name)],
        mode='lines',
        name=line_name))
fig.update_xaxes(title_text="Step")
fig.update_yaxes(title_text="Rock-mass Stress (MPa)",autorange="reversed")
fig.update_layout(
    title=go.layout.Title(
            text="<b>Major Principle Stress S1 (MPa)</b>",
            x=0.5,
            xref='paper'
    ),
    autosize=False,
    width = 1000,
    height = 500
)
fig.show()




'''%%%%%%%%%%%%%%%%%%%% PLOT Minor Principle Stress %%%%%%%%%%%%%%%%%%%%'''
data_set = cont_unsup_stress.fourpts_S3().loc[5000:]
'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''

fig=go.Figure()
for i in range(0,len(data_set.columns)):
    line_name = data_set.columns.values[i]
    fig.add_trace(go.Scattergl(x=data_set.index, y=data_set[str(line_name)],
        mode='lines',
        name=line_name))
fig.update_xaxes(title_text="Step")
fig.update_yaxes(title_text="Rock-mass Stress (MPa)",autorange="reversed")
fig.update_layout(
    title=go.layout.Title(
            text="<b>Minor Principle Stress S3 (MPa)</b>",
            x=0.5,
            xref='paper'
    ),
    autosize=False,
    width = 1000,
    height = 500
)
fig.show()



'''%%%%%%%%%%%%%%%%%%%% PLOT Deviatoric Stress %%%%%%%%%%%%%%%%%%%%'''
data_set = cont_unsup_stress.fourpts_S1().loc[5000:] - cont_unsup_stress.fourpts_S3().loc[5000:]
'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''

fig=go.Figure()
for i in range(0,len(data_set.columns)):
    line_name = data_set.columns.values[i]
    fig.add_trace(go.Scattergl(x=data_set.index, y=data_set[str(line_name)],
        mode='lines',
        name=line_name))
fig.update_xaxes(title_text="Step")
fig.update_yaxes(title_text="Rock-mass Stress (MPa)",autorange="reversed")
fig.update_layout(
    title=go.layout.Title(
            text="<b>Deviatoric Stress (S1-S3) (MPa)</b>",
            x=0.5,
            xref='paper'
    ),
    autosize=False,
    width = 1000,
    height = 500
)
fig.show()

