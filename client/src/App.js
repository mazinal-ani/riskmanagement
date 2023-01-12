import React, { useState } from 'react';

function StockWeightForm() {
  const [stockData, setStockData] = useState([]);
  const [weightData, setWeightData] = useState([]);
  const [confidenceLevel, setConfidenceLevel] = useState([]);
  const [initialInvestment, setInitialInvestment] = useState([]);
  const [timePeriod, setTimePeriod] = useState([]);
  const [responseData, setResponseData] = useState(null);

  function handleSubmit(event) {
    event.preventDefault();


    const data = {
      stockData,
      weightData,
      confidenceLevel,
      initialInvestment,
      timePeriod
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
        setResponseData(result);
      });
  }

  return (
    <div>
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
        <label>
          Confidence Level:
          <input
            type="text"
            value={confidenceLevel}
            onChange={event => setConfidenceLevel(event.target.value)}
          />
        </label>
        <br />
        <label>
          Initial Investment (Dollars):
          <input
            type="text"
            value={initialInvestment}
            onChange={event => setInitialInvestment(event.target.value)}
          />
        </label>
        <br />
        <label>
          Time Period (Days):
          <input
            type="text"
            value={timePeriod}
            onChange={event => setTimePeriod(event.target.value)}
          />
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>
      <div>
        {responseData === null ? (
          <h1>
            Hello
          </h1>
        ) : (
          <div>
            <h1>Here is your encrypted message:</h1>
            <h1>{responseData}</h1>
          </div>
        )}
      </div>
    </div>  
  );
}

export default StockWeightForm;