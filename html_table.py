
def csvtohtml(file):
    filein=open(file,"r")
    fileout = open("templates\success.html", "w")
    data = filein.readlines()

    table ="{% extends 'index.html' %}\n"
    table +="{% block content %}\n"
    table += "<table class='table'>\n"

    # Create the table's column headers
    table +=" <thead class='thead-light'>\n"
    header = data[0].split(",")
    table += "   <tr>\n"
    for column in header:
        table += "     <th scope='col'>{0}</th>\n".format(column.strip())
    table += "   </tr>\n"
    table +=" </thead>\n"
    table +=" <tbody>\n"
    # Create the table's row data
    for line in data[1:]:
        row = line.split(",")
        table += "   <tr>\n"
        for column in row:
            table += "     <td>{0}</td>\n".format(column.strip())
        table += "   </tr>\n"
    table +=" </tbody>\n"
    table += "</table>\n"
    table +="{% endblock content %}"

    fileout.writelines(table)
    fileout.close()
    filein.close()