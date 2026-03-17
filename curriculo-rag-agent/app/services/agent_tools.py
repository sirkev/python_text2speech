import datetime
from typing import Optional, List
from sqlmodel import Session, select
from app.db.session import engine
from app.models.care import Employee, Shift, QCIncident, Client, CarePlan, Branch, IncidentSeverity
from app.core.logging import get_logger

logger = get_logger(__name__)

def get_current_time() -> str:
    """Returns the current date and time on the server."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_rota(employee_email: str) -> str:
    """
    Fetches the upcoming shifts for a specific employee by their email.
    """
    logger.info("tool_call", tool="get_rota", email=employee_email)
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

def create_incident(branch_name: str, title: str, description: str, severity: str = "Medium") -> str:
    """
    Creates a new quality/compliance incident report.
    """
    logger.info("tool_call", tool="create_incident", branch=branch_name, title=title)
    with Session(engine) as session:
        statement = select(Branch).where(Branch.name.ilike(f"%{branch_name}%"))
        branch = session.exec(statement).first()
        if not branch:
            return f"Branch '{branch_name}' not found."
        
        try:
            # Validate severity string matches enum
            sev_enum = IncidentSeverity(severity.capitalize())
        except ValueError:
            sev_enum = IncidentSeverity.MEDIUM
            
        incident = QCIncident(
            branch_id=branch.id,
            title=title,
            description=description,
            severity=sev_enum
        )
        session.add(incident)
        session.commit()
        return f"Incident '{title}' reported successfully for {branch.name}. ID: {incident.id}"

def get_compliance_status(branch_name: str) -> str:
    """
    Summarizes the current incidents and compliance status for a branch.
    """
    logger.info("tool_call", tool="get_compliance_status", branch=branch_name)
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

def list_branches() -> str:
    """Lists all branches currently operating in the system."""
    logger.info("tool_call", tool="list_branches")
    with Session(engine) as session:
        branches = session.exec(select(Branch)).all()
        if not branches:
            return "No branches found in the system."
        
        resp = "Branches operating:\n"
        for b in branches:
            resp += f"- {b.name} ({b.location}) - Status: {b.status}\n"
        return resp

def list_branch_members(branch_name: str) -> str:
    """Lists all employees assigned to a specific branch."""
    logger.info("tool_call", tool="list_branch_members", branch=branch_name)
    with Session(engine) as session:
        branch = session.exec(select(Branch).where(Branch.name.ilike(f"%{branch_name}%"))).first()
        if not branch:
            return f"Branch '{branch_name}' not found."
        
        employees = session.exec(select(Employee).where(Employee.branch_id == branch.id)).all()
        if not employees:
            return f"No employees found for {branch.name}."
        
        resp = f"Employees at {branch.name}:\n"
        for e in employees:
            resp += f"- {e.first_name} {e.last_name} ({e.role}) - Email: {e.email}\n"
        return resp

def get_employee_profile(email: str) -> str:
    """Retrieves full profile details for an employee by their email."""
    logger.info("tool_call", tool="get_employee_profile", email=email)
    with Session(engine) as session:
        employee = session.exec(select(Employee).where(Employee.email == email)).first()
        if not employee:
            return f"Employee with email {email} not found."
        
        branch = session.exec(select(Branch).where(Branch.id == employee.branch_id)).first()
        branch_name = branch.name if branch else "Unknown"
        
        profile = f"Employee Profile for {employee.first_name} {employee.last_name}:\n"
        profile += f"- Role: {employee.role}\n"
        profile += f"- Branch: {branch_name}\n"
        profile += f"- Email: {employee.email}\n"
        return profile

def list_clients(branch_name: str) -> str:
    """Lists all active clients assigned to a specific branch."""
    logger.info("tool_call", tool="list_clients", branch=branch_name)
    with Session(engine) as session:
        branch = session.exec(select(Branch).where(Branch.name.ilike(f"%{branch_name}%"))).first()
        if not branch:
            return f"Branch '{branch_name}' not found."
        
        clients = session.exec(select(Client).where(Client.branch_id == branch.id)).all()
        if not clients:
            return f"No clients found for {branch.name}."
        
        resp = f"Active Clients at {branch.name}:\n"
        for c in clients:
            resp += f"- {c.first_name} {c.last_name} (Status: {c.status})\n"
        return resp

def list_incidents(branch_name: str) -> str:
    """Lists all recorded incidents for a specific branch."""
    return get_compliance_status(branch_name)

def generate_compliance_report(branch_name: str) -> str:
    """Generates a detailed compliance summary report for a branch."""
    logger.info("tool_call", tool="generate_compliance_report", branch=branch_name)
    summary = get_compliance_status(branch_name)
    report = f"--- COMPLIANCE REPORT: {branch_name.upper()} ---\n"
    report += f"Generated on: {get_current_time()}\n"
    report += summary
    report += "\nAssessment: Action required if incidents are High/Critical severity."
    return report

def create_rota_shift(email: str, start_time: str, end_time: str) -> str:
    """
    Creates a new shift for an employee. 
    Times should be in YYYY-MM-DD HH:MM:SS format.
    """
    logger.info("tool_call", tool="create_rota_shift", email=email, start=start_time, end=end_time)
    with Session(engine) as session:
        employee = session.exec(select(Employee).where(Employee.email == email)).first()
        if not employee:
            return f"Employee with email {email} not found."
        
        try:
            start_dt = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_dt = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return "Invalid time format. Use YYYY-MM-DD HH:MM:SS."
        
        shift = Shift(
            employee_id=employee.id,
            start_time=start_dt,
            end_time=end_dt
        )
        session.add(shift)
        session.commit()
        return f"Shift created successfully for {employee.first_name} {employee.last_name}."

def calculate_training_hours(employee_count: int, hours_per_week: float) -> str:
    """Calculates total team training capacity."""
    total = employee_count * hours_per_week
    return f"Total team training capacity: {total} hours/week."

