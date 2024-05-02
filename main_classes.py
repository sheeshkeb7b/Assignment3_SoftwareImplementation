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


class Person:
    def __init__(self, name, DOB, passport, age):
        self._name = name
        self._DOB = DOB
        self._passport = passport
        self._age = age

class Employee(Person):
    def __init__(self, name, DOB, passport, age, employee_ID, basic_salary, department, job_title, manager_ID=None):
        super().__init__(name, DOB, passport, age)
        self._employee_ID = employee_ID
        self._basic_salary = basic_salary
        self._department = department
        self._job_title = job_title
        self._manager_ID = manager_ID
        self._employee_list = []

        # Assigns a manager ID if the employee job title is not manager (managers would not have the attribute as None)
        if self._job_title in (EmployeeType.SALES_MANAGERS, EmployeeType.MARKETING_MANAGERS):
            self._manager_ID = None


    # Getter and setter methods for manager ID
    def get_manager_ID(self):
        return self._manager_ID

    def set_manager_ID(self, manager_ID):
        self._manager_ID = manager_ID



