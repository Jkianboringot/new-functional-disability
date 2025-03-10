from matplotlib import markers
import openpyxl
import streamlit as st
import pandas as pd 
import numpy as np
import os
import json
import plotly.express as px
import pickle


pwd=os.getcwd()
df=pd.read_csv(pwd+"/functional_difficulty_dataset/keep/csv/total_disability_per100k.csv")
regprov_population=pd.read_csv(pwd + r"/functional_difficulty_dataset/keep/csv/regprov_population.csv")
geolocation = json.load(open(pwd+"/functional_difficulty_dataset/keep/geojson/regions/regions.0.01.json","r"))

def check_file(reg_prov_fol,file):
     check=os.path.join(reg_prov_fol,file)
     try:
       
          if os.path.exists(check):
               return json.load(open(check,"r"))
          else:
                 print(f"File {check} dont exist")
     except FileNotFoundError:
               print(f"File {check} dont exist")


def region_figure(x):# -> Any:
    geojson_prov=pwd+"/functional_difficulty_dataset/keep/geojson/regions"
    prov_file=f"regions.0.01"
    f=json.load(open(rf'{geojson_prov}/{prov_file}.json'))
    value=df.loc[df["Status"]==(x).capitalize().strip()]
    fig = px.choropleth_map(
            data_frame = value, 
            geojson =  f,
            featureidkey = 'properties.ADM1_PCODE',
            locations = "RegCode_New",
           color="scale affected",
           center={"lat":12.8797,"lon":121.7740},zoom=4,
            hover_data="Person affected by disability per 100k",
                hover_name="Region")
    fig.update_geos(fitbounds="locations",visible=False)

    return fig
    #return value


dic_regcode={}
for x in geolocation["features"]:
    x['id']=x["properties"]["ADM1_PCODE"]
    dic_regcode[x["properties"]["ADM1_EN"]]=x["id"]



def province_figure(y,x):# -> An
    folder_path=pwd+"/functional_difficulty_dataset/keep/geojson/provinces"
    prov_file=f"provinces-region-{dic_regcode[y].lower()}.0.01.json"
    value=df.loc[(df["Status"]==(x).capitalize().strip())
                                           & (df["RegCode_New"]== dic_regcode[y])]
    try:
        fig = px.choropleth_map(
                data_frame = value, 
                geojson =  check_file(folder_path,prov_file), # this thing will probably run if i put it in the fucntion like a normal person
                featureidkey = 'properties.ADM2_PCODE',
                locations = "Province_pcode",
            color="scale affected",     
              center={"lat":12.8797,"lon":121.7740},zoom=4,
                hover_data="Person affected by disability per 100k",
                hover_name="Province")
        fig.update_geos(fitbounds="locations",visible=False)        
        return fig
 
       
    except FileNotFoundError:
       print(f"File dont exist")



 


#put all this in a new file for clearer readibility
def app_layout():
    st.set_page_config(page_title="PH Fucntional Disability Distribution",page_icon=":zany_face:")
    st.title("Philippine Fucntional Disability For Household Population Five Years Old and Over")
    st.markdown("choroleth visualization for people with **fucntional disability** by region/province  in phillipines")
    
    col1,col2=st.columns([1,2],gap="large")
    with col1:
        option=st.selectbox("choose an option",options=["Select Option","Region","Province"])
    with col2:
         status=st.radio("Disability Status",options=["Mild","Moderate","Severe"],horizontal=True)
    if option == "Region":
        st.header("Region Visualization")
        st.write(region_figure(x=status))
    elif option == "Province":
        k =st.selectbox("Province **Fucntional Disability** Visualization",options=[x for x in dic_regcode])
       
        st.write(province_figure(y=k,x=status))
    
app_layout()

















#goal for the day is comple all inter active functions