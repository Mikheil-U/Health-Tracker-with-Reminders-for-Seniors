import sqlite3
from db_columns import DatabaseColumns


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

    def read_table_data(self, table_name: str):
        """
            Prints the entire data for the given table
        :param table_name: The name of a table
        :return:
        """
        query = f'''
            SELECT * FROM {table_name}
        '''
        try:
            self.__cursor.execute(query)
            rows = self.__cursor.fetchall()
            for row in rows:
                print(row)
        except sqlite3.Error as err:
            print(f"Error fetching data from table {table_name}")

    def get_patient_email(self, first_name: str, last_name: str):
        pass

    def get_doctor_info(self, first_name: str, last_name: str):
        pass

    def get_patient_appointment(self, patient_f_name: str, patient_l_name: str):
        pass


my_db = Database()
# print(my_db.create_table('Doctor', DOCTOR_COLUMNS))
# print(my_db.create_table('Patient', PATIENT_COLUMNS))
# print(my_db.create_table('Appointment', APPOINTMENT_COLUMNS))
# print(
#     my_db.insert_into_patient_table('Jessica', 'Doe', '01-27-1997', 'jessicadoe@yahoo.com', '214-123-4344', 'Dr. Nick'))
# print(my_db.insert_into_doctor_table('Nick', 'Wazowski', 'wazovskinick@gmail.com', '123-456-4343'))
my_db.read_table_data('Patient')
db_cols = DatabaseColumns()
print(my_db.create_table('Patient', db_cols.get_patient_columns()))
