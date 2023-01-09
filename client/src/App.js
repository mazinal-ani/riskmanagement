import React, { useState } from 'react';

function StockWeightForm() {
  const [stockData, setStockData] = useState([]);
  const [weightData, setWeightData] = useState([]);

  function handleSubmit(event) {
    event.preventDefault();


    const data = {
      stockData,
      weightData
    };


    fetch('http://127.0.0.1:5000/valueatrisk', {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(result => {
        console.log(result);
      });
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Stock Data:
        <input
          type="text"
          value={stockData}
          onChange={event => setStockData(event.target.value)}
        />
      </label>
      <br />
      <label>
        Weight Data:
        <input
          type="text"
          value={weightData}
          onChange={event => setWeightData(event.target.value)}
        />
      </label>
      <br />
      <button type="submit">Submit</button>
    </form>
  );
}

export default StockWeightForm;