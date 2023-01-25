from typing import Optional
from sqlalchemy import select, insert

from sobesity.domain.interfaces import ISkillRepository
from sobesity.domain.entities import SkillEntity, SkillFilterEnitity, SkillId
from sobesity.infrastructure.models import skill_table
from sobesity.infrastructure.repositories.mapper import build_skill_entity


class SkillRepository(ISkillRepository):
    def __init__(self, datasource) -> None:
        self.datasource = datasource

    def __patch_query(self, query, skill_filter: SkillFilterEnitity):
        if skill_filter.name:
            query.where(skill_table.c.name.in_(skill_filter.name))
        if skill_filter.skill_id:
            query.where(skill_table.c.skill_id.in_(skill_filter.skill_id))
        return query

    def get_list(self, skill_filter: Optional[SkillFilterEnitity] = None) -> list[SkillEntity]:
        query = select(skill_table)

        if skill_filter is not None:
            query = self.__patch_query(query, skill_filter)

        with self.datasource() as conn:
            result = conn.execute(query).fetchall()

        return [build_skill_entity(cur) for cur in result]

    def create(self, skill: SkillEntity) -> None:
        query = insert(skill_table).values(
            name=skill.name
        )
        with self.datasource() as conn:
            conn.execute(query)


    def update(self, old_skill: SkillEntity, update: SkillFilterEnitity) -> list[SkillId]:
        pass

    def delete(self, skill_id: SkillId) -> None:
        pass
