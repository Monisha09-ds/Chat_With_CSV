from pandasai.llm.local_llm import LocalLLM
from pandasai import SmartDataframe
import pandas as pd
import streamlit as st 

#Function that helps to chat with CSV 
def chat_with_csv(df,query):
    llm = LocalLLM(
        api_base="http://localhost:11434/v1",
        model = "llama3"
    )

    pandas_ai = SmartDataframe(df,config={"llm" : llm})
    result = pandas_ai.chat(query)
    return result

# Set layout configuration for Streamlit Page
st.set_page_config(layout="wide")
st.title("Multiple-CSV chatapp powered by LLM")

input_csvs = st.sidebar.file_uploader("Upload your CSV files",type=['csv'],accept_multiple_files= True)

if input_csvs:
    selected_file = st.selectbox("Select a CSV file",[file.name for file in input_csvs])
    selected_index = [file.name for file in input_csvs].index(selected_file)
    
    st.info("CSV uploaded successfully")
    data = pd.read_csv(input_csvs[selected_index])
    st.dataframe(data.head(),use_container_width = True)
    
#Enter the query analysis
st.info("Chat Below Please")
input_text = st.text_area("Enter the query")

if input_text:
    if st.button("Chat with CSV"):
        st.info("Your Query :" + input_text)
        result = chat_with_csv(data,input_text)
        st.success(result)
        
    