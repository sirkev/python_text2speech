from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column, Text
from datetime import datetime
from enum import Enum

class BranchStatus(str, Enum):
    OPERATING = "Operating"
    CLOSED = "Closed"

class ClientStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class ShiftStatus(str, Enum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class IncidentSeverity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class IncidentStatus(str, Enum):
    OPEN = "Open"
    UNDER_INVESTIGATION = "Under Investigation"
    RESOLVED = "Resolved"

class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    branches: List["Branch"] = Relationship(back_populates="company")

class Branch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="company.id")
    name: str = Field(index=True)
    location: str
    service_type: str
    status: BranchStatus = Field(default=BranchStatus.OPERATING)
    
    company: Company = Relationship(back_populates="branches")
    employees: List["Employee"] = Relationship(back_populates="branch")
    clients: List["Client"] = Relationship(back_populates="branch")
    incidents: List["QCIncident"] = Relationship(back_populates="branch")

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    branch_id: int = Field(foreign_key="branch.id")
    first_name: str
    last_name: str
    email: str = Field(unique=True)
    role: str
    
    branch: Branch = Relationship(back_populates="employees")
    shifts: List["Shift"] = Relationship(back_populates="employee")

class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    branch_id: int = Field(foreign_key="branch.id")
    first_name: str
    last_name: str
    status: ClientStatus = Field(default=ClientStatus.ACTIVE)
    
    branch: Branch = Relationship(back_populates="clients")
    care_plans: List["CarePlan"] = Relationship(back_populates="client")

class CarePlan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    title: str
    content: str = Field(sa_column=Column(Text))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    client: Client = Relationship(back_populates="care_plans")

class Shift(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    start_time: datetime
    end_time: datetime
    status: ShiftStatus = Field(default=ShiftStatus.SCHEDULED)
    
    employee: Employee = Relationship(back_populates="shifts")

class QCIncident(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    branch_id: int = Field(foreign_key="branch.id")
    title: str
    description: str = Field(sa_column=Column(Text))
    severity: IncidentSeverity = Field(default=IncidentSeverity.LOW)
    status: IncidentStatus = Field(default=IncidentStatus.OPEN)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    branch: Branch = Relationship(back_populates="incidents")
