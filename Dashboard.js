import { useEffect, useState } from "react";
import axios from "axios";

function Dashboard({ token }) {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/tasks/", {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => setTasks(res.data));
  }, []);

  return (
    <div>
      <h2>Tasks</h2>
      {tasks.map(t => (
        <div key={t.id}>{t.title}</div>
      ))}
    </div>
  );
}
