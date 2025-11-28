import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- SECURITY STEP ---

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found. Make sure you have a .env file!")
    exit()

genai.configure(api_key=api_key)

# --- YOUR AGENT SETUP ---
def search_documentation(topic: str):
    """Searches internal knowledge base for C programming topics."""
    print(f"\n[System] Agent is searching docs for: '{topic}'...")
    knowledge_base = {
        "segmentation fault": "A segmentation fault occurs when a program attempts to access a memory location that it is not allowed to access.",
        "malloc": "malloc() allocates size bytes of uninitialized memory.",
        "printf": "printf formats and prints data to standard output."
    }
    for key in knowledge_base:
        if key in topic.lower():
            return knowledge_base[key]
    return "No specific documentation found."

tools = [search_documentation]

system_instruction = "You are a helpful C programming tutor. Use the search_documentation tool for technical definitions."

# Using the standard model name
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=tools,
    system_instruction=system_instruction
)

chat_session = model.start_chat(enable_automatic_function_calling=True)

def run_chat():
    print("\n--- Code Learning Companion (Local) ---")
    print("Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        try:
            response = chat_session.send_message(user_input)
            print(f"Agent: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_chat()