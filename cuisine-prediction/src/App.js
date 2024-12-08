import React, { useState } from 'react';
import axios from "axios"; 

function App() {
  const [ingredient, setIngredient] = useState('');
  const [ingredientList, setIngredientList] = useState([]);
  const [prediction, setPrediction] = useState(null);

  const handleIngredientValue = (e) => {
    setIngredient(e.target.value);
  };

  const handleAddIngredient = () => {
    setIngredientList((prevList) => [...prevList, ingredient.trim()]);
    setIngredient(''); 
    
  };

  const handleClear = () => {
    setIngredientList([]); // Reset the list of ingredients
    setIngredient(''); // Clear the input field
  };

  const handleSubmit = event => {
    
    event.preventDefault();
    axios.post('https://vinayakg311.pythonanywhere.com/predict',ingredientList).then(
      res => {
        console.log(res);
        setPrediction(res.data.output)});
    
  };
  
  return (
    <div style={{ width:'350px', margin:'0 auto',padding:'20px', textAlign: 'center' }}>
      <div>
        <input
          type="text"
          value={ingredient}
          onChange={handleIngredientValue}
          placeholder="Enter an ingredient"
        />
        <button onClick={handleAddIngredient}>+</button>
      </div>
      <ul>
        {ingredientList.map((ing, index) => (
          <li key={index}>{ing}</li>
        ))}
      </ul>
        <button type="submit" style={{ padding:'10px 20px',marginTop:'10px'}} onClick={handleSubmit}>Predict</button>
        <button style={{ padding:'10px 20px',marginTop:'10px'}} onClick={handleClear}>Clear</button>
      {prediction && (
        <div style={{ marginTop:'20px',color: 'red' }}>
          <strong>Prediction:</strong> {prediction}
        </div>
      )}
    </div>
  );
}

export default App;
