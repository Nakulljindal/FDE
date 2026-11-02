# TODO : Create Booking Model
# Fields:
#  - user_id : int
#  - room_id : int
#  - nights : int (must be >= 1)
#  - rate_per_night : float
# Also, add computed field : total amount = nights * rate_per_night


from pydantic import BaseModel, field_validator, model_validator, computed_field, Field

class BookingModel(BaseModel):
    user_id = int
    room_id = int
    nights : int = Field(..., ge=1)
    rate_per_night : int

    @field_validator(user_id, room_id, nights, rate_per_night)
    def validate(cls, values):
        if values.user_id < 0:
            raise ValueError("User ID is invalid")
        if values.room_id < 0:
            raise ValueError("Room ID is invalid")
        return values

    @computed_field
    @property
    def total_amount(self) -> float:
        return self.rate_per_night * self.nights