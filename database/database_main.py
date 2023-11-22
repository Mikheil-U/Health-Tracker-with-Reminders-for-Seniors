import sqlite3

# This list is used to create a doctor table, the list will be passed as an argument to create_table()
DOCTOR_COLUMNS = [
    "doctor_id INTEGER PRIMARY KEY",
    "first_name TEXT NOT NULL",
    "last_name TEXT NOT NULL",
    "email TEXT",
    "phone_no TEXT",

]
# This list is used to create a patient table, the list will be passed as an argument to create_table()
PATIENT_COLUMNS = [
    "patient_id INTEGER PRIMARY KEY",
    "first_name TEXT NOT NULL",
    "last_name TEXT NOT NULL",
    "dob TEXT NOT NULL",
    "email TEXT",
    "phone_no TEXT",
    "assigned_doctor TEXT",
    "FOREIGN KEY(assigned_doctor) REFERENCES Doctor(doctor_id)"
]
# This list is used to create an appointment table, the list will be passed as an argument to create_table()
APPOINTMENT_COLUMNS = [
    "id INTEGER PRIMARY KEY",
    "description TEXT"
    "app_date TEXT",
    "doctor_id INT",
    "patient_id INT",
    "FOREIGN KEY(doctor_id) REFERENCES Doctor(doctor_id)",
    "FOREIGN KEY(patient_id) REFERENCES Patient(patient_id)"
]


class Database:

    def __init__(self):
        self.__sql_connection = sqlite3.connect('hospital.db')
        self.__cursor = self.__sql_connection.cursor()

    def create_table(self, table_name: str, columns: list[str]):
        """
        To create a SqLite table
        :param table_name: A name of a table we are creating
        :param columns: Columns names for table we are creating
        :return: None
        """
        query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})
            '''
        try:
            self.__cursor.execute(query)
            self.__sql_connection.commit()
            return f"Success! {table_name} has been created"
        except sqlite3.Error as err:
            return f"Error creating table: {table_name}: {err}"

    def insert_into_patient_table(self, first_name: str, last_name: str, dob: str,
                                  email: str, phone_no: str, assigned_doctor: str):
        query = '''
                INSERT INTO Patient(first_name, last_name, dob, email, phone_no, assigned_doctor)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
        values = (first_name, last_name, dob, email, phone_no, assigned_doctor)
        try:
            self.__cursor.execute(query, values)
            self.__sql_connection.commit()
            return f"Data inserted into Patient table successfully!"
        except sqlite3.Error as err:
            return f"Error inserting data into Patient table: {err}"

    def insert_into_doctor_table(self, first_name: str, last_name: str,
                                 email: str, phone_no: str, ):
        query = '''
            INSERT INTO Doctor(first_name, last_name, email, phone_no)
            VALUES (?, ?, ?, ?)
        '''
        values = (first_name, last_name, email, phone_no)
        try:
            self.__cursor.execute(query, values)
            self.__sql_connection.commit()
            return f"Data inserted into Doctor table successfully!"
        except sqlite3.Error as err:
            return f"Error inserting data into Doctor table: {err}"

    def insert_into_appointment_table(self, description: str, doctor_id: str,
                                      patient_id: str):
        query = '''
            INSERT INTO Doctor(description, doctor_id, patient_id)
            VALUES (?, ?, ?, ?)
        '''
        values = (description, doctor_id, patient_id)
        try:
            self.__cursor.execute(query, values)
            self.__sql_connection.commit()
            return f"Data inserted into Appointment table successfully!"
        except sqlite3.Error as err:
            return f"Error inserting data into Appointment table: {err}"


my_db = Database()
# print(my_db.create_table('Doctor', DOCTOR_COLUMNS))
# print(my_db.create_table('Patient', PATIENT_COLUMNS))
# print(my_db.create_table('Appointment', APPOINTMENT_COLUMNS))
# print(
#     my_db.insert_into_patient_table('Jessica', 'Doe', '01-27-1997', 'jessicadoe@yahoo.com', '214-123-4344', 'Dr. Nick'))
print(my_db.insert_into_doctor_table('Nick', 'Wazowski', 'wazovskinick@gmail.com', '123-456-4343'))
