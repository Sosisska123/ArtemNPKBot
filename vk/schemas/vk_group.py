from typing import Optional
from pydantic import BaseModel


class VkGroupSchema(BaseModel):
    domain: str
    group_name_shortcut: str
    start_post_offset: int

    return_file_type: str
    files_url: Optional[str] = None
    post_date: Optional[str] = None


class KNNVkGroup(VkGroupSchema):
    post_title: Optional[str] = None


class NPKVkGroup(VkGroupSchema):
    file_by_order: Optional[int] = 1
