import { useState } from 'react';

function LoginForm({ onLoginSuccess }) {
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  function handleLogin(e) {
    e.preventDefault();
    fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone, password }),
    })
      .then((res) => {
        if (!res.ok) throw new Error('Login failed');
        return res.json();
      })
      .then((data) => onLoginSuccess(data.access_token))
      .catch((err) => setError(err.message));
  }

  return (
    <div>
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        <input type="text" placeholder="Phone" value={phone} onChange={(e) => setPhone(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button type="submit">Login</button>
      </form>
      {error && <p>Error: {error}</p>}
    </div>
  );
}

export default LoginForm;
