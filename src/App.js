import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./App.css";


function App() {
    const [formData, setFormData] = useState({
        CustomerID: '', 
        Surname: '', 
        CreditScore: '',
        Age: '',
        Tenure: '',
        Balance: '',
        NumOfProducts: '',
        HasCrCard: '',
        IsActiveMember: '',
        EstimatedSalary: '',
        Geography: '',
        Gender: ''
    });
    const [prediction, setPrediction] = useState(null);


    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
        console.log("Updated formData:", formData); 
    };
   
    const handleSubmit = async (e) => {
        e.preventDefault();
    
        // Retrieve the token from localStorage
        const token = localStorage.getItem('jwt');
        if (!token) {
            console.error("No token found. Please log in first.");
            alert("No token found. Please log in.");
            return; 
        }
    
        
        try {
            const response = await fetch('http://localhost:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`, 
                },
                body: JSON.stringify(formData), 
            });
    
            if (!response.ok) {
                const errorMessage = await response.text();
                console.error("Error response:", errorMessage);
                alert("Failed to fetch prediction. Please check your input or login status.");
                return;
            }
    
            // Parse the JSON response
            const result = await response.json();
            console.log("Response:", result);
    
    
            setPrediction(result.prediction);
        } catch (error) {
            
            console.error("Error fetching prediction:", error);
            alert("An error occurred while fetching prediction. Please try again.");
        }
    };

    return (
        <div className="container mt-5">
            <h1 className="text-center text-success">Bank Customer Churn Prediction</h1>
            <form onSubmit={handleSubmit} className="mt-4">
             {/* CustomerID */}
             <div className="form-group">
                    <label>Customer ID</label>
                    <input
                        type="number"
                        name="CustomerID"
                        value={formData.CustomerID}
                        onChange={handleChange}
                        className="form-control"
                        required
                    />
                </div>
                 {/* Surname */}
                 <div className="form-group">
                    <label>Surname</label>
                    <input
                        type="text"
                        name="Surname"
                        value={formData.Surname}
                        onChange={handleChange}
                        className="form-control"
                        required
                    />
                </div>
                {/* CreditScore */}
                <div className="form-group">
                    <label>Credit Score</label>
                    <input type="number" name="CreditScore" value={formData.CreditScore} onChange={handleChange} className="form-control" />
                </div>
                {/* Age */}
                <div className="form-group">
                    <label>Age</label>
                    <input type="number" name="Age" value={formData.Age} onChange={handleChange} className="form-control" />
                </div>
                {/* Tenure */}
                <div className="form-group">
                    <label>Tenure</label>
                    <input type="number" name="Tenure" value={formData.Tenure} onChange={handleChange} className="form-control" />
                </div>
                {/* Balance */}
                <div className="form-group">
                    <label>Balance</label>
                    <input type="number" name="Balance" value={formData.Balance} onChange={handleChange} className="form-control" />
                </div>
                {/* NumOfProducts */}
                <div className="form-group">
                    <label>Number of Products</label>
                    <input type="number" name="NumOfProducts" value={formData.NumOfProducts} onChange={handleChange} className="form-control" />
                </div>
                {/* HasCrCard */}
                <div className="form-group">
                    <label>Has Credit Card</label>
                    <input type="number" name="HasCrCard" value={formData.HasCrCard} onChange={handleChange} className="form-control" />
                </div>
                {/* IsActiveMember */}
                <div className="form-group">
                    <label>Is Active Member</label>
                    <input type="number" name="IsActiveMember" value={formData.IsActiveMember} onChange={handleChange} className="form-control" />
                </div>
                {/* EstimatedSalary */}
                <div className="form-group">
                    <label>Estimated Salary</label>
                    <input type="number" name="EstimatedSalary" value={formData.EstimatedSalary} onChange={handleChange} className="form-control" />
                </div>
                {/* Geography */}
                <div className="form-group">
                    <label>Geography</label>
                    <input type="text" name="Geography" value={formData.Geography} onChange={handleChange} className="form-control" />
                </div>
                {/* Gender */}
                <div className="form-group">
                    <label>Gender</label>
                    <input type="text" name="Gender" value={formData.Gender} onChange={handleChange} className="form-control" />
                </div>

                <button type="submit" className="btn btn-primary mt-4">Predict</button>
            </form>

            {/* Display Prediction Result */}
            {prediction !== null && (
                <div className="mt-5 text-center">
                    <h2 className={prediction === 1 ? "text-danger" : "text-success"}>
                        {prediction === 1 ? "Customer will leave the bank" : "Customer will not leave the bank"}
                    </h2>
                </div>
            )}
        </div>
    );
}

export default App;
