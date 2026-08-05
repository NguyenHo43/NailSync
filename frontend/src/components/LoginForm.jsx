import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { User, Lock } from "lucide-react";

function LoginForm({ onLoginSuccess }) {
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  function handleLogin(e) {
    e.preventDefault();
    fetch(`${import.meta.env.VITE_API_URL}/auth/login` , {
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
    <div className="flex items-center justify-center min-h-screen bg-pink-50">
      <form onSubmit={handleLogin} className="bg-white p-8 rounded-lg shadow-md w-80 space-y-3">
        <h1 className="text-center text-3xl">Login</h1>
        <div className="relative">
            <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input type="text" placeholder="Phone" value={phone} onChange={(e) => setPhone(e.target.value)} className="w-full text-xl pl-9"/>
        </div>
        <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full text-xl pl-9"/>
        </div>
        <Button type="submit" className="w-full">Login</Button>
        {error && <p>Error: {error}</p>}
      </form>
    </div>
  );
}

export default LoginForm;
