import sqlite3
from database.db_columns import DatabaseColumns


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

    def insert_into_health_history(self, first_name: str, last_name: str, weight: str, height: str, age: str, dob: str):
        query = f"""
            INSERT INTO Health_History(first_name, last_name, weight, height, age, dob)
            VALUES (?, ?, ?, ?, ?, ?) 
        """
        try:
            self.__cursor.execute(query, (first_name, last_name, weight, height, age, dob))
            self.__sql_connection.commit()
            return f"Data inserted into Health History table successfully!"
        except sqlite3.Error as err:
            return f"Error inserting data into Health History table: {err}"

    def insert_into_patient_table(self, first_name: str, last_name: str,
                                  email: str, phone_no: str):
        query = '''
                INSERT INTO Patient(first_name, last_name, email, phone_no)
                VALUES (?, ?, ?, ?)
            '''
        values = (first_name, last_name, email, phone_no)
        try:
            self.__cursor.execute(query, values)
            self.__sql_connection.commit()
            return f"Data inserted into Patient table successfully!"
        except sqlite3.Error as err:
            return f"Error inserting data into Patient table: {err}"

    def insert_into_medications(self, first_name: str, last_name: str, prescription_date: str, prescribed_meds: str):
        query = f"""
                    INSERT INTO Medications(first_name, last_name, prescription_date, prescribed_meds)
                    VALUES (?, ?, ?, ?) 
                """
        try:
            self.__cursor.execute(query, (first_name, last_name, prescription_date, prescribed_meds))
            self.__sql_connection.commit()
            return f"Data inserted into Medications table successfully!"
        except sqlite3.Error as err:
            return f"Error inserting data into Medications table: {err}"

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

    def update_patient_data(self, current_username: str, first_name: str, last_name: str, email: str):
        """This function is used to update patient's data after creating their account.
            During sign up we only ask for username and password
        """
        query = """
            UPDATE Patient
            SET first_name = ?, last_name = ?, email = ?
            WHERE user_name = ?
        """
        try:
            # execute the query
            self.__cursor.execute(query, (first_name, last_name, email, current_username))
            # save the changes
            self.__sql_connection.commit()
            if self.__cursor.rowcount > 0:
                return f"{current_username} information has been updated"
            else:
                return f"No such username: {current_username}"
        except sqlite3.Error as err:
            return f"An error occurred while updating patient's data: {err}"

    def assign_doctor(self, patient_first_name: str, patient_last_name: str,
                      doctor_first_name: str, doctor_last_name: str):
        """This function assigns doctor to a current patient.
            If doctor is found in Doctor table it's id will be saved in Patient's table in assigned_doctor_id as FK.
        """
        query = f"""SELECT doctor_id FROM Doctor 
            WHERE first_name = ? AND last_name = ?
            """
        try:
            self.__cursor.execute(query, (doctor_first_name, doctor_last_name))
            result = self.__cursor.fetchone()

            if result:
                doc_id = result[0]
                assign_query = f"""
                                UPDATE Patient SET assigned_doctor_id = ? 
                                WHERE first_name = ? AND last_name = ?"""
                self.__cursor.execute(assign_query, (doc_id, patient_first_name, patient_last_name))
                # save the changes
                self.__sql_connection.commit()
                if self.__cursor.rowcount > 0:
                    return "Doctor assigned to patient successfully."
                else:
                    return "No patient found with the given first name and last name."
            else:
                return f"Doctor with the given first name and last name couldn't be found"

        except sqlite3.Error as err:
            return f"An error occurred: {err}"

    def create_appointment(self, patient_first_name: str, patient_last_name: str,
                           app_date: str, app_time: str, doctor_f_name: str, doctor_l_name: str):
        query = f"""
            INSERT INTO Appointment(app_date, app_time, patient_first_name, patient_last_name, doctor_first_name, doctor_last_name)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            self.__cursor.execute(query, (app_date, app_time, patient_first_name, patient_last_name, doctor_f_name, doctor_l_name))
            self.__sql_connection.commit()
        except sqlite3.Error as err:
            return f"Error creating appointment: {err}"

    def get_patient_email(self, first_name: str, last_name: str):
        query = f"""
            SELECT email FROM Patient
            WHERE first_name = ? AND last_name = ?
        """
        try:
            self.__cursor.execute(query, (first_name, last_name))
            email = self.__cursor.fetchone()
            if email:
                return email[0]
            else:
                return f"Patient with the given first name and last name couldn't be found"
        except sqlite3.Error as err:
            return f"An error occurred: {err}"

    def get_patient_details(self, username: str, password: str):
        query = f"""
            SELECT email, first_name, last_name FROM Patient
            WHERE user_name = ? AND password = ?
        """
        try:
            self.__cursor.execute(query, (username, password))
            result = self.__cursor.fetchone()
            if result:
                return result
            else:
                return f"Patient with the given username and password couldn't be found"
        except sqlite3.Error as err:
            return f"An error occurred: {err}"

    def get_doctor_info(self, patient_first_name: str, patient_last_name: str):
        # Get the doctor's ID from the Patient table
        query = f"""
                SELECT doctor_id FROM Patient
                WHERE first_name = ? AND last_name = ?
            """
        try:
            self.__cursor.execute(query, (patient_first_name, patient_last_name))
            result = self.__cursor.fetchone()

            if result:
                doctor_id = result[0]
                # Get the doctor's data from the Doctror table
                query_doc = "SELECT * FROM Doctor WHERE doctor_id =?"
                self.__cursor.execute(query_doc, (doctor_id, ))
                doctor_data = self.__cursor.fetchone()

                if doctor_data:
                    return doctor_data
                else:
                    return f"Doctor not found"
            else:
                return "Patient not found"
        except sqlite3.Error as err:
            return f"An error occurred finding doctor's data: {err}"

    def get_patient_appointments(self, patient_first_name: str, patient_last_name: str):

        query = f"""
                        SELECT doctor_first_name, doctor_last_name, app_date, app_time FROM Appointment
                        WHERE patient_first_name = ? AND patient_last_name = ?
                    """
        try:
            self.__cursor.execute(query, (patient_first_name, patient_last_name))
            result = self.__cursor.fetchall()

            if result:
                return result
            else:
                return f"No appointmentsfound!"
        except sqlite3.Error as err:
            return f"An error occurred finding patient's appointment data: {err}"

    def get_patient_medications(self, first_name: str, last_name:str):
        query = f"""
                SELECT prescribed_meds, prescription_date FROM Medications
                WHERE first_name = ? AND last_name = ?
            """
        try:
            self.__cursor.execute(query, (first_name, last_name))
            result = self.__cursor.fetchall()

            if result:
                return result
            else:
                return f"Patient was not found!"
        except sqlite3.Error as err:
            return f"An error occurred fetching patient's medications : {err}"

    def get_patient_health_history(self, first_name: str, last_name: str):
        query = f"""
                SELECT * FROM Health_History
                WHERE first_name = ? AND last_name = ?
            """
        try:
            self.__cursor.execute(query, (first_name, last_name))
            result = self.__cursor.fetchone()
            if result:
                return result
            else:
                return f"No patient with the given first and last names"
        except sqlite3.Error as err:
            return f"Error fetching patient health history: {err}"

    def delete_medications_data(self, first_name: str, last_name: str, prescription_date: str, prescribed_meds:str):
        query = f"""
            DELETE FROM Medications 
            WHERE first_name = ? AND last_name = ? AND prescription_date = ? and prescribed_meds = ?
        """
        try:
            self.__cursor.execute(query, (first_name, last_name, prescription_date, prescribed_meds))
            # save the changes
            self.__sql_connection.commit()

            if self.__cursor.rowcount > 0:
                return f"Medication deleted successfully"
            else:
                return f"No medication found with the given information."
        except sqlite3.Error as err:
            return f"Error deleting medication data: {err}"

    def delete_appointment_data(self, patient_first_name: str, patient_last_name: str, app_date: str, app_time: str):
        query = f"""
                    DELETE FROM Appointment 
                    WHERE patient_first_name = ? AND patient_last_name = ? AND app_date = ? AND app_time = ?
                """
        try:
            self.__cursor.execute(query, (patient_first_name, patient_last_name, app_date, app_time))
            # save the changes
            self.__sql_connection.commit()

            if self.__cursor.rowcount > 0:
                return f"Appointment data deleted successfully"
            else:
                return f"No appointment found with the information."
        except sqlite3.Error as err:
            return f"Error deleting appointment data: {err}"

    def register_user(self, username: str, password: str):
        query = "INSERT INTO Patient(user_name, password) VALUES (?, ?)"
        values = (username, password)
        try:
            self.__cursor.execute(query, values)
            self.__sql_connection.commit()
            return f"You have successfully registered!"
        except sqlite3.Error as err:
            return f"Error creating an account: {err}"

    def authenticate(self, username: str, password: str) -> list[str]:
        """This function will check whether the user with the given username and password exist in a database"""
        query = "SELECT * FROM Patient WHERE user_name = ? AND password = ?"
        try:
            self.__cursor.execute(query, (username, password))
            # get one record
            result = self.__cursor.fetchone()
            # check if any record was found
            if result:
                return result[3:5]
            else:
                return []
        except sqlite3.Error as err:
            return ['Error occurred', err]


db_cols = DatabaseColumns()
my_db = Database()


def create_tables():
    """A helper function to initialize Database and create all tables"""
    print(my_db.create_table('Doctor', db_cols.get_doctor_columns()))
    print(my_db.create_table('Patient', db_cols.get_patient_columns()))
    print(my_db.create_table('Appointment', db_cols.get_appointment_columns()))
    print(my_db.create_table('Medications', db_cols.get_medications_columns()))
    print(my_db.create_table('Health_History', db_cols.get_health_info_columns()))


def populate_database():
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William",
                   "Elizabeth"]

    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez",
                  "Martinez"]
    doc_names = ['Jessica', 'Michael', 'Mary']
    doc_lnames = ['Smith', 'Doe', 'Miller']

    # populate Patient DB
    for i in range(len(first_names)):
        print(my_db.insert_into_patient_table(first_names[i], last_names[i],
                                              f'email{i}yahoo.com', f'{i}25-4{i}1-414{i}'))

    # populate Doctor DB
    for i in range(3):
        print(my_db.insert_into_doctor_table(doc_names[i], doc_lnames[i],
                                             f'{doc_names[i]}{doc_lnames}@gmail.com', f'215-4{i}3-{i}52{i}'))

    # Assign doctors to patients
    for i in range(len(first_names)):
        print(my_db.assign_doctor(first_names[i], last_names[i], doc_names[i], doc_lnames[i]))


def init_db():
    pass



