from flask import Flask, render_template, request, url_for, abort
import mysql.connector
import stripe 

mydb = mysql.connector.connect(host="127.0.0.1",
                                user="root",
                                password="",
                                database="agms",
                                auth_plugin='mysql_native_password')
mycursor = mydb.cursor()

app=Flask(__name__)


app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51Hbn4EJQL31GMhtilucQFnvzOY95TDnnPa8rzV8qiojYstG3nnI6bjUPQNsL9XmKWFe9nfRxyICif9twEF4k3jHV00D1PTHh6e'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51Hbn4EJQL31GMhtiWYMD7OgzZuNsTXrMgBsBlzYap8KapIrxblXWWYxsKZxh9HhdTckIcXNr0xs0fd9Dyxz8A5yb00YJ1OS9Co'


stripe.api_key = app.config['STRIPE_SECRET_KEY']


curr_user = ""
curr_user_type=""




@app.route('/toLogin', methods = ['POST','GET'])
def home1():
    return render_template("login.html")

@app.route('/',methods = ['POST','GET'])
def home2():
    return render_template("register.html")
    #return render_template('wishlist.html')

@app.route('/signIn', methods = ['POST', 'GET'])
def signIn():
    global curr_user
    global curr_user_type
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        print(username)
        print(password)
        myquery = "select exists(select * from users where username=%s)"
        rec_tup = (username,)
        mycursor.execute(myquery, rec_tup)
        if mycursor.fetchone()[0]==1:
            new_query = "select password from users where username=%s"
            mycursor.execute(new_query, rec_tup)
            if mycursor.fetchone()[0]==password:
                curr_user = username
                req_query = "select usertype from users where username=%s"
                mycursor.execute(req_query,rec_tup)
                curr_user_type=mycursor.fetchone()[0]
                return render_template("homepage.html")
            else:
                return render_template('Err.html', message="Username/Password Wrong")
        else:
            return render_template('Err.html', message="Username/Password Wrong")

@app.route('/signUp', methods = ['POST', 'GET'])
def signUp():
    if request.method == 'POST':
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        confirmPassword = request.form["cnfpassword"]
        usertype = request.form["usertype"]
        email = request.form["email"]

        print(name, username, password, email)
        
        myquery = "select exists(select * from users where username=%s)"
        rec_tup = (username,)
        mycursor.execute(myquery, rec_tup)
        if mycursor.fetchone()[0]==1:
            return render_template('Err.html', message="Username already exists")
        elif password!=confirmPassword:
            return render_template('Err.html', message="Passwords Don't Match")
        else:
            mysql_query = "insert into users values(%s, %s, %s, %s, %s)"
            records = (name, username, password, email, usertype)
            mycursor.execute(mysql_query, records)
            print(name, username, password, email, usertype)
            mydb.commit()
        return render_template("login.html")

@app.route('/addArtToWishlist<id>', methods = ['POST', 'GET'])
def addArtToWishlist(id):
    curr_user_type=""
    myquery = "select exists(select name, username, email, usertype from users where username=%s)"
    rec_tup = (curr_user,)
    mycursor.execute(myquery, rec_tup)
    if mycursor.fetchone()[0]==1:
        myquery = "select name, username, email, usertype from users where username=%s"
        mycursor.execute(myquery, rec_tup)
        for i in mycursor.fetchall():
            curr_user_type = i[3]
    print(curr_user_type)
    if request.method == 'POST':
        # return render_template('Err.html', message="HELLO")
        if curr_user_type=="Customer":
            myquery = "select username, art_id from wishlist where username=%s"
            rec_tup = (curr_user,)           
            mycursor.execute(myquery,rec_tup)
            for i in mycursor.fetchall():
                print(i)
                if i[1]==id:
                    # return '<body>Art already in wishlist!</body>'
                    return render_template('Err.html', message="Art already in wishlist!")
                else:
                    continue
            mysql_query = "insert into wishlist values(%s, %s)"
            records = (curr_user, id)
            mycursor.execute(mysql_query, records)
            # print(name, username, password, email, usertype)
            mydb.commit()
            # return '<body>Art added to wishlist successfully!</body>'
            return render_template('Err1.html', message="Art added to wishlist successfully!")
        else:
            # return '<body>Only customers are allowed to add art(s) to wishlist!</body>'
            return render_template('Err.html', message="Only customers are allowed to add art(s) to wishlist!")
    else:
        return render_template('Err.html', message="You are not allowed to add art to wishlist!")
        # return '<body>You are not allowed to add art to wishlist!</body>'

