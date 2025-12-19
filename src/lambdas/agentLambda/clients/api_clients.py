import requests


def fetch_clinic_context():
    res = requests.get(
        "https://ts0g4u3nu2.execute-api.us-east-1.amazonaws.com/prod/clinic?phoneNumberIndexId=762197213646084"
    ).json()
    print(res)
    return res["body"]


def fetch_doctors_info():
    res = requests.get(
        "https://ts0g4u3nu2.execute-api.us-east-1.amazonaws.com/prod/clinic/doctors?tenantId=opal-clinic"
    ).json()
    print(res)
    return res["body"]


def fetch_post_appointments_api(
    tenant_id: str,
    user_id: str,
    doctor_id: str,
    start_iso,
    duration_minutes: int,
    patient_name: str,
):
    payload = {
        "tenantId": tenant_id,
        "userId": user_id,
        "doctorId": doctor_id,
        "startIso": start_iso,
        "durationMinutes": duration_minutes,
        "patientName": patient_name,
    }
    print(payload)
    res = requests.post(
        "https://ts0g4u3nu2.execute-api.us-east-1.amazonaws.com/prod/appointments",
        data=payload,
    ).json()
    print(res)
    return res["body"]


def fetch_get_appointments_by_doctor_id_api(tenant_id: str, doctor_id: str, date: str):
    res = requests.get(
        f"https://ts0g4u3nu2.execute-api.us-east-1.amazonaws.com/prod/appointments/availability?tenantId={tenant_id}&doctorId={doctor_id}&date={date}"
    ).json()
    print(res)
    return res["body"]


def fetch_patch_appointments_by_appointment_id(
    appointment_id: str, new_start_date: str, new_end_date: str, tenant_id: str
):
    payload = {
        "tenantId": tenant_id,
        "newStartIso": new_start_date,
        "newEndIso": new_end_date,
    }
    print(payload)
    res = requests.patch(
        f"https://ts0g4u3nu2.execute-api.us-east-1.amazonaws.com/prod/appointments/{appointment_id}",
        data=payload,
    ).json()
    print(res)
    return res["body"]


# `tenantId`, `userId`, `doctorId`, `startIso` + `endIso | durationMinutes`
