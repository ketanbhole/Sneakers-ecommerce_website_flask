from flask import Flask
from flask_mysqldb import MySQL
import pymysql


app = Flask(__name__)

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Dell@2017#',
    db='user_system',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


cursor = connection.cursor()
app.secret_key = 'xyzsdfg'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Dell@2017#'
app.config['MYSQL_DB'] = 'user_system'

mysql = MySQL(app)

