# 🧠 AI_ExamCrafter | QuestionPaper_Generator

An AI-powered tool to generate structured question papers from uploaded syllabus PDFs using NLP and HuggingFace Transformers. Automatically creates 1-mark MCQs, 2-mark short questions, and 14-mark long questions via a simple and intuitive Streamlit interface.

---

## 🚀 Features

- 📤 Upload syllabus or unit notes in `.pdf` format
- 🔍 Automatically extract key content and generate:
  - 1 Mark MCQs (with options)
  - 2 Mark short answer questions
  - 14 Mark long answer questions
- 🤖 Uses HuggingFace’s T5-based QG model and NLTK for NLP processing
- 🧮 Choose total marks and customize mark split-up
- 📄 Preview and download your question paper instantly

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit  
- **Backend / NLP**: HuggingFace Transformers (`valhalla/t5-base-qg-hl`), NLTK  
- **PDF Handling**: pdfplumber  
- **Language**: Python

---

AI-Generated Question Paper

Part A – 1 Mark Questions (Choose the correct answer)
1. _____ handles memory management.
   a) RAM
   b) CPU
   c) Kernel
   d) Storage

Part B – 2 Mark Questions (Short Answers)
1. What is the role of an operating system?

Part C – 14 Mark Questions (Long Answers)
1. Explain the types of network topologies in detail. (14 marks)
