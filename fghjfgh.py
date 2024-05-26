import mysql.connector
from appJar import gui

app = gui("Login window", "400x200")
app.setBg("orange")
app.setFont(18)
app.addLabel("title", "Please login")

app.addLabelEntry("IP")
app.addLabelEntry("Username")
app.addSecretLabelEntry("Password")
app.setFocus("Username")


def databaselogin(h, u, p):
    try:
        global mydblogin
        mydblogin = mysql.connector.connect(
            host=h,
            user=u,
            password=p
        )
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


app.addButtons(["Submit", "Cancel"], press)

app.go()