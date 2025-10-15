import React, {useState} from 'react';
import DatabaseConnector from './components/DatabaseConnector';
import DocumentUploader from './components/DocumentUploader';
import QueryPanel from './components/QueryPanel';
import ResultsView from './components/ResultsView';

function App(){
  const [res, setRes] = useState(null);
  return (<div style={{padding:20,fontFamily:'Arial'}}>
    <h2>NLP Query Engine - React UI</h2>
    <DatabaseConnector />
    <DocumentUploader />
    <QueryPanel onResult={setRes} />
    <ResultsView result={res} />
  </div>);
}

export default App;
