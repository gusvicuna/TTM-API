from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Text,
    Boolean,
    Integer,
    ForeignKey,
    UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Survey(Base):
    __tablename__ = "surveys"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)


class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(
        Integer,
        ForeignKey('surveys.id'),
        primary_key=True,
        index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # puede ser 'driver', 'like' o 'ut'
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)


class Component(Base):
    __tablename__ = "components"
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(
        Integer,
        ForeignKey('drivers.id'),
        primary_key=True,
        index=True)
    survey_id = Column(
        Integer,
        ForeignKey('drivers.survey_id'),
        primary_key=True,
        index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)


class Aception(Base):
    __tablename__ = "aceptions"
    id = Column(Integer, primary_key=True, index=True)
    component_id = Column(Integer, ForeignKey('components.id'), nullable=False)
    driver_id = Column(
        Integer,
        ForeignKey('components.driver_id'),
        nullable=False)
    survey_id = Column(
        Integer,
        ForeignKey('components.survey_id'),
        nullable=False)
    phrase = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            'phrase', 'component_id', 'driver_id', 'survey_id',
            name='uq_aception_details'),
    )


class Answer(Base):
    __tablename__ = "answers"
    token = Column(String, primary_key=True, index=True)
    answer_text = Column(Text, nullable=False)
    has_been_processed = Column(Boolean, nullable=False, default=False)
    survey_id = Column(Integer, ForeignKey('surveys.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)


# Relationships
Survey.drivers = relationship(
    "Driver",
    back_populates="survey",
    foreign_keys=[Driver.survey_id])
Survey.answers = relationship(
    "Answer",
    back_populates="survey",
    foreign_keys=[Answer.survey_id])

Driver.survey = relationship(
    "Survey",
    back_populates="drivers",
    foreign_keys=[Driver.survey_id])
Driver.components = relationship(
    'Component',
    back_populates='driver',
    primaryjoin="and_(Driver.id==Component.driver_id," +
    " Driver.survey_id==Component.survey_id)",
    foreign_keys=[Component.driver_id, Component.survey_id])

Component.driver = relationship(
    "Driver",
    back_populates="components",
    primaryjoin="and_(Component.driver_id==Driver.id," +
    " Component.survey_id==Driver.survey_id)",
    foreign_keys=[Component.driver_id, Component.survey_id])
Component.aceptions = relationship(
    "Aception",
    back_populates="component",
    primaryjoin="and_(Aception.component_id==Component.id, " +
    "Aception.driver_id==Component.driver_id," +
    " Aception.survey_id==Component.survey_id)",
    foreign_keys=[
        Aception.component_id,
        Aception.driver_id,
        Aception.survey_id])

Aception.component = relationship(
    "Component",
    back_populates="aceptions",
    primaryjoin="and_(Aception.component_id==Component.id, " +
    "Aception.driver_id==Component.driver_id, " +
    "Aception.survey_id==Component.survey_id)",
    foreign_keys=[
        Aception.component_id,
        Aception.driver_id,
        Aception.survey_id])

Answer.survey = relationship(
    "Survey",
    back_populates="answers",
    foreign_keys=[Answer.survey_id])
