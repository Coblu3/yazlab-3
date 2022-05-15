from unicodedata import name
from flask import Flask, render_template, redirect, session, url_for
from flask import request
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import EmailField, PasswordField, StringField, IntegerField , Form , SelectField 
import os
from db_classes import User, Article, Type, Researcher
import sys
from neomodel import db
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config, EmailProperty
import socket
import base64

config.DATABASE_URL = 'bolt://neo4j:yazlab@localhost:7687'

researcherNodes = []

class Form(FlaskForm):
    researcherNodes = Researcher.nodes.all()
    researcher = SelectField("Choose Researcher", choices = researcherNodes)
    articleNodes = Article.nodes.all() 
    article = SelectField('Choose Article', choices = articleNodes)
    typeNodes = Type.nodes.all() 
    type = SelectField('Choose Type', choices = typeNodes)


    

class dataForm(FlaskForm):
    researcher = StringField('researcher')
    article = StringField('article')
    year = StringField('year')


class LoginForm(FlaskForm):
    email = EmailField("Email:",validators=[DataRequired()])
    password = PasswordField("Password:",validators=[DataRequired()])


class ResearcherForm(FlaskForm):
    nameR = StringField("Name:",validators=[DataRequired()])
    surname = StringField("Surname:",validators=[DataRequired()])


class ArticleForm(FlaskForm):
    nameA = StringField("Name:",validators=[DataRequired()])
    year = IntegerField("Year:",validators=[DataRequired()])


class TypeForm(FlaskForm):
    nameT = StringField("Name:",validators=[DataRequired()])
    publicationPlace = StringField("Publication Place:",validators=[DataRequired()])

app = Flask(__name__)
data = []
result = []
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/", methods=['GET', 'POST'])
def index():
    form = dataForm()
    article_name = form.article.data
    year = form.year.data
    researcher_name = form.researcher.data
    result = []

    if request.method=="POST":
        results = []
        if article_name and researcher_name and not year:
            try :
                name = researcher_name.split(" ")[0].lower()
                surname = researcher_name.split(" ")[1].lower()
                query = "MATCH (type:Type)--(article:Article {name: '"+article_name+"'})<-[:AUTHOR]-(researcher:Researcher {name: '"+name+"',surname:'"+surname+"'}) RETURN article.name,researcher.name,researcher.researcher_id,article.year,researcher.surname,type.name,type.publication_place"
                results, meta = db.cypher_query(query)
            except:
                query = "MATCH (type:Type)--(article:Article {name: '"+article_name+"'})<-[:AUTHOR]-(researcher:Researcher {name: '"+researcher_name+"'}) RETURN article.name,researcher.name,researcher.researcher_id,article.year,researcher.surname,type.name,type.publication_place"
                results, meta = db.cypher_query(query)

        if article_name and not researcher_name and not year:
            query = "MATCH (type:Type)--(article:Article {name: '"+article_name+"'})<-[:AUTHOR]-(researcher:Researcher) RETURN article.name,researcher.name,researcher.researcher_id,article.year,researcher.surname,type.name,type.publication_place"
            results, meta = db.cypher_query(query)
            
        elif researcher_name and not article_name and not year: 
            try :
                name = researcher_name.split(" ")[0].lower()
                surname = researcher_name.split(" ")[1].lower()
                query = "MATCH (type:Type)--(article:Article)<-[:AUTHOR]-(researcher:Researcher {name: '"+name+"',surname:'"+surname+"'}) RETURN article.name,researcher.name,researcher.researcher_id,article.year,researcher.surname,type.name,type.publication_place"
                results, meta = db.cypher_query(query)
            except:
                query = "MATCH (type:Type)--(article:Article)<-[:AUTHOR]-(researcher:Researcher {name: '"+researcher_name+"'}) RETURN article.name,researcher.name,researcher.researcher_id,article.year,researcher.surname,type.name,type.publication_place"
                results, meta = db.cypher_query(query)

        elif year and not article_name and not researcher_name:
            query = "MATCH (type:Type)--(article:Article {year: "+year+"})<-[:AUTHOR]-(researcher:Researcher) RETURN article.name,researcher.name,researcher.researcher_id,article.year,researcher.surname,type.name,type.publication_place"
            results, meta = db.cypher_query(query)

        elif year and  article_name and not researcher_name:
            query = "MATCH (type:Type)--(article:Article {year: "+year+",name:'"+article_name+"'})<-[:AUTHOR]-(researcher:Researcher) RETURN article.name,researcher.name,researcher.researcher_id,article.year,researcher.surname,type.name,type.publication_place"
            results, meta = db.cypher_query(query)

        elif year and  researcher_name and not article_name:
            try :
                name = researcher_name.split(" ")[0].lower()
                surname = researcher_name.split(" ")[1].lower()
                query = "MATCH (type:Type)--(article:Article {year: "+year+"})<-[:AUTHOR]-(researcher:Researcher {name: '"+name+"', surname:'"+surname+"'}) RETURN article.name,researcher.name,researcher.researcher_id,article.year,researcher.surname,type.name,type.publication_place"
                results, meta = db.cypher_query(query)
            except:
                query = "MATCH (type:Type)--(article:Article {year: "+year+"})<-[:AUTHOR]-(researcher:Researcher {name: '"+researcher_name+"'}) RETURN article.name,researcher.name,researcher.researcher_id,article.year,researcher.surname,type.name,type.publication_place"
                results, meta = db.cypher_query(query)

        elif year and  researcher_name and article_name:
            try :
                name = researcher_name.split(" ")[0].lower()
                surname = researcher_name.split(" ")[1].lower()
                query = "MATCH (type:Type)--(article:Article {year: "+year+" , name:'"+article_name+"'})<-[:AUTHOR]-(researcher:Researcher {name: '"+name+"', surname:'"+surname+"'}) RETURN article.name,researcher.name,researcher.researcher_id,article.year,researcher.surname,type.name,type.publication_place"
                results, meta = db.cypher_query(query)
            except:
                query = "MATCH (type:Type)--(article:Article {year: "+year+", name:'"+article_name+"'})<-[:AUTHOR]-(researcher:Researcher {name: '"+researcher_name+"'}) RETURN article.name,researcher.name,researcher.researcher_id,article.year,researcher.surname,type.name,type.publication_place"
                results, meta = db.cypher_query(query)

        elif not year and not  researcher_name and not article_name:
            query = "MATCH (type:Type)--(article:Article)<-[:AUTHOR]-(researcher:Researcher) RETURN article.name,researcher.name,researcher.researcher_id,article.year,researcher.surname,type.name,type.publication_place"
            results, meta = db.cypher_query(query)

        else:
            pass
            
    
        return render_template("index.html", form=form, result=results)

    return render_template("index.html", form=form, data=data, result=result)


