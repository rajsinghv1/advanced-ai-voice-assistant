from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage

from app.config import GOOGLE_API_KEY, GEMINI_MODEL
from app.memory import memory
from app.tools import TOOLS
from app.rag import RAG_TOOL


llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=GOOGLE_API_KEY,
)

agent = create_agent(
    model=llm,
    tools=TOOLS + [RAG_TOOL],
    system_prompt=(
        "You are an advanced AI voice assistant. "
        "Answer clearly and helpfully. "
        "Use the calculator tool for mathematical calculations. "
        "Use the date and time tool when asked about current date or time. "
        "Use ask_documents when the user asks about uploaded documents. "
        "Base document-specific answers on retrieved information. "
        "Do not invent document contents. "
        "If the documents do not contain the answer, say so. "
        "Do not claim to have used a tool unless it was actually called."
    ),
)


def _message_text(content):
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
            elif isinstance(item, str):
                parts.append(item)

        return "\n".join(part for part in parts if part)

    return str(content)


def get_ai_response(user_message: str, session_id: str = "default") -> str:
    history = memory.get_history(session_id)

    messages = [
        {"role": item["role"], "content": item["content"]}
        for item in history
        if item.get("role") in ("user", "assistant")
    ]

    messages.append({"role": "user", "content": user_message})

    result = agent.invoke({"messages": messages})

    final_message = next(
        (
            message
            for message in reversed(result["messages"])
            if isinstance(message, AIMessage) and not message.tool_calls
        ),
        None,
    )

    if final_message is None:
        raise RuntimeError("The AI agent did not return a final response.")

    answer = _message_text(final_message.content)

    memory.add_message(session_id, "user", user_message)
    memory.add_message(session_id, "assistant", answer)

    return answer
