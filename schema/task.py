from pydantic import BaseModel, Field, model_validator, ValidationInfo

class TaskSchema(BaseModel):
    id: int | None = None
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int | None = None
    
    class Config:
        from_attributes = True
    
    @model_validator(mode="after")
    def check_name_or_pomodoro_count_is_not_none(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("name or pomodoro_count must be provided")
        print(self)
        return self