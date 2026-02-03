from datetime import datetime, date, time
from typing import List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

############################################
# Classes are defined here
############################################
class CommentCreate(BaseModel):
    timestamp: date
    content: str
    authorName: str
    blogpost: int  # N:1 Relationship (mandatory)


class BlogPostCreate(BaseModel):
    image: str
    content: str
    title: str
    timestamp: date
    authorName: str
    hasComments: Optional[List[int]] = None  # 1:N Relationship


