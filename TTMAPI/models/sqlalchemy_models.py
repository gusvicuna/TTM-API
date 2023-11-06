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
    has_been_described = Column(Boolean, nullable=False, default=False)
    did_have_an_error = Column(Boolean, nullable=False, default=False)
    default_ut_driver_id = Column(Integer, nullable=False)
    default_ut_component_id = Column(Integer, nullable=False)
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
    default_ut_driver_id = Column(Integer, nullable=True)
    default_ut_component_id = Column(Integer, nullable=True)
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
    has_manual_desc = Column(
        Boolean,
        nullable=False,
        default=False)
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
    experience_type = Column(String, nullable=False)  # puede ser 'MB','B'o'M'
    has_been_processed = Column(Boolean, nullable=False, default=False)
    did_have_an_error = Column(Boolean, default=False)
    survey_id = Column(Integer, ForeignKey('surveys.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)


class AnswerComponent(Base):
    __tablename__ = "answer_components"
    answer_token = Column(
        String,
        ForeignKey('answers.token'),
        primary_key=True,
        index=True)
    component_id = Column(Integer, ForeignKey('components.id'), nullable=False)
    driver_id = Column(
        Integer,
        ForeignKey('components.driver_id'),
        nullable=False)
    survey_id = Column(
        Integer,
        ForeignKey('components.survey_id'),
        nullable=False)
    gpt_process = Column(Integer, nullable=False)
    ttm_process = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)


class ErrorProcess(Base):
    __tablename__ = "error_process"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    answer_token = Column(
        String,
        ForeignKey('answers.token'),
        primary_key=True,
        index=True)
    error_details = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# Relationships
Survey.drivers = relationship(
    "Driver",
    back_populates="survey",
    foreign_keys=[Driver.survey_id]
)
Survey.answers = relationship(
    "Answer",
    back_populates="survey",
    foreign_keys=[Answer.survey_id]
)

Driver.survey = relationship(
    "Survey",
    back_populates="drivers",
    foreign_keys=[Driver.survey_id]
)
Driver.components = relationship(
    'Component',
    back_populates='driver',
    primaryjoin="and_(Driver.id==Component.driver_id," +
    " Driver.survey_id==Component.survey_id)",
    foreign_keys=[Component.driver_id, Component.survey_id]
)

Component.driver = relationship(
    "Driver",
    back_populates="components",
    primaryjoin="and_(Component.driver_id==Driver.id," +
    " Component.survey_id==Driver.survey_id)",
    foreign_keys=[Component.driver_id, Component.survey_id]
)
Component.aceptions = relationship(
    "Aception",
    back_populates="component",
    primaryjoin="and_(Aception.component_id==Component.id, " +
    "Aception.driver_id==Component.driver_id," +
    " Aception.survey_id==Component.survey_id)",
    foreign_keys=[
        Aception.component_id,
        Aception.driver_id,
        Aception.survey_id]
)
Component.answer_components = relationship(
    "AnswerComponent",
    back_populates="component",
    primaryjoin="and_(AnswerComponent.component_id==Component.id, " +
    "AnswerComponent.driver_id==Component.driver_id," +
    " AnswerComponent.survey_id==Component.survey_id)",
    foreign_keys=[
        AnswerComponent.component_id,
        AnswerComponent.driver_id,
        AnswerComponent.survey_id]
)

Aception.component = relationship(
    "Component",
    back_populates="aceptions",
    primaryjoin="and_(Aception.component_id==Component.id, " +
    "Aception.driver_id==Component.driver_id, " +
    "Aception.survey_id==Component.survey_id)",
    foreign_keys=[
        Aception.component_id,
        Aception.driver_id,
        Aception.survey_id]
)

Answer.survey = relationship(
    "Survey",
    back_populates="answers",
    foreign_keys=[Answer.survey_id]
)
Answer.answer_components = relationship(
    "AnswerComponent",
    back_populates="answer",
    foreign_keys=[AnswerComponent.answer_token]
)

AnswerComponent.answer = relationship(
    "Answer",
    back_populates="answer_components",
    foreign_keys=[AnswerComponent.answer_token]
)
AnswerComponent.component = relationship(
    "Component",
    back_populates="answer_components",
    primaryjoin="and_(AnswerComponent.component_id==Component.id, " +
    "AnswerComponent.driver_id==Component.driver_id," +
    " AnswerComponent.survey_id==Component.survey_id)",
    foreign_keys=[
        AnswerComponent.component_id,
        AnswerComponent.driver_id,
        AnswerComponent.survey_id]
)
