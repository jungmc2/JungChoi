import mysql.connector
import pandas as pd



def return_uni_names():
    user = 'root'
    password = '123456yoyo'
    host = 'localhost' 
    conn = mysql.connector.connect(user=user, password=password, host=host, database='academicworld')
    query = "SELECT DISTINCT name FROM university"
    cursor = conn.cursor()
    cursor.execute(query) 
    prelim_data = cursor.fetchall()
    cursor.close()
    
    uni_names = pd.DataFrame(prelim_data, columns=['name'])
    
    return uni_names
    

def widget1_helper(selected_university):
    user = 'root'
    password = '123456yoyo'
    host = 'localhost' 
    conn = mysql.connector.connect(user=user, password=password, host=host, database='academicworld')
    query = f"""SELECT k.name FROM faculty f 
            INNER JOIN faculty_keyword fk  ON f.id = fk.faculty_id 
            INNER JOIN keyword k  ON fk.keyword_id = k.id 
            INNER JOIN university u 
            ON f.university_id = u.id  
            where u.name = '{selected_university}' """
    
    cursor = conn.cursor()
    cursor.execute(query) 
    prelim_data = cursor.fetchall()
    cursor.close()
    
    df = pd.DataFrame(prelim_data, columns = ['name'])
    counts = df.groupby('name')['name'].count().sort_values(ascending=False).values
    words = df.groupby('name')['name'].count().sort_values(ascending=False).index
    df = pd.DataFrame({'words':words, 'counts':counts})
    df = df.iloc[:10]

    return df

def widget2_helper(input_words):
    user = 'root'
    password = '123456yoyo'
    host = 'localhost' 
    conn = mysql.connector.connect(user=user, password=password, host=host, database='academicworld')
    output_query = f"""
            SELECT distinct f.name faculty, u.name university, p.title 
            FROM publication p 
            INNER JOIN publication_keyword pk 
            ON p.id = pk.publication_id 
            INNER JOIN keyword k 
            ON pk.keyword_id = k.id 
            INNER JOIN faculty_publication fp 
            ON p.id = fp.publication_id 
            INNER JOIN faculty f 
            ON fp.faculty_id = f.id
            INNER JOIN university u
            ON f.university_id = u.id 
            WHERE k.name = '{input_words}'
            LIMIT 30; 
    """
    
    view_query = f"""
            CREATE OR REPLACE VIEW user_selected_keyword as 
            SELECT distinct f.name faculty, u.name university, p.title 
            FROM publication p 
            INNER JOIN publication_keyword pk 
            ON p.id = pk.publication_id 
            INNER JOIN keyword k 
            ON pk.keyword_id = k.id 
            INNER JOIN faculty_publication fp 
            ON p.id = fp.publication_id 
            INNER JOIN faculty f 
            ON fp.faculty_id = f.id
            INNER JOIN university u
            ON f.university_id = u.id 
            WHERE k.name = '{input_words}'
            LIMIT 30; 
            """
    
    cursor = conn.cursor()
    cursor.execute(output_query) 
    prelim_data = cursor.fetchall()
    df = pd.DataFrame(prelim_data, columns = ['faculty','university','title'])
    cursor.close()

    cursor = conn.cursor()
    cursor.execute(view_query)
    cursor.close() 
    
    return df



def widget3_helper(input_words):
    user = 'root'
    password = '123456yoyo'
    host = 'localhost' 
    conn = mysql.connector.connect(user=user, password=password, host=host, database='academicworld')
    query = """SELECT university, COUNT(university) num_of_mentions
               FROM user_selected_keyword
               GROUP BY university
            """
    
    cursor = conn.cursor()
    cursor.execute(query) 
    prelim_data = cursor.fetchall()
    cursor.close()
    
    df = pd.DataFrame(prelim_data, columns = ['university','num_of_mentions'])
    
    return df


def get_colleges_final():
    user = 'root'
    password = '123456yoyo'
    host = 'localhost' 
    conn = mysql.connector.connect(user=user, password=password, host=host, database='academicworld')
    
    query = f"SELECT DISTINCT university_name FROM university_table"
    cursor = conn.cursor()
    cursor.execute(query)
    
    data = cursor.fetchall() 

    cursor.close()
    
    return data


def widget6_helper(query):
    user = 'root'
    password = '123456yoyo'
    host = 'localhost' 
    conn = mysql.connector.connect(user=user, password=password, host=host, database='academicworld')
    
    cursor = conn.cursor()
    cursor.execute(query) 
    prelim_data = cursor.fetchall()
    cursor.close()
    
    df = pd.DataFrame(prelim_data, columns = ['university_name', 'count_faculty', 'count_publications', 'most_frequent_keyword'])
    
    return df

def upload_final_table(university_name):
    user = 'root'
    password = '123456yoyo'
    host = 'localhost' 
    conn = mysql.connector.connect(user=user, password=password, host=host, database='academicworld')
    query = f"""CREATE OR REPLACE VIEW university_table AS 
               SELECT name as university_name, count_faculty, count_publications, keyword_name as most_frequent_keyword
               FROM university u
               INNER JOIN (SELECT university_id, count(*) as count_faculty
               FROM faculty 
               GROUP BY university_id) num_faculty
               ON u.id = num_faculty.university_id 
               INNER JOIN (SELECT u.id, count(p.id) count_publications
                           FROM faculty f 
                           INNER JOIN faculty_publication fp 
                           ON f.id = fp.faculty_id
                           INNER JOIN publication p
                           ON fp.publication_id = p.id
                           INNER JOIN university u 
                           ON u.id = f.university_id
                           GROUP BY u.id) num_publications
               ON u.id = num_publications.id
               INNER JOIN (SELECT id, keyword_name
                           FROM 
                           (SELECT id, keyword_name,  
                            ROW_NUMBER() OVER (PARTITION BY id ORDER BY count_of_keywords DESC) AS rn
                            FROM 
                            (SELECT u.id, k.name keyword_name, count(k.name) count_of_keywords
                            FROM faculty f 
                            INNER JOIN university u 
                            ON f.university_id = u.id 
                            INNER JOIN faculty_keyword fk 
                            ON f.id = fk.faculty_id 
                            INNER JOIN keyword k 
                            ON fk.keyword_id = k.id 
                            GROUP BY id, k.name) a) b
                            WHERE rn = 1) most_frequent_word
                            ON u.id = most_frequent_word.id
                WHERE name = '{university_name}'
                """
    
    constraint_query = """ALTER TABLE university 
                    MODIFY name VARCHAR(255) NOT NULL;
                    """
           
    cursor = conn.cursor()
    cursor.execute(query) 
    cursor.execute(constraint_query)
    cursor.close()    



    



    

    
    
    


    
    
    
