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


def region_figure(x:str):# -> Any:
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
region_figure(x="severe")

dic_regcode={}
for x in geolocation["features"]:
    x['id']=x["properties"]["ADM1_PCODE"]
    dic_regcode[x["properties"]["ADM1_EN"]]=x["id"]



def province_figure(y:str,x:str):# -> An
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

    #return value

st.write(region_figure(x="severe"))
st.write(province_figure(y="Region II",x="moderate"))
#actually before doing all this i need to finanlize all then do this after that test out if making a been file is even 
#worth it,why do this becuase i have to put all me file in where unles i can call it