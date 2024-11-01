import os
from flask import Flask
from flask import Flask, render_template, request, redirect, flash

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))

database_file = "sqlite:///{}".format(os.path.join(project_dir, "BancoDeJogos.db"))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

#Classes
class Jogos(db.Model):
    Nome = db.Column(db.String(80), unique = True, nullable = False, primary_key = True)
    def __repr__(self):
        return "<Nome: {}>".format(self.Nome)


#Rotas
@app.route('/', methods=["GET", "POST"])
def Home():
    Nomes = None
    if request.method == "POST":
        nome_jogo = request.form.get("NomeJogo")
        if nome_jogo:
            jogo_existente = Jogos.query.filter_by(Nome=nome_jogo).first()
            if not jogo_existente:
                novo_jogo = Jogos(Nome=nome_jogo)
                db.session.add(novo_jogo)
                db.session.commit()
            else:
                flash("O jogo já existe!", "Tente Outro") 

    Nomes = Jogos.query.all()
    return render_template('Principal.html', Nomes=Nomes)

@app.route('/Alterar', methods=["GET", "POST"])    
def Alterar():
    Velho = request.form.get('VelhoNome')
    Novo = request.form.get('NovoNome')
    
    Jogo = Jogos.query.filter_by(Nome = Velho).first()

    if Jogo: 
        Jogo.Nome = Novo  
        db.session.commit()  
        
        return redirect("/")

    return render_template("Principal.html")

@app.route('/Apagar', methods=['POST']) 
def delete():
    Nome = request.form.get("NomeJogo")
    
    Jogo = Jogos.query.filter_by(Nome = Nome).first()
    
    if Jogo:  
        db.session.delete(Jogo)
        db.session.commit() 
    
    return redirect("/") 

@app.route('/Adicionar') 
def Adicionar():
    Nomes = Jogos.query.all()
    
    return render_template('Criar.html', Nomes=Nomes)

@app.route('/Renomear') 
def Renomear():
    return render_template('Renomear.html', Jogos=Jogos)

@app.route('/Apagar') 
def Apagar():
    return render_template('Apagar.html', Jogos=Jogos)

    
#Comandos do Banco de Dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)