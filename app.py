

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
from datetime import datetime
import psycopg2
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt


# Load preprocessor and model
preprocessor = pickle.load(open('preprocessor.pkl', 'rb'))
rfc = pickle.load(open('rfc.pkl', 'rb'))

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'wLQq3pi2pltTQ3X3'  
jwt = JWTManager(app)


EMPLOYEES = {
    "Sohini": bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()),
    "employee2": bcrypt.hashpw("secure456".encode('utf-8'), bcrypt.gensalt()),
} 

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the username exists and password matches
    if username in EMPLOYEES and bcrypt.checkpw(password.encode('utf-8'), EMPLOYEES[username]):
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"error": "Invalid credentials"}), 401


def db_conn():
    return psycopg2.connect(
        database="Bank_Customer",
        host="localhost",
        user="postgres",
        password="Sohini@2",
        port="5432"
    )




@app.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    print("Predict endpoint reached")
    try:
       
        request_data = request.get_json()
        print("Received data:", request_data)

        if not request_data:
            return jsonify({"error": "No input data provided"}), 400
        data = request_data.get('data', {})  

        CustomerID = int(request_data.get('CustomerID', 0))
        Surname = str(request_data.get('Surname', '')).strip()
        CreditScore = int(request_data.get('CreditScore', 0))
        Age = int(request_data.get('Age', 0))
        Tenure = int(request_data.get('Tenure', 0))
        Balance = float(request_data.get('Balance', 0))
        NumOfProducts = int(request_data.get('NumOfProducts', 0))
        HasCrCard = bool(int(request_data.get('HasCrCard', 0)))  
        IsActiveMember = bool(int(request_data.get('IsActiveMember', 0)))  
        EstimatedSalary = float(request_data.get('EstimatedSalary', 0))
        Geography = str(request_data.get('Geography','Spain')).strip()
        Gender = str(request_data.get('Gender','Female')).strip()

        print("Geography:", Geography)  
        print("Gender:", Gender)  

        
        if Geography.lower() == "germany":
            Geography_Germany = 1
            Geography_Spain = 0
        elif Geography.lower() == "spain":
            Geography_Germany = 0
            Geography_Spain = 1
        else:
            Geography_Germany = 0
            Geography_Spain = 0
        Gender_Male = 1 if Gender.lower() == "male" else 0

    
        input_data = pd.DataFrame([[
            CreditScore, Age, Tenure, Balance, NumOfProducts, HasCrCard,
            IsActiveMember, EstimatedSalary, Geography, Gender
        ]], columns=[
            'CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard',
            'IsActiveMember', 'EstimatedSalary', 'Geography', 'Gender'
        ])

        print("Input data for preprocessing:", input_data)

        
        input_processed = preprocessor.transform(input_data)
        pred = rfc.predict(input_processed)[0]
        pred_proba = rfc.predict_proba(input_processed)[0][1] * 100 

        print("Extracted values:")
        print(f"CustomerID: {CustomerID}, Surname: {Surname}, CreditScore: {CreditScore}, Age: {Age}, "
        f"Tenure: {Tenure}, Balance: {Balance}, NumOfProducts: {NumOfProducts}, "
        f"HasCrCard: {HasCrCard}, IsActiveMember: {IsActiveMember}, EstimatedSalary: {EstimatedSalary}, "
        f"Geography: {Geography}, Gender: {Gender}")
        store_customer_data({
            "CustomerID": CustomerID,
            "Surname": Surname,
            "CreditScore": CreditScore,
            "Geography": Geography,
            "Gender": Gender,
            "Age": Age,
            "Tenure": Tenure,
            "Balance": Balance,
            "NumOfProducts": NumOfProducts,
            "HasCrCard": HasCrCard,
            "IsActiveMember": IsActiveMember,
            "EstimatedSalary": EstimatedSalary,
        }, pred)

        store_prediction_data(CustomerID, pred_proba)
        return jsonify({"prediction": int(pred)})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 400
def store_customer_data(data, prediction):
    try:
        conn = db_conn()
        if conn:
            print("Database connection successful")
        cur = conn.cursor()

        insert_query = """
        INSERT INTO customers (
            CustomerID, Surname, CreditScore, Geography, Gender, Age, Tenure, Balance, 
            NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Exited, 
            CreatedOn, UpdatedOn, CreatedBy, UpdatedBy
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        record = (
            data.get("CustomerID"),
            data.get("Surname"),
            data.get("CreditScore"),
            data.get("Geography"),
            data.get("Gender"),
            data.get("Age"),
            data.get("Tenure"),
            data.get("Balance"),
            data.get("NumOfProducts"),
            data.get("HasCrCard"),
            data.get("IsActiveMember"),
            data.get("EstimatedSalary"),
            bool(prediction),
            datetime.now(),
            datetime.now(),
            "admin",
            "admin"
        )
        print("Executing query with record:", record)
        cur.execute(insert_query, record)
        conn.commit()
        print("Data inserted successfully")
        cur.close()
        conn.close()
    except Exception as e:
        print("Error storing customer data:", e)       
def store_prediction_data(customer_id, prediction_score, created_by="admin"):
    try:
        conn = db_conn()
        if conn:
            print("Database connection successful for predictions table")
        cur = conn.cursor()

        
        insert_query = """
        INSERT INTO predictions (
            CustomerID, PredictionScore, PredictionDate, CreatedOn, UpdatedOn, CreatedBy, UpdatedBy
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        record = (
            customer_id,               
            float(prediction_score),   
            datetime.now(),            
            datetime.now(),            
            datetime.now(),           
            created_by,               
            created_by               
        )
        print("Executing query for predictions table with record:", record)
        cur.execute(insert_query, record)
        conn.commit()
        print("Prediction data inserted successfully")
        cur.close()
        conn.close()
    except Exception as e:
        print("Error storing prediction data:", e)

# Home route
@app.route('/')
def home():
    return "Welcome to the Customer Prediction App!"

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
