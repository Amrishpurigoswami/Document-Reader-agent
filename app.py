import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Step 1: Load API Key from the .env file
load_dotenv()

# Step 2: Initialize the LLM using Groq API
# We use llama-3.1-8b-instant, which is free, fast, and powerful.
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0
)

# Step 3: Set up conversation memory (simple list)
conversation_history = []

# Step 4: Define a custom prompt template
# This forces the agent to greet the user exactly as requested.
system_prompt = """The following is a friendly conversation between a human and an AI study assistant.
The AI is helpful, polite, and remembers details about the human.

If the human tells you their name (e.g., "My name is [Name]"), you MUST reply in this exact format:
"Nice to meet you [Name], I am your AI assistant." followed by a brief introduction."""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

# Step 5: Create the chain
chain = prompt | llm

# Step 6: Define a simple loop to run the chatbot in the terminal
if __name__ == "__main__":
    print("🤖 AI Study Assistant is ready! (Type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        
        # Add user message to history
        conversation_history.append(HumanMessage(content=user_input))
        
        # Get response from the LLM
        response = chain.invoke({"history": conversation_history, "input": user_input})
        
        # Extract text from response
        response_text = response.content if hasattr(response, 'content') else str(response)
        
        # Add AI response to history
        conversation_history.append(AIMessage(content=response_text))
        
        print(f"Agent: {response_text}")
        print("-" * 50)
