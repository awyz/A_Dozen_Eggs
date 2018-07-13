# all the imports
import os
import cx_Oracle
import cgi
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import random

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py
amount = 0
price = 0.0
type = "Bread"
name = ""
month1= ""
seed1 = 14
# RANDOMIZE SEED NUMBER EACH SESSION


# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='awy',
    PASSWORD='hothotleg'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


con = cx_Oracle.connect('awy/hothotleg @127.0.0.1/XE')
cur = con.cursor()


@app.route('/')
def hello():
    #db = get_db()
    #init_db()
    #connect_db()
    return render_template('index.html')


form = cgi.FieldStorage()


@app.route('/add', methods=['GET', 'POST'])
def get_info():
    global seed1, type, name, amount, price, month1
    if request.method == 'POST':
        seed1 = random.randint(0, 1000000000000)
        id = seed1
        type = str(request.values.get('type'))
        name = str(request.values.get('name'))
        amount = float(request.values.get('amount'))
        price = float(request.values.get('price'))
        month1 = str(request.values.get('month1'))
    # Inserts data into the database after hitting submit
        rows = [(id, name, type, amount, price, month1)]
        cur.bindarraysize = 1
        cur.setinputsizes(int, 50, 50, int, float, 50)
        cur.executemany("insert into entries(id, name, type, amount, price, month1) values (:1, :2, :3, :4, :5, :6)", rows)
        con.commit()
    # End data insertion
    print(seed1)
    print(name)
    print(type)
    print(amount)
    print(price)
    print(month1)
    return render_template('add.html')


@app.route('/delete/<id>')
def delete(id):
    cur.prepare("DELETE FROM entries WHERE id= :id")
    cur.execute(None, {'id': id})
    return render_template('delete.html')


@app.route('/edit_entry/<id>', methods=['GET', 'POST'])
def edit_entry(id):
    print(id)
    cur = con.cursor()
    # Hardcoded for one thing right now!!! Make sure you change this!!!!
    # FOR MONTH1
    cur.prepare("select month1 from entries where id= :id")
    cur.execute(None, {'id': id})
    data = cur.fetchall()
    data=[i[0] for i in data]
    # FOR NAME2
    cur.prepare("select name from entries where id= :id")
    cur.execute(None, {'id': id})
    name2 = cur.fetchall()
    name2 = [i[0] for i in name2]
    # FOR PRICE2
    cur.prepare("select price from entries where id= :id")
    cur.execute(None, {'id': id})
    price2 = cur.fetchall()
    price2 = [i[0] for i in price2]
    # FOR AMOUNT2
    cur.prepare("select amount from entries where id= :id")
    cur.execute(None, {'id': id})
    amount2 = cur.fetchall()
    amount2 = [i[0] for i in amount2]
    # FOR TYPE2
    cur.prepare("select type from entries where id= :id")
    cur.execute(None, {'id': id})
    type2 = cur.fetchall()
    type2 = [i[0] for i in type2]
    # UPDATES TUPLE IN DB AFTER SUBMISSION
    if request.method == 'POST':
        cur = con.cursor()
        thetype = str(request.values.get('type'))
        thename = str(request.values.get('name'))
        theamount = float(request.values.get('amount'))
        theprice = float(request.values.get('price'))
        themonth1 = str(request.values.get('month1'))
    # Inserts data into the database after hitting submit
        statement = "UPDATE entries SET type=\'"+thetype+"\', name=\'"+thename+"\', amount="+str(theamount)+", price="\
                    +str(theprice)+", month1=\'"+themonth1+"\' WHERE id="+str(id)
        print("pls")
        cur.execute(statement)
        con.commit()
    # END UPDATE TUPLE IN DB
    return render_template('edit_entry.html', type2=type2, data=data, name2=name2, price2=price2, amount2=amount2, id=id)


@app.route('/inventory')
def inventory():
    return render_template('inventory.html')


@app.route('/all_inv')
def all_inv():
    cur = con.cursor()
    cur.execute("select * from entries")
    data = cur.fetchall()
    return render_template('all_inv.html', data=data)


@app.route('/bread')
def bread():
    cur = con.cursor()
    cur.execute("select * from entries where type='Bread'")
    data = cur.fetchall()
    print(data)
    return render_template('bread.html', data=data)


