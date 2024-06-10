import React, { useState } from "react";
import axios from "axios";

const FileUpload = () => {
  const [files, setFiles] = useState(null);

  const handleChange = (event) => {
    setFiles(event.target.files);
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

  return (
    <div>
      <h2>Multiple File Upload</h2>
      <input type="file" multiple onChange={handleChange} />
      <button onClick={handleSubmit}>Upload</button>
      <button onClick={handleClear}>Clear</button>
    </div>
  );
};

export default FileUpload;
