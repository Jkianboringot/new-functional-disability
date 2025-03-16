from typing import Union
import streamlit as st
import pandas as pd 
import numpy as np
import plotly.graph_objects as go 
import os
import json
import plotly.express as px
import pickle


pwd=os.getcwd()
df=pd.read_csv(pwd+"/functional_difficulty_dataset/keep/csv/func_dis_dataset.csv")
geolocation = json.load(open(pwd+"/functional_difficulty_dataset/keep/geojson/regions/regions.0.01.json","r"))
age_regional_disibality=pd.read_csv(pwd+"/functional_difficulty_dataset/keep/csv/groupbys_dataset/age_regional_disibality.csv")
gender_serverity_disability=pd.read_csv(pwd+"/functional_difficulty_dataset/keep/csv/groupbys_dataset/gender_serverity_disability.csv")
age_to_viz=pd.read_csv(pwd+"/functional_difficulty_dataset/keep/csv/groupbys_dataset/age_to_viz.csv")
total_disability_population=pd.read_csv(pwd+"/functional_difficulty_dataset/keep/csv/groupbys_dataset/total_disability_population.csv")



ages_groupby=(df.loc[(df["Sex"] == "Both Sexes") & (df["Status"] == "All")]
    .groupby(["Region","Disability"], as_index=False)[['Age: 5-19',"Age: 20-34","Age: 35–54","Age: 55-80+","Household Population 5 Years Old and Over with Functional Difficulty"]]
    .sum()
    )

group_age_to_viz=age_to_viz.groupby("age/ave_affected",as_index=False)["age affection"].sum()





def pivot_table():
    return {"age_regional_disibality_pivot":age_regional_disibality.pivot_table(index="Region",columns="Disability").head(5),
    "gender_serverity_disability_pivot":gender_serverity_disability.pivot_table(index=["Region","Sex","Status"],columns=["Disability"]),
    "top_disability_region":ages_groupby.pivot_table(index=["Region"],aggfunc="max")
    }
    



def groupbys(group:Union[str, list[str]]):
    return df.loc[(df["Sex"] != "Both Sexes")& (df["Status"] != "All") ].groupby(group, 
             as_index=False)["Household Population 5 Years Old and Over with Functional Difficulty"].sum()


def check_file(reg_prov_fol,file):
     check=os.path.join(reg_prov_fol,file)
     try:
       
          if os.path.exists(check):
               return json.load(open(check,"r"))
          else:
                 print(f"File {check} dont exist")
     except FileNotFoundError:
               print(f"File {check} dont exist")

def fig_layout(fig,var:str):
     
        if var == "choro":                     
                
            figchorolet=fig.update_layout(
            coloraxis=dict(colorbar=dict(orientation='h', y=0.9)),
            coloraxis_colorbar = dict(title = 'Disability'), 
            margin={"r":0,"t":0,"l":0,"b":0}, 
            paper_bgcolor = 'rgba(0,0,0,0)', 
            plot_bgcolor = 'rgba(0,0,0,0)',
            geo = dict(bgcolor = 'rgba(0,0,0,0)', ), 
            modebar_bgcolor = 'rgba(0,0,0,0)',
            modebar_color = '#6d0006',
            modebar_activecolor = '#323140',
            modebar_orientation = 'v')

            return figchorolet
        
        else:
             figviz=fig.update_layout(uniformtext_minsize=10, uniformtext_mode="hide",
                            margin=dict(autoexpand=False,l=50,r=100,t=25),autosize=True,showlegend=True,
                            title_font=dict(color="#bae03a"),
                            font=dict(color="#ab22bd"), 
                            paper_bgcolor = 'rgba(0,0,0,0)', 
                            plot_bgcolor = 'rgba(0,0,0,0)',
                        coloraxis=dict(colorbar=dict(orientation='v', y=0.5)))
                # figviz.update_traces(marker=dict(colorscale=colors))
             return figviz
        

color_scale_values = np.linspace(0, 1, len(age_to_viz["age affection"]))  
colors = px.colors.sample_colorscale("Plasma", color_scale_values) 
choro="choro"
viz="viz"

st.cache_data()
def dataframe():
     return df

st.cache_data()
def region_figure(x:str):# -> Any:
    value=total_disability_population.loc[total_disability_population["Status"]==(x).capitalize().strip()]
    geojson_prov=pwd+"/functional_difficulty_dataset/keep/geojson/regions"
    prov_file=f"regions.0.01.json"
    if not check_file(geojson_prov,prov_file):
       pass
    else:
        fig = px.choropleth(
                data_frame = value, 
                geojson = check_file(geojson_prov,prov_file),
                featureidkey = 'properties.ADM1_PCODE',
                locations = "RegCode_Old",
            color="scale affected",
            center={"lat":12.8797,"lon":121.7740},
                hover_data="Person affected by disability per 100k",
                    hover_name="Region",color_continuous_scale=colors)
        fig.update_geos(fitbounds="locations",visible=False)
        fig_layout(fig,choro) 

        
        return fig
