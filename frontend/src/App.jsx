import { useState } from 'react';
import LoginForm from './components/LoginForm';
import EmployeeList from './components/EmployeeList';

function App(){
  const [token, setToken] = useState(null);

  return(
    <div>
      {!token && <LoginForm onLoginSuccess={setToken} />}
      {token && (
        <div>
          <p>Logged in!</p>
          <EmployeeList token={token} />
        </div>
      )}
    </div>
  );
}

export default App;