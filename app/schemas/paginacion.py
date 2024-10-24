from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T')

class PaginacionBase(GenericModel, Generic[T]):
    total: int
    page: int
    pages: int
    limit: int
    prev_page: Optional[int]
    next_page: Optional[int]
    items: List[T]