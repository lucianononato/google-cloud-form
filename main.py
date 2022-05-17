from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL


app = Flask(__name__) 

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='formpessoas'
mysql.init_app(app)


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/cadastros')
def cadastros():

    sql="SELECT * FROM `infopessoas`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    infopessoas=cursor.fetchall()
    print(infopessoas)

    conn.commit()
    return render_template('cadastros.html', infopessoas=infopessoas)

@app.route('/apagar/<int:id>')
def apagar(id):
    conn=mysql.connect()
    cursor=conn.cursor()

    cursor.execute("DELETE FROM infopessoas WHERE id= %s", (id))
    conn.commit()
    return redirect('../cadastros')

@app.route('/edit/<int:id>')
def edit(id):

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM infopessoas WHERE id=%s", (id))
    infopessoas=cursor.fetchall()
    conn.commit()
    return render_template('edit.html', infopessoas=infopessoas)

@app.route('/update', methods=['POST'])
def update():

    _name=request.form['name']
    _email=request.form['email']
    _whatsApp=request.form['whatsApp']
    id=request.form['txtID']

    sql= "UPDATE infopessoas SET name=%s, email=%s, whatsApp=%s WHERE id=%s;"
    
    dados=(_name, _email, _whatsApp, id)

    conn= mysql.connect()
    cursor=conn.cursor()

    cursor.execute(sql, dados)
    
    conn.commit()

    return redirect('../cadastros')

@app.route('/addcontato')
def addcontato():
    return render_template('addcontato.html')

@app.route('/voltar')
def voltar():
    return render_template('index.html')
    
@app.route('/form', methods=['POST'])
def form():
    _name=request.form['name']
    _email=request.form['email']
    _whatsApp=request.form['whatsApp']

    sql="INSERT INTO `infopessoas` (`id`, `name`, `email`, `whatsApp`) VALUES (NULL, %s, %s, %s);"
    
    dados=(_name, _email, _whatsApp)

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql, dados)
    conn.commit()

    return render_template('form.html') 




if __name__ == '__main__':
    
    app.run(host='127.0.0.1', port=8080, debug=True) 