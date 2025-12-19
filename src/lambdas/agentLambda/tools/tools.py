from langchain.tools import tool, ToolRuntime
from pydantic import BaseModel, Field
from clients.api_clients import (
    fetch_clinic_context,
    fetch_doctors_info,
    fetch_post_appointments_api,
    fetch_get_appointments_by_doctor_id_api,
    fetch_patch_appointments_by_appointment_id
)
from typing import Annotated
from utils.types import Context


class schedule_apointment_input(BaseModel):
    """Inputs fot schedule appointment."""

    doctor_id: str = Field(description="doctorId of the doctor to schedule with")
    apointment_date: str = Field(
        description="Date when the appointment will be schedule"
    )
    patient_name: str = Field(
        description="Name of the patient to schedule the appointment"
    )


@tool(
    description="Use this when the user wants to create calendar appointments.",
    args_schema=schedule_apointment_input,
)
def schudule_appointments_tool(
    runtime: ToolRuntime[Context],
    doctor_id: str,
    apointment_date: str,
    patient_name: str,
    duration_minutes: int = 30,
) -> dict:
    """
    Use this when the user wants to create calendar appointments.
    """
    tenant_id = runtime.context.tenant_id
    user_id = runtime.context.user_id

    res = fetch_post_appointments_api(
        tenant_id, user_id, doctor_id, apointment_date, duration_minutes, patient_name
    )
    print(
        f"This will schedule a metting with -> {user_id} and {tenant_id} pass it though the context it will last {duration_minutes}"
    )
    return res


class re_schedule_apointment_input(BaseModel):
    """Inputs fot re schedule appointment."""

    new_start: str = Field(
        description="New start date re schedule the appointment in ISO format"
    )
    new_end: str = Field(
        description="New end date to re schedule the appointment in ISO format"
    )
    apointment_date: str = Field(
        description="Unique identifier that was deliver once the appointment was scheduled"
    )


@tool(
    description="Use this tool when you need to re schedule an event",
    args_schema=re_schedule_apointment_input,
)
def re_schudule_appointments_tool(
    runtime: ToolRuntime[Context],
    new_start: str,
    new_end:str,
    appointment_id: str,
) -> dict:
    """
    Use this tool when you need to re schedule an event
    """
    tenant_id = runtime.context.tenant_id

    res= fetch_patch_appointments_by_appointment_id(appointment_id, new_start, new_end, tenant_id)
    return {"sucess": res}


class delete_apointment_input(BaseModel):
    """Inputs fot schedule appointmen."""

    doctor_id: str = Field(description="doctorId of the doctor to schedule with")
    apointment_date: str = Field(
        description="Date when the appointment will be schedule"
    )
    patient_name: str = Field(
        description="Name of the patient to schedule the appointment"
    )


@tool(
    description="Use this tool when you are sure you need to delete an appointment",
    args_schema=schedule_apointment_input,
)
def delete_appointments_tool(
    runtime: ToolRuntime[Context],
    doctor_id: str,
    apointment_date: str,
    patient_name: str,
    duration_minutes: int = 30,
) -> dict:
    """
    Use this tool when you are sure you need to delete an appointment
    """
    tenant_id = runtime.context.tenant_id
    user_id = runtime.context.user_id

    fetch_post_appointments_api(
        tenant_id, user_id, doctor_id, apointment_date, duration_minutes, patient_name
    )
    print(
        f"This will schedule a metting with -> {user_id} and {tenant_id} pass it though the context it will last {duration_minutes}"
    )
    res = f"Metting scheluded with for context {doctor_id} at {apointment_date}"
    return {"sucess": res}


#######################################
class consult_availability_tool_by_day_and_doctor_id_input(BaseModel):
    """Inputs for consult the availability by day and doctor_id appointmen."""

    doctor_id: str = Field(description="doctorId of the doctor fot consult with")
    appointment_date: str = Field(
        description="Date to consult doctor availability, only accepts formats: '2024-06-15' -> 'YYYY-MM-DD'"
    )


@tool(
    description="Use this tool when you need to consult the availability of a doctor in a specific date in the calendar",
    args_schema=consult_availability_tool_by_day_and_doctor_id_input,
)
def consult_availability_tool_by_day_and_doctor_id(
    runtime: ToolRuntime[Context], doctor_id: str, appointment_date: str
) -> dict:
    """
    Use this tool when you need to consult the availability of a doctor in a specific date in the calendar, it returns an array with all the calendar events for that specific doctor
    """
    print(f"Cheching Availability for doctor {doctor_id} on {appointment_date}\n")
    tenant_id = runtime.context.tenant_id
    res = fetch_get_appointments_by_doctor_id_api(
        tenant_id, doctor_id, appointment_date
    )
    print(f"Availability for doctor {doctor_id} on {appointment_date}")

    print(res)
    return res


#############################################


@tool(
    description="Use this tool when you need to schedule an event",
    args_schema=schedule_apointment_input,
)
def check_availability_appointment_tool(
    doctor_name: str, doctor_id: str, schedule_date: str
) -> dict:
    """
    Use this when the user wants to create calendar appointments.
    """

    print({"dodctorId": doctor_id, "schedule": schedule_date})
    res = f"Metting scheluded with doctor: ${doctor_name} at ${schedule_date}"
    return {"sucess": res}


@tool(description="Use this tool to get the information about the clinic")
def get_clinic_info_tool() -> dict:
    """
    Use this when the user wants to create calendar appointments.
    """
    res = fetch_clinic_context()
    return res


@tool(
    description="Use this tool when you need information about the doctors for schedule appointments"
)
def get_doctors_info():
    res = fetch_doctors_info()
    return res
