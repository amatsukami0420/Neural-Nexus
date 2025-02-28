from typing import List
import logging

logger = logging.getLogger(__name__)

class ConversationManager:
    def __init__(self):
        self.context = []
        self.max_messages = 20
        self.system_prompt = """You are a helpful and knowledgeable AI assistant. You are direct and concise in your responses, 
        while maintaining a friendly tone. You help users with their questions across various topics including coding, analysis, 
        and general knowledge. If you're unsure about something, you'll acknowledge it honestly."""
        
        # Initialize context with system prompt
        self.context.append({"role": "system", "content": self.system_prompt})
        
    def add_to_context(self, user_input: str, bot_response: str):
        try:
            self.context.append({"role": "user", "content": user_input})
            self.context.append({"role": "assistant", "content": bot_response})
            
            # Keep only last 20 messages (10 exchanges)
            if len(self.context) > self.max_messages:
                self.context = self.context[-self.max_messages:]
        except Exception as e:
            logger.error(f"Error adding to context: {str(e)}")
            
    def get_formatted_context(self) -> str:
        # Format context for Gemini consumption
        formatted_context = "Previous conversation:\n"
        for msg in self.context:
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted_context += f"{role}: {msg['content']}\n"
        return formatted_context
        
    def get_context(self) -> List[dict]:
        return self.context
        
    def clear_context(self):
        self.context = [{"role": "system", "content": self.system_prompt}]
