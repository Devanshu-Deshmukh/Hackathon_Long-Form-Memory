from memory_ops import MemoryRag

def start_chat():
    print("Initializing Memory System...")
    bot = MemoryRag()
    
    turn = 1
    print("\n🤖 Bot: Online! I remember everything. (Type 'exit' to quit)\n")
    
    while True:
        user_input = input(f"You (Turn {turn}): ")
        if user_input.lower() in ["exit", "quit"]:
            print("🤖 Bot: Saving memories... Goodbye!")
            break
            
        # --- 1. RETRIEVAL (Remembering) ---
        response, used_memory = bot.retrieval_pipeline(user_input)
        
        # (Optional) Show what the bot "remembered" - Good for Hackathon Demos!
        if used_memory:
            print(f"\n   🔍 [Thinking]: I recalled -> {used_memory}")
        
        print(f"🤖 Bot: {response}\n")
        
        # --- 2. INGESTION (Learning) ---
        # We save what the user said so we remember it later
        bot.ingestion_pipeline(user_input, turn)
        
        turn += 1

if __name__ == "__main__":
    start_chat()