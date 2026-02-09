from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
from memory_ops import MemoryRag

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for API requests

# Initialize the Brain (Global Variable)
print("⚡ Starting Memory Engine...")
try:
    bot = MemoryRag()
    logger.info("Memory RAG system initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Memory RAG: {e}")
    bot = None

@app.route("/")
def home():
    """Renders the Chat Interface"""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """API Endpoint: Receives JSON, Returns JSON"""
    try:
        # Validate bot initialization
        if bot is None:
            return jsonify({
                "error": "Memory system not initialized",
                "response": "Sorry, the memory system is currently unavailable.",
                "memory_used": "System error"
            }), 500

        # Parse request
        user_data = request.json
        user_message = user_data.get("message", "").strip()
        turn = user_data.get("turn", 0)

        # Validate input
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        logger.info(f"Turn {turn}: Processing message: {user_message[:50]}...")

        # 1. RETRIEVE & THINK (The "Read" Path)
        try:
            response_text, retrieved_context = bot.retrieval_pipeline(user_message)
            logger.info(f"Turn {turn}: Response generated successfully")
        except Exception as e:
            logger.error(f"Turn {turn}: Retrieval pipeline error: {e}")
            response_text = "I apologize, but I encountered an error processing your message."
            retrieved_context = None

        # 2. SAVE MEMORY (The "Write" Path)
        # We save strictly *after* answering to keep latency low for the user
        try:
            bot.ingestion_pipeline(user_message, turn)
            logger.info(f"Turn {turn}: Memory saved successfully")
        except Exception as e:
            logger.error(f"Turn {turn}: Ingestion pipeline error: {e}")

        # Return the response + the "thought process" (for the UI to show)
        return jsonify({
            "response": response_text,
            "memory_used": retrieved_context if retrieved_context else "No relevant memory found.",
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        return jsonify({
            "error": "Internal server error",
            "response": "An unexpected error occurred. Please try again.",
            "memory_used": "Error"
        }), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy" if bot is not None else "unhealthy",
        "timestamp": datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {e}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    print("📍 Navigate to http://localhost:5000 to use the Memory Bot")
    app.run(debug=True, port=5000, host='0.0.0.0')