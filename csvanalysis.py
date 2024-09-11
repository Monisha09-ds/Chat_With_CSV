import pandas as pd
from langchain_groq import ChatGroq
import streamlit as st 
from dotenv import load_dotenv
from pandasai import SmartDataframe
import os


load_dotenv()

def csv_analysis(df,query):
    load_dotenv()
    
    groq_api_key = os.environ["GROQ_API_KEY"]
    
    llm = ChatGroq(
        groq_api_key = groq_api_key,model_name = "llama3-70b-8192",
        temperature=0.2)
    pandas_ai = SmartDataframe(df,config={"llm":llm})
    result = pandas_ai.chat(query)
    return result


st.set_page_config(layout='wide')
# Set title for the Streamlit application
st.title("Multiple-CSV ChatApp powered by LLM")

input_csvs = st.sidebar.file_uploader("Upload your CSV files",type=['csv'],accept_multiple_files= True)

if input_csvs:
    selected_file = st.selectbox("Select a CSV file",[file.name for file in input_csvs])
    selected_index = [file.name for file in input_csvs].index(selected_file)
    
    
    st.info("CSV Uploaded")
    data  = pd.read_csv(input_csvs[selected_index])
    st.dataframe(data.head(3),use_container_width=True)
    
    st.info("Chat Please")
    input_text = st.text_area("Enter the Query")
    
    if input_text:
        if st.button("Chat with CSV"):
            st.info("Query Please : "+input_text)
            result = csv_analysis(data,input_text)
            st.success(result)
            