# AI Assistant using LangChain
Overview

This project is a simple AI Assistant built using LangChain and OpenAI. The assistant interacts with users, greets them by name, and introduces itself as an AI assistant. The project demonstrates the fundamentals of working with Large Language Models (LLMs), prompt templates, and LangChain workflows.

Features
User name input
Personalized greeting generation
OpenAI LLM integration
LangChain PromptTemplate usage
Environment variable management using python-dotenv
Modern LangChain invoke() workflow
Technologies Used
Python 3.14.4
LangChain
LangChain OpenAI
OpenAI API
Python Dotenv

Project Structure

project/
│
├── app.py
├── .env
├── requirements.txt
└── README.md
Installation
1. Clone the Repository
git clone <repository-url>
cd <repository-name>
2. Create Virtual Environment
python -m venv venv
3. Activate Virtual Environment

Windows:

venv\Scripts\activate
4. Install Dependencies
pip install -r requirements.txt
5. Configure Environment Variables

Create a .env file and add your OpenAI API key:

OPENAI_API_KEY=your_api_key_here
Running the Project
python app.py
Example

Input:

Enter your name: Amrish

Output:

Hello Amrish! Nice to meet you.
I am your AI Assistant.
Concepts Learned
Large Language Models (LLMs)
LangChain Framework
Prompt Engineering
PromptTemplate
OpenAI Integration
Environment Variables
LangChain Runnable Architecture
invoke() Method
Future Enhancements
Conversational Memory
Retrieval-Augmented Generation (RAG)
PDF Question Answering
FAISS Vector Database
Voice-to-Text Integration
LangChain Evaluation Framework
VibeVoice-ASR Integration
Author

Amrish Puri Goswami

Computer Science Student | AI & Machine Learning Enthusiast
