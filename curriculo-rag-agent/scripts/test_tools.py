import asyncio
from app.services import agent_tools
from app.db.session import engine
from sqlmodel import Session, select
from app.models.care import Employee

def test_tools():
    print("Testing get_current_time...")
    print(agent_tools.get_current_time())
    
    print("\nTesting get_rota...")
    print(agent_tools.get_rota("michael.s@carewise.co.uk"))
    
    print("\nTesting get_compliance_status...")
    print(agent_tools.get_compliance_status("London"))
    
    print("\nTesting report_incident...")
    print(agent_tools.report_incident("London", "Test Incident", "Test Description", "Low"))

if __name__ == "__main__":
    test_tools()
