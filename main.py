import numpy
import openpyxl
import streamlit as st
import streamlit.components.v1 as components
from streamlit import StreamlitAPIException
import pandas as pd
from jinja2 import Template
from jinja2 import Environment
import jinja2

# coloring rules
color_map = {"Development": "green",
                        "Test Only": "blue",
                        "TSO": "red",
                        "Not Identified": ""

             }


def color(value ):
    return f"background-color: {color_map[value]}"


@st.cache
def read_excel(path, sheetname):
    return pd.read_excel(path, sheetname)


@st.cache
def read_sheet_names(path):
    xlsx = openpyxl.load_workbook(path)
    return xlsx.get_sheet_names()


# upload file from hd


uploaded_file = st.file_uploader("Choose an excel file")
if uploaded_file is not None:
    sheet_name = st.selectbox("Select Sheet", read_sheet_names(uploaded_file), index=0)
    dataframe = read_excel(uploaded_file, sheetname=sheet_name)
    # dataframe.style.applymap()
    # Create three columns/filters
    col1, col2, col3 = st.columns(3)

    with col1:
        sim_list = numpy.append(["All"], dataframe["SIM"].unique())
        # period_list.sort()
        st.container()
        sim = st.selectbox("SIM", sim_list, index=0)
        slider = st.slider("Development", 0,100, 5)
    if sim == "All":
        st.write(dataframe)
    else:
        try:
            dataframe = dataframe.loc[dataframe["SIM"] == sim]
            dataframe = dataframe.style.applymap(color, subset=["PI3 Impact","SIM"])
            st.write(dataframe)



        except StreamlitAPIException as e:
            st.write(f"Cannot read sheet {sheet_name}")

# Data prepartion to only retrieve fields that are relevent to this project
