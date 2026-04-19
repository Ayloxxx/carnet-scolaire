from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

DATABASE = 'carnet.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY,
                    username TEXT,
                    password TEXT)''')


    cur.execute('''CREATE TABLE IF NOT EXISTS matieres (
                                                        id INTEGER PRIMARY KEY, 
                                                        nom  TEXT,
                                                        couleur  TEXT,
                                                        user_id INTEGER)
                ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS cours
                   (
                       id INTEGER PRIMARY KEY,
                       matiere_id INTEGER,
                       titre TEXT,
                       contenu TEXT,
                       devoirs TEXT,
                       jours TEXT,
                       semaine TEXT,
                       heure TEXT,
                       prof TEXT,
                       salle TEXT,
                       user_id INTEGER
                   )
    ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS controles (
    id integer PRIMARY KEY,
    matiere_id INTEGER,
    titre TEXT,
    note TEXT,
    date TEXT,
    user_id INTEGER
    )
    ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS devoir(
    id INTEGER PRIMARY KEY,
    matiere_id INTEGER,
    titre TEXT,
    contenu TEXT,
    date TEXT,
    heure TEXT,
    semaine TEXT,
    user_id INTEGER)
    ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS commentaires(
    id INTEGER PRIMARY KEY,
    matiere_id INTEGER,
    prof TEXT,
    commentaire TEXT,
    periode TEXT,
    date TEXT,
    user_id INTEGER)
    ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS profs(
                   id INTEGER PRIMARY KEY,
                   prof TEXT,
                   matiere_id INTEGER,
                   user_id INTEGER
                   )''')
    conn.commit()
    conn.close()

def get_matieres(user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM matieres WHERE user_id=? ''', (user_id,))
    result = cur.fetchall()
    conn.close()
    return result

def add_matiere(nom,couleur,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''INSERT INTO matieres (nom,couleur,user_id) VALUES (?,?,?)''', (nom,couleur,user_id,))
    conn.commit()
    conn.close()

def delete_matiere(id,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''DELETE FROM matieres WHERE id = ? AND user_id=?''', (id,user_id,))
    conn.commit()
    conn.close()

def update_matiere(id, nom, couleur,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE matieres SET nom=?,couleur=? WHERE id=? AND user_id=?''', (nom, couleur, id,user_id,))
    conn.commit()
    conn.close()

def get_matiere_by_id(id,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM matieres WHERE id = ? AND user_id=? ''', (id,user_id,))
    result = cur.fetchone()
    conn.close()
    return result

def get_controles(user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM controles WHERE user_id=?''',(user_id,))
    result = cur.fetchall()
    conn.close()
    return result

def add_controle(titre,date, matiere_id, note,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''INSERT INTO controles (titre,date,matiere_id,note,user_id ) VALUES (?,?,?,?,?)''', (titre, date, matiere_id,note,user_id,))
    conn.commit()
    conn.close()

def get_cours(user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM cours WHERE user_id=?''',(user_id,))
    result = cur.fetchall()
    conn.close()
    return result

def add_cours(titre,contenu,matiere_id,devoirs,jours,semaine,heure,prof,salle,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(''' INSERT INTO cours (titre,contenu,matiere_id,devoirs,jours,semaine,heure,prof,salle,user_id) VALUES (?,?,?,?,?,?,?,?,?,?)''', (titre,contenu,matiere_id,devoirs,jours,semaine,heure,prof,salle,user_id))
    conn.commit()
    conn.close()

def delete_cours(id,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''DELETE FROM cours WHERE id = ? AND user_id=?''', (id,user_id,))
    conn.commit()
    conn.close()

def get_cour_by_id(id,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM cours WHERE id = ? AND user_id=? ''', (id,user_id))
    result = cur.fetchone()
    conn.close()
    return result

def update_cours(id, contenu, matiere_id, devoirs, jours, semaine, heure, prof, salle,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE cours SET contenu=?, matiere_id=?, devoirs=?, jours=?, semaine=?, heure=?, prof=?, salle=? WHERE id=? AND user_id=?''', (contenu, matiere_id, devoirs, jours, semaine, heure, prof, salle, id,user_id,))
    conn.commit()
    conn.close()

