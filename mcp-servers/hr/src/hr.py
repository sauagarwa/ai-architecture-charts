from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP
import json
from datetime import datetime, timedelta

# Initialize FastMCP server
mcp = FastMCP("hr", host="0.0.0.0")

# Sample HR data for demo purposes
COMPANY_INFO = {
    "name": "TechCorp Solutions",
    "founded": "2015",
    "employees": 250,
    "headquarters": "San Francisco, CA",
    "industry": "Technology Solutions"
}

POLICIES = {
    "vacation_policy": {
        "title": "Vacation Policy",
        "content": "Employees accrue 15 days of vacation per year for the first 2 years, 20 days for years 3-5, and 25 days after 5 years of service. Vacation must be requested at least 2 weeks in advance for approval."
    },
    "sick_leave": {
        "title": "Sick Leave Policy", 
        "content": "Employees receive 10 sick days per year. Sick leave can be used for personal illness, medical appointments, or caring for immediate family members. No advance notice required for unexpected illness."
    },
    "remote_work": {
        "title": "Remote Work Policy",
        "content": "Employees may work remotely up to 3 days per week with manager approval. Full remote work arrangements require VP approval and are evaluated case-by-case."
    },
    "dress_code": {
        "title": "Dress Code Policy",
        "content": "Business casual is the standard dress code. On client meeting days, business professional attire is expected. Casual Friday allows jeans and casual tops."
    },
    "benefits_overview": {
        "title": "Benefits Overview",
        "content": "Full-time employees receive health insurance (80% company paid), dental and vision coverage, 401k with 4% company match, life insurance, and flexible spending accounts."
    }
}

DEPARTMENTS = {
    "engineering": {"name": "Engineering", "manager": "Sarah Chen", "employees": 45},
    "sales": {"name": "Sales", "manager": "Mike Rodriguez", "employees": 30},
    "marketing": {"name": "Marketing", "manager": "Lisa Park", "employees": 15},
    "hr": {"name": "Human Resources", "manager": "David Kim", "employees": 8},
    "finance": {"name": "Finance", "manager": "Jennifer Walsh", "employees": 12},
    "operations": {"name": "Operations", "manager": "Tom Anderson", "employees": 20}
}

SAMPLE_EMPLOYEES = [
    {"id": "EMP001", "name": "John Smith", "department": "engineering", "role": "Senior Software Engineer", "hire_date": "2022-03-15", "manager": "Sarah Chen"},
    {"id": "EMP002", "name": "Emily Johnson", "department": "sales", "role": "Account Executive", "hire_date": "2023-01-10", "manager": "Mike Rodriguez"},
    {"id": "EMP003", "name": "Alex Thompson", "department": "marketing", "role": "Marketing Specialist", "hire_date": "2021-09-20", "manager": "Lisa Park"},
    {"id": "EMP004", "name": "Maria Garcia", "department": "hr", "role": "HR Generalist", "hire_date": "2020-05-12", "manager": "David Kim"},
    {"id": "EMP005", "name": "Robert Wilson", "department": "finance", "role": "Financial Analyst", "hire_date": "2022-11-08", "manager": "Jennifer Walsh"}
]

@mcp.tool()
async def get_company_info() -> str:
    """Get general information about the company."""
    info = f"""
    Company: {COMPANY_INFO['name']}
    Founded: {COMPANY_INFO['founded']}
    Employees: {COMPANY_INFO['employees']}
    Headquarters: {COMPANY_INFO['headquarters']}
    Industry: {COMPANY_INFO['industry']}
    """
    return info.strip()

@mcp.tool()
async def get_policy(policy_name: str) -> str:
    """Get details about a specific HR policy.
    
    Args:
        policy_name: Name of the policy (vacation_policy, sick_leave, remote_work, dress_code, benefits_overview)
    """
    policy_name = policy_name.lower()
    
    if policy_name not in POLICIES:
        available_policies = ", ".join(POLICIES.keys())
        return f"Policy '{policy_name}' not found. Available policies: {available_policies}"
    
    policy = POLICIES[policy_name]
    return f"{policy['title']}:\n\n{policy['content']}"

@mcp.tool()
async def list_policies() -> str:
    """List all available HR policies."""
    policies_list = []
    for key, policy in POLICIES.items():
        policies_list.append(f"- {key}: {policy['title']}")
    
    return "Available HR Policies:\n" + "\n".join(policies_list)