@app.route("/vis", methods=['GET', 'POST'])
def vis():
    return render_template("vis.html")

@app.route("/dashboard" , methods=['GET', 'POST'])
def dashboard():
    rForm = ResearcherForm()
    aForm = ArticleForm()
    tForm = TypeForm()
    

    if rForm.validate_on_submit() and request.method == "POST":

        nameR = rForm.nameR.data
        surname = rForm.surname.data

        researcher = Researcher(name=nameR, surname=surname)
        researcher.save()
        rForm.data.clear()
        return render_template("dashboard.html", rForm=rForm, aForm=aForm, tForm=tForm )

    if aForm.validate_on_submit() and request.method == "POST":
        
        nameA = aForm.nameA.data
        year = aForm.year.data

        article = Article(name=nameA,year=year)
        article.save()
        
        aForm.data.clear()
        return render_template("dashboard.html", rForm=rForm, aForm=aForm, tForm=tForm )

    if tForm.validate_on_submit() and request.method == "POST":
        
        nameT = tForm.nameT.data
        publication_place = tForm.publicationPlace.data

        type = Type(name=nameT,publication_place=publication_place)
        type.save()

        tForm.data.clear()
        return render_template("dashboard.html", rForm=rForm, aForm=aForm, tForm=tForm ) 

    
    return render_template("dashboard.html", rForm=rForm, aForm=aForm, tForm=tForm)


@app.route("/connect", methods=['GET', 'POST'])
def connect():
    SelectForm = Form()

    SelectForm.researcher.choices = [(r.researcher_id,"Researcher Name: "+r.name + " -- Researcher Surname: " + r.surname) for r in Researcher.nodes.all()]
    SelectForm.type.choices = [(t.type_id,"Type Name: "+t.name + " -- Publication Place: " + t.publication_place) for t in Type.nodes.all()]
    SelectForm.article.choices = [(a.article_id,"Article Name : "+a.name + " -- Article Year: " + str(a.year)) for a in Article.nodes.all()]

    if request.method == "POST":
        researcher = SelectForm.researcher.data
        article = SelectForm.article.data
        type = SelectForm.type.data

        
        researcher = Researcher.nodes.get_or_none(researcher_id = researcher)
        article = Article.nodes.get_or_none(article_id = article)
        type = Type.nodes.get_or_none(type_id = type)

        article.type.connect(type)
        researcher.article.connect(article)
        article.researcher.connect(researcher)


        return render_template("connect.html",rSelect = SelectForm )

    return render_template("connect.html",rSelect = SelectForm)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() and request.method == "POST":
        # login session
        if User.nodes.get_or_none(email=form.email.data, password=form.password.data):
            session["logged_in"] = True
            session["email"] = form.email.data
            return redirect(url_for("index"))

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
