import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import Success from './Success'
import './App.css'

function App() {
  const [showSuccess, setShowSuccess] = useState(false);
  const [isEmpty, setIsEmpty] = useState('');
  const [code, setCode]=useState()
  const sendValue = (e) => {
    e.preventDefault();
    
    //qui verra fatto il fetch al backend
    fetch("http://127.0.0.1:5000/controlloPresenze", {
      method:"POST",
      headers:{"Content-type":"application/json",},
      body:JSON.stringify({codice:code})

    })
    console.log("ciao")
    setShowSuccess(true);
    setTimeout( () => setShowSuccess(false), 3000)
  
  }
  const handleCodeInput=(e)=>{
    checkIfEmpty(e)
    setCode(e.target.value)
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
          <input type="text" placeholder='Il tuo codice...' id='inputCodice' name='codice' onChange={handleCodeInput}/>
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
