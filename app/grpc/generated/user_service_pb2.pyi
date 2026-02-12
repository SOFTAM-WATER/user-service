from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ValidationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VALID: _ClassVar[ValidationStatus]
    NOT_FOUND: _ClassVar[ValidationStatus]
    BLOCKED: _ClassVar[ValidationStatus]
    INVALID_DATA: _ClassVar[ValidationStatus]
VALID: ValidationStatus
NOT_FOUND: ValidationStatus
BLOCKED: ValidationStatus
INVALID_DATA: ValidationStatus

class ValidateUserRequest(_message.Message):
    __slots__ = ("telegram_id", "phone", "full_name")
    TELEGRAM_ID_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    telegram_id: int
    phone: str
    full_name: str
    def __init__(self, telegram_id: _Optional[int] = ..., phone: _Optional[str] = ..., full_name: _Optional[str] = ...) -> None: ...

class ValidateUserResponse(_message.Message):
    __slots__ = ("user_id", "status")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    status: ValidationStatus
    def __init__(self, user_id: _Optional[str] = ..., status: _Optional[_Union[ValidationStatus, str]] = ...) -> None: ...
