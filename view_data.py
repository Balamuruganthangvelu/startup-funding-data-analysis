import pandas as pd
from db_connect  import get_connection
conn = get_connection()
query = "SELECT * FROM startup_funding_data"
df = pd.read_sql(query, conn)
print(df.head())
conn.close()