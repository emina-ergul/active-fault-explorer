import Map from './components/Map'
import Panel from './components/Panel'
// import { useState } from 'react'
import './App.css'


function App() {
  return (
    <div>
      <h1>Seismic Explorer</h1>
      <div className="container" style={{ display: 'flex', flexDirection: 'row' }}>
        <Panel />
        <Map />
      
    </div>
    </div>
    
  )
}

export default App
