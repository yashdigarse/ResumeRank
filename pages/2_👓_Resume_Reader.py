import streamlit as st
from pyresparser import ResumeParser
from streamlit_tags import st_tags
import json

import pandas as pd
import nltk
nltk.download('stopwords')



from openai import OpenAI
client = OpenAI(
  api_key= st.secrets["APIKEY"]
)





st.set_page_config(
    page_title="Resume Reader",
    page_icon="👓",
)

# web app
def main():
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
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TX91V7N5MJ"></script>
<script>
			window.dataLayer = window.dataLayer || [];
			function gtag(){dataLayer.push(arguments);}
			gtag('js', new Date());

			gtag('config', 'G-TX91V7N5MJ');
		</script>

""", unsafe_allow_html=True)

    st.markdown('<p ><span class="big-font">Resume Reader</span>  <span class="s-font">Powered by AI.</span></p>', unsafe_allow_html=True)

    
   

    uploaded_file = st.file_uploader('Upload Resume', type=['pdf'])
    if uploaded_file is not None:
         
         data = ResumeParser(uploaded_file).get_extracted_data()
         resSummary,interviewQuestion=st.tabs(["Resume Summary","Interview Questions",])
         with resSummary:
            st.header ("Resume Summary")
            with st.container(border=True):
                col1, col2 = st.columns([0.2,0.7],gap="small")

                with col1:
                    st.write("Name")
                    st.write("Email")
                    st.write("Contact Number")
                

                with col2:
                    st.write(f"**{data['name']}**")
                    st.write(f"**{data['email']}**")
                    st.write(f"**{data['mobile_number']}**")
            
            if data['skills'] is not None:
                designation = st_tags(label='### Skills',
                                   text='',
                                   value=data['skills'])
            if data['company_names'] is not None:
                designation = st_tags(label='### Company',
                                   text='',
                                   value=data['company_names'])
            if data['designation'] is not None:
                designation = st_tags(label='### Designation',
                                   text='',
                                   value=data['designation'])
        
          
        
         with interviewQuestion:
            st.header ("Interview Questions")
            
           
            keywords = st_tags(label='Update Skills to generate questions:', text='Press enter to add more', value=data['skills']) 
            skills = ','.join(keywords)
            query="Generate top random 5 interview question and answer on for each skills in "+skills + " individually for beginners."
            
            if st.button('### Generate Questions') and keywords !="":
                def get_chatgpt_response():
                    messages = [{"role": "user", "content": query}]
                    try:
                        response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        )
                        return response.choices[0].message
                    except openai.OpenAIError as e:
                        print("Error:", e)
                        return None
                response = get_chatgpt_response()
               
                content=response.content.replace("\nAnswer:","\n\n **Answer :**")
                #content=content.replace("\nA:","\n\n **Answer :**")

                #st.write(response)
                st.write(content)
                
        














if __name__ == "__main__":
    main()