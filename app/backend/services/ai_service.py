"""
AI Service for Azure OpenAI interactions
"""
import logging
from typing import Optional
from openai import AzureOpenAI
from config import Config

logger = logging.getLogger(__name__)


class AIService:
    """Service for interacting with Azure OpenAI"""
    
    def __init__(self):
        """Initialize Azure OpenAI client"""
        self.client: Optional[AzureOpenAI] = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Azure OpenAI client"""
        try:
            if Config.AZURE_OPENAI_ENDPOINT and Config.AZURE_OPENAI_API_KEY:
                self.client = AzureOpenAI(
                    azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
                    api_key=Config.AZURE_OPENAI_API_KEY,
                    api_version=Config.AZURE_OPENAI_API_VERSION
                )
                logger.info("Azure OpenAI client initialized successfully")
            else:
                logger.error("Azure OpenAI configuration missing!")
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI client: {e}")
            raise
    
    def get_completion(self, prompt: str, system_message: Optional[str] = None, max_tokens: int = 2000) -> str:
        """
        Get completion from Azure OpenAI
        
        Args:
            prompt: User prompt
            system_message: Optional system message to guide AI behavior
            max_tokens: Maximum tokens in response
            
        Returns:
            AI-generated response
        """
        if not self.client:
            return "Azure OpenAI client not configured properly."
        
        try:
            # Default system message if not provided
            if not system_message:
                system_message = """You are an expert AI Career Navigator specializing in tech careers.

                **Core Instructions:**
                - Your tone must always be friendly, professional, encouraging, and helpful.
                - Address the user directly as "you". Do not invent, use, or ask for the user's name.
                - Provide detailed, actionable, and specific advice tailored to the user's context.
                - When the user's prompt provides a specific structure or format, you MUST follow it precisely.
                - For any non-career-related questions, respond with: "I'm focused on career guidance only. Please ask about your tech career, job applications, interviews, or skill development."
                - Use HTML for formatting, such as `<h4>`, `<strong>`, `<ul>`, and `<li>` for clarity. Do not use markdown asterisks.
                """
            
            response = self.client.chat.completions.create(
                model=Config.AZURE_OPENAI_DEPLOYMENT,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return "I encountered an error processing your request. Please try again."

