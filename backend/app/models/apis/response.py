from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional
from pydantic.generics import GenericModel

T = TypeVar("T")

class ApiResponse(GenericModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None