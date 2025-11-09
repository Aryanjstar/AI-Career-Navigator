"""
AI Service module
Handles all Azure OpenAI interactions with retry logic
"""
import logging
import time
import openai
from openai import AzureOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION
)

logger = logging.getLogger(__name__)

# Initialize Azure OpenAI client
client = None
if AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY:
    try:
        client = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            timeout=60.0,
            max_retries=3
        )
        logger.info("✅ Azure OpenAI client initialized successfully")
    except Exception as e:
        logger.error(f"❌ Azure OpenAI initialization failed: {e}")
else:
    logger.error("❌ Azure OpenAI configuration missing!")

def get_client():
    """Get the Azure OpenAI client instance"""
    return client

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((openai.APIError, openai.APIConnectionError, openai.RateLimitError))
)
def get_ai_response(prompt, max_tokens=2000, system_prompt=None):
    """
    Get response from Azure OpenAI with retry logic
    
    Args:
        prompt: User prompt/message
        max_tokens: Maximum tokens in response
        system_prompt: Optional custom system prompt
        
    Returns:
        str: AI response text
    """
    if not client:
        return "⚠️ AI service is temporarily unavailable. Please check your configuration and try again."
    
    # Default system prompt
    if system_prompt is None:
        system_prompt = """You are an expert AI Career Navigator specializing in tech careers.
        
        **Core Instructions:**
        - Your tone must always be friendly, professional, encouraging, and helpful.
        - Address the user directly as "you". Do not invent, use, or ask for the user's name.
        - Provide detailed, actionable, and specific advice tailored to the user's context.
        - When the user's prompt provides a specific structure or format, you MUST follow it precisely.
        - For any non-career-related questions, respond with: "I'm focused on career guidance only. Please ask about your tech career, job applications, interviews, or skill development."
        - Use HTML for formatting, such as `<h4>`, `<strong>`, `<ul>`, and `<li>` for clarity. Do not use markdown asterisks.
        """
    
    try:
        logger.info(f"Sending request to OpenAI (max_tokens={max_tokens})")
        start_time = time.time()
        
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        elapsed_time = time.time() - start_time
        logger.info(f"✅ OpenAI response received in {elapsed_time:.2f}s")
        
        return response.choices[0].message.content
        
    except openai.RateLimitError as e:
        logger.error(f"❌ Rate limit exceeded: {e}")
        return "⚠️ Our AI service is experiencing high demand. Please wait a moment and try again."
    except openai.APIConnectionError as e:
        logger.error(f"❌ Connection error: {e}")
        return "⚠️ Unable to connect to AI service. Please check your internet connection and try again."
    except openai.APIError as e:
        logger.error(f"❌ API error: {e}")
        return "⚠️ The AI service encountered an error. Please try again in a moment."
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return f"⚠️ An unexpected error occurred. Please try again."

