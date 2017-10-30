from flask import Flask, redirect, request
import re
import sys

app = Flask(__name__)
app.config['DEBUG'] = True

signup_form = """
    <style>
        .error {{ color: red; }}
    </style>
    <h1>Signup</h1>
    <form method='POST'>
        <table>
            <tbody>
                <tr> <td>
        <label>Username
            <input name="username" type="text" value='{username}' />
        </label>
        <span class="error">{username_error}</p>
                </td></tr>
                <tr><td>
        <label>Password
            <input name="password" type="text" value='{password}' />
        </label>
        <span class="error">{password_error}</p>
                </tr></td>
                <tr><td>
        <label>Verify Password
            <input name="verify_password" type="text" value='{verify_password}' />
        </label>
        <span class="error">{verify_password_error}</p>
                </tr></td>
                <tr><td>
        <label>Email (optional)
            <input name="email" type="text" value='{email}' />
        </label>
        <span class="error">{email_error}</p>
                </tr></td>
        </tbody>
        </table>
        <input type="submit" value="Signup!" />
    </form>
    """

@app.route('/')
def index():
    return redirect('/signup')

@app.route('/signup')
def display_signup_form():
    return signup_form.format(username='', username_error='',
 password='', password_error='', verify_password='', verify_password_error='', email='', email_error='')

def is_valid(x): 
    if x is "" or x.find(" ") > -1 or len(x) <= 3 or len(x) > 20: 
        return False 
    
    else: 
        return True 

def is_valid_email(x):
    if x is "":
        return True

    if x.find(" ") > -1 or len(x) <= 3 or len(x) > 20: 
        return False
    
    elif x.find("@" and "."): 
        return True

    return False

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    print('request username={0}'.format(username), file=sys.stderr)

    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = '' 
    

    if not is_valid(username): 
        print('Invalid username={0}'.format(username), file=sys.stderr)
        username_error = "Not a valid username" 

    print('After validation username={0}'.format(username), file=sys.stderr)    

    if not is_valid(password):
        password_error = "Not a valid password"
        password = ''
        
    if not is_valid_email(email):
        email_error = "Not a valid email"

    if password != verify_password:
        verify_password_error = "Verify password does not match"
        verify_password = ''

    if username_error is '' and password_error is '' and verify_password_error is '' and email_error is '':
        login = str(username)
        print('Found valid username={0}'.format(username), file=sys.stderr)
        return redirect('/valid-signup?login={0}'.format(login))

    else:
        return signup_form.format(username=username, username_error=username_error, 
    password=password, password_error=password_error, 
    verify_password=verify_password, verify_password_error=verify_password_error, 
    email=email, email_error=email_error)
 
     

@app.route('/valid-signup')
def valid_signup():

    login=request.args.get('login')
    return '<h1>Welcome {0}.</h1>'.format(login)


app.run()