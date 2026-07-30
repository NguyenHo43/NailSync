import { useState, useEffect } from 'react';

function App(){
  const [employees, setEmployees] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/employees')
    .then((res) => res.json())
    .then((data) => setEmployees(data));
  }, []);

  return (
    <div>
      <h1>Employee List</h1>
      <ul>
        {employees.map((emp) => (
          <li key={emp.id}>{emp.name}</li>
        ))}
      </ul>
    </div>
  )
}

export default App;