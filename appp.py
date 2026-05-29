import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from pypdf import PdfReader
from pathlib import Path

# Step 1: Load API Key from the .env file In which API key that I copied from website and paste it in .env file, then load it here
load_dotenv()

# Step 2: Initialize the LLM using Groq API We use llama-3.1-8b-instant, which is free, fast, and powerful.
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0
)

# Step 3: Global variables
conversation_history = []
uploaded_document = ""
external_access_allowed = False

# Step 4: Helper function to read documents and extract text content (It'll support PDF, TXT, DOCX, and MD files)
def read_document(file_path):
    """Read various document types and extract text"""
    global uploaded_document
    
    file_path = Path(file_path)
    
    if not file_path.exists():
        return "❌ File not found!"
    
    try:
        if file_path.suffix.lower() == '.pdf':
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            uploaded_document = text
            return f"✅ PDF loaded! ({len(reader.pages)} pages, {len(text)} characters)"
        
        elif file_path.suffix.lower() in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            uploaded_document = text
            return f"✅ Text file loaded! ({len(text)} characters)"
        
        elif file_path.suffix.lower() in ['.docx']:
            from docx import Document
            doc = Document(file_path)
            text = '\n'.join([para.text for para in doc.paragraphs])
            uploaded_document = text
            return f"✅ DOCX loaded! ({len(text)} characters)"
        
        else:
            return "❌ Unsupported file type! Use: PDF, TXT, DOCX, MD"
    
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"

# Step 5: Create system prompt
def create_system_prompt():
    """Create dynamic system prompt based on document and external access"""
    base_prompt = """You are an AI study assistant. You are helpful, polite, and remember details.

If the human tells you their name (e.g., "My name is [Name]"), reply: "Nice to meet you [Name], I am your AI assistant." """
    
    if uploaded_document:
        base_prompt += f"""

📚 IMPORTANT - UPLOADED DOCUMENT:
You have access to an uploaded document. When answering questions, prioritize information from this document.
Here's the document content:
---
{uploaded_document[:3000]}{'...[document truncated]' if len(uploaded_document) > 3000 else ''}
---
"""
    
    if external_access_allowed:
        base_prompt += """

🌐 EXTERNAL ACCESS ENABLED:
The user has approved using external sources. If you need information beyond the document, you can ask the user to provide external sources or information."""
    else:
        base_prompt += """

⚠️ RESTRICTED MODE:
Only use information from the uploaded document. Don't use external knowledge for this document."""
    
    return base_prompt

# Step 6: Create the chain
def get_response(user_input):
    """Get AI response with document context"""
    system_prompt = create_system_prompt()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])
    
    chain = prompt | llm
    response = chain.invoke({"history": conversation_history, "input": user_input})
    return response.content if hasattr(response, 'content') else str(response)

# Step 7: Main chat loop
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 AI STUDY ASSISTANT WITH DOCUMENT SUPPORT")
    print("="*60)
    print("\n📋 COMMANDS:")
    print("  /upload <filepath>    - Upload a document (PDF, TXT, DOCX)")
    print("  /external yes         - Allow AI to use external sources")
    print("  /external no          - Only use document content")
    print("  /status               - Show document & access status")
    print("  /clear                - Clear document & reset")
    print("  quit or exit          - Exit the assistant")
    print("="*60 + "\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        # Handle special commands
        if user_input.lower() == "quit" or user_input.lower() == "exit":
            print("👋 Goodbye! Thank you for using AI Study Assistant.")
            break
        
        elif user_input.lower().startswith("/upload"):
            try:
                file_path = user_input.replace("/upload", "").strip()
                result = read_document(file_path)
                print(f"Assistant: {result}\n")
            except Exception as e:
                print(f"Assistant: ❌ Error: {str(e)}\n")
        
        elif user_input.lower().startswith("/external"):
            if "yes" in user_input.lower():
                external_access_allowed = True
                print("Assistant: 🌐 External access ENABLED. I can use external sources now.\n")
            elif "no" in user_input.lower():
                external_access_allowed = False
                print("Assistant: 🔒 External access DISABLED. I'll only use the document.\n")
        
        elif user_input.lower() == "/status":
            doc_status = "✅ Loaded" if uploaded_document else "❌ No document"
            ext_status = "🌐 Enabled" if external_access_allowed else "🔒 Disabled"
            print(f"Assistant: Document: {doc_status} | External Access: {ext_status}\n")
        
        elif user_input.lower() == "/clear":
            uploaded_document = ""
            external_access_allowed = False
            conversation_history = []
            print("Assistant: ✨ Cleared! Ready for new document.\n")
        
        else:
            # Regular conversation
            conversation_history.append(HumanMessage(content=user_input))
            response = get_response(user_input)
            conversation_history.append(AIMessage(content=response))
            print(f"Agent: {response}\n")
