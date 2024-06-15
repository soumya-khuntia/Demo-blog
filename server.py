from flask import Flask,render_template,request,url_for,session,redirect,flash
from flask_mail import Mail, Message
import mysql.connector
import random,math,json,uuid
from authlib.integrations.flask_client import OAuth

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
user = config_data.get('user', {})

db = mysql.connector.connect(user='root', password= 'soumya2004',database='contacts')
cursor= db.cursor()
app=Flask(__name__)
app.secret_key = 'This is a secret key'

# Google OAuth2 configuration
oauth = OAuth(app)
goog = oauth.register(
    name="google",
    client_id=user.get('client_id'),
    client_secret= user.get('client_secret'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'}
)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = user.get('mail')
app.config['MAIL_PASSWORD'] = user.get('password')
app.config['MAIL_DEFAULT_SENDER'] = user.get('mail')

mail = Mail(app)

def truncate_description(description, word_limit=20):
    words = description.split()
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + ' ....'
    return description

app.jinja_env.filters['truncate'] = truncate_description


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

    # Fetch the posts user's name from the database
    uname=[]
    for i in posts:
       uid=i[7]
       cursor.execute("SELECT name FROM blogins WHERE uuid = %s", (uid,))
       post1 = cursor.fetchone()
       if post1:
           uname.append(post1[0])
       if post1 is None:
           cursor.execute("SELECT fname FROM google_login WHERE uid = %s", (uid,))
           post2=cursor.fetchone()
           uname.append(post2[0])
    
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

    return render_template('index.html', post=posts, prev=prev, next=next, user=user,uname=uname)


@app.route('/all_blogs', methods=['GET','POST'])
def all_blogs():

    filter_by = request.args.get('filter_by', '')

    if filter_by == 'name':
        cursor.execute("SELECT * FROM bpost ORDER BY title ASC")
    elif filter_by == 'newest':
        cursor.execute("SELECT * FROM bpost ORDER BY date DESC")
    elif filter_by == 'oldest':
        cursor.execute("SELECT * FROM bpost ORDER BY date ASC")
    else:
        cursor.execute("SELECT * FROM bpost")

    posts = cursor.fetchall()

    uname=[]
    for i in posts:
        uid=i[7]
        cursor.execute("SELECT name FROM blogins WHERE uuid = %s", (uid,))
        post1 = cursor.fetchone()
        if post1:
            uname.append(post1[0])
        if post1 is None:
            cursor.execute("SELECT fname FROM google_login WHERE uid = %s", (uid,))
            post2=cursor.fetchone()
            uname.append(post2[0])

    return render_template('all_blogs.html', user=user, post=posts, uname=uname)

@app.route('/search', methods=['GET','POST'])
def search_posts():
    if request.method == 'GET':
        search=request.args.get('search', '')
        cursor.execute("SELECT * FROM bpost WHERE title LIKE %s", ('%'+search+'%',))
        posts=cursor.fetchall()
    
    uname=[]
    for i in posts:
        uid=i[7]
        cursor.execute("SELECT name FROM blogins WHERE uuid = %s", (uid,))
        post1 = cursor.fetchone()
        if post1:
            uname.append(post1[0])
        if post1 is None:
            cursor.execute("SELECT fname FROM google_login WHERE uid = %s", (uid,))
            post2=cursor.fetchone()
            uname.append(post2[0])
    
    return render_template('all_blogs.html', user=user, post=posts, uname=uname)

@app.route('/logout')
def logout():
    session.clear()
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
                cursor.execute("SELECT * FROM blogins WHERE email=%s",(semail,))
                useremail = cursor.fetchone()
                if useremail:
                    flash('Email already exists', 'danger')
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM blogins WHERE name=%s", (name,))
        lguser = cursor.fetchone()
        # Check if the entered name matches the user's name
        if lguser:
            if password == lguser[2]:
                session['logged_in'] = name
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect password!', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Username does not exist', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', user=user)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'logged_in' in session:
        cursor.execute("SELECT * FROM blogins WHERE name=%s", (session['logged_in'],))
        lg = cursor.fetchone()
        uname = lg[4]
        cursor.execute("SELECT * FROM bpost WHERE uname=%s", (uname,))
        post = cursor.fetchall()
        return render_template('dashboard.html', post=post, user=user)

    if 'google_logged_in' in session:
        cursor.execute("SELECT * FROM google_login WHERE email=%s", (session['google_logged_in'],))
        lg = cursor.fetchone()
        uid = lg[4]
        cursor.execute("SELECT * FROM bpost WHERE uname=%s", (uid,))
        post = cursor.fetchall()
        return render_template('dashboard.html', post=post, user=user)

    flash('You need to login first', 'warning')
    return redirect(url_for('login'))

@app.route('/google_login')
def google_login():
    google = oauth.create_client("google")
    redirect_uri = url_for('callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/callback')
def callback():
    token = oauth.google.authorize_access_token()
    name = token.get('userinfo', {}).get('name')
    fname = token.get('userinfo', {}).get('given_name')
    email = token.get('userinfo', {}).get('email')
    cursor.execute("SELECT * FROM google_login WHERE email=%s", (email,))
    user = cursor.fetchone()
    if user:
        session['google_logged_in'] = email
        session['name'] = fname
        return redirect('/dashboard')
    if user is None:
        uid = str(uuid.uuid4())
        cursor.execute("INSERT INTO google_login (name, fname, email, uid) VALUES (%s, %s, %s, %s)", (name, fname, email, uid))
        db.commit()
        session['google_logged_in'] = email
        return redirect('/dashboard')
    return redirect(url_for('login'))

    
@app.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    if request.method == 'POST':
        rmail=request.form['email']
        cursor.execute("SELECT * FROM blogins WHERE email=%s",(rmail,))
        useremail = cursor.fetchone()
        uname=useremail[1]
        if useremail:
            session['email'] = rmail
            try:
                subject = 'Password Reset'
                code = str(random.randint(10**5, 10**6 - 1)).zfill(6)
                session["password_reset_code"] = code
                msg = Message(subject, recipients=[rmail])
                msg.body = f"User Name:- {uname}\n\nYour password reset code is: {code}"
                mail.send(msg)
                flash('Passcode sent to email!', 'success')
            except:
                flash('Something went wrong!', 'danger')
            return redirect('/passcode')
        else:
            flash('Email does not exist', 'danger')
            return redirect('/password_reset')
    return render_template('password_reset.html', user=user)

@app.route('/passcode', methods=['GET', 'POST'])
def passcode():
    if request.method == 'POST':
        code=request.form['code']
        if code == session['password_reset_code']:
            flash('Passcode verified successfully', 'success')
            return redirect('/newpassword')
        else:
            flash('Incorrect code!', 'danger')
            return redirect('/passcode')
    return render_template('passcode.html', user=user)
        

@app.route('/newpassword', methods=['GET', 'POST'])
def newpassword():
    if request.method == 'POST':
        password=request.form['password']
        cpassword=request.form['cpassword']
        if password == cpassword:
            cursor.execute("UPDATE blogins SET password=%s WHERE email=%s",(password,session['email']))
            db.commit()
            session.pop('email')
            session.pop('password_reset_code')
            flash('Password changed successfully!','success')
            return redirect('/dashboard')
        else:
            flash('Passwords do not match', 'danger')
            return redirect('/newpassword')
    return render_template('newpassword.html', user=user)

@app.route('/about')
def about():
    return render_template('about.html', user=user)

@app.route('/post/<string:post_slug>', methods=['GET'])
def post_route(post_slug):
    try:
        cursor.execute("SELECT * FROM bpost WHERE slug = %s", (post_slug,))
        post = cursor.fetchone()
        uid=post[7]
        cursor.execute("SELECT name FROM blogins WHERE uuid = %s", (uid,))
        post1 = cursor.fetchone()
        if post1:
            uname=post1[0]
        if post1 is None:
            cursor.execute("SELECT fname FROM google_login WHERE uid = %s", (uid,))
            post2=cursor.fetchone()
            uname=post2[0]
    except:
        flash('Something goes wrong in database!', 'danger')
        return redirect('/')
    return render_template('post.html', post=post, user=user,uname=uname)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if 'logged_in' in session:
        # Fetch the logged-in user's name from the database
        cursor.execute("SELECT * FROM blogins WHERE name = %s", (session['logged_in'],))
        db_user = cursor.fetchone()
        uid=db_user[4]
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
    if 'google_logged_in' in session:
        # Fetch the logged-in user's name from the database
        cursor.execute("SELECT * FROM google_login WHERE email = %s", (session['google_logged_in'],))
        db_user = cursor.fetchone()
        uid=db_user[4]
        if request.method == 'POST':
            title=request.form.get('title')
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
    if 'logged_in' in session or 'google_logged_in' in session:
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
    if 'logged_in' in session or 'google_logged_in' in session:
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