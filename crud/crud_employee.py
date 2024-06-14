from crud.base import CRUDBase
from models.Employee import MACH_Employee
from schemas.employee import EmployeeCreate


class CRUDEmployee(CRUDBase[MACH_Employee, EmployeeCreate]):
    ...


employee = CRUDEmployee(MACH_Employee)