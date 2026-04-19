from flask import Flask, render_template, request, redirect, session
from database import (init_db, add_matiere, get_matieres, add_controle
, get_controles, add_cours, get_cours,delete_cours,get_cour_by_id,update_cours
,update_matiere,delete_matiere,get_matiere_by_id,delete_controle,update_controle
,get_control_id_by_id,add_devoir,get_devoir_by_id,update_devoir,delete_devoir,
get_devoir,add_commentaires,get_commentaire_id_by_id,update_commentaires,delete_commentaires,
get_commentaires,add_user,get_user_by_username,add_prof,get_prof_by_id,update_prof,delete_prof,get_prof )
import datetime
from werkzeug.security import check_password_hash

datetime.datetime.now().isocalendar()[1]

app = Flask(__name__)
app.secret_key = 'carnet_scolaire_secret_2024'
@app.before_request
def before_request():
    init_db()
    pages_libres = ['/connexion', '/inscriptions']
    if request.path not in pages_libres and 'user' not in session:
        return redirect('/connexion')
@app.route('/')

def index():
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    vacances = [
        (datetime.date(2025, 10, 18), datetime.date(2025, 11, 2)),  # Toussaint
        (datetime.date(2025, 12, 20), datetime.date(2026, 1, 4)),  # Noël
        (datetime.date(2026, 2, 14), datetime.date(2026, 3, 1)),  # Hiver
        (datetime.date(2026, 4, 11), datetime.date(2026, 4, 26)),  # Printemps
        (datetime.date(2026, 7, 4), datetime.date(2026, 8, 31)),  # Été
    ]
    jours_feries = [
        datetime.date(2026, 1, 1),  # Jour de l'an
        datetime.date(2026, 4, 6),  # Lundi de Pâques
        datetime.date(2026, 5, 1),  # Fête du travail
        datetime.date(2026, 5, 8),  # Victoire 1945
        datetime.date(2026, 5, 14),  # Ascension
        datetime.date(2026, 5, 15),  # Pont Ascension
        datetime.date(2026, 5, 25),  # Pentecôte
    ]

    def est_jour_off(date):
        d = date.date()
        if d in jours_feries:
            return True
        for debut, fin in vacances:
            if debut <= d <= fin:
                return True
        return False
    weekday = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi']
    next_day = datetime.datetime.now() + datetime.timedelta(days=1)
    while next_day.weekday() >= 5 or est_jour_off(next_day):
        next_day = next_day + datetime.timedelta(days=1)
    nextday = weekday[next_day.weekday()]
    numero_semaine = datetime.datetime.now().isocalendar()[1]
    if numero_semaine % 2 == 0:
        semaine_actuelle = 'A'
    else:
        semaine_actuelle = 'B'

    les_cours = get_cours(user_id)
    les_controles = get_controles(user_id)
    les_matieres = get_matieres(user_id)
    next_day_date = next_day.strftime('%A %d %B')
    return render_template('index.html', les_cours=les_cours, les_controles=les_controles, les_matieres=les_matieres, next_day=next_day,semaine_actuelle=semaine_actuelle,nextday=nextday, next_day_date=next_day_date)


@app.route('/profil')
def profil():
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    return render_template('profil.html')
#matiere
@app.route('/matieres', methods=['GET', 'POST'])
def matieres():
    user_id = session.get('user_id')
    print("USER ID:", user_id)
    if 'user' not in session:
        return redirect('/connexion')
    if request.method == 'POST':
        nom = request.form['nom']
        couleur = request.form['couleur']
        add_matiere(nom, couleur, user_id)
    les_matieres = get_matieres(user_id)
    return render_template('matieres.html', les_matieres=les_matieres)
@app.route('/matieres/modifier/<id>', methods=['GET', 'POST'])
def modifier_matiere(id):
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    if request.method == 'POST':
        nom = request.form['nom']
        couleur = request.form['couleur']
        matiere = update_matiere(id,nom,couleur,user_id)
        return redirect('/matieres')
    matiere = get_matiere_by_id(id,user_id)
    return render_template('modifier_matiere.html', matiere=matiere)

