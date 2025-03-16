import data as dt
import streamlit as st
import pandas as pd 
import plotly.graph_objects as go 
import json
import plotly.express as px


st.set_page_config(page_title="PH Fucntional Disability Distribution",page_icon=":zany_face:",layout="wide")

st.title("Philippine Fucntional Disability For Household Population Five Years Old and Over")
st.markdown("choroleth visualization for people with **fucntional disability** by region/province  in phillipines")



def app_layout():
    sidemenu = st.sidebar.selectbox(
    "Visualizations",
    ("Home", "Map Plot", "Bar Chart","Scatter Plot","Pie Chart")
)
    if sidemenu == "Home":
         pt=dt.pivot_table()
         st.dataframe(dt.dataframe(),use_container_width=False,height=None)       
         st.dataframe(pt["gender_serverity_disability_pivot"],use_container_width=True,height=None)
         st.dataframe(pt["top_disability_region"],use_container_width=True,height=None)
         st.dataframe(pt["age_regional_disibality_pivot"],use_container_width=True,height=None)
         st.dataframe(dt.df.describe())
    elif sidemenu == "Map Plot":
        col1,col2=st.columns([1,2],gap="large")
        with col1:
            option=st.selectbox("choose an option",options=["Select Option","Region","Province"])
        with col2:
            status=st.radio("Disability Status",options=["Mild","Moderate","Severe"],horizontal=True)
        if option == "Region":
            st.header("Region Visualization")
            st.plotly_chart(dt.region_figure(x=status),use_container_width=True)
            
        elif option == "Province":
            dic_regcode=dt.regcode()
            k =st.selectbox("Province **Fucntional Disability** Visualization",options=[x for x in dic_regcode])
            st.plotly_chart(dt.province_figure(y=k,x=status))
    elif sidemenu =="Bar Chart":
         option=st.selectbox("choose an option",options=["Disability","Age","Region","Sex","Status","Province"])
         st.plotly_chart(dt.bar_fig(option))
    elif sidemenu =="Scatter Plot":
         option=st.selectbox("choose an option",options=["Disability","Age","Region","Status","Province"])
         st.plotly_chart(dt.scatter_fig(option))
    elif sidemenu =="Pie Chart":
         option=st.selectbox("choose an option",options=["Disability","Age","Region","Sex","Status","Province"])
         st.plotly_chart(dt.Pie_fig(option))
app_layout()

















#goal for the day is comple all inter active functions