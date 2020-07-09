from flask import Flask, request, flash, redirect, render_template, request, url_for, session, g, abort
from random import randint
from flask_mail import Mail, Message
import os
from flaskext.mysql import MySQL
from functools import wraps
 

import pandas as pd
columns = ['Name', 'Links', 'Website', 'Phone', 'Address', 'E-mail']
contactdf = pd.DataFrame(columns=columns)

#Login to LinkedIn
from selenium import webdriver
from bs4 import BeautifulSoup
import getpass
import requests
from selenium.webdriver.common.keys import Keys
import pprint
from selenium.common.exceptions import NoSuchElementException
import csv
import time


app = Flask(__name__)


app.config['MYSQL_DATABASE_HOST'] = 'localhost' 
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'test1'

mysql = MySQL(app)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'YOUR GMAIL EMAIL ADDRESS',
    "MAIL_PASSWORD": 'GMAIL PASSWORD'
}

app.config.update(mail_settings)
mail = Mail(app)
 

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap            


@app.route("/")
def index():
    return "Flask App!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != "mukesh" :
            error = 'Invalid username'
        elif request.form['password'] != "mukesh" :
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            # flash('You were logged in')
            return redirect(url_for('form'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    # flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/form')
@login_required
def form():
	return render_template('form.html')

@app.route('/form', methods=['POST'])
def form_post():
    # text = request.form['email', 'pass', 'keyword', 'page']
    userid = request.form['mail']
    password = request.form['pasw']
    keyword = request.form['key']
    pagenum = request.form['num']

    print(keyword)

    # processed_text = text.upper()

    print(userid)
    options = webdriver.ChromeOptions()
    print(pagenum)
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    print(pagenum)  
    driver = webdriver.Chrome('./chromedriver', options=options)
    print(2)
    driver.get("https://www.linkedin.com")
    driver.implicitly_wait(6)
    print(3)
    
    # driver.find_element_by_xpath("""//*[@id="login-email"]""").send_keys(userid)
    # driver.find_element_by_xpath("""//*[@id="login-password"]""").send_keys(password)
    # driver.find_element_by_xpath("""//*[@id="login-submit"]""").click()

    driver.find_element_by_class_name('login-email').send_keys(userid)
    driver.find_element_by_class_name('login-password').send_keys(password)
    driver.find_element_by_xpath('//*[@type="submit"]').click()

	# keyword=input("Please search for people: ")
	# pagenum=input("Please enter search page number: ")
    print(4)
    search_bar="https://www.linkedin.com/search/results/people/v2/?keywords="+keyword+"&origin=SWITCH_SEARCH_VERTICAL&page="+pagenum
    print(search_bar)
    driver.get(search_bar)
    print("search_bar1")
    
    SCROLL_PAUSE_TIME = 4.0
    # Get scroll height

    print(2)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        print(2)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    cards = driver.find_elements_by_class_name('search-result__result-link')
    links =[]
    for card in cards:
        links.append(card.get_attribute('href'))

    onelinks =set(links)
    contactdf['Links']=list(onelinks)

    print(3)

    for i in range(len(contactdf)):
            driver.get(contactdf['Links'][i] + 'detail/contact-info')
            try:
                name = driver.find_element_by_id('pv-contact-info').text
            except NoSuchElementException:
                name = ""
            try:
                website = driver.find_element_by_class_name('ci-websites').find_element_by_class_name('pv-contact-info__contact-link').text
            except NoSuchElementException:
                website = ""

            try:
                phone = driver.find_element_by_class_name('ci-phone').find_element_by_class_name('pv-contact-info__ci-container').find_element_by_tag_name('span').text
            except NoSuchElementException:
                phone = ""

            try:
                address = driver.find_element_by_class_name('ci-address').find_element_by_class_name('pv-contact-info__contact-link').text
            except NoSuchElementException:
                address = ""

            try:
                email = driver.find_element_by_class_name('ci-email').find_element_by_class_name('pv-contact-info__contact-link').text
            except NoSuchElementException:
                email = ""

            print(i)
    
            contactdf['Name'][i] = name
            contactdf['Phone'][i] = phone
            contactdf['Address'][i] = address
            contactdf['E-mail'][i] = email
            contactdf['Website'][i] = website
            contactdf.fillna('Default')

            cur = mysql.get_db().cursor()

            sql = "INSERT INTO data (Name, Link, Website, Phone, Address, Mail) VALUES (%s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (name, contactdf['Links'][i], website, phone, address, email))

            mysql.get_db().commit()
            
    # print("To check the result type : contactdf")
    print(5)

    print(contactdf)
    driver.close()

    return contactdf.to_html()


@app.route('/send-mail')
@login_required
def send_mail():
    return render_template('mail_form.html')

@app.route('/send-mail', methods=['POST'])
def send():

    subject = request.form['subj']
    recipient = request.form['reci'].split(",")
    body = request.form['body']

    try:
        msg = Message(subject=subject,
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=recipient, # replace with your email for testing
                      body=body)
        mail.send(msg)
        return 'Mail Sent'

    except Exception as e:
        return str(e)

@app.route('/user-data')
@login_required

def list_users():
    cur = mysql.get_db().cursor()

    sql = "SELECT * from data"
    cur.execute(sql)

    data = cur.fetchall()

    # return data
    return render_template("user_show.html", data=data)            

 	
if __name__ == "__main__":

    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True, host='0.0.0.0', port=9002)
