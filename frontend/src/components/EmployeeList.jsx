import { useState } from 'react';
import { Button } from "@/components/ui/button";

function EmployeeList({ token }){
    const [employees, setEmployees] = useState([]);
    const [error, setError] = useState(null);

    function fetchEmployees(){
        fetch('http://localhost:8000/employees', {
            headers: { Authorization: `Bearer ${token}` },
        })
            .then((res) => {
                if (!res.ok) throw new Error('Failed to fetch employees');
                return res.json();
            })
            .then((data) => setEmployees(data))
            .catch((err) => setError(err.message))
    }
    return (
        <div>
            <Button onClick={fetchEmployees}>Load Employees</Button>
            {error && <p>Error: {error}</p>}
            <ul>
                {employees.map((emp) => <li key={emp.id}>{emp.name}</li>)}
            </ul>
        </div>
    );
}

export default EmployeeList;