import datetime
from typing import Optional, List
from sqlmodel import Session, select
from app.db.session import engine
from app.models.care import Employee, Shift, QCIncident, Client, CarePlan

def get_current_time() -> str:
    """Returns the current date and time on the server."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_rota(employee_email: str) -> str:
    """
    Fetches the upcoming shifts for a specific employee by their email.
    """
    with Session(engine) as session:
        statement = select(Employee).where(Employee.email == employee_email)
        employee = session.exec(statement).first()
        if not employee:
            return f"Employee with email {employee_email} not found."
        
        statement = select(Shift).where(Shift.employee_id == employee.id).order_by(Shift.start_time)
        shifts = session.exec(statement).all()
        
        if not shifts:
            return f"No scheduled shifts found for {employee.first_name} {employee.last_name}."
        
        rota_info = f"Rota for {employee.first_name} {employee.last_name}:\n"
        for shift in shifts:
            rota_info += f"- {shift.start_time.strftime('%Y-%m-%d %H:%M')} to {shift.end_time.strftime('%H:%M')} ({shift.status})\n"
        return rota_info

def report_incident(branch_name: str, title: str, description: str, severity: str = "Medium") -> str:
    """
    Reports a new quality/compliance incident.
    """
    from app.models.care import Branch, IncidentSeverity
    with Session(engine) as session:
        statement = select(Branch).where(Branch.name.ilike(f"%{branch_name}%"))
        branch = session.exec(statement).first()
        if not branch:
            return f"Branch '{branch_name}' not found."
        
        incident = QCIncident(
            branch_id=branch.id,
            title=title,
            description=description,
            severity=IncidentSeverity(severity.capitalize())
        )
        session.add(incident)
        session.commit()
        return f"Incident '{title}' reported successfully for {branch.name}."

def get_compliance_status(branch_name: str) -> str:
    """
    Summarizes the current incidents and compliance status for a branch.
    """
    from app.models.care import Branch
    with Session(engine) as session:
        statement = select(Branch).where(Branch.name.ilike(f"%{branch_name}%"))
        branch = session.exec(statement).first()
        if not branch:
            return f"Branch '{branch_name}' not found."
        
        statement = select(QCIncident).where(QCIncident.branch_id == branch.id)
        incidents = session.exec(statement).all()
        
        if not incidents:
            return f"Branch {branch.name} is fully compliant. No open incidents."
        
        status = f"Compliance Status for {branch.name}:\n"
        status += f"Total Incidents: {len(incidents)}\n"
        for inc in incidents:
            status += f"- [{inc.severity}] {inc.title}: {inc.status}\n"
        return status

def calculate_training_hours(employee_count: int, hours_per_week: float) -> str:
    """Calculates total training capacity."""
    total = employee_count * hours_per_week
    return f"Total team training capacity: {total} hours/week."
