# Importar las bibliotecas de tkinter
from tkinter.ttk import *
import tkinter.ttk as ttk
from tkinter import *

# Importar el conector de MySQL
import mysql.connector

# Bibioteca para imprimir mensajes
from tkinter import messagebox

# pip install pymysql
# pip install mysql-connector-python

# Configuración de la base de datos
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "secreto",
    database = "datacenter"
)
mycursor = mydb.cursor()

root = Tk()
root.title("Tecnologías de Información II")
# Tamano de la pantalla principal
root.geometry("750x550")

# Etiquetas para mostrar los textos
label1 = Label(root, text="Nombre: ", width=20, height=2).grid(row=1, column=0)
label2 = Label(root, text="Apellido: ", width=20, height=2).grid(row=2, column=0)
label3 = Label(root, text="Teléfono: ", width=20, height=2).grid(row=3, column=0)
label4 = Label(root, text="Edad: ", width=20, height=2).grid(row=4, column=0)
label5 = Label(root, width=20, height=2).grid(row=7, column=2)
label6 = Label(root, width=20, height=2).grid(row=7, column=4)

# Campos de texto
e1 = Entry(root, width=30, borderwidth=5)
e1.grid(row=1, column=2)

e2 = Entry(root, width=30, borderwidth=5)
e2.grid(row=2, column=2)

e3 = Entry(root, width=30, borderwidth=5)
e3.grid(row=3, column=2)

e4 = Entry(root, width=30, borderwidth=5)
e4.grid(row=4, column=2)

# Funcion para registros los datos a la base de datos
def Registrar():
    Insert = "Insert into empleado(nombre, apellido, telefono, edad) values(%s, %s, %s, %s)"
    # Se obtienen los datos del formulario
    nombre = e1.get()
    apellido = e2.get()
    telefono = e3.get()
    edad = e4.get()

    Value = (nombre, apellido, telefono, edad)

    mycursor.execute(Insert, Value)
    mydb.commit()
    messagebox.askokcancel("Information", "Record inserted")
    limpiar()
    Mostrar()

# Funcion para limpiar los campos de texto
def limpiar():
    e1.delete(0, 'end')
    e2.delete(0, 'end')
    e3.delete(0, 'end')
    e4.delete(0, 'end')

# Funcion para mostrar los registros
def Mostrar():   
    # Configuración de la tabla
    root.listTree = ttk.Treeview(root,height=14,columns=('Nombre','Apellido','Telefono','Edad'))
    root.vsb = ttk.Scrollbar(root,orient="vertical",command=root.listTree.yview)
    root.hsb = ttk.Scrollbar(root,orient="horizontal",command=root.listTree.xview)
    root.listTree.configure(yscrollcommand=root.vsb.set,xscrollcommand=root.hsb.set)

    # Colocar encabezados en la tabla
    root.listTree.heading("#0", text='ID')
    root.listTree.column("#0", width=50,minwidth=50,anchor='center')
    root.listTree.heading("Nombre", text='Nombre')
    root.listTree.column("Nombre", width=200, minwidth=200,anchor='center')
    root.listTree.heading("Apellido", text='Apellido')
    root.listTree.column("Apellido", width=200, minwidth=200,anchor='center')
    root.listTree.heading("Telefono", text='Telefono')
    root.listTree.column("Telefono", width=125, minwidth=125,anchor='center')
    root.listTree.heading("Edad", text='Edad')
    root.listTree.column("Edad", width=125, minwidth=125, anchor='center')

    # Colocacion de la tabla en la pantalla
    root.listTree.place(x=10,y=210)
    root.vsb.place(x=1150,y=361,height=287)
    root.hsb.place(x=200,y=650,width=966)
    ttk.Style().configure("Treeview",font=('Times new Roman',15))

    # Cargar los registros de la base de datos a la tabla
    mycursor.execute("Select * from empleado")
    pc = mycursor.fetchall()
    if pc:
        root.listTree.delete(*root.listTree.get_children())
        for row in pc:
            root.listTree.insert("",'end',text=row[0] ,values = (row[1],row[2],row[3],row[4]))
    
    # Evento del boton en la tabla
    root.listTree.bind('<<TreeviewSelect>>', OnClick)

# Eliminar registro de la base de datos
def Borrar():
    id = root.listTree.selection()[0]
    id = root.listTree.item(id, "text")
    Delete = "delete from empleado where id = " + str(id)

    mycursor.execute(Delete)
    mydb.commit()
    Mostrar()
    
# Seleccionar un registro de la tabla y setear los campos de texto
def OnClick(event):
    limpiar()
    item = root.listTree.selection()[0:1]
    e1.insert(0, root.listTree.item(item,"text"))

    for selection in root.listTree.selection():  
        item = root.listTree.item(selection)  
        
        # Setear los campos de texto
        nombre,apellido,telefono,edad = item["values"][0:4]  
        e1.insert(0, nombre)  
        e2.insert(0, apellido)  
        e3.insert(0, telefono)  
        e4.insert(0, edad)  

# Funcion para actualizar registros en la base de datos
def actualizar():
    id = root.listTree.selection()[0]
    id = root.listTree.item(id, "text")
    Insert = "update empleado set nombre = %s, apellido = %s, telefono = %s, edad = %s where id = " + str(id)
    nombre = e1.get()
    apellido = e2.get()
    telefono = e3.get()
    edad = e4.get()

    Value = (nombre, apellido, telefono, edad)

    mycursor.execute(Insert, Value)
    mydb.commit()
    messagebox.askokcancel("Information", "Record Updated")
    limpiar()
    Mostrar()

# Mostrar los registros al ejecutar el script
Mostrar()

# Botones 
button1 = Button(root, text="Registrar", width=10, height=2, command=Registrar).grid(row=5, column=1)
button2 = Button(root, text="Actualizar", width=10, height=2, command=actualizar).grid(row=5, column=0)
button3 = Button(root, text="Borrar", width=10, height=2, command=Borrar).grid(row=5, column=2)

# Muestra el resultado de aplicar las propiedades tkinter
root.mainloop()
