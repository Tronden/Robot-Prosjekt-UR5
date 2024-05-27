from flask import Flask, request, flash, session, render_template, redirect
from flask_bootstrap import Bootstrap
import json, argparse
from screen import screenlive

secret_key = u'f71b10b68b1bc00019cfc50d6ee817e75d5441bd5db0bd83453b398225cede69'

app = Flask(__name__)
app.secret_key = secret_key
Bootstrap(app)

@app.route('/')
def welcome():
    session.clear()
    if len(screenlive.password) == 0:
        session['access'] = True
        return render_template("screen.html")
    else:
        return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    session.clear()
    if len(screenlive.password) == 0:
        session['access'] = True
        return render_template("screen.html")

    p = request.form["password"]
    if p == screenlive.password:
        session['access'] = True
        return render_template("screen.html")
    else:
        session.clear()
        flash("Wrong password")
        return render_template("login.html")

@app.route('/screenfeed/', methods=["POST"])
def screenfeed():
    if 'access' in session and session['access']:
        screen_data = screenlive.gen()
        print(f"Screen data length: {len(screen_data)}")  # Debug print
        return json.dumps([True, screen_data])
    else:
        return redirect('/')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="port, default 18331", type=int, default=18331)
    parser.add_argument("-w", "--password", help="password, default no password", default="")
    parser.add_argument("-s", "--https", help="enable https, default http", action="store_true")
    parser.add_argument("-c", "--cert", help="certificate file")
    parser.add_argument("-k", "--key", help="private key file")

    args = parser.parse_args()
    port = args.port
    screenlive.password = args.password

    try:
        if args.https:
            if args.cert and args.key:
                app.run(host='0.0.0.0', port=port, threaded=True, ssl_context=(args.cert, args.key))
            else:
                app.run(host='0.0.0.0', port=port, threaded=True, ssl_context='adhoc')
        else:
            app.run(host='0.0.0.0', port=port, threaded=True)
    except Exception as e:
        print(e)
        print("Some errors in the command, fall back to the default http screen sharing!!!\n")
        app.run(host='0.0.0.0', port=port, threaded=True)
