import React from 'react';
export default function ResultsView({result}) {
  return (<div>
    <h3>Results</h3>
    <pre>{JSON.stringify(result, null, 2)}</pre>
  </div>);
}
