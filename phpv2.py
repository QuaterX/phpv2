import re
import mysql.connector
from appJar import gui

app = gui("PhPmyAdminV2", "1100x800")

dblist = list()
tblist = list()


# It's a class that will contain any methods related to databases and it's data
class DataQuery:
    @staticmethod
    def databases():
        query = mydblogin.cursor()
        query.execute("SHOW DATABASES")
        for database_instances in query:
            dblist.append(database_instances)

    @staticmethod
    def tables():
        tblist_length = len(tblist)
        tblist.clear()

        database = app.getOptionBox("Databases")
        dbname = re.sub("[(,)]", "", database)

        query = mydblogin.cursor()
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = " + dbname

        query.execute(sql)
        for instances in query:
            tblist.append(instances)
        if tblist_length > 0:
            app.changeOptionBox("Tables", tblist)

    @staticmethod
    def databaselogin(hostname, username, password):
        global mydblogin
        mydblogin = mysql.connector.connect(
            host=hostname,
            user=username,
            password=password
        )
        gui.initialize_main()


# It's a class containing gui methods for subwindows and main window
class GuiClass:

    @staticmethod
    def initialize_main():
        app.setBg("orange")
        app.setFont(18)

        data.databases()

        app.addOptionBox("Databases", dblist)
        app.setOptionBoxChangeFunction("Databases", data.tables)

        data.tables()

        app.addOptionBox("Tables", tblist)

        app.hideSubWindow("Login")

        gui.sql_subwindow()

        app.addButton("SQL", gui.show_sql_subwindow)

        app.show()

    @staticmethod
    def login_subwindow():
        app.startSubWindow("Login")

        app.addLabel("login_title", "Please login")
        app.addLabelEntry("IP")
        app.addLabelEntry("Username")
        app.addSecretLabelEntry("Password")
        app.setFocus("Username")
        app.addNamedButton("Submit", "login_submit", button.login_submit)
        app.addNamedButton("Cancel", "login_cancel", button.cancel)

        app.stopSubWindow()

    @staticmethod
    def sql_subwindow():
        app.startSubWindow("SQLQuery")

        app.addLabel("sql_title", "SQL query executor")
        app.addScrolledTextArea("SQL")
        app.addNamedButton("Submit", "sql_submit", button.sql_submit)

        app.stopSubWindow()

    @staticmethod
    def sql_faliure():
        app.setLabel("sql_title", "Something went wrong with your syntax")

    @staticmethod
    def sql_succes(query):
        app.setLabel("sql_title", query)

    @staticmethod
    def show_sql_subwindow():
        app.showSubWindow("SQLQuery")


# It's a class for methods that will be called upon pressing corresponding buttons
class ButtonPress:
    @staticmethod
    def cancel():
        app.stop()

    @staticmethod
    def login_submit():
        ip = app.getEntry("IP")
        user = app.getEntry("Username")
        if len(app.getEntry("Password")) > 0:
            passw = app.getEntry("Password")
        else:
            passw = ""
        data.databaselogin(ip, user, passw)

    @staticmethod
    def sql_submit():
        sql = app.getTextArea("SQL")
        if len(sql) > 0:
            try:
                query = mydblogin.cursor()
                query.execute(sql)
                gui.sql_succes(query)
            except:
                gui.sql_faliure()


# Naming for all classes
data = DataQuery
button = ButtonPress
gui = GuiClass

# App is started here with the login subwindow as it's starting window
gui.login_subwindow()
app.go(startWindow="Login")
