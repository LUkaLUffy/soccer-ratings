from extensions import app, db
from flask import  render_template, redirect, flash
from forms import RegisterF, LoginF, Vote
from models import Accounts
from flask_login import login_user, logout_user


footballers = {
    "allister" : {
                    "link" : "/static/allisterL.webp" ,
                    "info" : "Alexis Mac Allister is an Argentine midfielder known for his technical skill and creativity, playing for Brighton & Hove Albion in the Premier League.",
                    "id" : "1"},
    "camavinga" : {
                    "link" : "/static/camavingaL.webp" ,
                    "info" : "Eduardo Camavinga is a French midfielder known for his composure, passing ability, and playing for Real Madrid after transferring from Rennes in Ligue 1",
                    "id" : "2"},
    "debruin" : {
                    "link" : "/static/debruinL.webp" ,
                    "info" : "Kevin De Bruyne is a Belgian midfielder renowned for his vision, passing accuracy, and ability to control the game, playing for Manchester City in the Premier League.",
                    "id" : "3"},
    "fernandez" : {
                    "link" : "/static/fernandezL.webp" ,
                    "info" : "Bruno Fernandes is a Portuguese midfielder known for his creativity, goal-scoring ability, and leadership at Manchester United in the Premier League.",
                    "id" : "4"},
    "gabriel" : {
                    "link" : "/static/gabrielL.webp" ,
                    "info" : "Gabriel Barbosa, commonly known as Gabigol, he is a Brazilian forward known for his goal-scoring prowess, playing for Flamengo in Brazil and occasionally the Brazil national team.",
                    "id" : "5"},
    "haaland" : {
                    "link" : "/static/haalandL.webp" ,
                    "info" : "Erling Haaland is a Norwegian striker known for his exceptional pace, strength, and goal-scoring ability, currently playing for Borussia Dortmund in the Bundesliga.",
                    "id" : "6"},
    "havertz" : {
                    "link" : "/static/havertzL.webp" ,
                    "info" : "Kai Havertz is a German midfielder known for his versatility, technical skill, and ability to score crucial goals, playing for Chelsea FC in the Premier League.",
                    "id" : "7"},
    "kvara" : {
                    "link" : "/static/kvaraL.webp" ,
                    "info" : "Khvicha Kvaratskhelia is a Georgian winger known for his dribbling skills and creativity, currently playing for Rubin Kazan in the Russian Premier League.",
                    "id" : "8"},
    "messi" : {
                    "link" : "/static/messiL.webp" ,
                    "info" : "Lionel Messi is an Argentine forward widely regarded as one of the greatest footballers of all time, known for his dribbling, vision, and goal-scoring prowess, currently playing for Paris Saint-Germain (PSG) in Ligue 1.",
                    "id" : "9"},
    "miqautadze" : {
                    "link" : "/static/miqautadzeL.webp" ,
                    "info" : "Giorgi Mikautadze is a Georgian forward known for his goal-scoring ability and physical presence, currently playing for Dinamo Tbilisi in the Georgian Erovnuli Liga.",
                    "id" : "10"},
    "musiala" : {
                    "link" : "/static/musialaL.webp" ,
                    "info" : "Jamal Musiala is a German-English midfielder known for his dribbling, creativity, and technical ability, playing for Bayern Munich in the Bundesliga and the Germany national team.",
                    "id" : "11"},    
    "rashford" : {
                    "link" : "/static/rashfordL.webp" ,
                    "info" : "Marcus Rashford is an English forward known for his pace, skillful dribbling, and goal-scoring ability, playing for Manchester United in the Premier League and the England national team.",
                    "id" : "12"},
    "saka" : {
                    "link" : "/static/sakaL.webp" ,
                    "info" : "Bukayo Saka is an English winger known for his speed, versatility, and technical skill, playing for Arsenal in the Premier League and the England national team.",
                    "id" : "13"},
    "van" : {
                    "link" : "/static/vanL.webp" ,
                    "info" : "Virgil van Dijk is a Dutch defender known for his strength, aerial prowess, and leadership, playing for Liverpool FC in the Premier League and the Netherlands national team. He is not from France but represents the Netherlands internationally.",
                    "id" : "14"}
}

@app.route("/")
def home():

    return render_template("index.html", footballers = footballers)


@app.route("/layout")
def layout():
    return render_template("layout.html")

@app.route("/register", methods =["GET", "POST"])
def register():
    form = RegisterF()
    if form.validate_on_submit() and not Accounts.query.filter(Accounts.nickname == form.nickname.data).first():
        Ruser = { 
            "nickname": form.nickname.data,
            "password": form.password.data
        }
        account_to_add = Accounts(nickname = Ruser["nickname"], password = Ruser["password"])
        db.session.add(account_to_add)
        db.session.commit()

        flash("You successfully registered :) ", category="success")
        print(Ruser)
        print(Accounts.query.all())
        return redirect("/")
        
    if form.errors:
        print(form.errors)
        flash("You didnt register :( ", category="danger")
    return render_template("register.html", form = form)

