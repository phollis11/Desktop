from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys, hashlib


#Admin.py was designed to make changes to the database outside of the app functionality
#Allows changes to courses, user information, clubs, and others.
#Not designed to actually be used by user

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


def create_hole(par, description, lat, lon, course_id, image):
    query = QSqlQuery()
    query.prepare("""
        INSERT INTO holes (par, description, lat, lon, course_id, image)
        VALUES (?, ?, ?, ?, ?, ?)
    """)
    query.addBindValue(par)
    query.addBindValue(description)
    query.addBindValue(lat)
    query.addBindValue(lon)
    query.addBindValue(course_id)
    query.addBindValue(image)
    if not query.exec_():
        print("Error inserting hole:", query.lastError().text())



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

def create_musket_ridge():
    # Create the course
    query = QSqlQuery()
    query.prepare("INSERT INTO courses (course_name) VALUES (?)")
    query.addBindValue("Musket Ridge")
    if not query.exec_():
        print("Error creating course:", query.lastError().text())
        return

    # Get the new course_id
    course_id = query.lastInsertId()

    holes = [
        (4, "Fairway: Left 225 Bunkers, Right Trees, Long 280. Green: Left hill, Right Bunker, Long Bunker", 
         39.494167, -77.547778, "hole1.png"),

        (3, "Green: Left Short Bunker, Left Long Bunker, Right Long Bunker", 
         39.49472222, -77.54666667, "hole2.png"),

        (4, "Fairway: Left Rough, Long Bunker, Right Short OB, Dogleg Fairway. Green: Left safe, Right Bunker, Long rough", 
         39.49611111, -77.54972222, "hole3.png"),

        (4, "Fairway: Left Trees/Bunker 240, Right Bunker/Steep Hill, Long Safe. Green: Left Safe, Right Bunker/Hill, Long Safe", 
         39.49777778, -77.55250000, "hole4.png"),

        (4, "Fairway:Left Treeline, Right bunkers and hill. Green: Left large bunker, Right Safe, Long bad", 
         0, 0, "hole5.png"),

        (5, "Fairway: Left OB, Left long bunkers, Right Safe rough. Layup zone 100 yards from green. Green: Bunker left and ob, Ob long, ob right", 
         0, 0, "hole6.png"),

        (4, "Fairway: Left OB, Right rough, hill, trees. Green: Bunker left, right rough, long rough/ob.", 
         0, 0, "hole7.png"),

        (3, "Green: Bunker Short Left, Bunker Right Long Green", 
         0, 0, "hole8.png"),

        (5, "Fairway: Left rough, right trees, 300 mid left bunkers, Green: Left hill, long hill, right bunker short and long", 
         0, 0, "hole9.png"),

        (5, "Fairway: Trees/hill left, Bunker/hill right, Layup Short right of green. Green: Bunkers Short Left, Bunker Left, Bunker right", 
         0, 0, "hole10.png"),

        (4, "Fairway: Dogleg left, Short left bunkers/ob, Right Bunkers/hill, Short layup zone, Long layup zone over bunkers on left. Green: Bunker left, bunker short, bunker right, long slope.", 
         0, 0, "hole11.png"),

        (5, "Fairway: Dogleg left. Left OB trees, 225 bunkers. Bunkers right entire hole. Left safe 2nd shot. Green: Bunker Short, Bunker Right, Left/long safe.", 
         0, 0, "hole12.png"),

        (3, "Green: Bunker left, bunker right, narrow green front", 
         0, 0, "hole13.png"),

        (4, "Fairway: Bunker left 220, Right rough. Green: Bunker short left, bunker right.", 
         0, 0, "hole14.png"),

        (4, "Fairway: Left trees, right ob. Green: Right ob/bunker, left safe, long ob.", 
         0, 0, "hole15.png"),

        (4, "Fairway: Dogleg right, left hill/trees safer, right ob, 220 safe middle. Green: short safe, ob right/long", 
         0, 0, "hole16.png"),

        (3, "Green: Left bunkers, right bunker, long hill, short big slope", 
         0, 0, "hole17.png"),

        (4, "Fairway: left bunker/trees, right hill/rough Green: Left bunkers, right safe, long hill", 
         0, 0, "hole18.png"),
    ]

    # Insert all holes
    for par, desc, lat, lon, image in holes:
        q = QSqlQuery()
        q.prepare("""
            INSERT INTO holes (par, description, lat, lon, course_id, image)
            VALUES (?, ?, ?, ?, ?, ?)
        """)
        q.addBindValue(par)
        q.addBindValue(desc)
        q.addBindValue(lat)
        q.addBindValue(lon)
        q.addBindValue(course_id)
        q.addBindValue(image)

        if not q.exec_():
            print("Error inserting hole:", q.lastError().text())

    print("✔ Musket Ridge course and all 18 holes created successfully!")