def delete_controle(id,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''DELETE FROM controles WHERE id = ? AND user_id=?''', (id,user_id,))
    conn.commit()
    conn.close()

def get_control_id_by_id(id,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM controles WHERE id = ? AND user_id=?''', (id,user_id,))
    result = cur.fetchone()
    conn.close()
    return result

def update_controle(titre,date,matiere_id,note,id,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE controles SET  titre=?, date=?,matiere_id=?,note=? WHERE id=? AND user_id=?''', (titre,date,matiere_id,note,id,user_id,))
    conn.commit()
    conn.close()

def add_devoir(matiere_id, titre, date, heure, semaine,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO devoir (matiere_id, titre, date, heure, semaine,user_id) VALUES (?,?,?,?,?,?) ''',
        (matiere_id, titre, date, heure, semaine,user_id,)
    )
    conn.commit()
    conn.close()

def get_devoir_by_id(id,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM devoir WHERE id = ? AND user_id=?''', (id,user_id,))
    result = cur.fetchone()
    conn.close()
    return result

def update_devoir(id, titre, date,heure,semaine,matiere_id,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE devoir SET titre=?, date=?, heure=?, semaine=?, matiere_id=? WHERE id=? AND user_id=?''', (titre, date, heure, semaine, matiere_id, id, user_id))
    conn.commit()
    conn.close()

def delete_devoir(id,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''DELETE FROM devoir WHERE id = ? AND user_id=?''', (id,user_id,))
    conn.commit()
    conn.close()

def get_devoir(user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM devoir WHERE user_id=?''',(user_id,))
    result = cur.fetchall()
    conn.close()
    return result

def get_commentaires(user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM commentaires WHERE user_id=?''',(user_id,))
    result = cur.fetchall()
    conn.close()
    return result

def add_commentaires(matiere_id, prof, commentaire, periode, date,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''INSERT INTO commentaires (matiere_id,prof,commentaire,periode,date,user_id)  VALUES (?,?,?,?,?,?) ''', (matiere_id, prof, commentaire, periode, date,user_id,))
    conn.commit()
    conn.close()

def update_commentaires(id, matiere_id, prof, commentaire, periode, date, user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE commentaires SET matiere_id=?,prof=?, commentaire=?,periode=?,date=?,user_id=? WHERE id=? ''', (matiere_id, prof, commentaire, periode, date, user_id, id))
    conn.commit()
    conn.close()

def delete_commentaires(id,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''DELETE FROM commentaires WHERE id = ? AND user_id=?''', (id,user_id,))
    conn.commit()
    conn.close()

def get_commentaire_id_by_id(id,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM commentaires WHERE id = ? AND user_id=?''', (id,user_id))
    result = cur.fetchall()
    conn.close()
    return result

def add_user(username, password):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    password = generate_password_hash(password)
    cur.execute(
        '''INSERT INTO users (username, password) VALUES (?,?) ''', (username, password)
    )
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM users WHERE username = ? ''', (username,))
    result = cur.fetchone()
    conn.close()
    return result

def add_prof(matiere_id, prof,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO profs (matiere_id, prof,user_id) VALUES (?, ?,?)''',
        (matiere_id, prof,user_id,)
    )
    conn.commit()
    conn.close()

def get_prof_by_id(id,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM profs WHERE id = ? AND user_id=?''', (id,user_id))
    result = cur.fetchone()
    conn.close()
    return result

def update_prof(id, prof, matiere_id,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''UPDATE profs SET prof=?, matiere_id=? WHERE id=? AND user_id=?''', (prof, matiere_id, id,user_id))
    conn.commit()
    conn.close()

def delete_prof(id,user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''DELETE FROM profs WHERE id = ? AND user_id=?''', (id,user_id))
    conn.commit()
    conn.close()

def get_prof(user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM profs WHERE user_id=?''', (user_id,))
    result = cur.fetchall()
    conn.close()
    return result
