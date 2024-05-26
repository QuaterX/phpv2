import re

import mysql.connector
from appJar import gui

dblist = list()
tblist = list()


def databases():
    x = mydblogin.cursor()
    x.execute("SHOW DATABASES")
    for y in x:
        dblist.append(y)


def tables():
    e = 0
    for h in tblist:
        e += 1
    tblist.clear()

    z = app.getOptionBox("Databases")
    db = re.sub("[(,)]", "", z)
    print(db)
    x = mydblogin.cursor()
    sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = " + db
    print(sql)
    x.execute(sql)
    for y in x:
        tblist.append(y)
    if e > 0:
        app.changeOptionBox("Tables", tblist)


def databaselogin(h, u, p):
    try:
        global mydblogin
        mydblogin = mysql.connector.connect(
            host=h,
            user=u,
            password=p
        )
        app.hideSubWindow("Login")
        app.show()
        databases()
        app.addOptionBox("Databases", dblist)
        app.setOptionBoxChangeFunction("Databases", tables)
        tables()
        app.addOptionBox("Tables", tblist)
    except:
        app.setLabel("title", "Login failure")


def press(button):
    if button == "Cancel":
        app.stop()
    else:
        ip = app.getEntry("IP")
        user = app.getEntry("Username")
        if len(app.getEntry("Password")) > 0:
            password = app.getEntry("Password")
        else:
            password = ""
        databaselogin(ip, user, password)


app = gui("PhPmyAdminV2", "1100x800")
app.setBg("orange")
app.setFont(18)

# Login subwindow beginning
app.startSubWindow("Login")

app.addLabel("title", "Please login")
app.addLabelEntry("IP")
app.addLabelEntry("Username")
app.addSecretLabelEntry("Password")
app.setFocus("Username")
app.addButtons(["Submit", "Cancel"], press)

app.stopSubWindow()
# Login subwindow ending

# SQL Query subwindow beginning
app.startSubWindow("SQL Query")

app.addLabel("title2", "Please write query in the textbox")

app.stopSubWindow()

app.go(startWindow="Login")
