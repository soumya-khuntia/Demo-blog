from flask import Flask,render_template,request,url_for,Request,session,redirect,flash
import mysql.connector
import json
import math
import uuid

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
    cursor.execute("SELECT COUNT(*) FROM bpost")  # Count the total number of posts in the database
    total_posts = cursor.fetchone()[0]  # Fetch the count
    last = math.ceil(total_posts / int(user.get('no_of_posts')))

    page = request.args.get('page')
    if not str(page).isnumeric():
        page = 1

    page = int(page)
    offset = (page - 1) * int(user.get('no_of_posts'))

    cursor.execute("SELECT * FROM bpost LIMIT %s, %s", (offset, int(user.get('no_of_posts'))))
    posts = cursor.fetchall()

    prev = "#"
    next = "#"

    if last > 1:
        if page == 1:
            next = "/?page=" + str(page + 1)
        elif page == last:
            prev = "/?page=" + str(page - 1)
        else:
            prev = "/?page=" + str(page - 1)
            next = "/?page=" + str(page + 1)

    return render_template('index.html', post=posts, prev=prev, next=next, user=user)


@app.route('/logout')
def logout():
    session.pop('logged_in')
    flash('You have been logged out','danger')
    return redirect('/')

    
@app.route('/sign_up', methods=['GET','POST'])
def sign_up(user = user):
    if request.method == 'POST':
        sname = request.form['username']
        spassword = request.form['password']
        scpassword = request.form['cpassword']
        semail = request.form['email']
        uid=str(uuid.uuid4())
        if spassword == scpassword:
            cursor.execute("SELECT * FROM blogins WHERE name=%s",(sname,))
            user = cursor.fetchone()
            if user:
                flash('Username already exists', 'danger')
                return redirect('/sign_up')
            else:
                cursor.execute("INSERT INTO blogins (name, password, email, uuid) VALUES (%s, %s, %s, %s)", (sname, spassword, semail, uid))
                db.commit()
                session['logged_in'] = sname
                return redirect('/dashboard')
        else:
            flash('Passwords do not match', 'danger')
            return redirect('/sign_up')
    return render_template('sign_up.html', user=user)

@app.route('/dashboard', methods=['GET','POST'])
def login():
    if 'logged_in' in session :
        cursor.execute("SELECT * FROM blogins WHERE name=%s",(session['logged_in'],))
        lg = cursor.fetchone()
        uname=lg[4]
        cursor.execute("SELECT * FROM bpost WHERE uname=%s",(uname,)) 
        post = cursor.fetchall()
        return render_template('dashboard.html',post=post,user=user)

    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM blogins WHERE name=%s", (name,))
        lguser = cursor.fetchone()
        # Check if the entered name matches the user's name
        if lguser:
            if password == lguser[2]:
                session['logged_in'] = name
                cursor.execute("SELECT * FROM blogins WHERE name=%s",(session['logged_in'],))
                lg = cursor.fetchone()
                uname=lg[4]
                cursor.execute("SELECT * FROM bpost WHERE uname=%s",(uname,)) 
                post = cursor.fetchall()
                return render_template('dashboard.html', post=post, user=user)
            else:
                flash('Incorrect password!', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Username does not exist', 'danger')
            return redirect(url_for('login'))
        
    return render_template('login.html', user=user)
    
@app.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    if request.method == 'POST':
        rname=request.form['username']
        rmail=request.form['email']
        rpassword=request.form['password']
        rcpassword=request.form['cpassword']
        cursor.execute("SELECT email FROM blogins WHERE name=%s", (rname,))
        user_data = cursor.fetchone()
        if user_data:
            email = user_data[0]
            if email == rmail:
                if rpassword == rcpassword:
                    # Update password
                    cursor.execute("UPDATE blogins SET password=%s WHERE name=%s", (rpassword, rname))
                    db.commit()
                    flash('Password reset successful', 'success')
                    return redirect(url_for('login'))
                else:
                    flash('Passwords do not match', 'danger')
            else:
                flash('Email does not match', 'danger')
        else:
            flash('Username does not exist', 'danger')

        return redirect(url_for('password_reset'))
    return render_template('password_reset.html', user=user)

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
    # Fetch the logged-in user's name from the database
    cursor.execute("SELECT * FROM blogins WHERE name = %s", (session['logged_in'],))
    db_user = cursor.fetchone()
    uid=db_user[4]
    if 'logged_in' in session:
        if request.method == 'POST':
            title = request.form.get('title')
            stitle = request.form.get('stitle')
            slug = request.form.get('slug')
            content = request.form.get('content')
            insert_query = "INSERT INTO bpost (title, sub_title, slug, content, uname) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (title, stitle, slug, content, uid))
            db.commit()
            flash(f'({title}) post added Successfully!', 'success')
            return redirect('/dashboard')
        return render_template('new_post.html', user=user)

@app.route('/edit/<string:sno>', methods=['GET', 'POST'])
def edit(sno):
    if 'logged_in' in session:
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
            flash(f'({title}) post updated Successfully!', 'info')
            return redirect('/dashboard')
            
        return render_template('edit.html', sno=sno, post=post, user=user)

@app.route('/delete/<string:sno>', methods=[ 'POST'])
def delete(sno):
    if 'logged_in' in session:
        if request.method == 'POST':
            cursor.execute("DELETE FROM bpost WHERE slno=%s",(int(sno),))
            db.commit()
        flash('Successfully Deleted', 'warning')
        return redirect('/dashboard')


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

    return render_template('contact.html', user=user)


if __name__=='__main__':
    app.run(debug=True)