from typing import List, Dict, Any


class MessageBuilder:
    """
    A helper class to build chat messages for OpenAI API calls.
    """
    
    def __init__(self, system_message: str, model: str):
        self.model = model
        self.messages: List[Dict[str, Any]] = []
        if system_message:
            self.messages.append({"role": "system", "content": system_message})
    
    def append_message(self, role: str, content: str) -> None:
        """Add a message to the conversation."""
        if content and content.strip():
            self.messages.append({"role": role, "content": content})
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """Get all messages."""
        return self.messages
    
    def clear_messages(self) -> None:
        """Clear all messages except system message."""
        system_messages = [msg for msg in self.messages if msg.get("role") == "system"]
        self.messages = system_messages 