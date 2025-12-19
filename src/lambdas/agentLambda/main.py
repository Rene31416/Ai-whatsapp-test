from agents.master_agent import master_agent
from utils.types import Context
import os

os.environ["OPENAI_API_KEY"]
#os.environ["AWS_REGION"]
os.environ["AWS_ACCESS_KEY_ID"]
os.environ["AWS_SECRET_ACCESS_KEY"]
os.environ["AWS_SESSION_TOKEN"]
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

ended = True


while ended:
    user_message = input(">>(q for exit): ")
    if user_message == "q":
        ended = False
    else:
        context = Context(tenant_id="opal-clinic", user_id="+50373145544")
        response = master_agent.invoke(
            {"messages": [{"role": "user", "content": user_message}]},
            context=context,
            config={"configurable": {"thread_id": "+73145544"}},
        )
        print(response["messages"][-1].content)
