# app.py
import os
from flask import Flask, request, jsonify
from memory_system.memory import MemorySystem
from memory_system.extractor import InformationExtractor
from memory_system.brain import Brain
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize components
memory_system = MemorySystem()
extractor = InformationExtractor()
brain = Brain(memory_system)

# Store conversation history (for context)
conversation_history = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('user_id', 'default_user')
    message = data.get('message')
    
    # Initialize conversation history for new users
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    # Add message to conversation history
    conversation_history[user_id].append({"role": "user", "content": message})
    
    # Extract important information
    key_info = extractor.extract_key_information(message)
    
    # Store in memory if there's important information
    if key_info:
        memory_system.store_memory(key_info, {"user_id": user_id})
    
    # Generate response
    response = brain.generate_response(message)
    
    # Add response to conversation history
    conversation_history[user_id].append({"role": "assistant", "content": response})
    
    return jsonify({
        "response": response
    })

if __name__ == '__main__':
    app.run(debug=True)