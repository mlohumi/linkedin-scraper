# Linkedin Scraper - Scrape LinkedIn profiles

This is a LinkedIn scraper to abstract data such as Name, Email, Contact Number etc of individuals and companies from LinkedIn. It has a rich UI to type in the keyword you would like to search in LinkedIn, the data will be collected and stored in the database. You can send e-mails to selected profiles from the frontend itself.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. You can further use it for production as well.

### Prerequisites

Download the chrome driver corresponding to your chrome version and os from

```
https://chromedriver.chromium.org/downloads
```

For those who are using latest version of MacOS - Catalina, locate the chrome driver and execute the following command on terminal

```
xattr -d com.apple.quarantine chromedriver
```
Windows and linux users, no need to worry about all these.

MySQL database server running.(you can also use the system without database)

### Installing 

Hope you have cloned the project, now locate the project directory

Firstly install the dependencies

```
pip install -r requirements.txt
```
## Deployment

Change the database credentials on line no.28 with yours. Then execute the following command on terminal

```
python3 app.py
```
you can now access the interface from your browser using 

```
http://localhost:9002/form
```

## Credentials

you can also use the flask authentication decorator to authenticate user's identity. By default it is not activated. Route for the same is

```
http://localhost:9002/login
```

Username : mukesh

Password : mukesh 


## To use mail server

Navigate to line number 40 & 41. Set you gmail's email address and password respectively.

## License

This project is free to use for educational and commercial purpose.

Happy Coding 😇
