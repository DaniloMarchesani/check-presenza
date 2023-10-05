import React from 'react'
import './success.css'

function Success({status}) {
  return (
    <div className='style-success' style={ status.code == "404" ? {backgroundColor: "red"} : {backgroundColor: "green"}}>
        {status.code == "404" ? <p>Codice errato</p> : <p> {status.msg}</p>}
    </div>
  )
}

export default Success