import re

import errno

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
            dblist.append(re.sub("[(,')]", "", database_instances[0]))

    @staticmethod
    def use_database():
        database = app.getOptionBox("Databases")
        dbname = re.sub("[(,')]", "", database)

        query = mydblogin.cursor()
        query.execute("USE " + dbname)

    @staticmethod
    def database_create():
        print()

    @staticmethod
    def database_delete():
        print()

    @staticmethod
    def tables():
        tblist_length = len(tblist)
        tblist.clear()

        database = app.getOptionBox("Databases")
        dbname = re.sub("[(,)]", "", database)

        query = mydblogin.cursor()
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = '" + dbname + "'"

        query.execute(sql)
        for instances in query:
            tblist.append(re.sub("[(,')]", "", instances[0]))
        if tblist_length > 0:
            app.changeOptionBox("Tables", tblist)

    @staticmethod
    def drop_table():
        table = app.getOptionBox("Tables")
        tbname = re.sub("[(,')]", "", table)

        query = mydblogin.cursor()
        query.execute("DROP TABLE " + tbname)
        data.tables()

    @staticmethod
    def create_table():
        amount_of_cols = int(app.getEntry("ColumnAmount"))
        loops = 1
        sql = "CREATE TABLE " + app.getEntry("table_name") + " ("
        indexes_amount = 0
        indexes = list()

        while loops <= amount_of_cols:
            col_name = app.getEntry("col_name_" + str(loops))
            col_type = app.getOptionBox("col_type_" + str(loops))
            col_length = app.getEntry("col_length_" + str(loops))

            if app.getCheckBox("col_isnull_" + str(loops)):
                col_isnull = "NULL"
            else:
                col_isnull = "NOT NULL"

            index_name = app.getEntry("index_name_" + str(loops))

            if app.getOptionBox("col_index_" + str(loops)) == "PRIMARY":
                col_index = app.getOptionBox("col_index_" + str(loops)) + " KEY (" + app.getEntry(
                    "col_name_" + str(loops)) + ")"
                indexes_amount += 1
                indexes.append(col_index)
            elif (app.getOptionBox("col_index_" + str(loops)) == "UNIQUE" or app.getOptionBox("col_index_" + str(loops))
                  == "INDEX"):
                col_index = app.getOptionBox(
                    "col_index_" + str(loops)) + " " + index_name + "" + " (" + app.getEntry(
                    "col_name_" + str(loops)) + ")"
                indexes_amount += 1
                indexes.append(col_index)

            if app.getCheckBox("col_ai_" + str(loops)):
                col_ai = "AUTO_INCREMENT"
            else:
                col_ai = ""

            if len(app.getEntry("col_comments_" + str(loops))) > 0:
                col_comments = "COMMENT '" + app.getEntry("col_comments_" + str(loops)) + "'"
            else:
                col_comments = ""

            if loops <= amount_of_cols:
                if col_type == "VARCHAR" or len(col_length) > 0:
                    sql += ("" + col_name + " " + col_type + "(" + col_length + ") " + col_isnull + " " + col_ai + " "
                            + col_comments + ",")
                else:
                    sql += "" + col_name + " " + col_type + " " + col_isnull + " " + col_ai + " " + col_comments + ","
                loops += 1

        loops = 0
        print(indexes_amount)
        if indexes_amount > 0:
            while loops < indexes_amount:
                print(loops)
                if loops == indexes_amount - 1:
                    sql += " " + indexes[loops] + ");"
                    loops += 1
                elif loops < indexes_amount:
                    sql += " " + indexes[loops] + ", "
                    loops += 1

        query = mydblogin.cursor()

        try:
            query.execute(sql)
        except:
            print("Something went wrong    " + sql)

    @staticmethod
    def column_select():
        sql = ("SELECT column_name FROM information_schema.columns WHERE table_name = '" +
               str(app.getOptionBox("Tables")) + "' && column_key = 'PRI'")
        # print(sql)

        query = mydblogin.cursor()
        query.execute(sql)

        loops = 1
        for instances in query:
            app.openScrollPane("RIGHT_SCROLLPANE")
            app.addLabel("col_name_" + str(loops), instances[0], 2, loops)
            app.stopScrollPane()
            loops += 1

        loops = 1
        sql = ("SELECT column_name FROM information_schema.columns WHERE table_name = '" +
               str(app.getOptionBox("Tables")) + "'")
        query.execute(sql)

        for instances in query:
            app.openScrollPane("RIGHT_SCROLLPANE")
            app.addLabel("col_name_" + str(loops + 1), instances[0], 2, loops + 1)
            app.stopScrollPane()
            loops += 1

    @staticmethod
    def column_data_select():
        sql = "SELECT * FROM " + app.getOptionBox("Tables")
        query = mydblogin.cursor()
        query.execute(sql)

        loops = 0
        for instances in query:
            how_much_cols = len(instances)
            if 
            loops += 1

    @staticmethod
    def database_login(hostname, username, password):
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
        app.setSticky("ew")
        app.setPadding([10, 10])
        app.setExpand("row")

        app.startFrame("LEFT", 0, 0, 2)
        app.setSticky("ew")
        app.setExpand("none")
        app.setPadding([0, 10])

        data.databases()
        app.addOptionBox("Databases", dblist, 1, 0)
        app.setOptionBoxChangeFunction("Databases", event.database_change)
        app.addNamedButton("Create database", "database_create", data.database_create, 2, 0)
        app.addNamedButton("Delete database", "database_delete", data.database_delete, 3, 0)
        data.use_database()

        app.addOptionBox("Tables", tblist, 4, 0)
        app.setOptionBoxChangeFunction("Tables", event.table_change)
        data.tables()

        app.hideSubWindow("Login")

        gui.sql_subwindow()

        app.addNamedButton("Drop selected table", "Drop_table_button", data.drop_table)

        app.stopFrame()
        app.addButton("SQL", gui.show_sql_subwindow, 1, 0)
        app.addButton("Exit", button.login_cancel, 1, 1)

        app.startFrame("RIGHT", 0, 2)
        app.addLabelEntry("ColumnAmount", 0, 0)
        app.addNamedButton("Create table", "create_table", button.create_table_subwindow_submit, 0, 1)
        app.startScrollPane("RIGHT_SCROLLPANE", 1, 0)
        app.addEmptyLabel("e")
        app.stopScrollPane()
        app.stopFrame()


        app.show()

    @staticmethod
    def login_subwindow():
        app.startSubWindow("Login")
        app.startLabelFrame("Login details")
        app.setSticky("ew")
        app.setFont(20)

        app.addLabel("login_label_1", "IP", 0, 0)
        app.addEntry("login_ip", 0, 1)
        app.setEntry("login_ip", "localhost")
        app.addLabel("login_label_2", "Username", 1, 0)
        app.addEntry("login_username", 1, 1)
        app.setEntry("login_username", "root")
        app.addLabel("login_label_3", "Password", 2, 0)
        app.addSecretEntry("login_password", 2, 1)
        app.setFocus("login_ip")
        app.addNamedButton("Submit", "login_submit", button.login_submit, 3, 1)
        app.addNamedButton("Cancel", "login_cancel", button.login_cancel, 3, 0)
        app.button('Accessibility', app.showAccess, icon='ACCESS')

        app.stopLabelFrame()
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

    @staticmethod
    def create_table_subwindow():
        if len(app.getEntry("ColumnAmount")) > 0:
            app.startSubWindow("CreateTable")
            amount_of_cols = int(app.getEntry("ColumnAmount"))
            loops = 1

            app.addLabel("TableName", "Table Name", 0, 0)
            app.addLabelEntry("table_name", 0, 1)
            app.addLabel("Name", "Name", 1, 0)
            app.addLabel("Type", "Type", 1, 1)
            app.addLabel("Length", "Length", 1, 2)
            app.addLabel("Null", "Null", 1, 3)
            app.addLabel("Index", "Index", 1, 4)
            app.addLabel("Index_Name", "Index Name", 1, 5)
            app.addLabel("A_I", "A_I", 1, 6)
            app.addLabel("Comments", "Comments", 1, 7)

            while loops <= amount_of_cols:
                app.addLabelEntry("col_name_" + str(loops), (loops + 1), 0)
                app.addOptionBox("col_type_" + str(loops), ["INT", "VARCHAR", "TEXT", "DATE"], (loops + 1), 1)
                app.addLabelEntry("col_length_" + str(loops), (loops + 1), 2)
                app.addCheckBox("col_isnull_" + str(loops), (loops + 1), 3)
                app.addOptionBox("col_index_" + str(loops), ["---", "PRIMARY", "UNIQUE", "INDEX"], (loops + 1), 4)
                app.addLabelEntry("index_name_" + str(loops), (loops + 1), 5)
                app.addCheckBox("col_ai_" + str(loops), (loops + 1), 6)
                app.addLabelEntry("col_comments_" + str(loops), (loops + 1), 7)
                loops += 1

            app.addNamedButton("Submit", "create_table_submit", button.create_table_submit)
            app.addNamedButton("Cancel", "create_table_cancel", button.create_table_cancel)

            app.stopSubWindow()


