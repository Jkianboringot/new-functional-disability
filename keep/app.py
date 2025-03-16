from typing import Union
import streamlit as st
import pandas as pd 
import numpy as np
import plotly.graph_objects as go 
import os
import json
import plotly.express as px
import pickle

st.set_page_config(page_title="PH Fucntional Disability Distribution",page_icon=":zany_face:",layout="wide")

st.title("Philippine Fucntional Disability For Household Population Five Years Old and Over")
st.markdown("choroleth visualization for people with **fucntional disability** by region/province  in phillipines")
    

pwd=os.getcwd()
df=pd.read_csv(pwd+"/functional_difficulty_dataset/keep/csv/func_dis_dataset.csv")
regprov_population=pd.read_csv(pwd + "/functional_difficulty_dataset/keep/csv/ph_population_2020.csv")
geolocation = json.load(open(pwd+"/functional_difficulty_dataset/keep/geojson/regions/regions.0.01.json","r"))


regprov_population=regprov_population.groupby(["Region","Province"],as_index=False)["Population"].sum()
regprov_population["Region"]=regprov_population["Region"].str.strip("")

disability_by_region = (
    df.loc[(df["Sex"] == "Both Sexes")& (df["Status"] != "All") ]
    .groupby(["Disability", "Region","Status","RegCode_Old","Province","ProvCode_Old"], 
             as_index=False)["Household Population 5 Years Old and Over with Functional Difficulty"].sum())

total_disability_population=pd.merge(disability_by_region,regprov_population,on=["Region","Province"])
total_disability_population["Person affected by disability per 100k"]=np.ceil(total_disability_population['Household Population 5 Years Old and Over with Functional Difficulty']
                                                                       /total_disability_population['Population']
                                                                       * 100000)
total_disability_population["scale affected"]=np.log10(total_disability_population["Person affected by disability per 100k"])

population=regprov_population.groupby(["Region"],as_index=False)["Population"].sum()
population["Region"]=population["Region"].str.strip("")

ages_groupby=(df.loc[(df["Sex"] == "Both Sexes") & (df["Status"] == "All")]
    .groupby(["Region","Disability"], as_index=False)[['Age: 5-19',"Age: 20-34","Age: 35–54","Age: 55-80+","Household Population 5 Years Old and Over with Functional Difficulty"]]
    .sum()
    )


gender_severety=(df.loc[(df["Sex"] != 'Both Sexes')& (df["Status"] != 'All')]
                 .groupby(["Region","Sex","Disability","Status"],as_index=False)
                 ["Household Population 5 Years Old and Over with Functional Difficulty"]
                 .sum())

total_disability_population=pd.merge(disability_by_region,regprov_population,on=["Region","Province"])
total_disability_population["Person affected by disability per 100k"]=np.ceil(total_disability_population['Household Population 5 Years Old and Over with Functional Difficulty']
                                                                       /total_disability_population['Population']
                                                                       * 100000)
total_disability_population["scale affected"]=np.log10(total_disability_population["Person affected by disability per 100k"])

age_regional_disibality=pd.merge(ages_groupby,population,on="Region")
age_group = {
    "5-19": "Age: 5-19",
    "20-34": "Age: 20-34",
    "35-54": "Age: 35–54",
    "55-80+": "Age: 55-80+"
}
for age_label, age_column in age_group.items():
     age_regional_disibality[f"average affected in Age: {age_label}"] = np.ceil(age_regional_disibality[age_column] / 
                                                                                age_regional_disibality['Population'] * 100000)
age_to_viz=age_regional_disibality.melt(id_vars=["Disability","Region","Population"],value_vars=list(age_group.values())
                                        ,value_name="age affection",
                                        var_name="age/ave_affected").drop_duplicates()

group_age_to_viz=age_to_viz.groupby("age/ave_affected",as_index=False)["age affection"].sum()



gender_serverity_disability=pd.merge(gender_severety,population,on="Region",how="left").assign(population=lambda x:x["Population"]/2)
gender_serverity_disability["Gender affected by disability per 100k"]=(gender_serverity_disability["Household Population 5 Years Old and Over with Functional Difficulty"]/(gender_serverity_disability['Population']/2)*100000).astype(int)
#gender_serverity_disability.rename(columns={"Population":"Total Population"},inplace=True)
gender_serverity_disability.rename(columns={"population":"Gender Population"},inplace=True)



age_regional_disibality_pivot=age_regional_disibality.pivot_table(index="Region",columns="Disability").head(5)

gender_serverity_disability_pivot=gender_serverity_disability.pivot_table(index=["Region","Sex","Status"],columns=["Disability"])
gender_serverity_disability_pivot["Gender affected by disability per 100k"]

top_disability_region=ages_groupby.pivot_table(index=["Region"],aggfunc="max")




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



dic_regcode={}
for x in geolocation["features"]:
    x['id']=x["properties"]["ADM1_PCODE"]
    dic_regcode[x["properties"]["ADM1_EN"]]=x["id"]



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

 



# put all this in a new file for clearer readibility
def app_layout():
   
   

    sidemenu = st.sidebar.selectbox(
    "Visualizations",
    ("Home", "Map Plot", "Bar Chart","Scatter Plot","Pie Chart")
)
    if sidemenu == "Home":
         st.dataframe(df,use_container_width=False,height=None)       
         st.dataframe(gender_serverity_disability_pivot,use_container_width=True,height=None)
         st.dataframe(top_disability_region,use_container_width=True,height=None)
         st.dataframe(age_regional_disibality_pivot,use_container_width=True,height=None)
         st.dataframe(df.describe())
    elif sidemenu == "Map Plot":
        col1,col2=st.columns([1,2],gap="large")
        with col1:
            option=st.selectbox("choose an option",options=["Select Option","Region","Province"])
        with col2:
            status=st.radio("Disability Status",options=["Mild","Moderate","Severe"],horizontal=True)
        if option == "Region":
            st.header("Region Visualization")
            st.plotly_chart(region_figure(x=status),use_container_width=True)
            
        elif option == "Province":
            k =st.selectbox("Province **Fucntional Disability** Visualization",options=[x for x in dic_regcode])
            st.plotly_chart(province_figure(y=k,x=status))
    elif sidemenu =="Bar Chart":
         option=st.selectbox("choose an option",options=["Disability","Age","Region","Sex","Status","Province"])
         st.plotly_chart(bar_fig(option))
    elif sidemenu =="Scatter Plot":
         option=st.selectbox("choose an option",options=["Disability","Age","Region","Status","Province"])
         st.plotly_chart(scatter_fig(option))
    elif sidemenu =="Pie Chart":
         option=st.selectbox("choose an option",options=["Disability","Age","Region","Sex","Status","Province"])
         st.plotly_chart(Pie_fig(option))
app_layout()

















#goal for the day is comple all inter active functions