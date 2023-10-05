import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import Success from './Success'
import './App.css'

function App() {
  const [showSuccess, setShowSuccess] = useState(false);
  const [isEmpty, setIsEmpty] = useState('');
  
  const sendValue = (e) => {
    e.preventDefault();
    //qui verra fatto il fetch al backend
    console.log("ciao")
    setShowSuccess(true);
    setTimeout( () => setShowSuccess(false), 3000)
  
  }

  const checkIfEmpty = (e) => {
    const valore = e.target.value;
    if(valore && valore.length > 5) {
      setIsEmpty(valore);
    } else {
      setIsEmpty(false)
    }
    
  }

  return (
    <div>
      <h1>Check Presenza</h1>
      <form onSubmit={sendValue}>
        <div className='form-style'>
          <label htmlFor="codice">Inserisci Codice Studente</label>
          <input type="text" placeholder='Il tuo codice...' id='inputCodice' name='codice' onChange={checkIfEmpty}/>
        </div>
        <button type="submit" id="btnEntra" disabled={!isEmpty}>Invia</button>
      </form>
      <p className='danger' hidden={isEmpty}>Il tuo codice deve essere di almeno 5 caratteri...</p>

    {
      showSuccess ? <Success /> : null
    }
    

    </div>
  )
}

export default App
