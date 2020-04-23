import React from 'react';
import './App.css';

import Viz from './Viz';

function App() {
  return (
    <div className="App">
      <div className="side-panel" id="side-panel-container"></div>
      <Viz />
    </div>
  );
}

export default App;
