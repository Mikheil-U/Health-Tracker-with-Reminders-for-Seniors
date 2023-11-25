from datetime import datetime, timedelta
import time
import email_reminders


# DOCTOR APPOINTMENTS

sent_appointment_reminders = set()

# Check the database for upcoming appointments and send a reminder
def check_appointments(stop_event):
    while not stop_event.is_set():
        # TODO - open db and store appointments table in a list of lists maybe?
        appointments = [["kaliashvililasha@gmail.com", "Dr. XX XXX", "2023-11-25 16:15:00"]]

        current_time = datetime.now()

        for appointment in appointments:
            appointment_time = datetime.strptime(appointment[2], "%Y-%m-%d %H:%M:%S")
            appointment_id = f"appointment_{appointment[0]}_{appointment[1]}_{appointment[2]}"

            # Check if the appointment time is within the next 60 minutes
            if current_time < appointment_time < current_time + timedelta(minutes=60) and appointment_id not in sent_appointment_reminders:
                send_appointment_reminder(appointment)
                sent_appointment_reminders.add(appointment_id)

        # Sleep for some time before checking again
        time.sleep(1)  # Sleep for 1 minute


# Function that sends a reminder for an upcoming appointment
def send_appointment_reminder(appointment):
    recipient_email = appointment[0]
    subject = "Doctor Appointment Reminder"
    body = f"Reminder: Your appointment with '{appointment[1]}' is scheduled for {appointment[2]}."
    email_reminders.send_email(recipient_email, subject, body)


# ----------------------------------------------------------------------------------------------------------------------
# MEDICATIONS

sent_medication_reminders = set()

# Check the database for upcoming medications and send a reminder
def check_medications(stop_event):
    while not stop_event.is_set():
        # TODO - open db and store medications table in a list of lists
        medications = [["kaliashvililasha@gmail.com", "Nebivolol", "2023-11-25 16:15:00"]]

        current_time = datetime.now()

        for medication in medications:
            medication_time = datetime.strptime(medication[2], "%Y-%m-%d %H:%M:%S")
            medication_id = f"medication_{medication[0]}_{medication[1]}_{medication[2]}"

            # Check if the time to take a medication is within the next 15 minutes
            if current_time < medication_time < current_time + timedelta(minutes=15) and medication_id not in sent_medication_reminders:
                send_medications_reminder(medication)
                sent_medication_reminders.add(medication_id)

        # Sleep for some time before checking again
        time.sleep(1)  # Sleep for 1 minute


# Function that sends a reminder for an upcoming appointment
def send_medications_reminder(medication):
    recipient_email = medication[0]
    subject = "Reminder to Take Your Medication"
    body = f"Reminder: Your medication '{medication[1]}' is scheduled for {medication[2]}."
    email_reminders.send_email(recipient_email, subject, body)