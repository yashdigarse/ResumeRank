import streamlit as st
import utility
import Resume
import re
from gensim.models.doc2vec import Doc2Vec
import numpy as np
from numpy.linalg import norm
import pandas as pd
from pyresparser import ResumeParser
import nltk
nltk.download('stopwords')




st.set_page_config(
    page_title="Resume Ranks",
    page_icon="⏫",
)




# web app
def main():
    utility.inject_ga()
    st.markdown("""
<style>
.big-font {
    font-size:44px !important;
    font-weight: bold;
}
<style>
.s-font {
    font-size:25px !important;
    font-weight: bold;
}
</style>

""", unsafe_allow_html=True)

    st.markdown('<p ><span class="big-font">Resume Rank</span>  <span class="s-font">Powered by AI.</span></p>', unsafe_allow_html=True)


    job_description = st.text_area("Enter the job description:")
    uploaded_files = st.file_uploader("Upload multiple resumes in pdf format" , type="pdf",accept_multiple_files=True)
    lstResume=[]
    if uploaded_files:
        for uploaded_file in uploaded_files:
       # Get resume details
       # Read resume text based on file type
            if uploaded_file.type == "application/pdf":
                resume_text = utility.read_pdf(uploaded_file)
                resume_bytes = uploaded_file.read()
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = docx2txt.process(uploaded_file)
                resume_bytes=""
    
            data=[]
            data = ResumeParser(uploaded_file).get_extracted_data()
            
        
            Name=data['name']
            if job_description =="":
                matchscore=0
            else :
                matchscore= utility.match(resume_text,job_description)
            
            res =Resume.Resume(uploaded_file.name,Name,matchscore)
    
            lstResume.append(res)
    if len(lstResume) > 0 :
        
        df = pd.DataFrame([t.__dict__ for t in lstResume])
        df1=df[['Name','Filename', 'MatchScore']]
        #st.write(df1)
        st.dataframe(
    df1,
    column_config={
        "Name": "Candiate Name",
        "Filename": "File Name",
         "MatchScore": st.column_config.ProgressColumn(
            "Match Score",
            help="Match Score in Percentages",
            format="%f",
            min_value=0,
            max_value=100,
        )
       
    },
    hide_index=False,
)
    
       

if __name__ == "__main__":
    main()