if __name__  == "__main__":
    open_db()
    #This should create musket ridge
    create_musket_ridge()

    #If not this can be uncommented to manually create the course and each hole in the course
    """
    create_course("Musket Ridge")
    #hole_id, par, desc, lat, lon, course_id, image

    create_hole(4, "Fairway: Left 225 Bunkers, Right Trees, Long 280. Green: Left hill, Right Bunker, Long Bunker", 39.494167, -77.547778, 1, "hole1.png"
    )
    create_hole(3, "Green: Left Short Bunker, Left Long Bunker, Right Long Bunker", 39.49472222, -77.54666667, 1,"hole2.png"
    )
    create_hole(4, "Fairway: Left Rough, Long Bunker, Right Short OB, Dogleg Fairway. Green: Left safe, Right Bunker, Long rough", 39.49611111, -77.54972222, 1,"hole3.png")
    create_hole(4, "Fairway: Left Trees/Bunker 240, Right Bunker/Steep Hill, Long Safe. Green: Left Safe, Right Bunker/Hill, Long Safe", 39.49777778, -77.55250000, 1, "hole4.png")
    create_hole(4, "Fairway:Left Treeline, Right bunkers and hill. Green: Left large bunker, Right Safe, Long bad", 0, 0, 1, "hole5.png")
    create_hole(5, "Fairway: Left OB, Left long bunkers, Right Safe rough. Layup zone 100 yards from green. Green: Bunker left and ob, Ob long, ob right", 0, 0, 1, "hole6.png")
    create_hole(4, "Fairway: Left OB, Right rough, hill, trees. Green: Bunker left, right rough, long rough/ob.", 0, 0, 1, "hole7.png")
    create_hole(3, "Green: Bunker Short Left, Bunker Right Long Green", 0, 0, 1, "hole8.png")
    create_hole(5, "Fairway: Left rough, right trees, 300 mid left bunkers, Green: Left hill, long hill, right bunker short and long", 0, 0, 1, "hole9.png")
    create_hole(5, "Fairway: Trees/hill left, Bunker/hill right, Layup Short right of green. Green: Bunkers Short Left, Bunker Left, Bunker right", 0, 0, 1, "hole10.png")
    create_hole(4, "Fairway: Dogleg left, Short left bunkers/ob, Right Bunkers/hill, Short layup zone, Long layup zone over bunkers on left. Green: Bunker left, bunker short, bunker right, long slope.", 0, 0 ,1, "hole11.png")
    create_hole(5, "Fairway: Dogleg left. Left OB trees, 225 bunkers. Bunkers right entire hole. Left safe 2nd shot. Green: Bunker Short, Bunker Right, Left/long safe.", 0, 0, 1, "hole12.png")
    create_hole(3, "Green: Bunker left, bunker right, narrow green front", 0, 0 , 1, "hole13.png")
    create_hole(4, "Fairway: Bunker left 220, Right rough. Green: Bunker short left, bunker right.", 0, 0 , 1, "hole14.png")
    create_hole(4, "Fairway: Left trees, right ob. Green: Right ob/bunker, left safe, long ob.", 0, 0, 1, "hole15.png")
    create_hole(4, "Fairway: Dogleg right, left hill/trees safer, right ob, 220 safe middle. Green: short safe, ob right/long", 0, 0, 1, "hole16.png")
    create_hole(3, "Green: Left bunkers, right bunker, long hill, short big slope", 0,0,1, "hole17.png")
    create_hole(4, "Fairway: left bunker/trees, right hill/rough Green: Left bunkers, right safe, long hill", 0, 0, 1, "hole18.png")
    """
    
    show_table("courses")
    show_table("holes")
    show_table("users")
    show_table("bags")
    show_table("rounds")
    show_table("scores")