region_figure(x="severe")


def regcode():
    dic_regcode={}
    for x in geolocation["features"]:
        x['id']=x["properties"]["ADM1_PCODE"]
        dic_regcode[x["properties"]["ADM1_EN"]]=x["id"]
    return dic_regcode

dic_regcode=regcode()


st.cache_data()
def province_figure(y,x):# -> An
    
    geojson_prov=pwd+"/functional_difficulty_dataset/keep/geojson/provinces"
    prov_file=f"provinces-region-{dic_regcode[y].lower()}.0.01.json"
    value=total_disability_population.loc[(total_disability_population["Status"]==(x).capitalize().strip())
                                           & (total_disability_population["RegCode_Old"]== dic_regcode[y])]
    
    fig = px.choropleth(
                        data_frame = value, 
                        geojson =  check_file(geojson_prov,prov_file), # this thing will probably run if i put it in the fucntion like a normal person
                        featureidkey = 'properties.ADM2_PCODE',
                        locations = "ProvCode_Old",
                    color="scale affected",     
                    center={"lat":12.8797,"lon":121.7740},
                        hover_data="Person affected by disability per 100k",
                hover_name="Province",color_continuous_scale=colors)
    fig.update_geos(fitbounds="locations",visible=False)        
    fig_layout(fig,choro)     
   
       
    return fig
province_figure(y="Region V",x="moderate")



st.cache_data()       
def bar_fig(fig:str):
    if fig == "Age":
        figage=px.bar(group_age_to_viz,x="age/ave_affected",y="age affection",
            color="age affection",title="Regional Disability Distribution",
            labels={"age/ave_affected":"age/ave_affected category",
                    "age affection":"age affection count"},
                    text="age affection", color_continuous_scale=colors
                    )
        figage.update_traces(texttemplate="%{text:.2s}",textposition="outside") 
        fig_layout(figage,viz)
        return figage
    else:
        figdis=px.bar(groupbys(fig),x=fig,y="Household Population 5 Years Old and Over with Functional Difficulty",
            color="Household Population 5 Years Old and Over with Functional Difficulty",title="Regional Disability Distribution",
            labels={"Disability":"Disability type",
                    "Household Population 5 Years Old and Over with Functional Difficulty":"Disability count"},
                    text="Household Population 5 Years Old and Over with Functional Difficulty",color_continuous_scale=colors
                    )
        figdis.update_traces(texttemplate="%{text:.2s}",textposition="outside")
        fig_layout(figdis,viz)
        return figdis



st.cache_data()
def scatter_fig(fig):
    
    figsc = go.Figure()
    figage=go.Figure()
    if fig == "Age":
        figsc.add_trace(go.Scatter(x=group_age_to_viz["age/ave_affected"],y=group_age_to_viz["age affection"],
                mode="markers", marker_color=group_age_to_viz["age affection"],
                                marker=dict(showscale=True ,colorscale=colors)))
        
        figsc.update_traces(marker_line_width=1,marker_size=16)
        figsc.update_layout(title=dict(text="Scatter plot by region disability"))  
        figsc.update_layout(
            margin=dict(autoexpand=False,r=100,l=50,t=50),showlegend=False,autosize=True)
        fig_layout(figsc,viz)
        return figsc
    else:
        scatter=groupbys(fig)
        figsc.add_trace(go.Scatter(x=scatter[fig],
                                y=scatter["Household Population 5 Years Old and Over with Functional Difficulty"],
                                mode="markers",  marker_color=scatter  ["Household Population 5 Years Old and Over with Functional Difficulty"],
                                marker=dict(showscale=True ,colorscale=colors)))
        figsc.update_traces(marker_line_width=1,marker_size=16)
        figsc.update_layout(title=dict(text="Scatter plot by region disability"))  
        figsc.update_layout(
            margin=dict(autoexpand=False,r=100,l=50,t=50),showlegend=False,autosize=True
                        )
        fig_layout(figsc,viz)
        return figsc




st.cache_data()      
def Pie_fig(fig:str):
    figpie = go.Figure()
    
    if fig == "Age":              
        
        figpie.add_trace(go.Pie(
            values=age_to_viz["age affection"],
            labels=age_to_viz["age/ave_affected"],
            insidetextorientation='radial',
            hole=0.3,
            marker=dict(colors=colors, line=dict(color='purple', width=1))  
        )) 
        fig_layout(figpie,viz)
        return figpie
    else:     
        pie=groupbys(fig)
        figpie.add_trace(go.Pie(values=pie["Household Population 5 Years Old and Over with Functional Difficulty"],
                                labels=pie[fig],insidetextorientation='radial',hole=0.3))
        figpie.update_traces(hoverinfo='label+value+percent', textinfo='percent', textfont_size=11,
                        marker=dict(colors=["#340f99","#9928ad"], line=dict(color='purple',width=1)))
        figpie.update_layout(title_text="Pie Chart")
        fig_layout(figpie,viz)
        return figpie

 

















#goal for the day is comple all inter active functions