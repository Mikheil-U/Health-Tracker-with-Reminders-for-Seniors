

class DatabaseColumns:

    def __init__(self):
        self.patient_col = None
        self.doctor_col = None
        self.appointment_col = None
        self.health_info_col = None
        self.medications_col = None

    def get_doctor_columns(self) -> list[str]:
        # This list is used to create a doctor table, the list will be passed as an argument to create_table()
        self.doctor_col = [
            "doctor_id INTEGER PRIMARY KEY",
            "first_name TEXT NOT NULL",
            "last_name TEXT NOT NULL",
            "email TEXT",
            "phone_no TEXT",
        ]
        return self.doctor_col

    def get_patient_columns(self) -> list[str]:
        # This list is used to create a patient table, the list will be passed as an argument to create_table()
        self.patient_col = [
            "patient_id INTEGER PRIMARY KEY",
            "first_name TEXT",
            "last_name TEXT",
            "user_name TEXT",
            "password TEXT",
            "email TEXT",
            "phone_no TEXT",
            "assigned_doctor_id TEXT",
            "FOREIGN KEY(assigned_doctor_id) REFERENCES Doctor(doctor_id)"
        ]
        return self.patient_col

    def get_appointment_columns(self) -> list[str]:
        # This list is used to create an appointment table, the list will be passed as an argument to create_table()
        self.appointment_col = [
            "id INTEGER PRIMARY KEY",
            "description TEXT",
            "app_date TEXT",
            "app_time TEXT",
            "patient_first_name TEXT",
            "patient_last_name TEXT",
            "doctor_first_name TEXT",
            "doctor_last_name TEXT",
        ]
        return self.appointment_col

    def get_medications_columns(self) -> list[str]:
        self.medications_col = [
            "id INTEGER PRIMARY KEY",
            "first_name TEXT",
            "last_name TEXT",
            "prescription_date TEXT",
            "prescribed_meds TEXT",
        ]
        return self.medications_col

    def get_health_info_columns(self) -> list[str]:
        self.health_info_col = [
            "first_name TEXT",
            "last_name TEXT",
            "weight TEXT",
            "height TEXT",
            "age TEXT",
            "dob TEXT"
        ]
        return self.health_info_col





