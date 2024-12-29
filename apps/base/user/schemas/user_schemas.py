from pydantic import field_serializer, Field, field_validator
from settings.dto_base import BaseDto
from user.models import UserRoles


class UserDTO(BaseDto):
    id: int
    username: str
    balance: float
    commission: float
    usdt_wallet: str
    role: UserRoles

    @field_serializer('balance')
    def serialize_date(self, balance: float):
        return round(balance, 3)


class EditUserAdminDTO(BaseDto):
    username: str | None = Field(default=None)
    balance: str | None = Field(default=None)
    commission: str | None = Field(default=None)
    usdt_wallet: str | None = Field(default=None)
    role: UserRoles | None | str = Field(default=None)

    @field_validator('username', 'balance', 'commission', 'usdt_wallet', 'role')
    @classmethod
    def get_fields(cls, v: str) -> str | None:
        return v if v else None


class EditUserDTO(BaseDto):
    username: str | None = Field(default=None)
    usdt_wallet: str | None = Field(default=None)

    @field_validator('username', 'usdt_wallet')
    @classmethod
    def get_fields(cls, v: str) -> str | None:
        return v if v else None