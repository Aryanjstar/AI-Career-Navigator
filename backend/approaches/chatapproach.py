import json
import logging
from collections.abc import AsyncGenerator
from typing import Any, Optional, Union

from openai import AsyncOpenAI, AsyncAzureOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from core.messagebuilder import MessageBuilder

logger = logging.getLogger(__name__)


class ChatApproach:
    """
    Simplified chat approach for AI Career Navigator that provides career guidance
    using GPT-4.1 without requiring search or embeddings.
    """
    
    def __init__(
        self,
        openai_client: Union[AsyncOpenAI, AsyncAzureOpenAI],
        chatgpt_model: str,
        chatgpt_deployment: Optional[str] = None,
        system_message_chat_conversation: str = None,
    ):
        self.openai_client = openai_client
        self.chatgpt_model = chatgpt_model
        self.chatgpt_deployment = chatgpt_deployment
        self.system_message_chat_conversation = system_message_chat_conversation or self._get_default_system_message()

    def _get_default_system_message(self) -> str:
        return """You are an AI Career Navigator, a professional career guidance assistant. Your role is to help users with:

1. **Career Planning**: Provide guidance on career paths, skill development, and professional growth
2. **Resume & Interview Preparation**: Help improve resumes, cover letters, and interview skills  
3. **Job Search Strategy**: Advise on job hunting techniques, networking, and application strategies
4. **Skill Gap Analysis**: Identify skills needed for target roles and recommend learning paths
5. **Industry Insights**: Share knowledge about different industries, job markets, and trends
6. **Professional Development**: Suggest ways to advance in current roles or transition to new ones

Guidelines:
- Provide specific, actionable advice tailored to the user's situation
- Ask clarifying questions when needed to give better guidance
- Be encouraging and supportive while being realistic about challenges
- Reference current industry standards and best practices
- Suggest concrete steps users can take to achieve their career goals
- If discussing salary or compensation, provide general market insights

Always maintain a professional, helpful, and encouraging tone. Focus on empowering users to make informed career decisions."""

    async def run(
        self,
        messages: list[dict],
        context: dict[str, Any] = None,
        session_state: Any = None,
    ) -> dict[str, Any]:
        """
        Run the chat approach and return a complete response.
        """
        try:
            # Build the message history
            message_builder = MessageBuilder(self.system_message_chat_conversation, self.chatgpt_model)
            
            # Add user messages
            for message in messages:
                if message.get("role") == "user":
                    message_builder.append_message("user", message.get("content", ""))
                elif message.get("role") == "assistant":
                    message_builder.append_message("assistant", message.get("content", ""))

            # Get response from OpenAI
            chat_completion: ChatCompletion = await self.openai_client.chat.completions.create(
                model=self.chatgpt_deployment or self.chatgpt_model,
                messages=message_builder.messages,
                temperature=0.7,
                max_tokens=1000,
                n=1,
            )

            response_message = chat_completion.choices[0].message
            
            return {
                "message": {
                    "content": response_message.content,
                    "role": response_message.role,
                },
                "session_state": session_state,
                "context": {
                    "data_points": [],
                    "thoughts": f"Responded using {self.chatgpt_model} for career guidance.",
                },
            }

        except Exception as e:
            logger.exception("Error in ChatApproach.run")
            return {
                "message": {
                    "content": "I apologize, but I'm experiencing technical difficulties. Please try again in a moment.",
                    "role": "assistant",
                },
                "session_state": session_state,
                "context": {
                    "data_points": [],
                    "thoughts": f"Error occurred: {str(e)}",
                },
            }

    async def run_stream(
        self,
        messages: list[dict],
        context: dict[str, Any] = None,
        session_state: Any = None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """
        Run the chat approach and return a streaming response.
        """
        try:
            # Build the message history
            message_builder = MessageBuilder(self.system_message_chat_conversation, self.chatgpt_model)
            
            # Add user messages
            for message in messages:
                if message.get("role") == "user":
                    message_builder.append_message("user", message.get("content", ""))
                elif message.get("role") == "assistant":
                    message_builder.append_message("assistant", message.get("content", ""))

            # Get streaming response from OpenAI
            chat_completion_stream = await self.openai_client.chat.completions.create(
                model=self.chatgpt_deployment or self.chatgpt_model,
                messages=message_builder.messages,
                temperature=0.7,
                max_tokens=1000,
                n=1,
                stream=True,
            )

            # Yield initial context
            yield {
                "session_state": session_state,
                "context": {
                    "data_points": [],
                    "thoughts": f"Responding using {self.chatgpt_model} for career guidance.",
                },
            }

            # Stream the response
            async for chunk in chat_completion_stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        yield {
                            "message": {
                                "content": delta.content,
                                "role": "assistant",
                            }
                        }

        except Exception as e:
            logger.exception("Error in ChatApproach.run_stream")
            yield {
                "message": {
                    "content": "I apologize, but I'm experiencing technical difficulties. Please try again in a moment.",
                    "role": "assistant",
                },
                "session_state": session_state,
                "context": {
                    "data_points": [],
                    "thoughts": f"Error occurred: {str(e)}",
                },
            }
