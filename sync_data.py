import mysql.connector
from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    'jsonkey.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])

sheet_id='1RepNEonUEKlcCRk4LcJPOq9O1ZVQn20JNOUhffiLebw'
sheet_range = 'Sheet1'
output = build('sheets', 'v4', credentials=creds)
sheet = output.spreadsheets()
result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_range).execute()
values = result.get('values', [])


# MySQL database configuration
config = {
    'user': 'root',
    'host': '34.131.6.232',
    'database': 'Dbsheets'
}

data =values

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

table_name = 'final_table'
table_exist_query = f"SELECT COUNT(*) FROM information_schema.TABLES WHERE TABLE_NAME='{table_name}'"

cursor.execute(table_exist_query)

table_exist = cursor.fetchone()[0]

if table_exist:
    cursor.execute(f"DROP TABLE {table_name}")
    cnx.commit()

columns = ', '.join(f'`{col}` VARCHAR(255)' for col in data[0])
query = f"CREATE TABLE {table_name} ({columns})"
cursor.execute(query)

for row in data[1:]:
    values = ', '.join(f"'{val}'" for val in row)
    query = f"INSERT INTO {table_name} VALUES ({values})"
    cursor.execute(query)

cnx.commit()
cursor.close()
cnx.close()
print("Data Inserted WoW")