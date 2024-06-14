import React, { useState } from "react";
import axios from "axios";
import "./FilesUpload.css";

const FileUpload = () => {
  const [files, setFiles] = useState([]);
  const [inputText, setInputText] = useState("");
  const [outputs, setOutputs] = useState([]);

  async function handleInput() {
    try {
      const response = await fetch("http://127.0.0.1:5000/gen_res", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ input_text: inputText }),
      });

      const data = await response.json();
      setOutputs([...outputs, data.generated_text]);
      setInputText("");
    } catch (error) {
      console.error("Error generating text:", error);
    }
  }

  const handleChange = (event) => {
    setFiles(Array.from(event.target.files));
  };

  const handleSubmit = async () => {
    if (!files) {
      alert("Please select files to upload");
      return;
    }

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append("files[]", files[i]);
    }

    try {
      await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      alert("Files uploaded successfully");
    } catch (error) {
      console.error("Error uploading files: ", error);
    }
  };
  function handleClear() {
    setFiles(null);
  }
  function input_e_h(e) {
    setInputText(e.target.value);
  }
  async function handledb() {
    try {
      const response = await axios.post("http://localhost:5000/cleardb");
      const data = await response.json();
      alert(data.message);
      setOutputs([]);
    } catch (e) {
      console.log(e);
    }
  }
  return (
    <div className="file-upload-container">
      <h2>Multiple File Upload</h2>
      <input type="file" multiple onChange={handleChange} />
      <div className="buttons">
        <button onClick={handleSubmit}>Upload</button>
        <button onClick={handleClear}>Clear</button>
      </div>

      <div className="file-list">
        <h3>Selected Files:</h3>

        {files && (
          <ul>
            {files.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
        )}
      </div>
      <div className="chat-container">
        <h2>Chat Input</h2>
        <div>
          <input
            type="text"
            value={inputText}
            onChange={input_e_h}
            placeholder="Type your message here..."
          />
          <button onClick={handleInput}>send</button>
          <button onClick={handledb}>cleardb</button>
        </div>
        <div
          className="chat-output"
          style={{
            maxHeight: "300px",
            overflowY: "auto",
            border: "1px solid #ccc",
            padding: "10px",
          }}
        >
          <h3>Chat Output:</h3>
          {outputs.map((output, index) => (
            <p key={index}>{output}</p>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