@mcp.tool()
async def get_department_info(department: str) -> str:
    """Get information about a specific department.
    
    Args:
        department: Department name (engineering, sales, marketing, hr, finance, operations)
    """
    department = department.lower()
    
    if department not in DEPARTMENTS:
        available_depts = ", ".join(DEPARTMENTS.keys())
        return f"Department '{department}' not found. Available departments: {available_depts}"
    
    dept = DEPARTMENTS[department]
    return f"""
    Department: {dept['name']}
    Manager: {dept['manager']}
    Number of Employees: {dept['employees']}
    """

@mcp.tool()
async def list_departments() -> str:
    """List all company departments with basic information."""
    dept_list = []
    for dept in DEPARTMENTS.values():
        dept_list.append(f"- {dept['name']}: {dept['employees']} employees, managed by {dept['manager']}")
    
    return "Company Departments:\n" + "\n".join(dept_list)

@mcp.tool()
async def search_employee(search_term: str) -> str:
    """Search for employees by name, ID, or department.
    
    Args:
        search_term: Name, employee ID, or department to search for
    """
    search_term = search_term.lower()
    results = []
    
    for emp in SAMPLE_EMPLOYEES:
        if (search_term in emp['name'].lower() or 
            search_term in emp['id'].lower() or 
            search_term in emp['department'].lower() or
            search_term in emp['role'].lower()):
            results.append(f"- {emp['name']} ({emp['id']}) - {emp['role']} in {emp['department'].title()}")
    
    if not results:
        return f"No employees found matching '{search_term}'"
    
    return "Search Results:\n" + "\n".join(results)

@mcp.tool()
async def get_employee_details(employee_id: str) -> str:
    """Get detailed information about a specific employee.
    
    Args:
        employee_id: The employee's ID (e.g., EMP001)
    """
    employee_id = employee_id.upper()
    
    for emp in SAMPLE_EMPLOYEES:
        if emp['id'] == employee_id:
            return f"""
            Employee Details:
            Name: {emp['name']}
            ID: {emp['id']}
            Role: {emp['role']}
            Department: {emp['department'].title()}
            Manager: {emp['manager']}
            Hire Date: {emp['hire_date']}
            """
    
    return f"Employee with ID '{employee_id}' not found"

@mcp.tool()
async def calculate_vacation_days(hire_date: str) -> str:
    """Calculate vacation days based on hire date and company policy.
    
    Args:
        hire_date: Employee hire date in YYYY-MM-DD format
    """
    try:
        hire_date_obj = datetime.strptime(hire_date, "%Y-%m-%d")
        years_of_service = (datetime.now() - hire_date_obj).days / 365.25
        
        if years_of_service < 2:
            vacation_days = 15
        elif years_of_service < 5:
            vacation_days = 20
        else:
            vacation_days = 25
            
        return f"""
        Years of Service: {years_of_service:.1f} years
        Annual Vacation Days: {vacation_days} days
        
        Policy: 15 days for 0-2 years, 20 days for 2-5 years, 25 days for 5+ years
        """
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD format."

@mcp.tool()
async def get_holiday_schedule() -> str:
    """Get the company holiday schedule."""
    current_year = datetime.now().year
    holidays = [
        f"New Year's Day - January 1, {current_year}",
        f"Martin Luther King Jr. Day - Third Monday in January",
        f"Presidents' Day - Third Monday in February", 
        f"Memorial Day - Last Monday in May",
        f"Independence Day - July 4, {current_year}",
        f"Labor Day - First Monday in September",
        f"Thanksgiving - Fourth Thursday in November",
        f"Black Friday - Day after Thanksgiving",
        f"Christmas Eve - December 24, {current_year}",
        f"Christmas Day - December 25, {current_year}",
        f"New Year's Eve - December 31, {current_year}"
    ]
    
    return f"Company Holiday Schedule {current_year}:\n\n" + "\n".join([f"- {holiday}" for holiday in holidays])

@mcp.tool()
async def get_hr_contacts() -> str:
    """Get HR department contact information."""
    return """
    HR Department Contacts:
    
    General HR Inquiries:
    - Email: hr@techcorpsolutions.com
    - Phone: (555) 123-4567
    
    HR Team:
    - David Kim (HR Manager): david.kim@techcorpsolutions.com
    - Maria Garcia (HR Generalist): maria.garcia@techcorpsolutions.com
    - Susan Lee (Recruiter): susan.lee@techcorpsolutions.com
    
    Office Hours: Monday-Friday, 9:00 AM - 5:00 PM PST
    """

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='sse')
