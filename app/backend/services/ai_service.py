"""
AI Service module
Handles all Azure OpenAI interactions with retry logic and caching
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
    AZURE_OPENAI_API_VERSION,
    TEMPERATURE
)
from utils.cache import get_cached_response, set_cached_response

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
    stop=stop_after_attempt(2),  # Reduced retries to save costs
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((openai.APIError, openai.APIConnectionError, openai.RateLimitError))
)
def get_ai_response(prompt, max_tokens=1200, system_prompt=None):
    """
    Get response from Azure OpenAI with retry logic
    COST-OPTIMIZED: Using GPT-3.5-Turbo with reduced tokens
    
    Args:
        prompt: User prompt/message
        max_tokens: Maximum tokens in response (default: 1200, reduced from 2000)
        system_prompt: Optional custom system prompt
        
    Returns:
        str: AI response text
    """
    if not client:
        return "⚠️ AI service is temporarily unavailable. Please check your configuration and try again."
    
    # Check cache first (COST SAVINGS!)
    cached = get_cached_response(prompt, max_tokens)
    if cached:
        logger.info("✅ Returning cached response (cost: $0.00)")
        return cached
    
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
            temperature=TEMPERATURE
        )
        
        elapsed_time = time.time() - start_time
        # Log token usage for cost monitoring
        usage = response.usage
        cost_estimate = (usage.prompt_tokens * 0.0005 + usage.completion_tokens * 0.0015) / 1000
        logger.info(f"✅ Response in {elapsed_time:.2f}s | Tokens: {usage.prompt_tokens}+{usage.completion_tokens}={usage.total_tokens} | Est. Cost: ${cost_estimate:.4f}")
        
        result = response.choices[0].message.content
        
        # Cache the response for future requests
        set_cached_response(prompt, max_tokens, result)
        
        return result
        
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

