import { useState } from "react";
import axios from "axios";

function Login({ setToken }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    const res = await axios.post("http://127.0.0.1:8000/login", null, {
      params: { username, password }
    });
    setToken(res.data.access_token);
  };

  return (
    <div>
      <input placeholder="username" onChange={e => setUsername(e.target.value)} />
      <input placeholder="password" type="password" onChange={e => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default Login;