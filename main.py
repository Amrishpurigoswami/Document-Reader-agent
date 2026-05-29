import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# Step 1: Load API Key from the .env file
load_dotenv()

# Step 2: Initialize the LLM using Groq API
# We use llama-3.1-8b-instant, which is free, fast, and powerful.
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0
)

# Step 3: Set up conversation memory
# ConversationBufferMemory stores the history of the conversation in memory.
memory = ConversationBufferMemory()

# Step 4: Define a custom prompt template
# This forces the agent to greet the user exactly as your mentor requested.
template = """The following is a friendly conversation between a human and an AI study assistant.
The AI is helpful, polite, and remembers details about the human.

If the human tells you their name (e.g., "My name is [Name]"), you MUST reply in this exact format:
"Nice to meet you [Name], I am your AI assistant." followed by a brief introduction.

Current conversation:
{history}
Human: {input}
AI:"""

prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=template
)

# Step 5: Assemble the Conversation Chain
# ConversationChain connects the LLM, the Memory, and our custom prompt.
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=False  # Setting verbose=True lets us see the prompt and history under the hood!
)

# Step 6: Define a simple loop to run the chatbot in the terminal
if __name__ == "__main__":
    print("🤖 AI Study Assistant is ready! (Type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break
            
        # Get response from the LangChain agent
        response = conversation.predict(input=user_input)
        print(f"Agent: {response}")
        print("-" * 50)
