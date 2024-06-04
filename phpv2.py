import re

import mysql.connector

from appJar import gui

app = gui("PhPmyAdminV2", "1100x800")

tblist = []


# It's a class that will contain any methods related to databases and it's data
class DataQuery:
    @staticmethod
    def databases():
        global dblist
        dblist = list()
        query = mydblogin.cursor()
        query.execute("SHOW DATABASES")
        for database_instances in query:
            dblist.append(re.sub("[(,')]", "", database_instances[0]))
        try:
            app.changeOptionBox("Databases", dblist)
        except:
            None

    @staticmethod
    def use_database():
        database = app.getOptionBox("Databases")
        dbname = re.sub("[(,')]", "", database)

        query = mydblogin.cursor()
        query.execute("USE " + dbname)

    @staticmethod
    def database_create():
        new_db = app.getEntry("database_name")
        sql = "CREATE DATABASE " + str(new_db)
        query = mydblogin.cursor()
        query.execute(sql)
        data.databases()

    @staticmethod
    def database_delete():
        del_db = app.getOptionBox("Databases")
        sql = f"DROP DATABASE {del_db}"
        query = mydblogin.cursor()
        query.execute(sql)
        data.databases()

    @staticmethod
    def tables():
        tblist_length = len(tblist)
        tblist.clear()

        database = app.getOptionBox("Databases")
        dbname = re.sub("[(,)]", "", database)

        query = mydblogin.cursor()
        sql = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{dbname}'"

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
        query.execute(f"DROP TABLE {tbname}")
        data.tables()

    @staticmethod
    def create_table():
        amount_of_cols = int(app.getEntry("ColumnAmount"))
        table_name = app.getEntry("table_name")
        sql = f"CREATE TABLE {table_name} ("
        indexes = []

        for i in range(1, amount_of_cols + 1):
            col_name = app.getEntry(f"col_name_{i}")
            col_type = app.getOptionBox(f"col_type_{i}")
            col_length = app.getEntry(f"col_length_{i}")
            col_isnull = "NULL" if app.getCheckBox(f"col_isnull_{i}") else "NOT NULL"
            index_name = app.getEntry(f"index_name_{i}")
            col_index_option = app.getOptionBox(f"col_index_{i}")
            col_ai = "AUTO_INCREMENT" if app.getCheckBox(f"col_ai_{i}") else ""
            col_comments = f"COMMENT '{app.getEntry(f"col_comments_{i}")}'" if app.getEntry(f"col_comments_{i}") else ""

            if col_index_option == "PRIMARY":
                indexes.append(f"{col_index_option} KEY ({col_name})")
            elif col_index_option in ["UNIQUE", "INDEX"]:
                indexes.append(f"{col_index_option} {index_name} ({col_name})")

            if col_type == "VARCHAR" or col_length:
                sql += f"{col_name} {col_type}({col_length}) {col_isnull} {col_ai} {col_comments},"
            else:
                sql += f"{col_name} {col_type} {col_isnull} {col_ai} {col_comments},"

        for i, index in enumerate(indexes):
            if i == len(indexes) - 1:
                sql += f" {index});"
            else:
                sql += f" {index}, "

        query = mydblogin.cursor()

        try:
            query.execute(sql)
        except Exception as e:
            print(f"Something went wrong: {e}\nSQL: {sql}")

    global column_list
    column_list = []

    @staticmethod
    def column_select():
        if column_list:
            for instance in column_list:
                app.removeLabel(instance)
            column_list.clear()

        sql = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{app.getOptionBox('Tables')}'"
        query = mydblogin.cursor()
        query.execute(sql)

        for loops, instance in enumerate(query, start=1):
            app.openScrollPane("RIGHT_SCROLLPANE")
            label_name = f"col_name_{loops + 1}"
            app.addLabel(label_name, instance[0], 2, loops)
            column_list.append(label_name)
            app.stopScrollPane()

    global column_data_list
    column_data_list = []

    global column_button_list
    column_button_list = []

    @staticmethod
    def column_data_select():
        if column_data_list:
            for instances in column_data_list:
                app.removeLabel(instances)
        if column_button_list:
            for instances in column_button_list:
                app.removeButton(instances)
        column_data_list.clear()
        column_button_list.clear()

        sql = "SELECT * FROM " + app.getOptionBox("Tables")
        query = mydblogin.cursor()
        query.execute(sql)

        rows = 0
        for instances in query:
            how_much_cols = len(instances)
            app.openScrollPane("RIGHT_SCROLLPANE")
            for columns in range(how_much_cols):
                label_name = f"column_data_col_{str(columns + 1)}_row_{str(rows + 1)}"
                app.addLabel(label_name, instances[columns], rows + 3, columns + 1)
                column_data_list.append(label_name)
            button_name = f"column_data_col_1_row_{str(rows + 1)}"
            app.addNamedButton("Delete", button_name, data.data_delete, rows + 3, how_much_cols + 1)
            column_button_list.append(button_name)
            app.stopScrollPane()
            rows += 1

    @staticmethod
    def column_data_append():
        sql = f"INSERT INTO {app.getOptionBox("Tables")} VALUES ("
        for instances in range(col_data_instances):
            value = app.getEntry(f"col_data_entry_{instances}")
            if value == "":
                sql += "NULL"
            else:
                if type(value) is int:
                    sql += f"{value}"
                else:
                    sql += f"'{value}'"

            if instances == col_data_instances - 1:
                sql += ")"
            else:
                sql += ", "
        query = mydblogin.cursor()
        query.execute(sql)
        mydblogin.commit()
        print(sql)

    @staticmethod
    def data_delete(btn):
        try:
            col_sql = (f"SELECT column_name FROM information_schema.columns WHERE table_name = '"
                       f"{str(app.getOptionBox("Tables"))}' && column_key = 'PRI'")

            get_col_query = mydblogin.cursor()
            get_col_query.execute(col_sql)
            col_list = [re.sub(r"[(),']", "", str(instance)) for instance in get_col_query]

            del_sql = (f"DELETE FROM {str(app.getOptionBox("Tables"))} WHERE {str(col_list[0])} = "
                       f"{str(app.getLabel(btn))}")
            del_query = mydblogin.cursor()
            del_query.execute(del_sql)
        except Exception as e:
            print(f"Something went wrong {e}")

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
        app.addNamedButton("Create database", "database_create", button.create_db_subwindow_submit, 2, 0)
        app.addNamedButton("Delete database", "database_delete", button.delete_db, 3, 0)
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
        app.addNamedButton("Add data", "add_data", button.add_data, 0, 2)
        app.startScrollPane("RIGHT_SCROLLPANE", 1, 0)
        app.addEmptyLabel("e")
        app.stopScrollPane()
        app.stopFrame()

        gui.column_data_append_subwindow()

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

            for i in range(1, amount_of_cols + 1):
                app.addLabelEntry(f"col_name_{str(i)}", i + 1, 0)
                app.addOptionBox(f"col_type_{str(i)}", ["INT", "VARCHAR", "TEXT", "DATE"], i + 1, 1)
                app.addLabelEntry(f"col_length_{str(i)}", i + 1, 2)
                app.addCheckBox(f"col_isnull_{str(i)}", i + 1, 3)
                app.addOptionBox(f"col_index_{str(i)}", ["---", "PRIMARY", "UNIQUE", "INDEX"], i + 1, 4)
                app.addLabelEntry(f"index_name_{str(i)}", i + 1, 5)
                app.addCheckBox(f"col_ai_{str(i)}", i + 1, 6)
                app.addLabelEntry(f"col_comments_{str(i)}", i + 1, 7)

            app.addNamedButton("Submit", "create_table_submit", button.create_table_submit)
            app.addNamedButton("Cancel", "create_table_cancel", button.create_table_cancel)

            app.stopSubWindow()

    @staticmethod
    def create_db_subwindow():
        app.startSubWindow("CreateDatabase")

        app.addEntry("database_name", 0, 0, 2)
        app.addNamedButton("Submit", "create_db_submit", button.create_db_submit, 1, 0)
        app.addNamedButton("Cancel", "create_db_cancel", button.create_db_cancel, 1, 1)

        app.stopSubWindow()

    @staticmethod
    def column_data_append_subwindow():
        global col_data_instances
        col_data_instances = 0
        col_select_sql = (f"SELECT column_name FROM information_schema.columns WHERE table_name = '"
                          f"{str(app.getOptionBox("Tables"))}'")
        query = mydblogin.cursor()
        query.execute(col_select_sql)
        col_name_list = [re.sub(r"[(),']", "", str(instance)) for instance in query]

        app.startSubWindow("ColumnDataAppend")

        for i, col_name in enumerate(col_name_list):
            app.addLabel(f"col_data_name_{i}", col_name, i, 0)
            app.addEntry(f"col_data_entry_{i}", i, 1)
            col_data_instances += 1
        app.addNamedButton("Cancel", "column_data_append_cancel", button.column_data_append_cancel, col_data_instances + 1, 0)
        app.addNamedButton("Submit", "column_data_append_submit", button.column_data_append_submit, col_data_instances + 1, 1)
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

        data.tables()

        data.create_table()

        app.destroySubWindow("CreateTable")

    @staticmethod
    def create_table_cancel():
        app.destroySubWindow("CreateTable")

    @staticmethod
    def create_db_subwindow_submit():
        gui.create_db_subwindow()

        app.showSubWindow("CreateDatabase")

    @staticmethod
    def create_db_submit():
        data.database_create()

        data.databases()

        app.destroySubWindow("CreateDatabase")

    @staticmethod
    def create_db_cancel():
        app.destroySubWindow("CreateDatabase")

    @staticmethod
    def delete_db():
        data.database_delete()

    @staticmethod
    def column_data_append_submit():
        data.column_data_append()

    @staticmethod
    def column_data_append_cancel():
        event.column_data_append_clear()

    @staticmethod
    def add_data():
        try:
            gui.column_data_append_subwindow()
        except:
            None
        app.showSubWindow("ColumnDataAppend")

class GuiEvents:
    @staticmethod
    def database_change():
        try:
            data.tables()
            data.use_database()
        except:
            None

    @staticmethod
    def table_change():
        try:
            data.column_select()
            app.thread(data.column_data_select)
        except:
            None

    @staticmethod
    def login_close():
        app.stop()

    @staticmethod
    def createtable_close():
        app.destroySubWindow("CreateTable")

    @staticmethod
    def column_data_append_clear():
        app.destroySubWindow("ColumnDataAppend")


# Naming for all classes
data = DataQuery
button = ButtonPress
gui = GuiClass
event = GuiEvents

# App is started here with the login subwindow as it's starting window
gui.login_subwindow()
app.go(startWindow="Login")