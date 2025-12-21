from agentLambda.agents.master_agent import master_agent


from agentLambda.utils.types import Context
import os

# os.environ["OPENAI_API_KEY"]
# os.environ["AWS_REGION"]
# os.environ["AWS_ACCESS_KEY_ID"]
# os.environ["AWS_SECRET_ACCESS_KEY"]
# os.environ["AWS_SESSION_TOKEN"]
# os.environ["AWS_DEFAULT_REGION"] 

ended = True

def handler(event, context):
    print('lambda event')
    print(event)
    print('lambda context')
    print(context)

def invoke_handler():
    while ended:
        user_message = 'Hola! Me llamo Oscar'
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
