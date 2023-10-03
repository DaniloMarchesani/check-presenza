import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import Success from './Success'
import './App.css'

function App() {
  const [showSuccess, setShowSuccess] = useState(false)
  
  const sendValue = (e) => {
    e.preventDefault();
    //qui verra fatto il fetch al backend
    console.log("ciao")
    setShowSuccess(true);
    setTimeout( () => setShowSuccess(false), 2000)
  
  }

  return (
    <div>
      <form onSubmit={sendValue}>
        <div className='form-style'>
          <label htmlFor="codice">Inserisci Codice Studente</label>
          <input type="text" placeholder='Il tuo codice...'/>
        </div>
        <input type="submit" value="Entra" id="btnEntra"/>
      </form>

    {
      showSuccess ? <Success /> : null
    }
    

    </div>
  )
}

export default App
