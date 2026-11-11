import { useState } from 'react'
import Map from './components/Map'
import Panel from './components/Panel'
import Menubar from './components/Menubar'
import './App.css'


function App() {
  const [earthquakesOn, setEarthquakesOn] = useState(true)
  const [faultsOn, setFaultsOn] = useState(true)
  return (
    <div className="outer-container">
      <div className="menubar-container">
        <Menubar />
      </div>

      <div className="map-layout">
        <Panel earthquakesOn={earthquakesOn} setEarthquakesOn={setEarthquakesOn} faultsOn={faultsOn} setFaultsOn={setFaultsOn} />
        <Map earthquakesOn={earthquakesOn} faultsOn={faultsOn} />
      </div>
    </div>
  )
}

export default App
