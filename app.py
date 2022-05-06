# importing needed libraries
from flask import *
from flask_bootstrap import Bootstrap
import pyotp
import random

# configuring flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "APP_SECRET_KEY"
Bootstrap(app)
# totp = pyotp.TOTP("base32secret3232")
# hotp = pyotp.HOTP("base32secret3232")

# homepage route
@app.route("/")
def index():
	return "<h1>Hello World!</h1>"

@app.route("/home", methods=['GET','POST'])
def home():
	if request.method == 'POST':
		otp = request.form['otp']
		return otp
	return render_template('home.html')

@app.route("/send_hotp", methods=['GET','POST'])
def send_hotp():
	# hotp method
	hotp = pyotp.HOTP("base32secret3232")
	counter = random.randint(100000,999999)
	otp = hotp.at(counter)
	session["o_counter"] = counter
	print(otp)
	
	return "OTP send"


@app.route("/verify_hotp", methods=['GET','POST'])
def verify_hotp():
	hotp = pyotp.HOTP("base32secret3232")
	if "o_counter" in session:
		counter = session['o_counter']
		if 'otp' in request.form:
			otp = request.form['otp']
			result = hotp.verify(otp, counter)
			if result:
				session.pop('o_counter', None)
			return {'data': result}
		else:
			return {'data': False}
	else:
		return {'data': False}

@app.route("/send_totp", methods=['GET','POST'])
def send_totp():
	# totp method
	secret = pyotp.random_base32()
	totp = pyotp.TOTP(secret)
	print(totp.now())
	session["totp_secret"] = secret

	return "OTP send"

@app.route("/verify_totp", methods=['GET','POST'])
def verify_totp():
	if "totp_secret" in session:
		secret = session["totp_secret"]
		if "otp" in request.form:
			otp = request.form["otp"]
			totp = pyotp.TOTP(secret)
			# if totp.verify(otp):
				# session.pop('o_counter', None)
			return {'data': totp.verify(otp)}
		else:
			return {'data': False}
	else:
		return {'data': False}


# running flask server
if __name__ == "__main__":
    app.run(debug=True)