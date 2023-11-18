import psycopg2


def create_table(conn):
    with conn.cursor() as cur:
        cur.execute('''DROP TABLE Persons;''')
        cur.execute('''
         CREATE TABLE IF NOT EXISTS  Persons (
            id SERIAL PRIMARY KEY,
            name VARCHAR(40),
            surname VARCHAR(40),
            UNIQUE (name, surname),
            CHECK (name !~ '\s' AND surname !~ '\s'),
            email VARCHAR(40),
            --CHECK (email ~ '@'),
            phone TEXT[]
            );
            ''')
        conn.commit()
def create_client(conn, name, surname, email=None, phone=None):
    with conn.cursor() as cur:
        sql = '''INSERT INTO Persons(name, surname) VALUES(%s, %s)'''
        params = (name, surname)
        cur.execute(sql, params)
        conn.commit()
def add_phone(conn, name, surname, phone):
    with conn.cursor() as cur:
        sql = '''UPDATE Persons SET phone = ARRAY_APPEND(phone, %s)
            WHERE name = %s AND surname = %s;'''
        params = (phone, name, surname)
        cur.execute(sql, params)
        conn.commit()
def ammend_client_data(conn, name, surname, email=None, phone=None):
    if phone:
        with conn.cursor() as cur:

            sql = '''UPDATE Persons SET phone = NULL WHERE name = %s AND surname = %s;'''
            params = (name, surname)
            cur.execute(sql, params)

            sql = '''UPDATE Persons SET phone = ARRAY_APPEND(phone, %s) WHERE name = %s AND surname = %s;'''
            params = (phone, name, surname)
            cur.execute(sql, params)
            conn.commit()
    if email:
        with conn.cursor() as cur:
            sql = '''UPDATE Persons SET email = %s WHERE name = %s AND surname = %s;'''
            params = (email, name, surname)
            cur.execute(sql, params)
            conn.commit()


def delete_phone(conn, name, surname, phone):
    with conn.cursor() as cur:
        sql = '''UPDATE Persons SET phone = ARRAY_REMOVE(phone, %s) WHERE name = %s AND surname = %s;'''
        params = (phone, name, surname)
        cur.execute(sql, params)
        conn.commit()

def delete_client(conn, name, surname):
    with conn.cursor() as cur:
        sql = '''DELETE FROM Persons WHERE name = %s AND surname = %s;'''
        params = (name, surname)
        cur.execute(sql, params)
        conn.commit()

def search_engine(conn, text):

    ''' можно вводить часть значения, а не целиком'''

    search_list =[]
    with conn.cursor() as cur:
        sql = f"SELECT * FROM Persons WHERE array_to_string(phone,',') LIKE '%{text}%'"
        cur.execute(sql)
        res = cur.fetchall()
        if len(res)>=1:
            search_list += res

        sql = f"SELECT * FROM Persons WHERE " \
              f"name LIKE '%{text}%' " \
              f"OR surname LIKE '%{text}%' " \
              f"OR surname LIKE '%{text}%'"
        cur.execute(sql)
        res = cur.fetchall()
        if len(res) >=1:
            search_list += res
    return search_list


if __name__ == "__main__":
    conn = psycopg2.connect(database='sql_homework', user='postgres', password='fedor1980')

    # create_table(conn)

    # create_client(conn, name='John', surname='Dack')

    # add_phone(conn, name='John', surname='Dack', phone='+7777')

    # ammend_client_data(conn, name='John', surname='Dack', phone='+7', email='ddd')

    #delete_phone(conn, name='John', surname='Dack', phone='+8')

    # delete_client(conn, name='John', surname='Dack')

    # search_list = search_engine(conn, 'o')
    # for item in search_list:
    #     print(item)

    conn.close()