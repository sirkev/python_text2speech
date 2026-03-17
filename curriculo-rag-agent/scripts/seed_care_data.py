import asyncio
from sqlmodel import Session, select
from app.db.session import engine
from app.models.care import (
    Company, Branch, Employee, Client, CarePlan, 
    BranchStatus, ClientStatus, Shift, ShiftStatus,
    QCIncident, IncidentSeverity, IncidentStatus
)
from datetime import datetime, timedelta

async def seed_data():
    with Session(engine) as session:
        # 1. Create Company
        company = Company(
            name="CareWise Solutions",
            email="admin@carewise.co.uk",
            phone="+44 20 7123 4567"
        )
        session.add(company)
        session.commit()
        session.refresh(company)
        
        # 2. Create Branches
        branch_london = Branch(
            company_id=company.id,
            name="London Central Branch",
            location="London, SW1A 1AA",
            service_type="Domiciliary Care",
            status=BranchStatus.OPERATING
        )
        branch_manchester = Branch(
            company_id=company.id,
            name="Manchester North Branch",
            location="Manchester, M1 1AF",
            service_type="Residential Care",
            status=BranchStatus.OPERATING
        )
        session.add(branch_london)
        session.add(branch_manchester)
        session.commit()
        session.refresh(branch_london)
        session.refresh(branch_manchester)
        
        # 3. Create Employees
        sarah = Employee(branch_id=branch_london.id, first_name="Sarah", last_name="Johnson", email="sarah.j@carewise.co.uk", role="Branch Manager")
        michael = Employee(branch_id=branch_london.id, first_name="Michael", last_name="Smith", email="michael.s@carewise.co.uk", role="Senior Carer")
        emma = Employee(branch_id=branch_manchester.id, first_name="Emma", last_name="Davis", email="emma.d@carewise.co.uk", role="Care Coordinator")
        
        session.add_all([sarah, michael, emma])
        session.commit()
        session.refresh(michael)
        
        # 4. Create Clients
        client_1 = Client(branch_id=branch_london.id, first_name="Robert", last_name="Brown", status=ClientStatus.ACTIVE)
        client_2 = Client(branch_id=branch_london.id, first_name="Alice", last_name="Wilson", status=ClientStatus.ACTIVE)
        session.add_all([client_1, client_2])
        session.commit()
        session.refresh(client_1)
        
        # 5. Create Care Plan
        care_plan = CarePlan(
            client_id=client_1.id,
            title="Standard Personal Care Plan",
            content="""
            Client requires assistance with:
            - Morning routine (washing and dressing)
            - Meal preparation (Breakfast and Lunch)
            - Medication prompting at 9 AM and 6 PM
            - Mobility support using walking frame
            """
        )
        session.add(care_plan)
        
        # 6. Create Rota (Shifts)
        now = datetime.utcnow()
        shifts = [
            Shift(
                employee_id=michael.id, 
                start_time=now + timedelta(hours=1), 
                end_time=now + timedelta(hours=9),
                status=ShiftStatus.SCHEDULED
            ),
            Shift(
                employee_id=michael.id, 
                start_time=now + timedelta(days=1, hours=8), 
                end_time=now + timedelta(days=1, hours=16),
                status=ShiftStatus.SCHEDULED
            )
        ]
        session.add_all(shifts)
        
        # 7. Create QC (Incidents)
        incident = QCIncident(
            branch_id=branch_london.id,
            title="Medication Discrepancy",
            description="Client Robert Brown reported a missed evening medication dose on March 15th.",
            severity=IncidentSeverity.MEDIUM,
            status=IncidentStatus.UNDER_INVESTIGATION
        )
        session.add(incident)
        
        session.commit()
        print("Successfully seeded Care SaaS data with Rota and QC entries!")

if __name__ == "__main__":
    asyncio.run(seed_data())
