import React, {useState} from 'react';

export default function DocumentUploader() {
  const [files, setFiles] = useState(null);
  const upload = async () => {
    if (!files) return alert('Choose files');
    const fd = new FormData();
    for (let f of files) fd.append('files', f);
    const res = await fetch('/api/ingest/documents', {method:'POST', body: fd});
    const j = await res.json();
    alert('Uploaded: ' + JSON.stringify(j));
  };
  return (<div>
    <h3>Upload Documents</h3>
    <input type="file" multiple onChange={e=>setFiles(e.target.files)} />
    <button onClick={upload}>Upload</button>
  </div>);
}
