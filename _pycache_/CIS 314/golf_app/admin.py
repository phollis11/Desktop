from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys, os, hashlib

def create_secure_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def open_db():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("golf.db")
    if not db.open():
        print("DB failed to open")
        sys.exit(1)

    # VERY IMPORTANT — enable foreign keys
    QSqlQuery().exec_("PRAGMA foreign_keys = ON;")

def clear_table(table_name):
    query = QSqlQuery()
    sql = f"DELETE FROM {table_name};"
    if query.exec_(sql):
        print(f"Table '{table_name}' cleared.")
    else:
        print(f"Failed to clear table '{table_name}': {query.lastError().text()}")

    if query.exec_(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';"):
        print(f"AUTOINCREMENT for '{table_name}' reset.")
    else:
        print(f"Failed to reset AUTOINCREMENT for '{table_name}': {query.lastError().text()}")

def clear_all_tables():
    tables = []#Change to clear multiple tables
    for t in tables:
        clear_table(t)


def create_course(name):
    query = QSqlQuery()
    query.prepare("INSERT INTO courses (course_name) VALUES (?)")
    query.addBindValue(name)
    query.exec_()


def create_hole(par, desc, front, middle, back, course_id, image):
    query = QSqlQuery()
    query.prepare("""
        INSERT INTO holes (par, desc, front_green, middle_green, back_green, course_id, image)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """)
    query.addBindValue(par)
    query.addBindValue(desc)
    query.addBindValue(front)
    query.addBindValue(middle)
    query.addBindValue(back)
    query.addBindValue(course_id)
    query.addBindValue(image)
    query.exec_()


def add_hole_to_course(hole_id, course_name):
    # find course id
    q = QSqlQuery()
    q.prepare("SELECT course_id FROM courses WHERE course_name = ?")
    q.addBindValue(course_name)
    q.exec_()

    if not q.next():
        return

    course_id = q.value(0)

    # update the hole to reference that course
    q2 = QSqlQuery()
    q2.prepare("UPDATE holes SET course_id = ? WHERE hole_id = ?")
    q2.addBindValue(course_id)
    q2.addBindValue(hole_id)
    q2.exec_()

    
def show_table(table_name):
    q = QSqlQuery(f"SELECT * FROM {table_name}")

    rec = q.record()
    column_count = rec.count()

    # print column names
    headers = []
    for i in range(column_count):
        headers.append(rec.fieldName(i))
    print("\nTABLE:", table_name)
    print(" | ".join(headers))
    print("-" * (len(" | ".join(headers))))

    # print rows
    while q.next():
        row = []
        for i in range(column_count):
            row.append(str(q.value(i)))
        print(" | ".join(row))

def drop_table(table_name):
    query = QSqlQuery()
    sql = f"DROP TABLE IF EXISTS {table_name};"
    if query.exec_(sql):
        print(f"Table '{table_name}' dropped.")
    else:
        print(f"Failed to drop table '{table_name}': {query.lastError().text()}")


    

if __name__  == "__main__":
    open_db()
    """
    clear_table("courses")
    clear_table("holes")

    create_course("Musket Ridge")
    #par, desc, front, middle, back, course_id
    create_hole(4, "Fairway: Left 225 Bunkers, Right Trees, Long 280. Green: Left hill, Right Bunker, Long Bunker", "5", "5", "5", 1, r"hole1.png"
    )
    create_hole(3, "Green: Left Short Bunker, Left Long Bunker, Right Long Bunker", "5", "5", "5", 1,r"hole2.png"
    )
    create_hole(4, "Fairway: Left Rough, Long Bunker, Right Short OB, Dogleg Fairway. Green: Left safe, Right Bunker, Long rough", "5", "5", "5", 1,r"hole3.png")
    create_hole(4, "Fairway: Left Trees/Bunker 240, Right Bunker/Steep Hill, Long Safe. Green: Left Safe, Right Bunker/Hill, Long Safe", "5", "5", "5", 1, r"hole4.png")
    """
    show_table("courses")
    show_table("holes")
    show_table("users")
    show_table("bags")
    show_table("rounds")
    show_table("scores")