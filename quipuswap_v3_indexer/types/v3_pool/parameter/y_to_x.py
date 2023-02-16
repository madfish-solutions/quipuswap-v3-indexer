# generated by datamodel-codegen:
#   filename:  y_to_x.json

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra


class YToXParameter(BaseModel):
    class Config:
        extra = Extra.forbid

    dy: str
    deadline: str
    min_dx: str
    to_dx: str
    referral_code: Optional[str]