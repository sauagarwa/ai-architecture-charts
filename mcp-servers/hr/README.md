# HR MCP Server

An MCP (Model Context Protocol) server for handling HR-related queries and operations. This server provides tools for accessing company information, HR policies, employee data, and other HR-related functionality.

## Features

The HR MCP server provides the following tools:

### Company Information
- `get_company_info()` - Get general information about the company
- `get_hr_contacts()` - Get HR department contact information

### HR Policies
- `get_policy(policy_name)` - Get details about a specific HR policy
- `list_policies()` - List all available HR policies
- Available policies:
  - `vacation_policy` - Company vacation policy and accrual rules
  - `sick_leave` - Sick leave policy and usage guidelines
  - `remote_work` - Remote work policy and approval process
  - `dress_code` - Company dress code guidelines
  - `benefits_overview` - Overview of employee benefits

### Department Information
- `get_department_info(department)` - Get information about a specific department
- `list_departments()` - List all company departments with basic information
- Available departments: engineering, sales, marketing, hr, finance, operations

### Employee Management
- `search_employee(search_term)` - Search for employees by name, ID, or department
- `get_employee_details(employee_id)` - Get detailed information about a specific employee
- `calculate_vacation_days(hire_date)` - Calculate vacation days based on hire date and company policy

### Scheduling & Holidays
- `get_holiday_schedule()` - Get the company holiday schedule

## Demo Data

This server includes sample data for demonstration purposes:

- **Company**: TechCorp Solutions (250 employees, founded 2015)
- **Departments**: 6 departments with managers and employee counts
- **Sample Employees**: 5 sample employees with various roles and departments
- **HR Policies**: Complete set of common HR policies

## Running the Server

### Local Development

1. Install dependencies:
```bash
cd src
pip install -r requirements.txt  # or use the pyproject.toml
```

2. Run the server:
```bash
python hr.py
```

The server will start on `http://0.0.0.0:8000` with SSE (Server-Sent Events) transport.

### Docker/Container

Build and run the container:

```bash
# Build the image
podman build -t hr-mcp-server .

# Run the container
podman run -p 8000:8000 hr-mcp-server
```

## Usage Examples

Once the MCP server is running, you can use any MCP-compatible client to interact with it. Here are some example interactions:

### Get Company Information
```
Tool: get_company_info
Result: Company details including name, founding year, employee count, etc.
```

### Check Vacation Policy
```
Tool: get_policy
Args: {"policy_name": "vacation_policy"}
Result: Detailed vacation policy with accrual rules
```

### Search for Employees
```
Tool: search_employee  
Args: {"search_term": "engineering"}
Result: List of employees in the engineering department
```

### Calculate Vacation Days
```
Tool: calculate_vacation_days
Args: {"hire_date": "2022-03-15"}
Result: Vacation days calculation based on years of service
```

## Configuration

The server currently uses hardcoded demo data. For production use, you would typically:

1. Connect to an HR database or HRMS system
2. Implement authentication and authorization
3. Add audit logging for HR data access
4. Configure environment-specific company data

## Dependencies

- Python 3.11+
- mcp[cli] >= 1.6.0

## Security Considerations

This is a demo implementation with sample data. For production use, consider:

- Implementing proper authentication and authorization
- Encrypting sensitive employee data
- Adding audit trails for data access
- Following data privacy regulations (GDPR, etc.)
- Implementing rate limiting and access controls

## License

This project is part of the Red Hat AI Architecture Charts and follows the same licensing terms.