@app.route('/addArt', methods = ['POST', 'GET'])
def addArt():
    return render_template('addart.html')

@app.route('/thanks')
def thanks():
    return render_template('Err1.html', message="Payment successfull, thanks for purchase")

@app.route('/insertArt', methods = ['POST', 'GET'])
def insertArt():
    if request.method == 'POST':
        art_id = request.form["art_id"]
        price = request.form["price"]
        if curr_user_type=="Artist":
            mysql_query = "insert into arts values(%s, %s, %s)"
            records = (curr_user, art_id, price)
            mycursor.execute(mysql_query, records)
            # print(name, username, password, email, usertype)
            mydb.commit()
            return render_template('Err.html', message="Art added successfully")
        else:
            return render_template('Err.html', message="Only artists are allowed to add art")

@app.route('/showWishlist', methods = ['POST', 'GET'])
def showWishlist():
    # global curr_user
    if request.method == 'POST':
        # fromDest = request.form["from"]
        # toDest = request.form["to"]
        # #depDate = request.form["depDate"]
        # classF = request.form["classF"]

        username = ""
        art_id = ""
        # a_code = []
        # depTime = []
        # arrTime = []
        # fare = []
        myquery = "select wishlist.art_id, arts.price from arts inner join wishlist on arts.art_id=wishlist.art_id where wishlist.username=%s"
        rec_tup = (curr_user,)
        mycursor.execute(myquery, rec_tup)
        data = mycursor.fetchall()
        print(data) 

        '''
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_1Hbn8MJQL31GMhtiEqCyOhMY',
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('showWishlist', _external=True),
        )
        '''


        return render_template('showwishlist.html', 
            data = data, 
            #csi = session['id'], 
            #cpk = app.config['STRIPE_PUBLIC_KEY'] 
            )


        # myquery = "select exists(select username, art_id from wishlist where username=%s)"
        # rec_tup = (curr_user,)
        # mycursor.execute(myquery, rec_tup)
        # if mycursor.fetchone()[0]==1:
        #     myquery = "select username, art_id from wishlist where username=%s"
        #     mycursor.execute(myquery, rec_tup)
        #     for i in mycursor.fetchall():
        #         username = i[0]
        #         art_id = i[1]
        #     return render_template("wishlist.html", username = username, art_id = art_id)
        # else:
        #     return "<body>No Flights Found according to your choices</body>"

@app.route('/userProfile', methods = ['POST', 'GET'])
def userProfile():
    # global curr_user
    if request.method == 'POST':
        # fromDest = request.form["from"]
        # toDest = request.form["to"]
        # #depDate = request.form["depDate"]
        # classF = request.form["classF"]

        name = ""
        username = ""
        email = ""        
        usertype = ""
        # a_code = []
        # depTime = []
        # arrTime = []
        # fare = []

        myquery = "select exists(select name, username, email, usertype from users where username=%s)"
        rec_tup = (curr_user,)
        mycursor.execute(myquery, rec_tup)
        if mycursor.fetchone()[0]==1:
            myquery = "select name, username, email, usertype from users where username=%s"
            mycursor.execute(myquery, rec_tup)
            for i in mycursor.fetchall():
                name = i[0]
                username = i[1]
                email = i[2]
                usertype = i[3]
            return render_template("userprofile.html", usertype = usertype, name = name, username = username, email = email)

@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    curr_user=""
    curr_user_type=""
    return render_template('login.html')


@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'whsec_nkO14mwqSr3h0Q4ceod6i5k8nVyDDC6b'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}

@app.route('/stripe_pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1Hbn8MJQL31GMhtiEqCyOhMY',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('showWishlist', _external=True),
    )
    print(session)
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }

if __name__ == "__main__":
    app.run(debug=True)