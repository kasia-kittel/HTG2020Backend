
#  covers only main user journeys


def test_request_availability_scheduled(client):
    # consumer request availability and professional schedules

    professional_id=3
    consumer_id=1

    # consumer issue request
    request = client.put(f"/appointments/request-availability/{professional_id}/{consumer_id}")
    request_id = request.get_json()["id"]

    assert request.status_code == 201
    assert request_id > 0

    # the request appears on request list for professional
    requests_list = client.get(f"/appointments/list-availability-requests/{professional_id}")
    requests_list_data = requests_list.get_json()

    assert requests_list.status_code == 200
    assert requests_list_data[0]["appointments_id"] == request_id

    # professional schedules appointment
    appointment_date_time = "2020-05-01 11:00:00"
    appointment_duration = 45
    schedule = client.post(f"/appointments/accept-availability-requests/{request_id}/{professional_id}",
                           data={'date-time': appointment_date_time , 'duration-min': appointment_duration})

    assert schedule.status_code == 202

    # the appointment appears on a list of scheduled appointments for consumer
    scheduled_appointments = client.get(f"/appointments/list-requested-scheduled/{consumer_id}")
    scheduled_appointments_data = scheduled_appointments.get_json()

    assert scheduled_appointments.status_code == 200
    assert len(scheduled_appointments_data)==1
    assert scheduled_appointments_data[0]["appointments_id"] == request_id
    assert scheduled_appointments_data[0]["professional_id"] == professional_id
    assert scheduled_appointments_data[0]["appointment_date"] == appointment_date_time
    assert scheduled_appointments_data[0]["appointment_duration"] == appointment_duration


def test_request_availability_rejected(client):
    # consumer request availability and professional rejects

    professional_id=5
    consumer_id=1

    # consumer issue request
    request = client.put(f"/appointments/request-availability/{professional_id}/{consumer_id}")
    request_id = request.get_json()["id"]

    assert request.status_code == 201
    assert request_id > 0

    # professional decline appointment
    decline = client.put(f"/appointments/decline-availability-requests/{request_id}/{professional_id}")

    assert decline.status_code == 202

    # the appointment appears on a list of declined appointments for consumer
    declined_appointments = client.get(f"/appointments/list-requested-declined/{consumer_id}")
    declined_appointments_data = declined_appointments.get_json()

    assert declined_appointments.status_code == 200
    assert len(declined_appointments_data)==1
    assert declined_appointments_data[0]["appointments_id"] == request_id
    assert declined_appointments_data[0]["professional_id"] == professional_id


def test_consumer_accepts_appointment(client):
    # consumer accepts scheduled appointment

    professional_id = 5
    consumer_id = 2

    # consumer issue request
    request = client.put(f"/appointments/request-availability/{professional_id}/{consumer_id}")
    request_id = request.get_json()["id"]

    assert request.status_code == 201
    assert request_id > 0

    # professional schedules appointment
    appointment_date_time = "2020-05-01 11:00:00"
    appointment_duration = 45
    schedule = client.post(f"/appointments/accept-availability-requests/{request_id}/{professional_id}",
                           data={'date-time': appointment_date_time , 'duration-min': appointment_duration})

    assert schedule.status_code == 202

    # consumer confirms scheduled time slot
    confirm = client.put(f"/appointments/accept-availability/{request_id}/{professional_id}/{consumer_id}")

    assert confirm.status_code == 202

    # appointment appears on a list of confirmed appointments for professional
    confirmed_appointments = client.get(f"/appointments/list-appointments-scheduled-and-confirmed/{professional_id}")
    confirmed_appointments_data = confirmed_appointments.get_json()

    assert confirmed_appointments.status_code == 200
    assert len(confirmed_appointments_data)==1
    assert confirmed_appointments_data[0]["appointments_id"] == request_id
    assert confirmed_appointments_data[0]["professional_id"] == professional_id
    assert confirmed_appointments_data[0]["consumer_id"] == consumer_id
    assert confirmed_appointments_data[0]["consumer_accepted"] != ""
    assert confirmed_appointments_data[0]["appointment_date"] == appointment_date_time
    assert confirmed_appointments_data[0]["appointment_duration"] == appointment_duration

def test_consumer_resign_form_appointment(client):
    # consumer resigns from scheduled appointment

    professional_id = 4
    consumer_id = 1

    # consumer issue request
    request = client.put(f"/appointments/request-availability/{professional_id}/{consumer_id}")
    request_id = request.get_json()["id"]

    assert request.status_code == 201
    assert request_id > 0

    # professional schedules appointment
    appointment_date_time = "2020-05-01 11:00:00"
    appointment_duration = 60
    schedule = client.post(f"/appointments/accept-availability-requests/{request_id}/{professional_id}",
                           data={'date-time': appointment_date_time , 'duration-min': appointment_duration})

    assert schedule.status_code == 202

    # consumer resigns from the scheduled time slot
    confirm = client.put(f"/appointments/reject-availability/{request_id}/{professional_id}/{consumer_id}")

    assert confirm.status_code == 202


    # appointment appears on a list of confirmed appointments for professional
    rejected_appointments = client.get(f"/appointments/list-appointments-scheduled-and-rejected/{professional_id}")
    rejected_appointments_data = rejected_appointments.get_json()

    assert rejected_appointments.status_code == 200
    assert len(rejected_appointments_data)==1
    assert rejected_appointments_data[0]["appointments_id"] == request_id
    assert rejected_appointments_data[0]["professional_id"] == professional_id
    assert rejected_appointments_data[0]["consumer_id"] == consumer_id
    assert rejected_appointments_data[0]["consumer_resigned"] != ""
