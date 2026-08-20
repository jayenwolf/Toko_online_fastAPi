from pydantic import BaseModel, Field
from typing import Optional

class Produk(BaseModel):
    id: int = Field(gt=0)
    nama: str = Field(min_length=1)
    stok: int = Field(ge=0)


class UpdateProduk(BaseModel):
    nama: Optional[str] = None
    stok: Optional[int] = None
