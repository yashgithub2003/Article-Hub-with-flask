from flask import Flask, render_template, flash, redirect, url_for,session,logging,request
# from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MySQL
mysql = MySQL(app)




# Articles = Articles()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    # Create Cursor
    cur = mysql.connection.cursor()

    # get articles
    results = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    cur.close()


    if results > 0:
        return render_template('articles.html',articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html',msg=msg)
    

@app.route('/article/<int:id>/')
def article(id):
    # Create Cursor
    cur = mysql.connection.cursor()

    # get articles
    results = cur.execute("SELECT * FROM articles WHERE id = %s",[id])

    article = cur.fetchone()

    cur.close()

    return render_template('article.html',article=article)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods =['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create Cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users( name, email, username, password) VALUES(%s, %s, %s, %s)",(name, email, username, password))

        # commit to DB
        mysql.connection.commit()

        # close connection
        cur.close()

        flash("You are now registered" , "success")

        return redirect(url_for('home'))
    return render_template('register.html',form=form)    




@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        # get the form field
        username = request.form['username']
        candidate_password = request.form['password']

        # create cursor
        cur = mysql.connection.cursor()

        # get user by username
        result = cur.execute(" SELECT * FROM users WHERE username = %s ",[username])

        if result > 0:
            # Get store hash 
            data = cur.fetchone()
            password = data['password']

            # compare password
            if sha256_crypt.verify(candidate_password,password):
                # passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))

            else:
                 # close connection
                cur.close()
                error = "Invalid Login"
                return render_template('login.html',error=error)
    
           
            
        else:
            error = "Username not found"
            return render_template('login.html',error=error)

    
    return render_template('login.html')

# check if user login
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create Cursor
    cur = mysql.connection.cursor()

    # get articles
    results = cur.execute("SELECT * FROM articles WHERE author = %s", (session['username'],))

    articles = cur.fetchall()

    cur.close()

    if results > 0:
        return render_template('dashboard.html',articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html',msg=msg)


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators
import bleach

class ArticleForm(FlaskForm):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])



@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm()

    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        author = session.get('username')

        # Sanitize HTML (CRITICAL)
        allowed_tags = ['p','b','i','u','strong','em','ul','ol','li','br']
        clean_body = bleach.clean(body, tags=allowed_tags, strip=True)

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO articles(title, body, author) VALUES (%s, %s, %s)",
                (title, clean_body, author)
            )
            mysql.connection.commit()
            flash("Article Created", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            mysql.connection.rollback()
            flash("Error creating article", "danger")
            print(e)
        finally:
            cur.close()

    return render_template('add_article.html', form=form)

@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    cur = mysql.connection.cursor()

    # Only get article owned by current user
    result = cur.execute(
        "SELECT * FROM articles WHERE id = %s AND author = %s",
        (id, session.get('username'))
    )

    if result == 0:
        flash("Unauthorized access", "danger")
        return redirect(url_for('dashboard'))

    article = cur.fetchone()
    cur.close()

    form = ArticleForm()

    # Populate form ONLY on GET
    if request.method == 'GET':
        form.title.data = article['title']
        form.body.data = article['body']

    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data

        import bleach
        allowed_tags = ['p','b','i','u','strong','em','ul','ol','li','br']
        clean_body = bleach.clean(body, tags=allowed_tags, strip=True)

        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE articles SET title=%s, body=%s WHERE id=%s AND author=%s",
            (title, clean_body, id, session.get('username'))
        )
        mysql.connection.commit()
        cur.close()

        flash('Article Updated', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)


# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM articles WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)