# It's a class for methods that will be called upon pressing corresponding buttons
class ButtonPress:
    @staticmethod
    def login_cancel():
        app.stop()

    @staticmethod
    def login_submit():
        ip = app.getEntry("login_ip")
        user = app.getEntry("login_username")
        if len(app.getEntry("login_password")) > 0:
            passw = app.getEntry("login_password")
        else:
            passw = ""
        data.database_login(ip, user, passw)

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

    @staticmethod
    def create_table_subwindow_submit():
        gui.create_table_subwindow()
        app.showSubWindow("CreateTable")

    @staticmethod
    def create_table_submit():
        app.hideSubWindow("CreateTable")

        data.create_table()

        app.destroySubWindow("CreateTable")

    @staticmethod
    def create_table_cancel():
        app.destroySubWindow("CreateTable")


class GuiEvents:
    @staticmethod
    def database_change():
        try:
            data.tables()
            data.use_database()
        except IOError:
            None
            # insert error handler here

    @staticmethod
    def table_change():
        try:
            data.column_select()
        except IOError as e:
            if e.errno == errno.ENOENT:
                print(e.strerror)
            elif e.errno == errno.EBADF:
                print(e.strerror)

    @staticmethod
    def login_close():
        app.stop()

    @staticmethod
    def createtable_close():
        app.destroySubWindow("CreateTable")

# Naming for all classes
data = DataQuery
button = ButtonPress
gui = GuiClass
event = GuiEvents

# App is started here with the login subwindow as it's starting window
gui.login_subwindow()
app.go(startWindow="Login")

