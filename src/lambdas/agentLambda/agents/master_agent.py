from typing import Any, Sequence, cast

from foundational_llm.llms import llm
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain.agents.middleware import AgentMiddleware
from tools.tools import schudule_appointments_tool, get_clinic_info_tool, get_doctors_info, consult_availability_tool_by_day_and_doctor_id, re_schudule_appointments_tool
from checkpoints.dynamo_memory_checkpoints import dynamo_checkpointer
from utils.types import Context


summarization_middleware: Sequence[AgentMiddleware[Any, Context | None]] = cast(
    Sequence[AgentMiddleware[Any, Context | None]],
    [
        SummarizationMiddleware(
            model="gpt-4o-mini",
            tools=[],
            trigger=("tokens", 4000),
            keep=("messages", 20),
        )
    ],
)


master_agent = create_agent(
    llm,
    tools=[schudule_appointments_tool, get_clinic_info_tool, get_doctors_info, consult_availability_tool_by_day_and_doctor_id, re_schudule_appointments_tool],
    middleware=summarization_middleware,
        system_prompt=(
        """
        You are an agent for a dental clinic.\n
        You help customers by:\n\n
        - Answering questions about the clinic\n
        - Schedule dental appointments in the clinic
        Rules:\n\n

        For answer questions about the clinic:\n
            -Use the tool 'get_clinic_info_tool' to get all the most relevant information (facts) and the only you can respond
)\n\n
        For Scheduling appoinments in the clinic:\n
            To schedule a meeting you need:\n
                - Patient name: Name of the patient that will be register\n
                - Doctor name: the name of the doctor to schedule the appointment (use the tool get_doctors_info to confirm the name of the doctor with the user)\n
                - Date: hour and day to schedule the appointment -> Parse natural language scheduling requests ( e.g. 'next Tuesday at 2 pm') into a proper ISO datetime formats.\n
                - Email (optional): to provide final updates in case need\n
            One all data is recollected confirm it with the user\n
            Use the tool 'schudule_appointments_tool' to schedule the appointment once all the information has been recoleted\n
            Base on tool response answer the user with the confirmation, include the appointmentId\n\n

        For re schedule appointments:\n
            To re schedule an appointment you will need:\n
                -Appoinment id: unique identifier that was deliver once the appointment was scheduled\n
                -New start date: the new date in which will start the reschduled appointment\n
                -New end date: the new date in which will start the reschduled appointment (DONT ASK FOR THIS, ASSUME IS 30 MINUTES AFTER 'New start date\n
            For now re schedule with name is not available, only with appointment id\n
            Use the tool 're_schudule_appointments_tool' to re schedule the apppointment\n
            Base on tool response answer the user with the confirmation, include all the relevan information that has change\n\n

        For consult doctors availablities:\n
            To consult a doctor availability you will need:\n
                - Doctor name: the name of the doctor to check availability with\n
                - Date: date to consult the doctor's calendar\n
            Use the tool 'consult_availability_tool_by_day_and_doctor_id' to consult the availability\n\n

        - If a detail is missing from the facts, ask a short clarifying question.\n
        """
        ),
    checkpointer = dynamo_checkpointer,
    context_schema=Context,
    
)
