import google.generativeai as genai
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.airtable_client import log_conversation
from src.agent.knowledge_base import search_knowledge_base

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""
You are a professional AI assistant for an immigration law firm.

CRITICAL INSTRUCTION: When FIRM DOCUMENTS CONTEXT is provided in the
user message, you MUST use that exact information to answer.
Do NOT say you don't have information if it appears in the context.
The context contains real information from our firm's documents.

For example:
- If context says "Initial consultations are $150" → answer "$150"
- If context says "Phone: +1 (555) 123-4567" → use that exact number
- If context says office hours → use those exact hours

Your role:
- Answer immigration questions using the provided context first
- Be clear, professional and empathetic
- Never give specific legal advice or guarantee outcomes
- Never discuss topics unrelated to immigration

End every response with:
"Would you like to schedule a consultation with one of our attorneys?"
""",
)

conversation_history = []


def chat_with_agent(
    user_message: str, client_name: str = "Unknown", log: bool = True
) -> str:
    """Send a message to the immigration agent and get a response."""

    # Search knowledge base
    context = search_knowledge_base(user_message)
    print(f"📄 Context found ({len(context)} chars)")

    # Inject context into message
    if context:
        enhanced_message = f"""Use the following information from our firm's documents to answer the question.

FIRM DOCUMENTS CONTEXT:
-----------------------
{context}
-----------------------

Client question: {user_message}

Remember: If the context contains specific details like phone numbers,
emails, pricing or hours, use those exact details in your answer."""
    else:
        enhanced_message = user_message

    # Add to history in Gemini format
    conversation_history.append({"role": "user", "parts": [enhanced_message]})

    # Call Gemini API
    chat = model.start_chat(history=conversation_history[:-1])
    response = chat.send_message(enhanced_message)
    reply = response.text

    # Store original message in history
    conversation_history[-1] = {"role": "user", "parts": [user_message]}
    conversation_history.append({"role": "model", "parts": [reply]})

    # Log to Airtable
    if log:
        try:
            log_conversation(
                client_name=client_name,
                message=user_message,
                ai_response=reply,
                channel="AI Agent",
            )
        except Exception as e:
            print(f"⚠️ Could not log conversation: {e}")

    return reply


def reset_conversation():
    """Clear conversation history."""
    global conversation_history
    conversation_history = []
    print("🔄 Conversation history reset.")
