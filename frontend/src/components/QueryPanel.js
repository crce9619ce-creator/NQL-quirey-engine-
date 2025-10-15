import React, {useState} from 'react';
export default function QueryPanel({onResult}) {
  const [q, setQ] = useState('');
  const run = async () => {
    if (!q) return alert('Enter query');
    const res = await fetch('/api/query/', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({q})});
    const j = await res.json();
    onResult(j);
  };
  return (<div>
    <h3>Query</h3>
    <textarea value={q} onChange={e=>setQ(e.target.value)} rows={4} cols={60} />
    <br/>
    <button onClick={run}>Run</button>
  </div>);
}