@app.route('/matieres/supprimer/<id>', methods=['GET', 'POST'])
def supprimer_matiere(id):
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    delete_matiere(id,user_id)
    return redirect('/matieres')
#cours
@app.route('/cours', methods=['GET', 'POST'])
def cours():
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    if request.method == 'POST':
        titre = request.form['titre']
        contenu = request.form['contenu']
        matiere_id = request.form['matiere_id']
        devoirs =request.form['devoirs']
        jours =request.form['jours']
        semaine = request.form['semaine']
        heure = request.form['heure']
        prof = request.form['prof']
        salle = request.form['salle']
        add_cours(titre, contenu, matiere_id, devoirs,jours,semaine,heure,prof,salle,user_id)
    les_cours = get_cours(user_id)
    numero_semaine = datetime.datetime.now().isocalendar()[1]
    if numero_semaine % 2 == 0:
        semaine_actuelle = 'A'
    else:
        semaine_actuelle = 'B'
    les_matieres = get_matieres(user_id)
    les_prof = get_prof(user_id)
    return render_template('cours.html', les_cours=les_cours, semaine_actuelle=semaine_actuelle,les_matieres=les_matieres, les_prof=les_prof)
#control
@app.route('/controles', methods=['GET', 'POST'])
def controles():
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    if request.method == 'POST':
        titre = request.form['titre']
        date = request.form['date']
        matiere_id = request.form['matiere_id']
        add_controle(titre, date, matiere_id, None, user_id)
    les_controles = get_controles(user_id)
    les_matieres = get_matieres(user_id)
    return render_template('controles.html', les_controles=les_controles,les_matieres = les_matieres)
@app.route('/controles/modifier/<id>', methods=['GET', 'POST'])
def modifier_controle(id):
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    if request.method == 'POST':
        titre = request .form['titre']
        date = request.form['date']
        note = request.form['note']
        matiere_id = request.form['matiere_id']
        controle_id = update_controle(titre, date, matiere_id, note, id, user_id)
        return redirect('/controles')
    matieres = get_matieres(user_id)
    les_prof = get_prof(user_id)
    controle = get_control_id_by_id(id, user_id)
    return render_template('modifier_controle.html', controle=controle, les_matieres=matieres, les_prof=les_prof)
@app.route('/controles/supprimer/<id>')
def supprimer_controle(id):
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    delete_controle(id, user_id)
    return redirect('/controles')


#cours
@app.route('/cours/supprimer/<id>')
def supprimer_cours(id):
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    delete_cours(id, user_id)
    return redirect('/cours')


@app.route('/cours/modifier/<id>', methods=['GET', 'POST'])
def modifier_cours(id):
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    if request.method == 'POST':
        contenu = request.form['contenu']
        matiere_id = request.form['matiere_id']
        devoirs = request.form['devoirs']
        jours = request.form['jours']
        semaine = request.form['semaine']
        heure = request.form['heure']
        prof = request.form['prof']
        salle = request.form['salle']
        cours = update_cours(
            id,
            contenu,
            matiere_id,
            devoirs,
            jours,
            semaine,
            heure,
            prof,
            salle,
            user_id
        )
        les_matieres = get_matieres(user_id)
        return redirect('/cours')
    cours = get_cour_by_id(id, user_id)
    return render_template('modifier_cours.html', cours=cours, les_matieres=get_matieres(user_id))
#devoire
@app.route('/devoirs', methods=['GET', 'POST'])
def devoirs():
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    if request.method == 'POST':
        matiere_id = request.form['matiere_id']
        titre = request.form['titre']
        date = request.form['date']
        heure = request.form['heure']
        semaine = request.form['semaine']
        add_devoir(matiere_id, titre, date, heure, semaine, user_id)
    les_devoirs = get_devoir(user_id)
    les_matieres = get_matieres(user_id)
    return render_template('devoirs.html', les_devoirs=les_devoirs,les_matieres=les_matieres)

