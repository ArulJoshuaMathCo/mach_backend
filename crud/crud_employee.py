from crud.base import CRUDBase
from models.Employee import MACH_Employee
from schemas.employee import EmployeeCreate,EmployeeUpdate


class CRUDEmployee(CRUDBase[MACH_Employee, EmployeeCreate,EmployeeUpdate]):
    ...


employee = CRUDEmployee(MACH_Employee)