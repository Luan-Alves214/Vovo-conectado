from flask import Flask, render_template, request, g, redirect, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app = app
app.secret_key = 'LuanEguh'

# Banco de dados
def ligarBanco():
    if 'contato.db' not in g:
        g._database = sqlite3.connect(os.path.join(os.path.dirname(__file__), '../contato.db'))
    return g._database

@app.teardown_appcontext
def fechar_conexao(exception):
    db = g.pop('_database', None)
    if db is not None:
        db.close()

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/sobre')
def Sobre():
    return render_template('Sobre.html')

@app.route('/contato')
def Contact():
    return render_template('Contato.html')

@app.route('/depoimentos')
def Depoimentos():
    return render_template('Depoimentos.html')

@app.route('/criar', methods=['POST'])
def Criar():
    nome = request.form['nome']
    email = request.form['email']
    assunto = request.form['assunto']
    mensagem = request.form['message']
    date_envio = datetime.now()
    banco = ligarBanco()
    cursor = banco.cursor()
    cursor.execute('INSERT INTO contato (Nome,Email,Assunto,Mensagem, DataHora) VALUES (?,?,?,?,?)', (nome,email, assunto, mensagem, date_envio))
    banco.commit()
    return render_template('Contato.html')

@app.route('/adm')
def Adm():
    if 'usuario' in session:
        return redirect("/mensagens")
    return render_template('login.html')

@app.route('/logout')
def Logout():
    session.pop('usuario')
    return redirect('/')

@app.route('/autenticar', methods=['POST'])
def Autenticar():
    usuariodigitado= request.form['usuario']
    senhadigitada = request.form['senha']
    banco = ligarBanco()
    cursor = banco.cursor()
    cursor.execute('SELECT * FROM Adm')
    usuariosEsenhas = cursor.fetchall()

    for usuario in usuariosEsenhas:
        if usuario[1] == usuariodigitado and usuario[2] == senhadigitada:
            session['usuario'] = usuariodigitado
            return redirect('/mensagens')
    return redirect('/adm')


@app.route('/mensagens')
def Mensagens():
    if 'usuario' in session:
        banco = ligarBanco()
        cursor = banco.cursor()
        cursor.execute('SELECT * FROM contato')
        mensagens = cursor.fetchall()
        return render_template('Mensagens.html', mensagens=mensagens)
    return redirect('/adm')

if __name__ == '__main__':
    app.run()
