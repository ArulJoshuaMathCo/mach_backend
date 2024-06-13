from crud.base import CRUDBase
from models.skills import Skills1
from schemas.skills import SkillsBase


class CRUDSkills(CRUDBase[Skills1, SkillsBase]):
    ...


skills = CRUDSkills(Skills1)