import sqlite3
import BazaDeDate
from flask import Flask, render_template, request, redirect, flash
import re


def regex(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None


app = Flask(__name__)

connection = sqlite3.connect(BazaDeDate.DATABASE_PATH, check_same_thread=False)
connection.create_function("REGEXP", 2, regex)


@app.route("/")
# ------------------DETALII MASINI------------------
@app.route("/detaliimasini")
def detaliimasini():
    details = []
    cur = connection.cursor()
    cur.execute('SELECT * FROM detaliimasini')
    curr = cur.fetchall()
    for rez in curr:
        detail = {}
        detail['nr_inmatriculare'] = rez[0]
        detail['model'] = rez[1]
        detail['an_fabricatie'] = rez[2]
        detail['serie_sasiu'] = rez[3]
        detail['valabilitate_itp'] = rez[4]
        details.append(detail)
    cur.close()
    return render_template('detaliimasini.html', details=details)


@app.route('/addDetails', methods=['POST'])
def add_details():
    if request.method == 'POST':
        cur = connection.cursor()
        values = []
        values.append("'" + request.form['nr_inmatriculare'] + "'")
        values.append("'" + request.form['model'] + "'")
        values.append("'" + request.form['an_fabricatie'] + "'")
        values.append("'" + request.form['serie_sasiu'] + "'")
        values.append("'" + request.form['valabilitate_itp'] + "'")
        fields = ['nr_inmatriculare', 'model', 'an_fabricatie', 'serie_sasiu', 'valabilitate_itp']
        query = 'INSERT INTO {} ({}) VALUES ({})'.format('detaliimasini', ', '.join(fields), ', '.join(values))
    try:
        cur.execute(query)
    except:
        cur.close()
        return redirect('/detaliimasini')
    # cur.execute("COMMIT")
    cur.close()
    return redirect('/detaliimasini')


@app.route('/deleteDetails', methods=['POST'])
def delete_details():
    pk = "'" + request.form['nr_inmatriculare'] + "'"
    cur = connection.cursor()
    cur.execute('DELETE FROM detaliimasini WHERE nr_inmatriculare=' + pk)
    # cur.execute("COMMIT")
    cur.close()
    return redirect('/detaliimasini')


@app.route('/getDetails', methods=['POST'])
def get_detalii():
    pk = "'" + request.form['nr_inmatriculare'] + "'"
    cur = connection.cursor()
    cur.execute("SELECT * FROM detaliimasini WHERE nr_inmatriculare=" + pk)
    dets = cur.fetchone()
    details = {}
    details['nr_inmatriculare'] = dets[0]
    details['model'] = dets[1]
    details['an_fabricatie'] = dets[2]
    details['serie_sasiu'] = dets[3]
    details['valabilitate_itp'] = dets[4]
    cur.close()
    return render_template("detaliimasiniEdit.html", details=details)


@app.route('/editDetails', methods=['POST'])
def edit_detalii():
    nr_inmatriculare = "'" + request.form['nr_inmatriculare'] + "'"
    model = "'" + request.form['model'] + "'"
    an_fabricatie = "'" + request.form['an_fabricatie'] + "'"
    serie_sasiu = "'" + request.form['serie_sasiu'] + "'"
    valabilitate_itp = "'" + request.form['valabilitate_itp'] + "'"
    cur = connection.cursor()
    query = "UPDATE detaliimasini SET model={}, an_fabricatie={}, serie_sasiu={}, valabilitate_itp={} WHERE nr_inmatriculare={}".format(
        model, an_fabricatie, serie_sasiu, valabilitate_itp, nr_inmatriculare)
    try:
        cur.execute(query)
    except:
        cur.close()
        return redirect('/detaliimasini')
    # cur.execute("COMMIT")
    cur.close()
    return redirect('/detaliimasini')


# ------------------DETALII MASINI------------------
# ---------------------PERSONAL---------------------
@app.route('/personal')
def personal():
    people = []
    cur = connection.cursor()
    cur.execute("SELECT * FROM personal")
    curr = cur.fetchall()
    for pers in curr:
        person = {}
        person['id_angajat'] = pers[0]
        person['nume'] = pers[1]
        person['id_meserie'] = pers[2]
        person['vechime'] = pers[3]
        person['salariu'] = pers[4]
        people.append(person)
    cur.close()
    return render_template('personal.html', people=people)


@app.route('/deletePersonal', methods=['POST'])
def delete_personal():
    pk = "'" + request.form['id_angajat'] + "'"
    cur = connection.cursor()
    cur.execute('DELETE FROM personal WHERE id_angajat=' + pk)
    # cur.execute("COMMIT")
    cur.close()
    return redirect('/personal')


@app.route('/addPersonal', methods=['POST'])
def add_personal():
    if request.method == 'POST':
        cur = connection.cursor()
        values = []
        values.append("'" + request.form['nume'] + "'")
        values.append("'" + request.form['id_meserie'] + "'")
        values.append("'" + request.form['vechime'] + "'")
        values.append("'" + request.form['salariu'] + "'")
        fields = ['nume', 'id_meserie', 'vechime', 'salariu']
        query = 'INSERT INTO {} ({}) VALUES({})'.format('personal', ', '.join(fields), ', '.join(values))
    try:
        cur.execute(query)
    except:
        cur.close()
        return redirect('/personal')
    # cur.execute("COMMIT")
    cur.close()
    return redirect('/personal')


@app.route('/getPersonal', methods=['POST'])
def get_personal():
    pk = "'" + request.form['id_angajat'] + "'"
    cur = connection.cursor()
    cur.execute("SELECT * FROM personal WHERE id_angajat=" + pk)
    pers = cur.fetchone()
    person = {}
    person['id_angajat'] = pers[0]
    person['nume'] = pers[1]
    person['id_meserie'] = pers[2]
    person['vechime'] = pers[3]
    person['salariu'] = pers[4]
    cur.close()
    return render_template("personalEdit.html", person=person)


@app.route('/editPersonal', methods=['POST'])
def edit_personal():
    id_angajat = "'" + request.form['id_angajat'] + "'"
    nume = "'" + request.form['nume'] + "'"
    id_meserie = "'" + request.form['id_meserie'] + "'"
    vechime = "'" + request.form['vechime'] + "'"
    salariu = "'" + request.form['salariu'] + "'"
    cur = connection.cursor()
    query = "UPDATE personal SET nume={}, id_meserie={}, vechime={}, salariu={} WHERE id_angajat={}".format(nume,
                                                                                                            id_meserie,
                                                                                                            vechime,
                                                                                                            salariu,
                                                                                                            id_angajat)
    try:
        cur.execute(query)
    except:
        cur.close()
        return redirect('/personal')
    # cur.execute("COMMIT")
    cur.close()
    return redirect("/personal")


# ---------------------PERSONAL---------------------
# ---------------------LUCRARI----------------------
@app.route('/lucrari')
def lucrari():
    works = []
    cur = connection.cursor()
    cur.execute('SELECT * FROM lucrari')
    curr = cur.fetchall()
    for lucrare in curr:
        work = {}
        work['id_lucrare'] = lucrare[0]
        work['nume_lucrare'] = lucrare[1]
        work['id_meserie'] = lucrare[2]
        work['cost_ora'] = lucrare[3]
        works.append(work)
    cur.close()
    return render_template('lucrari.html', works=works)


@app.route('/deleteLucrari', methods=['POST'])
def delete_lucrare():
    pk = "'" + request.form['id_lucrare'] + "'"
    cur = connection.cursor()
    cur.execute('DELETE FROM lucrari WHERE id_lucrare=' + pk)
    # cur.execute("COMMIT")
    cur.close()
    return redirect('/lucrari')


@app.route('/addLucrari', methods=['POST'])
def add_lucrari():
    if request.method == 'POST':
        cur = connection.cursor()
        values = []
        values.append("'" + request.form['nume_lucrare'] + "'")
        values.append("'" + request.form['id_meserie'] + "'")
        values.append("'" + request.form['cost_ora'] + "'")
        fields = ['nume_lucrare', 'id_meserie', 'cost_ora']
        query = 'INSERT INTO {} ({}) VALUES({})'.format('lucrari', ', '.join(fields), ', '.join(values))
    try:
        cur.execute(query)
    except:
        cur.close()
        return redirect('/lucrari')
    # cur.execute("COMMIT")
    cur.close()
    return redirect('/lucrari')


@app.route("/getLucrari", methods=['POST'])
def get_lucrari():
    pk = "'" + request.form['id_lucrare'] + "'"
    cur = connection.cursor()
    cur.execute("SELECT * FROM lucrari WHERE id_lucrare=" + pk)
    lucr = cur.fetchone()
    work = {}
    work['id_lucrare'] = lucr[0]
    work['nume_lucrare'] = lucr[1]
    work['id_meserie'] = lucr[2]
    work['cost_ora'] = lucr[3]
    cur.close()
    return render_template("lucrariEdit.html", work=work)


@app.route("/editLucrari", methods=['POST'])
def edit_lucrari():
    id_lucrare = "'" + request.form['id_lucrare'] + "'"
    nume_lucrare = "'" + request.form['nume_lucrare'] + "'"
    id_meserie = "'" + request.form['id_meserie'] + "'"
    cost_ora = "'" + request.form['cost_ora'] + "'"
    cur = connection.cursor()
    query = "UPDATE lucrari SET nume_lucrare={}, id_meserie={}, cost_ora={} WHERE id_lucrare={}".format(nume_lucrare,
                                                                                                        id_meserie,
                                                                                                        cost_ora,
                                                                                                        id_lucrare)
    try:
        cur.execute(query)
    except:
        cur.close()
        return redirect('/lucrari')
    # cur.execute("COMMIT")
    cur.close()
    return redirect("/lucrari")


# ---------------------LUCRARI----------------------
# ---------------------LUCRARIPERSONAL---------------
@app.route('/lucraripersonal')
def lucraripersonal():
    works = []
    cur = connection.cursor()
    cur.execute("SELECT * FROM lucraripersonal")
    curr = cur.fetchall()
    for lucrare in curr:
        work = {}
        work['id_serv_pers'] = lucrare[0]
        work['lucrari_id_lucrare'] = lucrare[1]
        work['personal_id_angajat'] = lucrare[2]
        works.append(work)
    personal = []
    cur.execute("SELECT id_angajat from personal")
    curr = cur.fetchall()
    for pers in curr:
        personal.append(pers)
    lucrari = []
    cur.execute("SELECT id_lucrare FROM lucrari")
    curr = cur.fetchall()
    for lucr in curr:
        lucrari.append(lucr)
    cur.close()
    return render_template("lucraripersonal.html", works=works, personal=personal, lucrari=lucrari)


@app.route("/deleteLucrariPersonal", methods=['POST'])
def delete_lucraripersonal():
    pk = "'" + request.form['id_serv_pers'] + "'"
    cur = connection.cursor()
    cur.execute("DELETE FROM lucraripersonal WHERE id_serv_pers=" + pk)
    # cur.execute("COMMIT")
    cur.close()
    return redirect("/lucraripersonal")


@app.route("/addLucrariPersonal", methods=['POST'])
def add_lucraripersonal():
    if request.method == 'POST':
        cur = connection.cursor()
        values = []
        values.append("'" + request.form['lucrari_id_lucrare'] + "'")
        values.append("'" + request.form['personal_id_angajat'] + "'")
        fields = ['lucrari_id_lucrare', 'personal_id_angajat']
        query = "INSERT INTO {} ({}) VALUES ({})".format('lucraripersonal', ', '.join(fields), ', '.join(values))
    cur.execute(query)
    # cur.execute("COMMIT")
    cur.close()
    return redirect("/lucraripersonal")


# ---------------------LUCRARIPERSONAL---------------
# ---------------------MASINI------------------------
@app.route("/masini")
def masini():
    cars = []
    cur = connection.cursor()
    cur.execute("SELECT * FROM masini")
    curr = cur.fetchall()
    for masina in curr:
        car = {}
        car['telefon_proprietar'] = masina[0]
        car['detaliimasini_nr_inmatriculare'] = masina[1]
        cars.append(car)
    details = []
    cur.execute("SELECT nr_inmatriculare FROM detaliimasini")
    curr = cur.fetchall()
    for det in curr:
        details.append(det[0])
    return render_template("masini.html", cars=cars, details=details)


@app.route("/deleteMasini", methods=['POST'])
def delete_masini():
    pk = "'" + request.form['detaliimasini_nr_inmatriculare'] + "'"
    cur = connection.cursor()
    cur.execute("DELETE FROM masini WHERE detaliimasini_nr_inmatriculare=" + pk)
    # cur.execute("COMMIT")
    cur.close()
    return redirect("/masini")


@app.route("/addMasini", methods=['POST'])
def add_masini():
    if request.method == 'POST':
        cur = connection.cursor()
        values = []
        values.append("'" + request.form['telefon_proprietar'] + "'")
        values.append("'" + request.form['detaliimasini_nr_inmatriculare'] + "'")
        fields = ['telefon_proprietar', 'detaliimasini_nr_inmatriculare']
        query = "INSERT INTO {} ({}) VALUES ({})".format('masini', ', '.join(fields), ', '.join(values))
    try:
        cur.execute(query)
    except:
        cur.close()
        return redirect('/masini')
    # cur.execute("COMMIT")
    cur.close()
    return redirect("/masini")


@app.route("/getMasini", methods=['POST'])
def get_masini():
    pk = "'" + request.form['detaliimasini_nr_inmatriculare'] + "'"
    cur = connection.cursor()
    cur.execute("SELECT * FROM masini WHERE detaliimasini_nr_inmatriculare=" + pk)
    masina = cur.fetchone()
    car = {}
    car['telefon_proprietar'] = masina[0]
    car['detaliimasini_nr_inmatriculare'] = masina[1]
    cur.close()
    return render_template("masiniEdit.html", car=car)


@app.route("/editMasini", methods=['POST'])
def edit_masini():
    detaliimasini_nr_inmatriculare = "'" + request.form['detaliimasini_nr_inmatriculare'] + "'"
    telefon_proprietar = "'" + request.form['telefon_proprietar'] + "'"
    cur = connection.cursor()
    query = "UPDATE masini SET telefon_proprietar={} WHERE detaliimasini_nr_inmatriculare={}".format(telefon_proprietar,
                                                                                                     detaliimasini_nr_inmatriculare)
    try:
        cur.execute(query)
    except:
        cur.close()
        return redirect('/masini')
    # cur.execute("COMMIT")
    cur.close()
    return redirect("/masini")


# ---------------------MASINI------------------------
# ---------------------REVIZII-----------------------
@app.route("/revizii")
def revizii():
    revizii = []
    cur = connection.cursor()
    cur.execute("UPDATE revizii SET pret=durata*(SELECT cost_ora FROM lucrari,lucraripersonal WHERE lucrari.id_lucrare=lucraripersonal.lucrari_id_lucrare AND lucraripersonal_id_serv_pers=lucraripersonal.id_serv_pers);")
    cur.execute("COMMIT")
    cur.execute("SELECT * FROM revizii")
    curr = cur.fetchall()
    for rez in curr:
        revizia = {}
        revizia['id_revizie'] = rez[0]
        revizia['lucraripersonal_id_serv_pers'] = rez[1]
        revizia['masini_nr_inmatriculare'] = rez[2]
        revizia['data_efectuarii'] = rez[3]
        revizia['tip_revizie'] = rez[4]
        revizia['durata'] = rez[5]
        revizia['pret']=rez[6]
        revizii.append(revizia)
    lucrari = []
    masini = []
    cur.execute("SELECT detaliimasini_nr_inmatriculare FROM masini")
    curr = cur.fetchall()
    for rez in curr:
        masini.append(rez[0])
    cur.execute("SELECT id_serv_pers FROM lucraripersonal")
    curr = cur.fetchall()
    for rez in curr:
        lucrari.append(rez[0])
    return render_template("revizii.html", lucrari=lucrari, masini=masini, revizii=revizii)


@app.route("/deleteRevizii", methods=['POST'])
def delete_revizii():
    pk = "'" + request.form['id_revizie'] + "'"
    cur = connection.cursor()
    cur.execute("DELETE FROM revizii WHERE id_revizie=" + pk)
    # cur.execute("COMMIT")
    cur.close()
    return redirect("/revizii")


@app.route("/addRevizii", methods=['POST'])
def add_revizii():
    if request.method == 'POST':
        cur = connection.cursor()
        values = []
        values.append("'" + request.form['lucraripersonal_id_serv_pers'] + "'")
        values.append("'" + request.form['masini_nr_inmatriculare'] + "'")
        values.append("'" + request.form['data_efectuarii'] + "'")
        values.append("'" + request.form['tip_revizie'] + "'")
        values.append("'" + request.form['durata'] + "'")
        fields = ['lucraripersonal_id_serv_pers', 'masini_nr_inmatriculare', 'data_efectuarii', 'tip_revizie', 'durata']
        query = "INSERT INTO {} ({}) VALUES ({})".format('revizii', ', '.join(fields), ', '.join(values))
    try:
        cur.execute(query)
    except:
        cur.close()
        return redirect('/revizii')
    # cur.execute("COMMIT")
    cur.close()
    return redirect("/revizii")


@app.route("/getRevizii", methods=['POST'])
def get_revizii():
    pk = "'" + request.form['id_revizie'] + "'"
    cur = connection.cursor()
    cur.execute("SELECT * FROM revizii WHERE id_revizie=" + pk)
    rez = cur.fetchone()
    revizie = {}
    revizie['id_revizie'] = rez[0]
    revizie['lucraripersonal_id_serv_pers'] = rez[1]
    revizie['masini_nr_inmatriculare'] = rez[2]
    revizie['data_efectuarii'] = rez[3]
    revizie['tip_revizie'] = rez[4]
    revizie['durata'] = rez[5]
    serviri = []
    masini = []
    cur.execute("SELECT detaliimasini_nr_inmatriculare FROM masini")
    curr = cur.fetchall()
    for rezu in curr:
        masini.append(rezu[0])
    cur.execute("SELECT id_serv_pers FROM lucraripersonal")
    curr = cur.fetchall()
    for rezu in curr:
        serviri.append(rezu[0])
    return render_template("reviziiEdit.html", revizie=revizie, serviri=serviri, masini=masini)


@app.route("/editRevizii", methods=['POST'])
def edit_revizii():
    id_revizie = "'" + request.form['id_revizie'] + "'"
    lucraripersonal_id_serv_pers = "'" + request.form['lucraripersonal_id_serv_pers'] + "'"
    masini_nr_inmatriculare = "'" + request.form['masini_nr_inmatriculare'] + "'"
    data_efectuarii = "'" + request.form['data_efectuarii'] + "'"
    tip_revizie = "'" + request.form['tip_revizie'] + "'"
    durata = "'" + request.form['durata'] + "'"
    cur = connection.cursor()
    query = "UPDATE revizii SET lucraripersonal_id_serv_pers={}, masini_nr_inmatriculare={}, data_efectuarii={}, tip_revizie={}, durata={} WHERE id_revizie={}".format(
        lucraripersonal_id_serv_pers, masini_nr_inmatriculare, data_efectuarii, tip_revizie, durata, id_revizie)
    try:
        cur.execute(query)
    except:
        cur.close()
        return redirect('/revizii')
    # cur.execute("COMMIT")
    cur.close()
    return redirect("/revizii")


# ---------------------REVIZII-----------------------

if __name__ == '__main__':
    app.run(debug=True)
    connection.close()
