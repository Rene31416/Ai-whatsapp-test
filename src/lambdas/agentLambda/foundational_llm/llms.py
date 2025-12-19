from langchain.chat_models import init_chat_model
from langchain_openai import OpenAI
llm = init_chat_model("gpt-4.1", temperature=0.7)