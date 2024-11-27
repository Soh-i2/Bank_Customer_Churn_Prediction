
import psycopg2


def db_conn():
    return psycopg2.connect(
        database="Bank_Customer",
        host="localhost",
        user="postgres",
        password="Sohini@2",
        port="5432"
    )


def init_db():
    try:
        conn = db_conn()
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            RowNumber SERIAL PRIMARY KEY,
            CustomerID INTEGER UNIQUE NOT NULL,
            Surname VARCHAR(50),
            CreditScore INTEGER,
            Geography VARCHAR(50),
            Gender VARCHAR(10),
            Age INTEGER,
            Tenure INTEGER,
            Balance NUMERIC(15, 2),
            NumOfProducts INTEGER,
            HasCrCard BOOLEAN,
            IsActiveMember BOOLEAN,
            EstimatedSalary NUMERIC(15, 2),
            Exited BOOLEAN,
            CreatedOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UpdatedOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CreatedBy VARCHAR(50),
            UpdatedBy VARCHAR(50)
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            PredictionID SERIAL PRIMARY KEY,
            CustomerID INTEGER NOT NULL REFERENCES customers(CustomerID) ON DELETE CASCADE,
            PredictionScore NUMERIC(5, 2) NOT NULL,
            PredictionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CreatedOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UpdatedOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CreatedBy VARCHAR(50),
            UpdatedBy VARCHAR(50)
        );
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully!")

    except Exception as e:
        print(f"Error initializing database: {e}")

# Main execution
if __name__ == "__main__":
    init_db()
