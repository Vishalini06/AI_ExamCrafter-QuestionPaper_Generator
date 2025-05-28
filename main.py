import streamlit as st
import pdfplumber
import nltk
import random
import re
from transformers import pipeline
import io


nltk.download('punkt')
nltk.download('stopwords')

from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))


try:
    qg_pipeline = pipeline("text2text-generation", model="valhalla/t5-base-qg-hl")
except:
    qg_pipeline = None


st.set_page_config(page_title="AI Question Paper Generator", layout="wide")
st.title("🧠 Smart AI-Based Question Paper Generator")


uploaded_file = st.file_uploader("📤 Upload syllabus/unit notes (.pdf only)", type=["pdf"])


def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        return ''.join([page.extract_text() or "" for page in pdf.pages])


def generate_mcq(sentence):
    words = [w for w in re.findall(r'\b\w+\b', sentence) if w.lower() not in stop_words and len(w) > 3]
    if len(words) < 4:
        return None  
    correct_answer = random.choice(words)
    distractors = random.sample([w for w in words if w != correct_answer], 3)
    options = [correct_answer] + distractors
    random.shuffle(options)
    labeled_options = [f"{label}) {opt}" for label, opt in zip(['a', 'b', 'c', 'd'], options)]
    question = sentence.replace(correct_answer, "_____")
    return question, labeled_options, correct_answer


def nlp_question(sentence):
    if qg_pipeline:
        try:
            res = qg_pipeline(f"generate question: {sentence}")
            return res[0]['generated_text']
        except:
            pass
    return f"What is {sentence[:60]}?"


if uploaded_file:
    content = extract_text_from_pdf(uploaded_file)
    st.success("✅ File uploaded and processed!")

    total_marks = st.radio("🎯 Select total marks:", [50, 100])
    st.markdown("### 🧮 Choose mark split-up:")
    col1, col2, col3 = st.columns(3)

    with col1:
        one_mark_count = st.number_input("1 Mark Questions", min_value=0, value=5)
    with col2:
        two_mark_count = st.number_input("2 Mark Questions", min_value=0, value=5)
    with col3:
        fourteen_mark_count = st.number_input("14 Mark Questions", min_value=0, value=2)

    expected_total = one_mark_count * 1 + two_mark_count * 2 + fourteen_mark_count * 14
    if expected_total != total_marks:
        st.warning(f"⚠️ Your selected questions add up to {expected_total} marks, not {total_marks} marks.")
    else:
        if st.button("✨ Generate Question Paper"):
            st.subheader("📄 Generated Question Paper")

            sentences = [s for s in sent_tokenize(content) if len(s.split()) > 5]
            random.shuffle(sentences)

            question_paper_text = "AI-Generated Question Paper\n\n"

            # Part A
            question_paper_text += "Part A – 1 Mark Questions (Choose the correct answer)\n"
            mcq_index = 1
            for s in sentences:
                if mcq_index > one_mark_count:
                    break
                result = generate_mcq(s)
                if result:
                    question, options, answer = result
                    question_paper_text += f"{mcq_index}. {question}\n"
                    for opt in options:
                        question_paper_text += f"   {opt}\n"
                    question_paper_text += "\n"
                    mcq_index += 1

            # Part B
            question_paper_text += "\nPart B – 2 Mark Questions (Short Answers)\n"
            for i in range(two_mark_count):
                if i + one_mark_count < len(sentences):
                    q = nlp_question(sentences[i + one_mark_count])
                    question_paper_text += f"{i+1}. {q}\n\n"

            # Part C
            question_paper_text += "Part C – 14 Mark Questions (Long Answers)\n"
            for i in range(fourteen_mark_count):
                if i + one_mark_count + two_mark_count < len(sentences):
                    q = nlp_question(sentences[i + one_mark_count + two_mark_count])
                    question_paper_text += f"{i+1}. {q} (14 marks)\n\n"

            
            st.text_area("📝 Preview of Generated Question Paper", question_paper_text, height=500)

            
            st.download_button(
                label="⬇️ Download as Text File",
                data=question_paper_text.encode('utf-8'),
                file_name="generated_question_paper.txt",
                mime="text/plain"
            )
            st.success("🎉 Question Paper Generated Successfully!")
