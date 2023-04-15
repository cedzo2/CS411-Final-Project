import pymysql

db = pymysql.connect(host='localhost',
                user='root',
                password='root_password',
                database='academicworld',
                charset='utf8mb4',
                port=3306,
                cursorclass=pymysql.cursors.DictCursor)

def sql_insert(input_value):
    with db.cursor() as cursor:
        sql = 'INSERT INTO faculty_rec SELECT faculty.id AS faculty_id, faculty.name AS faculty_name, keyword.name AS keyword_name, score FROM faculty, faculty_keyword, keyword WHERE faculty.id=faculty_keyword.faculty_id AND faculty_keyword.keyword_id=keyword.id AND NOT EXISTS (SELECT * FROM faculty_rec WHERE keyword="' + input_value + '") AND (keyword.name="' + input_value + '");'
        cursor.execute(sql)
        db.commit()
        sql = 'INSERT INTO pub_rec SELECT publication.id AS pub_id, title, keyword.name AS keyword, score FROM publication, publication_keyword, keyword WHERE publication.id=publication_keyword.publication_id AND publication_keyword.keyword_id=keyword.id AND NOT EXISTS (SELECT * FROM pub_rec WHERE keyword="' + input_value + '") AND (keyword.name="' + input_value + '");'
        cursor.execute(sql)
        db.commit()
    
def sql_delete(input_value):
    with db.cursor() as cursor:
        sql = 'DELETE FROM faculty_rec WHERE keyword="' + input_value + '";'
        cursor.execute(sql)
        db.commit()
        sql = 'DELETE FROM pub_rec WHERE keyword="' + input_value + '";'
        cursor.execute(sql)
        db.commit()

def sql_select():
    with db.cursor() as cursor:
        sql = 'SELECT DISTINCT keyword FROM faculty_rec UNION SELECT DISTINCT keyword FROM pub_rec;'
        cursor.execute(sql)
        result1 = cursor.fetchall()
        sql = 'SELECT faculty_name, COUNT(*) AS num_matches, SUM(score) AS total_score FROM faculty_rec GROUP BY faculty_id, faculty_name ORDER BY num_matches DESC, total_score DESC LIMIT 5;'
        cursor.execute(sql)
        result2 = cursor.fetchall()
        sql = 'SELECT title, COUNT(*) AS num_matches, SUM(score) AS total_score FROM pub_rec GROUP BY pub_id, title ORDER BY num_matches DESC, total_score DESC LIMIT 5;'
        cursor.execute(sql)
        result3 = cursor.fetchall()
        return result1, result2, result3

# "data mining"
# "computer science"
# "computer graphics"