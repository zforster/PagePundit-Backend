from humps import camelize
from pydantic import BaseModel


class SnakeToCamelCaseModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True

    def to_dict_by_alias(self) -> dict:
        return self.dict(by_alias=True)
