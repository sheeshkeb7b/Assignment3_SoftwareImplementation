import pickle
from enum import Enum


class EmployeeType(Enum):
    SALES_MANAGERS = "Sales Managers"
    SALESPERSON = "Salesperson"
    MARKETING_MANAGERS = "Marketing Managers"
    MARKETERS = "Marketers"
    ACCOUNTANTS = "Accountants"
    DESIGNERS = "Designers"
    HANDYMEN = "Handymen"


class EmployeeDepartment(Enum):
    SALES = "Sales"
    MARKETING = "Marketing"
    ACCOUNTING = "Accounting"
    DESIGNERS = "Designers"
    FACILITIES_MANAGEMENT = "Facilities Management"

class EventType(Enum):
    WEDDINGS = "Weddings"
    BIRTHDAYS = "Birthdays"
    THEMED_PARTIES = "Themed Parties"
    GRADUATIONS = "Graduations"

class SupplierType(Enum):
    CATERING = "Catering"
    CLEANING =  "Cleaning"
    FURNITURE = "Furniture"
    DECORATIONS = "Decorations"
    ENTERTAINMENT = "Entertainment"

class Person:
    def __init__(self, name):
        self._name = name

    def display(self):
        print(f"Name: {self._name}")

class Employee(Person):
    def __init__(self, employee_ID, name, department, job_title, basic_salary, manager_ID=None):
        super().__init__(name)
        self._employee_ID = employee_ID
        self._basic_salary = basic_salary
        self._department = department
        self._job_title = job_title
        self._manager_ID = manager_ID
        self._employee_list = []

        # Assigns a manager ID if the employee job title is not manager (managers would not have the attribute as None)
        if self._job_title not in (EmployeeType.SALES_MANAGERS, EmployeeType.MARKETING_MANAGERS):
            self._manager_ID = None

    def get_id(self):
        return self._employee_ID

    def get_name(self):
        return self._name

    def get_department(self):
        return self._department

    def get_job_title(self):
        return self._job_title

    def get_salary(self):
        return self._basic_salary

    def get_manager_id(self):
        return self._manager_ID


    def display(self):
        print("---" * 10, "Employee", "---" * 10)
        super().display()
        print(f"Employee ID: {self._employee_ID}")
        print(f"Basic Salary: {self._basic_salary}")
        print(f"Department: {self._department}")
        print(f"Job Title: {self._job_title}")
        print(f"Manager ID: {self._manager_ID}")

    # Getter and setter methods for manager ID
    def get_manager_ID(self):
        return self._manager_ID

    def set_manager_ID(self, manager_ID):
        self._manager_ID = manager_ID

    # Methods to be used in the system
    def add_employee(self):
        "This method adds an employee to the employee_list"
        pass # This is implemented in the GUI

    def delete_employee(self):
        "This method removes an existing employee from the employee_list"
        pass # This is implemented in the GUI

    def modify_employee(self):
        "This method updates an existing employee's attributes"
        pass # This is implemented in the GUI



class Client(Person):
    def __init__(self, name, client_id, address, contact_details, budget):
        super().__init__(name)
        self._client_id = client_id
        self._address = address
        self._contact_details = contact_details
        self._budget = budget

    def display(self):
        print("---" * 10, "Client", "---" * 10)
        super().display()
        print(f"Client ID: {self._client_id}")
        print(f"Address: {self._address}")
        print(f"Contact Details: {self._contact_details}")
        print(f"Budget: {self._budget}")


    # Methods to be used in the system
    def add_clients(self):
        "This method adds a client to the client list"
        pass  # This is implemented in the GUI

    def delete_client(self):
        "This method removes an existing client from the client_list"
        pass  # This is implemented in the GUI

    def modify_client(self):
        "This method updates an existing client's attributes"
        pass  # This is implemented in the GUI

class Guest(Person):
    def __init__(self, name, guest_id, contact_details):
        super().__init__(name)
        self._guest_ID = guest_id
        self._contact_details = contact_details

    def display(self):
        print("---" * 10, "Guest", "---" * 10)
        super().display()
        print(f"Guest ID: {self._guest_ID}")
        print(f"Contact Details: {self._contact_details}")


    # Methods to be used in the system
    def add_guests(self):
        "This method adds a guest to a guest list (which will then be added to an event's guest list)"
        pass  # This is implemented in the GUI

    def delete_guest(self):
        "This method removes an existing guest from a guest list"
        pass  # This is implemented in the GUI

    def modify_guest(self):
        "This method updates an existing client's attributes"
        pass  # This is implemented in the GUI

class Venue:
    def __init__(self, venue_id, name, address, contact_details, min_guests, max_guests):
        self._venue_id = venue_id
        self._name = name
        self._address = address
        self._contact_details = contact_details
        self._min_guests = min_guests
        self._max_guests = max_guests

    def display(self):
        print("---" * 10, "Venue", "---" * 10)
        print("Venue ID:", self._venue_id)
        print("Name:", self._name)
        print("Address:", self._address)
        print("Contact Details:", self._contact_details)
        print("Minimum Guests:", self._min_guests)
        print("Maximum Guests:", self._max_guests)


    # Methods to be used in the system
    def add_venue(self):
        "This method adds a venue to the venue list"
        pass  # This is implemented in the GUI

    def delete_venue(self):
        "This method removes an existing venue from the venue list"
        pass  # This is implemented in the GUI

    def modify_venue(self):
        "This method updates an existing venue's attributes"
        pass  # This is implemented in the GUI

class Supplier:
    def __init__(self, supplier_id, name, contact_details, service_type):
        self._supplier_id = supplier_id
        self._name = name
        self._contact_details = contact_details
        self._service_type = service_type



    def display(self):
        print("---" * 10, "Supplier", "---" * 10)
        print("Supplier ID:", self._supplier_id)
        print("Name:", self._name)
        print("Contact Details:", self._contact_details)
        print("Service Type:", self._service_type)

    # Methods to be used in the system
    def add_supplier(self):
        "This method adds a supplier to the supplier list"
        pass  # This is implemented in the GUI

    def delete_supplier(self):
        "This method removes an existing supplier from the supplier list"
        pass  # This is implemented in the GUI

    def modify_supplier(self):
        "This method updates an existing supplier's attributes"
        pass  # This is implemented in the GUI

class Event:
    def __init__(self, event_id, type: EventType, theme, date, time, duration, venue, client_id, suppliers,
                 guest_list, invoice):

        self._event_id = event_id
        self._type = type
        self._theme = theme
        self._date = date
        self._time = time
        self._duration = duration
        self._venue = venue
        self._client_id = client_id
        self._suppliers = suppliers
        self._guest_list = guest_list
        self._invoice = invoice

    def display(self):
        print("---" * 10, "Event", "---" * 10)
        print("Event ID:", self._event_id)
        print("Type:", self._type)
        print("Theme:", self._theme)
        print("Date:", self._date)
        print("Time:", self._time)
        print("Duration:", self._duration)
        print("Venue:", self._venue)
        print("Client ID:", self._client_id)
        print("Suppliers:", self._suppliers)
        print("Guest List:", self._guest_list)
        print("Invoice:", self._invoice)


    # Methods to be used in the system
    def add_event(self):
        "This method adds a event to the event list"
        pass  # This is implemented in the GUI

    def delete_event(self):
        "This method removes an existing event from the event list"
        pass  # This is implemented in the GUI

    def modify_event(self):
        "This method updates an existing event's attributes"
        pass  # This is implemented in the GUI

# Functions to save and load data using pickle
def load_data(file_path):
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("File not found. Initializing new data.")
        return {}

def save_data(data, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)