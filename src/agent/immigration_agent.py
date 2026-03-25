from groq import Groq
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.airtable_client import log_conversation
from src.agent.knowledge_base import search_knowledge_base

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a professional AI assistant for an immigration law firm.

CRITICAL INSTRUCTION: When FIRM DOCUMENTS CONTEXT is provided in the 
user message, you MUST use that exact information to answer. 
Do NOT say you don't have information if it appears in the context.
The context contains real information from our firm's documents.

For example:
- If context says "Initial consultations are $150" → answer "$150"
- If context says "Phone: (+237)-68074-9528" → use that exact number
- If context says office hours → use those exact hours

Your role:
- Answer immigration questions using the provided context first
- Be clear, professional and empathetic
- Never give specific legal advice or guarantee outcomes
- Never discuss topics unrelated to immigration

End every response with:
"Would you like to schedule a consultation with one of our attorneys?"
"""

# Add user message to history
conversation_history = []


def chat_with_agent(
    user_message: str, client_name: str = "Unknown", log: bool = True
) -> str:
    """Send a message to the immigration agent and get a response."""

    # Search knowledge base for relevant context
    context = search_knowledge_base(user_message)
    print(f"Context found ({len(context)}) chars")

    # Inject context into the user message if found
    if context:
        enhanced_message = f"""Üse the following information from our firm's documents to answer the question.
        
    FIRM DOCUMENTS CONTEXT:
    -----------------------
    {context}
    -----------------------
    
    client question: {user_message}
    
    Remember: If the context contains specific details like phone numbers,
    emails, pricing or hours, use those exact details in your answer."""
    else:
        enhanced_message = user_message
    # Add enhanced message to history
    conversation_history.append({"role": "user", "content": enhanced_message})

    # Call Groq API with full conversation history

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
        temperature=0.7,
        max_tokens=1000,
    )

    # Extract reply

    reply = response.choices[0].message.content

    # Store original message in history (not enhanced version)
    conversation_history[-1] = {"role": "user", "content": user_message}
    conversation_history.append({"role": "assistant", "content": reply})

    # Log conversation to Airtable
    if log:
        try:
            log_conversation(
                client_name=client_name,
                message=user_message,
                ai_response=reply,
                channel="AI Agent",
            )
        except Exception as e:
            print(f" ⚠️ Could not log conversation: {e}")
    return reply


def reset_conversation():
    """Clear conversation history to start a fresh session."""
    global conversation_history
    conversation_history = []
    print("🔄 Conversation history reset.")