@app.route('/detail/<int:id>')
def detail(id):
    current = Product.query.get(id)

    return render_template("details.html", product=current)

@app.route("/login",  methods =["GET", "POST"])
def login():
    form = LoginF()
    if form.validate_on_submit():
        exists = Accounts.query.filter(Accounts.nickname == form.nickname.data).first()
        print(exists)
        if exists and exists.verify_password(form.password.data):
            login_user(exists)
            flash("You have successfully logged in. Now you can vote for your favorite players.", category="success")
            return redirect("/")
        else:
            flash("Incorrect password, try again :(", category="danger")
    return render_template("login.html", form = form)

used_allister = False
used_camavinga = False
used_debruin = False
used_fernandez = False
used_gabriel = False
used_haaland = False
used_havertz = False
used_kvara = False
used_messi = False
used_miqautadze = False
used_musiala = False
used_rashford = False
used_saka = False
used_van = False
@app.route("/votes",   methods =["GET", "POST"])
def vote():
    global used_allister
    global used_camavinga
    global used_debruin
    global used_fernandez
    global used_gabriel
    global used_haaland
    global used_havertz
    global used_kvara
    global used_messi
    global used_miqautadze
    global used_musiala
    global used_rashford
    global used_saka
    global used_van
    form = Vote()
    if form.validate_on_submit():
        if form.vote.data == "allister" and not used_allister:
            used_allister = True
            footballers["allister"]["link"] = footballers["allister"]["link"].replace("L", "B")             
            flash("You successfully applied vote", category="success")
            return redirect("/")
        elif form.vote.data == "camavinga" and not used_camavinga:
            used_camavinga = True
            footballers["camavinga"]["link"] = footballers["camavinga"]["link"].replace("L", "B")             
            flash("You successfully applied vote", category="success")
            return redirect("/")
        elif form.vote.data == "debruin" and not used_debruin:
            used_debruin = True
            footballers["debruin"]["link"] = footballers["debruin"]["link"].replace("L", "B")             
            flash("You successfully applied vote", category="success")
            return redirect("/")
        elif form.vote.data == "fernandez" and not used_fernandez:
            used_fernandez = True
            footballers["fernandez"]["link"] = footballers["fernandez"]["link"].replace("L", "B")             
            flash("You successfully applied vote", category="success")
            return redirect("/")
        elif form.vote.data == "gabriel" and not used_gabriel:
            used_gabriel = True
            footballers["gabriel"]["link"] = footballers["gabriel"]["link"].replace("L", "B")             
            flash("You successfully applied vote", category="success")
            return redirect("/")
        elif form.vote.data == "haaland" and not used_haaland:
            used_haaland = True
            footballers["haaland"]["link"] = footballers["haaland"]["link"].replace("L", "B")             
            flash("You successfully applied vote", category="success")
            return redirect("/")
        elif form.vote.data == "havertz" and not used_havertz:
            used_havertz = True
            footballers["havertz"]["link"] = footballers["havertz"]["link"].replace("L", "B")             
            flash("You successfully applied vote", category="success")
            return redirect("/")
        elif form.vote.data == "kvara" and not used_kvara:
            used_kvara = True
            footballers["kvara"]["link"] = footballers["kvara"]["link"].replace("L", "B")             
            flash("You successfully applied vote", category="success")
            return redirect("/")
        elif form.vote.data == "messi" and not used_messi:
            used_messi = True
            footballers["messi"]["link"] = footballers["messi"]["link"].replace("L", "B")             
            flash("You successfully applied vote", category="success")
            return redirect("/")
        elif form.vote.data == "miqautadze" and not used_miqautadze:
            used_miqautadze = True
            footballers["miqautadze"]["link"] = footballers["miqautadze"]["link"].replace("L", "B")             
            flash("You successfully applied vote", category="success")
            return redirect("/")
        elif form.vote.data == "musiala" and not used_musiala:
            used_musiala = True
            footballers["musiala"]["link"] = footballers["musiala"]["link"].replace("L", "B")             
            flash("You successfully applied vote", category="success")
            return redirect("/")
        elif form.vote.data == "rashford" and not used_rashford:
            used_rashford = True
            footballers["rashford"]["link"] = footballers["rashford"]["link"].replace("L", "B")             
            flash("You successfully applied vote", category="success")
            return redirect("/")
        elif form.vote.data == "saka" and not used_saka:
            used_saka = True
            footballers["saka"]["link"] = footballers["saka"]["link"].replace("L", "B")             
            flash("You successfully applied vote", category="success")
            return redirect("/")
        elif form.vote.data == "van" and not used_van:
            used_van = True
            footballers["van"]["link"] = footballers["van"]["link"].replace("L", "B")             
            flash("You successfully applied vote", category="success")
            return redirect("/")
        else:
            flash("You've already cast your vote, or the name is incorrect.", category="danger")
    return render_template("votes.html", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")