@app.route('/devoirs/modifier/<id>', methods=['GET', 'POST'])
def modifier_devoir(id):
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    if request.method == 'POST':
        matiere_id = request.form['matiere_id']
        titre = request.form['titre']
        date = request.form['date']
        heure = request.form['heure']
        semaine = request.form['semaine']
        update_devoir(id,matiere_id,titre, date, heure, semaine, user_id)
        return redirect('/devoirs')
    devoir = get_devoir_by_id(id, user_id)
    return render_template('modifier_devoir.html',devoir=devoir,les_matieres=get_matieres(user_id))

@app.route('/devoirs/supprimer/<id>')
def supprimer_devoir(id):
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    delete_devoir(id, user_id)
    return redirect('/devoirs')
#commentair
@app.route('/commentaires', methods=['GET', 'POST'])
def commetaire():
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    if request.method == 'POST':
        matiere_id = request.form['matiere_id']
        prof= request.form['prof']
        commentaire = request.form['commentaire']
        periode = request.form['periode']
        date = request.form['date']
        add_commentaires(matiere_id, prof, commentaire, periode, date, user_id)
    les_commentaire = get_commentaires(user_id)
    return render_template('commentaires.html', les_commentaire=les_commentaire, les_matieres=get_matieres(user_id))

@app.route('/commentaires/modifier/<id>', methods=['GET', 'POST'])
def modifier_commentaires(id):
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    if request.method == 'POST':
        matiere_id = request.form['matiere_id']
        prof= request.form['prof']
        commentaire = request.form['commentaire']
        periode = request.form['periode']
        date = request.form['date']
        update_commentaires(id, matiere_id, prof, commentaire, periode, date, user_id)
        return redirect('/commentaires')
    les_commentaires = get_commentaires(user_id)
    return render_template('commentaires.html', commentaires=les_commentaires,les_matieres=get_matieres(user_id))

@app.route('/commentaires/supprimer/<id>')
def supprimer_commentaires(id):
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    delete_commentaires(id, user_id)
    return redirect('/commentaires')
#vvvv
@app.route('/profs', methods=['GET', 'POST'])
def profs():
    user_id = session.get('user_id')
    if 'user' not in session:
        return redirect('/connexion')
    if request.method == 'POST':
        prof = request.form['prof']
        matiere_id = request.form['matiere_id']
        add_prof(matiere_id, prof, user_id)
        return redirect('/profs')
    les_profs = get_prof(user_id)
    return render_template("profs.html", les_matieres=get_matieres(user_id),les_prof=les_profs)

@app.route('/profs/modifier/<id>', methods=['GET', 'POST'])
def modifier_profs(id):
    user_id = session.get('user_id')
    if request.method == 'POST':
        matiere_id = request.form['matiere_id']
        prof= request.form['prof']
        update_prof(id, prof, matiere_id, user_id)
        return redirect('/profs')
    prof = get_prof_by_id(id, user_id)
    return render_template('modifier_profs.html', prof=prof, les_matieres=get_matieres(user_id))

@app.route('/profs/supprimer/<id>')
def supprimer_profs(id):
    if 'user' not in session:
        return redirect('/connexion')
    delete_prof(id, session.get('user_id'))
    return redirect('/profs')


#connexion/inscription
@app.route('/inscriptions', methods=['GET', 'POST'])
def inscriptions():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = add_user(username, password)
        return redirect('/connexion')
    return render_template('inscription.html')

@app.route('/connexion',methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and check_password_hash(user[2], password):
            session['user'] = username
            session['user_id'] = user[0]
            print("USER:", user)
            print("USER ID:", user[0])
            return redirect('/')
        else:
            return render_template('connexion.html', erreur="Identifiants incorrects")
    return render_template('connexion.html')

@app.route('/deconnexion')
def deconnexion():
    session.pop('user', None)
    return redirect('/connexion')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)