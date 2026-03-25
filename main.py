from src.agent.immigration_agent import chat_with_agent, reset_conversation
from src.agent.knowledge_base import build_vector_store, CHUNKS_DB_PATH
from src.automations.followup import run_all_sequences
from src.automations.document_checklist import run_all_checklist_automations
from src.database.airtable_client import schedule_consultation, get_all_leads
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()

# Only build knowledge base if not already built
if not os.path.exists(CHUNKS_DB_PATH):
    build_vector_store()
else:
    print("Knowledge base already exist, skipping build.")


# Test follow-up automations
print("\n Testing Follow-Up Automations...")

# Schedule a test consultation for the first lead (1 hour form now)
leads = get_all_leads()
if leads:
    test_lead = leads[0]
    record_id = test_lead["id"]
    name = test_lead["fields"].get("Name", "")
    consultation_time = (datetime.now() + timedelta(hours=1)).isoformat()
    schedule_consultation(record_id, consultation_time)
    print(f"Schedule consultation for: {name}")


run_all_sequences()

# Run all automation sequences
run_all_checklist_automations()

# Start interactive chat
reset_conversation()

print("=" * 60)
print("🏛️ Immigration Law Firm AI Agent (RAG Enabled)")
print("Type 'quit' to exit | Type 'reset' to start over.")
print("=" * 60)

client_name = input("\nEnter your name:").strip() or "Anonymous"
print(f"\nWelcome, {client_name}! How can I assist you today?\n")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue
    if user_input.lower() == "quit":
        print("👋 Goodbye! If you have more questions, feel free to come back anytime.")
        break
    if user_input.lower() == "reset":
        reset_conversation()
        print("🔄 Starting a new conversation.\n")
        continue

    print("\n🤖 Agent: ", end="", flush=True)

    agent_response = chat_with_agent(user_message=user_input, client_name=client_name)
    print(agent_response)
    print("-" * 60)
