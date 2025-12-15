from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain.agents.middleware import dynamic_prompt, ModelRequest
import os
clinic_facts = {
   "clinic_name":"Opal clinica",
   "phone":"73145544",
   "address": "1st avenue of not here",
   "availability":"8am to 5pm, moday to friday"
}

os.environ["OPENAI_API_KEY"]
llm = init_chat_model("gpt-4.1", temperature=0.7)

calendar_agent = create_agent(
    llm,
    tools=[],
    system_prompt="""
    You are a calendar scheduling assistant
    Parse natural language scheduling requests ( e.g. 'next Tuesday at 2 pm') into a proper ISO datetime formats.
    Use get_available_time_slots to check availability when neede
    Use create_calendar_events to schedule events
    always confirm what was schediling in you final response
    """,
)

def fetch_clinic_context():
    #fetch real data from dynamo, create endpoint
    return clinic_facts


@tool(description="Use this tool when you need to schedule an event")
def apponitment_tool(request: str) -> str:
    """
    Use this when the user wants to create, modify, or check calendar appointments.
    Handles date/time parsing, availability checking, and event creation.

    Input: Natural language scheduling request (e.g., 'meeting with design team
    next Tuesday at 2pm')
    """
    result = calendar_agent.invoke({
        "messages":[{"role": "user", "content":request}]
    })

    print("this is the log")
    return result["messages"][-1].text

@dynamic_prompt
def buil_prompt(request:ModelRequest) -> str:
    clinic = fetch_clinic_context()
    clinic_block = (
        "Authoritative clinic facts (use exactly as written):\n"
        f"- Clinic name: {clinic.get('clinic_name', 'N/A')}\n"
        f"- Phone: {clinic.get('phone', 'N/A')}\n"
        f"- Address: {clinic.get('address', 'N/A')}\n"
        f"- Availablity : { clinic.get('availability', 'N/A')}"
    )

    prompt = (
        "You are an agent for a dental clinic.\n"
        "You help customers by:\n"
        "- Answering questions about the clinic\n"
        "- Scheduling appointments\n"
        "- Routing the request to a real agent when needed\n\n"
        "Rules:\n"
        "- If the user asks for clinic details (name/phone/address), answer using the clinic facts.\n"
        "Break down user requests into appropriate tool calls and coordinate the results.\n" 
        "When a request involves multiple actions, use multiple tools in sequence\n"
        "- If a detail is missing from the facts, ask a short clarifying question.\n\n"
        f"{clinic_block}"
    )

    return prompt


classifier_agent = create_agent(
    llm,
    tools=[apponitment_tool],
    middleware=[buil_prompt]
)

output_parser = StrOutputParser()

ended = True

while ended:
    user_message = input(">>(q for exit): ")
    if user_message == "q":
        ended = False
    else:
        # print(f'user Message: ${user_message}')
        # chain = prompt | llm | output_parser
        response = classifier_agent.invoke(
            {"messages": [{"role": "user", "content": user_message}]}
        )
        print(response["messages"][-1].content)
