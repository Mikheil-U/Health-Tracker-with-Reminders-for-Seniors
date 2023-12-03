from datetime import datetime, timedelta, date
import time
import email_reminders
from database.database_main import Database


# DOCTOR APPOINTMENTS

# To see if a reminder was sent already or not
sent_appointment_reminders = set()

# Check the database for upcoming appointments and send a reminder
def check_appointments(stop_event, email, first_name, last_name):
    my_db = Database()

    # While the stop event is not set from main.py
    while not stop_event.is_set():
        # If there are any appointments in the database, get them; if not, create an empty set
        if type(my_db.get_patient_appointments(first_name, last_name)) == str:
            appointments = set()
        else:
            appointments = my_db.get_patient_appointments(first_name, last_name)

        # Get the current time
        current_time = datetime.now()

        # Check all the appointments of the user
        for appointment in appointments:
            appointment_date_list = appointment[2].split('/')
            appointment_date = appointment_date_list[2] + "-" + appointment_date_list[0] + "-" + appointment_date_list[1]
            appointment_date_and_time = appointment_date + " " + appointment[3] + ":00"
            appointment_time = datetime.strptime(appointment_date_and_time, "%Y-%m-%d %H:%M:%S")
            appointment_id = f"appointment_{appointment[0]}_{appointment[1]}_{appointment_date_and_time}"

            # Check if the appointment time is within the next 60 minutes
            if current_time < appointment_time < current_time + timedelta(minutes=60) and appointment_id not in sent_appointment_reminders:
                doctor = appointment[0] + " " + appointment[1]
                send_appointment_reminder(email, doctor, appointment_date_and_time)
                sent_appointment_reminders.add(appointment_id)

        # Sleep for some time before checking again
        time.sleep(5)  # Sleep for 5 seconds


# Function that sends a reminder for an upcoming appointment
def send_appointment_reminder(recipient_email, doctor, appointment_time):
    subject = "Doctor Appointment Reminder"
    body = f"Reminder: Your appointment with {doctor} is scheduled for {appointment_time}."
    email_reminders.send_email(recipient_email, subject, body)


# ----------------------------------------------------------------------------------------------------------------------
# MEDICATIONS

# To see if a reminder was sent already or not
sent_medication_reminders = set()

# Check the database for upcoming medications and send a reminder
def check_medications(stop_event, email, first_name, last_name):
    my_db = Database()

    # While the stop event is not set from main.py
    while not stop_event.is_set():
        # If there are any medications in the database, get them; if not, create an empty set
        if type(my_db.get_patient_medications(first_name, last_name)) == str:
            medications = set()
        else:
            medications = my_db.get_patient_medications(first_name, last_name)

        # Get the current time
        current_time = datetime.now()

        # Check all the medications of the user
        for medication in medications:
            medication_date_and_time = str(date.today()) + " " + medication[1] + ":00"
            medication_time = datetime.strptime(medication_date_and_time, "%Y-%m-%d %H:%M:%S")
            medication_id = f"medication_{medication[0]}_{medication_date_and_time}"

            # Check if the time to take a medication is within the next 30 minutes
            if current_time < medication_time < current_time + timedelta(minutes=30) and medication_id not in sent_medication_reminders:
                medication_name = medication[0]
                send_medications_reminder(email, medication_name, medication_date_and_time)
                sent_medication_reminders.add(medication_id)

        # Sleep for some time before checking again
        time.sleep(5)  # Sleep for 5 seconds


# Function that sends a reminder for an upcoming appointment
def send_medications_reminder(recipient_email, medication_name, medication_date_and_time):
    subject = "Reminder to Take Your Medication"
    body = f"Reminder: Your medication {medication_name} is scheduled for {medication_date_and_time}."
    email_reminders.send_email(recipient_email, subject, body)