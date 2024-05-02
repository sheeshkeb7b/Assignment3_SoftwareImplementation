# Testing the program
# Exception Handling
from main_classes import *
from pickle import *


person1 = Person("Kendall Roy", "1980-12-18", "HFIEWUH213", 43)
employee1 = Employee(person1, person1, person1, person1, 436121, 53000, EmployeeDepartment.SALES, EmployeeType.SALES_MANAGERS)

person2 = Person("Alan Thompson", "2001-04-21", "AA3RDF21", 23)
employee2 = Employee(person2, person2, person2, person2, 112314, 18000, EmployeeDepartment.SALES, EmployeeType.SALESPERSON, employee1._employee_ID)

person3 = Person("Shyam Sundar", "1997-02-10", "XG35GA1A",26 )
employee3 = Employee(person3, person3, person3, person3, "11234", 20000, EmployeeDepartment.SALES, EmployeeType.SALESPERSON, employee1._employee_ID)

person4 = Person("Joy Rogers", "1984-09-04", "SV421GS42", 40)
employee4 = Employee(person4, person4, person4, person4, 81774,24000, EmployeeDepartment.MARKETING, EmployeeType.MARKETING_MANAGERS)

person5 = Person("Salma J Sam", "2004-12-01", "PP41CGDS1", 19)
employee5 = Employee(person5, person5, person5, person5, 98637,8000, EmployeeDepartment.FACILITIES_MANAGEMENT, EmployeeType.HANDYMEN)

