from pydantic import BaseModel
import stringcase as stringcase


def to_camel(string):
    return stringcase.camelcase(string)


class BaseApiModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        orm_mode = True
