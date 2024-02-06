from flask import Flask,render_template,request,url_for,Request,session,redirect,flash
import mysql.connector
import json
import math

db = mysql.connector.connect(user='root', password= 'soumya2004',database='contacts')
cursor= db.cursor()
app=Flask(__name__)
app.secret_key = 'this is a secret key'

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
user = config_data.get('user', {})

@app.route('/')
def home():
    # Pagination logic
    cursor.execute("SELECT * FROM bpost")
    posts = cursor.fetchall()
    last = math.ceil(len(posts)/int(user.get('no_of_posts')))
    page=request.args.get('page')
    if(not str(page).isnumeric()):
        page=1
    
    page=int(page)
    posts=posts[((page-1)*int(user.get('no_of_posts'))):((page-1)*int(user.get('no_of_posts'))+int(user.get('no_of_posts')))]
    if(page==1):
        prev = "#"
        next = "/?page=" + str(page+1)
    elif(page==last):
        prev = "/?page=" + str(page-1)
        next = "#"
    else:
        prev = "/?page=" + str(page-1)
        next = "/?page=" + str(page+1)
    return render_template('index.html', post=posts, prev=prev, next=next, user=user)


@app.route('/logout')
def logout():
    session.pop('logged_in')
    return redirect('/')

@app.route('/delete/<string:sno>', methods=[ 'POST'])
def delete(sno):
    if 'logged_in' in session and session['logged_in'] == user.get('name'):
        if request.method == 'POST':
            cursor.execute("DELETE FROM bpost WHERE slno=%s",(int(sno),))
            db.commit()
        return redirect('/dashboard')

@app.route('/dashboard', methods=['GET','POST'])
def login():
    cursor.execute("SELECT * FROM bpost")
    post = cursor.fetchall()
    if 'logged_in' in session and session['logged_in'] == user.get('name'):
        return render_template('dashboard.html',post=post)

    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        #Adding data into database
        """insert_query = "INSERT INTO blogins (name, password) VALUES (%s, %s)"
        cursor.execute(insert_query, (name, password))
        db.commit()"""
        # Check if the entered name matches the user's name
        if name == user.get('name') and password == user.get('password'):
            session['logged_in'] = name
            return render_template('dashboard.html', post=post)
        else:
            flash('Invalid username/password!', 'danger')
            return redirect(url_for('login'))
        
    return render_template('login.html', user=user)

@app.route('/about')
def about():
    return render_template('about.html', user=user)

@app.route('/post/<string:post_slug>', methods=['GET'])
def post_route(post_slug):
    cursor.execute("SELECT * FROM bpost WHERE slug = %s", (post_slug,))
    post = cursor.fetchall()
    return render_template('post.html', post=post, user=user)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if 'logged_in' in session and session['logged_in'] == user.get('name'):
        if request.method == 'POST':
            title = request.form.get('title')
            stitle = request.form.get('stitle')
            slug = request.form.get('slug')
            content = request.form.get('content')
            insert_query = "INSERT INTO bpost (title, sub_title, slug, content) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (title, stitle, slug, content))
            db.commit()
            return redirect('/dashboard')
        return render_template('new_post.html')

@app.route('/edit/<string:sno>', methods=['GET', 'POST'])
def edit(sno):
    if 'logged_in' in session and session['logged_in'] == user.get('name'):
        cursor.execute("SELECT * FROM bpost WHERE slno=%s", (sno,))
        post = cursor.fetchall()
        if request.method == 'POST':
            title = request.form.get('title')
            stitle = request.form.get('stitle')
            slug = request.form.get('slug')
            content = request.form.get('content')
            # img_file = request.form.get('img_file')

            sno = int(sno)
            update_query = "UPDATE bpost SET title=%s, sub_title=%s, slug=%s, content=%s WHERE slno=%s"
            cursor.execute(update_query, (title, stitle, slug, content, sno))
            db.commit()
            return redirect('/dashboard')
            
        return render_template('edit.html', sno=sno, post=post)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if (request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        #Adding data into database
        insert_query = "INSERT INTO bcontact (name, email, ph_num, msg) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (name, email, phone, message))
        db.commit()
        flash('Thank you for contacting us and we will get back to you soon', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')


if __name__=='__main__':
    app.run(debug=True)