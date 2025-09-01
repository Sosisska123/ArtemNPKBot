from typing import Optional
from pydantic import BaseModel


class VkGroupSchema(BaseModel):
    domain: str
    group_name_shortcut: str
    start_post_offset: int

    return_file_type: str
    files_url: Optional[list[str]] = None


class NPKVkGroup(VkGroupSchema):
    photo_date: Optional[str] = None


class KNNVkGroup(VkGroupSchema):
    doc_title: Optional[str] = None
    doc_date: Optional[str] = None
