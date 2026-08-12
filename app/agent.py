import logging

from app.config import settings
from app.memory import get_history
from app.prompts import SYSTEM_PROMPT
from app.tools.faq_search import search_faq
from app.tools.sheets import save_booking
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

logger = logging.getLogger(__name__)
_agent = None


def build_agent():
    global _agent
    if settings.llm_provider == "gemini":
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",  # <--- Use gemini-2.0-flash or gemini-1.5-flash
            google_api_key=settings.google_api_key,
        )
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {settings.llm_provider}")

    _agent = create_agent(
        llm, tools=[search_faq, save_booking], system_prompt=SYSTEM_PROMPT
    )
    logger.info("Agent built with tools [search_faq, save_booking].")
    return _agent


async def reply(user_id: str, message: str) -> str:
    history = get_history(user_id)
    result = await _agent.ainvoke(
        {"messages": history.messages + [HumanMessage(content=message)]}
    )
    reply_text = result["messages"][-1].text

    history.add_user_message(message)
    history.add_ai_message(reply_text)
    return reply_text