import re
from PyPDF2 import PdfReader
from gensim.models.doc2vec import Doc2Vec
import numpy as np
from numpy.linalg import norm
import pandas as pd
import nltk
import pathlib
import bs4

from bs4 import BeautifulSoup

import shutil
nltk.download('stopwords')




def preprocess_text(text):
    text=clean_resume(text)
    # Convert the text to lowercase
    text = text.lower()
    # Remove punctuation from the text
    text = re.sub('[^a-z]', ' ', text)
    # Remove numerical values from the text
    text = re.sub(r'\d+', '', text)
    # Remove extra whitespaces
    text = ' '.join(text.split())
    return text

def match(resume,jd_input):
    input_cv = preprocess_text(resume)
    input_jd = preprocess_text(jd_input)
    model = Doc2Vec.load('cvjdm.model')
    v1 = model.infer_vector(input_cv.split())
    v2 = model.infer_vector(input_jd.split())
    similarity = 100 * (np.dot(np.array(v1), np.array(v2))) / (norm(np.array(v1)) * norm(np.array(v2)))
    return similarity

def clean_resume(resume_text):
    clean_text = re.sub('http\S+\s*', ' ', resume_text)
    clean_text = re.sub('RT|cc', ' ', clean_text)
    clean_text = re.sub('#\S+', '', clean_text)
    clean_text = re.sub('@\S+', '  ', clean_text)
    clean_text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean_text)
    clean_text = re.sub(r'[^\x00-\x7f]', r' ', clean_text)
    clean_text = re.sub('\s+', ' ', clean_text)
    return clean_text


def read_pdf(file):
    pdfReader = PdfReader(file)
    count = len(pdfReader.pages)
    all_page_text = ""
    for i in range(count):
        page = pdfReader.pages[i]
        all_page_text += page.extract_text()
    return all_page_text

def show_pdf(resume_bytes):
    #with open(file_path, "rb") as f:
    base64_pdf = base64.b64encode(resume_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def inject_ga():
    GA_ID = "google_analytics"


    GA_JS = """
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-TX91V7N5MJ"></script>
    <script>
			window.dataLayer = window.dataLayer || [];
			function gtag(){dataLayer.push(arguments);}
			gtag('js', new Date());

			gtag('config', 'G-TX91V7N5MJ');
		</script>
    """

   


