from flask import Flask, render_template, redirect, url_for, request, flash
from flask.helpers import send_file
from io import BytesIO
import sqlite3
from datetime import date

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

    final_rs = []

    for i in rs:
        i = list(i)
        c.execute("SELECT COUNT(custid) FROM bookings WHERE iscleared =0 AND custid = '"+str(i[0])+"'")
        count = c.fetchone()
        i.append(count[0])
        final_rs.append(i)


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
    return render_template('customer.html', final_rs=final_rs)

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
@app.route('/booking', methods = ['POST', 'GET'])
def booking():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT custid, custname FROM customers")
    customers = c.fetchall()

    c.execute("SELECT * FROM bookings where iscleared = '0'")
    bookings = c.fetchall()

    final_bookings = []

    for i in bookings:
        i = (list(i))
        for j in customers:
            if i[1] == j[0]:
                i.append(j[1])
                final_bookings.append(i)
                break

    if request.method == 'POST':
        customerid = request.form['customerid']
        droneshottype = request.form['droneshottype']
        location = request.form['location']
        deadlinedate = request.form['deadlinedate']
        createdate = today = date.today()

        c.execute("INSERT INTO bookings (custid, droneshottype, location, createdate, deadlinedate) VALUES (?, ?, ?, ?, ?)", (customerid, droneshottype, location, createdate, deadlinedate))
        conn.commit()
        flash("Booking Created !", 'booking_register')

        return(redirect(url_for('booking')))

    conn.close()

    context = {
        'customers': customers,
        'final_bookings': final_bookings
    }

    return render_template('booking.html', **context)

@app.route('/booking_update<int:id>')
def booking_update(id):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("UPDATE bookings SET iscleared = '1' WHERE bookingid = '"+str(id)+"'")
    conn.commit()

    c.execute("SELECT custid FROM bookings WHERE bookingid = '"+str(id)+"'")
    rs = c.fetchone()

    c.execute("UPDATE customers SET clearedbooking = (clearedbooking + 1) WHERE custid = '"+str(rs[0])+"'")
    conn.commit()

    conn.close()

    flash("Booking Cleared ! ", 'booking_clear')
    return redirect(url_for('booking'))

@app.route('/booking_delete<int:id>')
def booking_delete(id):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("DELETE FROM bookings WHERE bookingid = '"+str(id)+"'")
    conn.commit()
    conn.close()
    flash("Booking Cancelled ! ", 'booking_delete')
    return redirect(url_for('booking'))

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