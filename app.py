from flask import Flask, render_template, redirect, url_for, request, flash
from flask.helpers import send_file
from io import BytesIO
import sqlite3

app = Flask(__name__)
app.secret_key = 'ritesh'

database = './db.sqlite'

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

###############################################################
#   --- Customer Management Functionalities - START ---       #
###############################################################

@app.route('/customer', methods=['POST', 'GET'])
def customer():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM customers")
    rs = c.fetchall()

    if request.method == 'POST':
        custname = request.form['custname']
        custemail = request.form['custemail']
        custphone = request.form['custphone']
        custpic = request.files['custpic']

        c.execute("SELECT custemail, custphone from customers")
        li = c.fetchall()
        for li in li:
            if (custemail == li[0]) or (custphone == li[1]):
                flash("Email or Phone Number already associated with a customer", 'validemail')
                break
        else:
            c.execute("""
            INSERT into customers (custname, custemail, custphone, custpic) VALUES (?, ?, ?, ?)""", (custname, custemail, custphone, custpic.read()))
            conn.commit()
            flash("Customer Registration Sucessfull ! You can now do booking for this customer", 'customer_register')
            
        return redirect(url_for('customer'))

    conn.close()
    return render_template('customer.html', rs=rs)

@app.route('/customer_profile<int:id>')
def customer_profile(id):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM customers WHERE custid = '"+str(id)+"'")
    rs = c.fetchone()
    custpic = rs[4]
    conn.close()

    return send_file(BytesIO(custpic), download_name='customer_profile.png', as_attachment=False)

    return redirect(url_for('customer'))

@app.route('/customer_update<int:id>', methods=['POST', 'GET'])
def customer_update(id):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM customers WHERE custid = '"+str(id)+"'")
    rs = c.fetchone()

    if request.method == 'POST':
        custname = request.form['custname']
        custemail = request.form['custemail']
        custphone = request.form['custphone']
        custpic = request.files['custpic']

        c.execute("""
        UPDATE customers SET (custname, custemail, custphone, custpic) = (?, ?, ?, ?) WHERE custid = ?""", (custname, custemail, custphone, custpic.read(), id))
        conn.commit()
        flash("Customer Data Updated Sucessfully !", 'customer_update')

        return(redirect(url_for('customer')))
    
    return render_template('customer_update.html', rs=rs)

@app.route('/customer_delete<int:id>')
def customer_delete(id):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("DELETE FROM customers WHERE custid = '"+str(id)+"'")
    conn.commit()
    conn.close()
    flash("Customer Data deleted ! ", 'customer_delete')
    return redirect(url_for('customer'))

###############################################################
#   --- Customer Management Functionalities - END ---         #
###############################################################



###############################################################
#   --- Booking Management Functionalities - START ---        #
###############################################################

# Booking Page
@app.route('/booking')
def booking():
    return render_template('booking.html')

###############################################################
#   --- Booking Management Functionalities - END ---          #
###############################################################



###############################################################
#   --- Drone Management Functionalities - START ---          #
###############################################################
@app.route('/drone', methods=['POST', 'GET'])
def drone():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM drones")
    rs = c.fetchall()

    if request.method == 'POST':
        droneshottype = request.form['droneshottype']
        location = request.form['location']
        videolink = request.files['videolink']

        c.execute("""
        INSERT into drones (droneshottype, location, videolink) VALUES (?, ?, ?)""", (droneshottype, location, videolink.read()))
        conn.commit()
        flash("Drone Shot Registration Sucessfull ! You can now do booking for this drone shot", 'drone_register')
            
        return redirect(url_for('drone'))

    conn.close()
    return render_template('drone.html', rs=rs)

@app.route('/drone_video<int:id>')
def drone_video(id):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT * FROM drones WHERE droneid = '"+str(id)+"'")
    rs = c.fetchone()
    dronevideo = rs[3]
    conn.close()

    return send_file(BytesIO(dronevideo), download_name='drone_video.mp4', as_attachment=False)

    return redirect(url_for('drone'))

@app.route('/drone_delete<int:id>')
def drone_delete(id):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("DELETE FROM drones WHERE droneid = '"+str(id)+"'")
    conn.commit()
    conn.close()
    flash("Drone Shot deleted ! ", 'drone_delete')
    return redirect(url_for('drone'))

###############################################################
#   --- Drone Management Functionalities - END ---            #
###############################################################

if __name__ == '__main__':
    app.run(debug=True)