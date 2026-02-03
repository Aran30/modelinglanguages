import enum
from typing import List, Optional
from sqlalchemy import (
    create_engine, Column, ForeignKey, Table, Text, Boolean, String, Date, 
    Time, DateTime, Float, Integer, Enum
)
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped, mapped_column, relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date

class Base(DeclarativeBase):
    pass



# Tables definition for many-to-many relationships

# Tables definition
class Comment(Base):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(100))
    authorName: Mapped[str] = mapped_column(String(100))
    timestamp: Mapped[dt_date] = mapped_column(Date)
    blogpost_id: Mapped[int] = mapped_column(ForeignKey("blogpost.id"))

class BlogPost(Base):
    __tablename__ = "blogpost"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(String(100))
    authorName: Mapped[str] = mapped_column(String(100))
    timestamp: Mapped[dt_date] = mapped_column(Date)
    image: Mapped[str] = mapped_column(String(100))


#--- Relationships of the comment table
Comment.blogpost: Mapped["BlogPost"] = relationship("BlogPost", back_populates="hasComments", foreign_keys=[Comment.blogpost_id])

#--- Relationships of the blogpost table
BlogPost.hasComments: Mapped[List["Comment"]] = relationship("Comment", back_populates="blogpost", foreign_keys=[Comment.blogpost_id])

# Database connection
DATABASE_URL = "sqlite:///Class_Diagram.db"  # SQLite connection
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
Base.metadata.create_all(engine, checkfirst=True)