from typing import Optional
import asyncio

class CustomerServiceAgent:
    def __init__(self):
        """Initialize the customer service agent."""
        self.initialized = False
        self.product_docs = {
            "password_reset": "To reset password: 1) Click 'Forgot Password' 2) Enter email 3) Follow link",
            "billing": "Billing cycle runs monthly. Payment processed on 1st of each month.",
            "features": "Product includes: cloud storage, sync, sharing, and admin controls."
        }
    
    async def initialize(self):
        """Initialize the agent with necessary configurations."""
        self.initialized = True
        return True
    
    async def process_input(self, context: str, user_input: str) -> str:
        """Process user input and generate a response."""
        if not self.initialized:
            raise RuntimeError("Agent not initialized. Call initialize() first.")
        
        # Simple keyword matching for demo purposes
        response = "I apologize, but I don't have specific information about that topic."
        
        if "password" in user_input.lower():
            response = self.product_docs["password_reset"]
        elif "billing" in user_input.lower() or "payment" in user_input.lower():
            response = self.product_docs["billing"]
        elif "feature" in user_input.lower() or "include" in user_input.lower():
            response = self.product_docs["features"]
        
        return response
