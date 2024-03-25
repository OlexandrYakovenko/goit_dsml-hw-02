#import psycopg2
import psycopg2
import pandas as pd
from IPython.core.display_functions import display

import faker
from random import randint, choice


QUANTITY_USERS=10
QUANTITY_TASKS=15

def generate_fake_users(quantity_users) -> tuple():
    fake_fullname = []# тут зберігатимемо ФІО
    fake_email = []# тут зберігатимемо email, мають бути унікальними
    
    #fake_data = faker.Faker('ua_UA') #на жаль, українська локалізація відсутня
    fake_data = faker.Faker()
    
    # Створимо набір компаній у кількості number_companies
    for _ in range(quantity_users):
        fake_fullname.append(fake_data.name())
        
    for _ in range(quantity_users):
        fake_email.append(fake_data.unique.email())
        
    return fake_fullname, fake_email

def generate_fake_tasks(quantity_tasks) -> tuple():
    fake_title = []
    fake_description = []
    
    fake_data = faker.Faker()
    
    for _ in range(quantity_tasks):
        fake_title.append(fake_data.sentence())

    for _ in range(quantity_tasks):
        fake_description.append(fake_data.text())
        
    return fake_title, fake_description    



def prepare_data(fake_fullname, fake_email, fake_title, fake_description) -> tuple():
    for_users = []
    for_tasks = []
    
    size_of_users = len(fake_fullname)
    for fn_index in range(size_of_users):
        for_users.append((fn_index + 1, fake_fullname[fn_index], fake_email[fn_index]))
    
    size_of_tasks = len(fake_title)
    for fn_index in range(size_of_tasks):
        for_tasks.append((fn_index + 1, fake_title[fn_index], fake_description[fn_index], randint(1,3),randint(1,size_of_users)))  
    
    return  for_users, for_tasks 



def insert_data_to_db(for_users, for_tasks) -> None:
    connection = psycopg2.connect(
        database="db", user='postgres',
        password='mysecretpassword', host='localhost', port=5432
    )

    cursor = connection.cursor()



    sql_to_tasks_delete = """
    DELETE FROM public.tasks;
    """
    cursor.execute(sql_to_tasks_delete)
   
    sql_to_users_delete = """
    DELETE FROM public.users;
    """
    cursor.execute(sql_to_users_delete)
   
    sql_to_status_delete = """
    DELETE FROM public.status;
    """
    cursor.execute(sql_to_status_delete)
    
    
    
    sql_to_status = """
    INSERT INTO public.status
    (id, "name")
    values
    (1, ('new')),
    (2, ('in progress')),
    (3, ('completed'))
    ;
    """
    cursor.execute(sql_to_status)
    
     
    sql_to_users = """
    INSERT INTO public.users
    (id, fullname, email)
    VALUES( %s, %s, %s);
    """
    cursor.executemany(sql_to_users,for_users)
    
     
    sql_to_tasks = """
    INSERT INTO public.tasks
    (id, title, description, status_id, user_id)
    VALUES( %s, %s, %s, %s, %s);
    """
    cursor.executemany(sql_to_tasks,for_tasks)
    
    
    connection.commit()
    
    cursor.close()
    connection.close()
    
if __name__ == "__main__": 
    
    fake_fullname, fake_email = generate_fake_users(QUANTITY_USERS)
    fake_title, fake_description = generate_fake_tasks(QUANTITY_TASKS)
    
    for_users, for_tasks = prepare_data(fake_fullname, fake_email, fake_title, fake_description)
    
    insert_data_to_db(for_users, for_tasks)   