@app.route('/calendar')
def calendar():
    # January
    cur.execute("select sum(price) from entries where month1='Jan'")
    jan1 = cur.fetchall()
    jan1=[i[0] for i in jan1]
    if jan1[0] is None:
        jan1 = 0.0
    cur.execute("select type, count(type) as type_o from entries where month1 = 'Jan' group by type order by type_o desc")
    jan2 = cur.fetchall()
    jan2=[i[0] for i in jan2]
    # February
    cur.execute("select sum(price) from entries where month1='Feb'")
    feb1= cur.fetchall()
    feb1 = [i[0] for i in feb1]
    if feb1[0] is None:
        feb1 = 0.0
    cur.execute("select type, count(type) as type_o from entries where month1 = 'Feb' group by type order by type_o desc")
    feb2 = cur.fetchall()
    feb2=[i[0] for i in feb2]
    # March
    cur.execute("select sum(price) from entries where month1='March'")
    march1 = cur.fetchall()
    march1 = [i[0] for i in march1]
    if march1[0] is None:
        march1 = 0.0
    cur.execute("select type, count(type) as type_o from entries where month1 = 'March' group by type order by type_o desc")
    march2 = cur.fetchall()
    march2=[i[0] for i in march2]
    # April
    cur.execute("select sum(price) from entries where month1='April'")
    april1 = cur.fetchall()
    april1 = [i[0] for i in april1]
    if april1[0] is None:
        april1 = 0.0
    cur.execute("select type, count(type) as type_o from entries where month1 = 'April' group by type order by type_o desc")
    april2 = cur.fetchall()
    april2 =[i[0] for i in april2]
    # May
    cur.execute("select sum(price) from entries where month1='May'")
    may1 = cur.fetchall()
    may1 = [i[0] for i in may1]
    if may1[0] is None:
        may1 = 0.0
    cur.execute("select type, count(type) as type_o from entries where month1 = 'May' group by type order by type_o desc")
    may2 = cur.fetchall()
    may2 = [i[0] for i in may2]
    # June
    cur.execute("select sum(price) from entries where month1='June'")
    june1 = cur.fetchall()
    june1 = [i[0] for i in june1]
    if june1[0] is None:
        june1 = 0.0
    cur.execute("select type, count(type) as type_o from entries where month1 = 'June' group by type order by type_o desc")
    june2 = cur.fetchall()
    june2 = [i[0] for i in june2]
    # July
    cur.execute("select sum(price) from entries where month1='July'")
    july1 = cur.fetchall()
    july1 = [i[0] for i in july1]
    if july1[0] is None:
        july1 = 0.0
    cur.execute("select type, count(type) as type_o from entries where month1 = 'July' group by type order by type_o desc")
    july2 = cur.fetchall()
    july2 = [i[0] for i in july2]
    # August
    cur.execute("select sum(price) from entries where month1='Aug'")
    aug1 = cur.fetchall()
    aug1 = [i[0] for i in aug1]
    if aug1[0] is None:
        aug1 = 0.0
    cur.execute("select type, count(type) as type_o from entries where month1 = 'Aug' group by type order by type_o desc")
    aug2 = cur.fetchall()
    aug2=[i[0] for i in aug2]
    # September
    cur.execute("select sum(price) from entries where month1='Sep'")
    sep1 = cur.fetchall()
    sep1 = [i[0] for i in sep1]
    if sep1[0] is None:
        sep1 = 0.0
    cur.execute("select type, count(type) as type_o from entries where month1 = 'Sep' group by type order by type_o desc")
    sep2 = cur.fetchall()
    sep2 = [i[0] for i in sep2]
    # October
    cur.execute("select sum(price) from entries where month1='Oct'")
    oct1 = cur.fetchall()
    oct1 = [i[0] for i in oct1]
    if oct1[0] is None:
        oct1 = 0.0
    cur.execute("select type, count(type) as type_o from entries where month1 = 'Oct' group by type order by type_o desc")
    oct2 = cur.fetchall()
    oct2=[i[0] for i in oct2]
    # November
    cur.execute("select sum(price) from entries where month1='Nov'")
    nov1 = cur.fetchall()
    nov1 = [i[0] for i in nov1]
    if nov1[0] is None:
        nov1 = 0.0
    cur.execute("select type, count(type) as type_o from entries where month1 = 'Nov' group by type order by type_o desc")
    nov2 = cur.fetchall()
    nov2=[i[0] for i in nov2]
    # December
    cur.execute("select sum(price) from entries where month1='Dec'")
    dec1 = cur.fetchall()
    dec1 = [i[0] for i in dec1]
    if dec1[0] is None:
        dec1 = 0.0
    cur.execute("select type, count(type) as type_o from entries where month1 = 'Dec' group by type order by type_o desc")
    dec2 = cur.fetchall()
    dec2=[i[0] for i in dec2]
    return render_template('calendar.html', jan1=jan1, jan2=jan2, feb1=feb1, feb2=feb2, march1=march1, march2=march2, april2=april2, may2=may2, june2=june2, july2=july2, aug2=aug2, sep2=sep2, oct2=oct2, nov2=nov2, dec2=dec2, april1=april1, may1=may1, june1=june1, july1=july1, aug1=aug1, sep1=sep1, oct1=oct1, nov1=nov1, dec1=dec1)


@app.route('/can')
def can():
    cur = con.cursor()
    cur.execute("select * from entries where type='Can'")
    data = cur.fetchall()
    print(data)
    return render_template('can.html', data=data)


@app.route('/drink')
def drink():
    cur = con.cursor()
    cur.execute("select * from entries where type='Drink'")
    data = cur.fetchall()
    print(data)
    return render_template('drink.html', data=data)


@app.route('/dry')
def dry():
    cur = con.cursor()
    cur.execute("select * from entries where type='Dry'")
    data = cur.fetchall()
    print(data)
    return render_template('dry.html', data=data)


@app.route('/frozen')
def frozen():
    cur = con.cursor()
    cur.execute("select * from entries where type='Frozen'")
    data = cur.fetchall()
    print(data)
    return render_template('frozen.html', data=data)


@app.route('/meat')
def meat():
    cur = con.cursor()
    cur.execute("select * from entries where type='Meat'")
    data = cur.fetchall()
    print(data)
    return render_template('meat.html', data=data)


@app.route('/produce')
def produce():
    cur = con.cursor()
    cur.execute("select * from entries where type='Produce'")
    data = cur.fetchall()
    print(data)
    return render_template('produce.html', data=data)


@app.route('/dairy')
def dairy():
    cur = con.cursor()
    cur.execute("select * from entries where type='Dairy'")
    data = cur.fetchall()
    print(data)
    return render_template('dairy.html', data=data)


@app.route('/index')
def index():
    return render_template('index.html')




