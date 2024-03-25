import psycopg2
import pandas as pd
from IPython.core.display_functions import display

# 0. Our sample query
create_table_query = """
CREATE TABLE genders (
  id INT PRIMARY KEY,
  name VARCHAR(30),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

fill_table_query = """
INSERT INTO genders (id, name)
VALUES (1, 'male'), (2, 'female');
"""

select_info_query = """
SELECT * FROM genders;
"""


connection = psycopg2.connect(
    database="db", user='postgres',
    password='mysecretpassword', host='localhost', port=5432
)

cursor = connection.cursor()

# cursor.execute(create_table_query)
# cursor.execute(fill_table_query)
# connection.commit()


cursor.execute(select_info_query)
result = cursor.fetchall()
display(pd.DataFrame(result))

cursor.close()
connection.close()