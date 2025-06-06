"""
Database models for the Growth Accelerator Staffing Platform
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, UniqueConstraint, JSON
from sqlalchemy.orm import relationship
from flask_login import UserMixin

# Import db from app module to avoid circular imports
from app import db

class User(UserMixin, db.Model):
    """User model representing platform users"""
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True)
    username = Column(String(80), unique=True, nullable=True)
    email = Column(String(120), unique=True, nullable=True)
    password_hash = Column(String(256))
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    profile_image_url = Column(String(255), nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        display_name = getattr(self, 'username', None) or getattr(self, 'email', None) or str(getattr(self, 'id', 'Unknown'))
        return f'<User {display_name}>'
        
    # Override UserMixin's is_active property
    @property
    def is_active(self):
        # This allows you to disable users if needed
        # For now, all users are active
        return True


class OAuth(db.Model):
    """OAuth model for social login"""
    __tablename__ = 'oauth'

    id = Column(Integer, primary_key=True)
    provider = Column(String(50), nullable=False)
    provider_user_id = Column(String(256), nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'))
    token = Column(JSON, nullable=False)
    browser_session_key = Column(String(100), nullable=False)
    
    # Relationships
    user = relationship("User")
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'browser_session_key', 'provider', name='uq_user_browser_session_key_provider'),
    )
    
    def __repr__(self):
        return f'<OAuth {self.provider}:{self.provider_user_id}>'


class Client(db.Model):
    """Client model representing companies that post jobs"""
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    industry = Column(String(100))
    website = Column(String(200))
    contact_name = Column(String(100))
    contact_email = Column(String(120))
    contact_phone = Column(String(20))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    jobs = relationship("Job", back_populates="client")
    
    def __repr__(self):
        return f'<Client {self.name}>'


class Consultant(db.Model):
    """Consultant model representing professionals available for jobs"""
    __tablename__ = 'consultants'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20))
    linkedin_url = Column(String(200))
    resume_url = Column(String(200))
    workable_id = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String(50), nullable=True)
    availability_date = Column(DateTime, nullable=True)
    hourly_rate = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = relationship("Application", back_populates="consultant")
    placements = relationship("Placement", back_populates="consultant")
    
    def __repr__(self):
        return f'<Consultant {self.first_name} {self.last_name}>'

class Job(db.Model):
    """Job model representing open positions"""
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'))
    description = Column(Text)
    requirements = Column(Text)
    location = Column(String(100))
    job_type = Column(String(50))  # Full-time, Part-time, Contract
    salary_range = Column(String(100))
    remote = Column(Boolean, default=False)
    workable_id = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="jobs")
    applications = relationship("Application", back_populates="job")
    job_skills = relationship("JobSkill", back_populates="job")
    
    def __repr__(self):
        return f'<Job {self.title}>'


class Skill(db.Model):
    """Skills model representing consultant skills and job requirements"""
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100))
    
    # Relationships
    job_skills = relationship("JobSkill", back_populates="skill")
    
    def __repr__(self):
        return f'<Skill {self.name}>'


class JobSkill(db.Model):
    """Many-to-many relationship between jobs and skills"""
    __tablename__ = 'job_skills'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    skill_id = Column(Integer, ForeignKey('skills.id'))
    importance = Column(Integer, default=1)  # 1-5 rating of importance
    
    # Relationships
    job = relationship("Job", back_populates="job_skills")
    skill = relationship("Skill", back_populates="job_skills")
    
    def __repr__(self):
        return f'<JobSkill {self.job_id}:{self.skill_id}>'


class Application(db.Model):
    """Application model representing a consultant applying to a job"""
    __tablename__ = 'applications'
    
    id = Column(Integer, primary_key=True)
    consultant_id = Column(Integer, ForeignKey('consultants.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))
    status = Column(String(50), default='applied')  # applied, screening, interview, hired, rejected
    notes = Column(Text)
    match_score = Column(Float)
    application_date = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    consultant = relationship("Consultant", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    
    def __repr__(self):
        return f'<Application {self.consultant_id} for job {self.job_id}>'


class Placement(db.Model):
    """Placement model representing hired consultants"""
    __tablename__ = 'placements'
    
    id = Column(Integer, primary_key=True)
    consultant_id = Column(Integer, ForeignKey('consultants.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    hourly_rate = Column(Float)
    status = Column(String(50), default='pending')  # pending, active, completed, terminated
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    consultant = relationship("Consultant", back_populates="placements")
    
    def __repr__(self):
        return f'<Placement {self.consultant_id} for job {self.job_id}>'