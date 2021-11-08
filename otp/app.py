from dotenv.main import load_dotenv
from flask import Flask, render_template, flash
from flask.globals import request, session
import random
import json
import os
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
service = os.getenv("service")



client = Client(account_sid, auth_token)
app = Flask(__name__)
app.secret_key = 'your secret key here'


@app.route('/', methods=["POST", "GET"])
def home():
    return render_template('index.html')


@app.route('/getotp', methods=['POST'])
def getotp():
    number = request.form['number']
    # val = getOTPApi(number)
    verification = client.verify \
                     .services(service) \
                     .verifications \
                     .create(to='+917890032256', channel='sms')

    print(verification.status)
    if verification:
        return render_template('enterotp.html')
    else:
        flash("Error")


@app.route('/verifyotp', methods=['POST', 'GET'])
def verifyotp():
    recv_code = request.form['otp']
    verification_check = client.verify \
                           .services(service) \
                           .verification_checks \
                           .create(to='+917890032256', code = recv_code)

    print(verification_check.status)
    if verification_check:
        print("OTP verified")
        return render_template("resultpage.html")
    else:
        print("OTP not verified")
    return render_template("resultpage2.html")


if __name__ == '__main__':
    app.run(host='localhost', port=5000)