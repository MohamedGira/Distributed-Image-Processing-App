// src/App.js
import ImageUploadForm from "./UploadForm";
import { useState } from "react";
import React  from "react";
function App() {
  const [taskIds, setTaskIds] = useState<string[]>([]);
  return (
    <div className="App m-5" >
      <ImageUploadForm taskIds={taskIds} setTaskIds={setTaskIds} />
      <div>
        <h2 className="form-label">Tasks</h2>
        <ul>
          {taskIds.map((taskId) => (
            <li key={taskId}>{taskId}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
