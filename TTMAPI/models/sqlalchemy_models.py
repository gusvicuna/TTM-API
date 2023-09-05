from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, DateTime, Text)
from sqlalchemy.orm import relationship


Base = declarative_base()


class Survey(Base):
    __tablename__ = "surveys"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    drivers = relationship("Driver", back_populates="survey")
    answers = relationship("Answer", back_populates="survey")


class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)  # puede ser 'driver', 'like' o 'ut'
    survey_id = Column(Integer, ForeignKey('surveys.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    survey = relationship("Survey", back_populates="drivers")
    components = relationship("Component", back_populates="driver")


class Component(Base):
    __tablename__ = "components"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    driver_id = Column(Integer, ForeignKey('drivers.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    driver = relationship("Driver", back_populates="components")
    aceptions = relationship("Aception", back_populates="component")


class Aception(Base):
    __tablename__ = "aceptions"
    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(String)
    component_id = Column(Integer, ForeignKey('components.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    component = relationship("Component", back_populates="aceptions")


class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)
    answer = Column(Text)
    has_been_processed = Column(Boolean, default=False)
    survey_id = Column(Integer, ForeignKey('surveys.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    survey = relationship("Survey", back_populates="answers")
