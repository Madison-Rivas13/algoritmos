import tkinter as tk 
from tkinter import ttk
import sqlite3
import tkinter.messagebox as messagebox

class Mantenimiento_de_vehiculos:
    def __init__(self, root):
        self.root = root
        self.root.title("Mantenimiento de vehiculos")
        self.root.configure(bg="teal")
        self.root.geometry('500x300')

        # Conectar a la base de datos SQLite
        self.conexion = sqlite3.connect("mantenimiento.db")
        self.crear_tabla()

        # Crear widgets
        self.etiqueta_crear = ttk.Label(root, text="Crear Vehiculos:")
        self.entry_crear = ttk.Entry(root)

        self.etiqueta_editar = ttk.Label(root, text="Editar Vehiculo:")
        self.entry_editar = ttk.Entry(root)

        self.etiqueta_eliminar = ttk.Label(root, text="Eliminar Vehiculo:")
        self.entry_eliminar = ttk.Entry(root)

        self.etiqueta_listar = ttk.Label(root, text="Listar Vehiculos:")
        self.entry_listar = ttk.Entry(root)

       
        self.boton_agregar = ttk.Button(root, text="Agregar", command=self.Agregar_vehiculo)
        self.boton_editar = ttk.Button(root, text="Editar", command=self.editar_vehiculo)
        self.boton_guardar = ttk.Button(root, text="Guardar", command=self.guardar_edicion)
        self.boton_guardar.grid_remove()  # Ocultar el botón Guardar inicialmente

        self.etiqueta_busqueda = ttk.Label(root, text="Búsqueda:")
        self.entry_busqueda = ttk.Entry(root)
        self.boton_buscar = ttk.Button(root, text="Buscar", command=self.buscar_productos)


   # Crear estilo personalizado para el Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12), background="gray", foreground="black")
        style.configure("Treeview", font=("Helvetica", 11), background="green", foreground="black")
        style.map("Treeview", background=[("selected", "blue")])

        # Posicionar widgets
        self.etiqueta_busqueda.grid(row=9, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_busqueda.grid(row=9, column=1, padx=5, pady=5)
        self.boton_buscar.grid(row=10, column=1, padx=10, pady=10)
    

        # Treeview para mostrar los productos existentes
        self.tree = ttk.Treeview(root, columns=('Crear vehiculos', 'editar vehiculos', 'Eliminar vehiculo', 'Listar vehiculos'))
        self.tree.heading('Crear vehiculos', text='Crear vehiculos')
        self.tree.heading('editar vehiculos', text='editar vehiculos')
        self.tree.heading('eliminar vehiculos', text='eliminar vehiculos')
        self.tree.heading('listar vehiculos', text='listar vehiculos')
       

        # Posicionar widgets
        self.etiqueta_crear.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_crear.grid(row=0, column=1, padx=5, pady=5)

        self.etiqueta_editar.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_editar.grid(row=1, column=1, padx=5, pady=5)

        self.etiqueta_eliminar.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_eliminar.grid(row=2, column=1, padx=5, pady=5)

        self.etiqueta_listar.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_listar.grid(row=3, column=1, padx=5, pady=5)

        
        self.boton_agregar.grid(row=7, column=0, columnspan=2, pady=10)
        self.boton_editar.grid(row=10, column=2, columnspan=2, pady=10, padx=10)
        self.boton_eliminar = ttk.Button(root, text="Eliminar", command=self.eliminar_producto)
        self.boton_eliminar.grid(row=7, column=2, columnspan=2, pady=10,padx=10)

        self.tree.grid(row=0, column=2, rowspan=7, padx=10)
       

        # Cargar productos existentes al Treeview
        self.cargar_productos()

        

    def buscar_productos(self):
        # Obtener el criterio de búsqueda
        cursor = self.conexion.cursor()
        criterio = self.entry_busqueda.get()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        # Filtrar los productos
        productos_filtrados = []
        for producto in productos:
            if criterio in producto[1]:
                productos_filtrados.append(producto)

        # Actualizar el Treeview
        self.tree.delete(*self.tree.get_children())
        for producto in productos_filtrados:
            self.tree.insert('', 'end', values=producto)
    def actualizar_tabla(self):
        # Cargar los productos de la base de datos

        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        # Limpiar el Treeview
        self.tree.delete(*self.tree.get_children())

        # Agregar los productos al Treeview
        for producto in productos:
            self.tree.insert('', 'end', values=producto)


    def crear_tabla(self):
        cursor = self.conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                crear INTEGER PRIMARY KEY AUTOINCREMENT,
                editar TEXT NOT NULL,
                eliminar TEXT,
                listar INTEGER NOT NULL,
              
        ''')
        self.conexion.commit()

    def agregar_producto(self):
        crear = self.entry_nombre.get()
        editar = self.entry_descripcion.get()
        eliminar = self.entry_cantidad.get()
        listar  = self.entry_proveedor.get()
    
        if crear and editar:
            cursor = self.conexion.cursor()
            cursor.execute("INSERT INTO productos (crear, editar, eliminar, listar) VALUES (?, ?, ?, ?)",
                           (crear, editar, eliminar, listar,))
            self.conexion.commit()
            print("Producto agregado correctamente.")
            self.limpiar_campos()
            self.cargar_productos()
        else:
            print("Por favor, ingrese nombre y cantidad.")

    def cargar_productos(self):
        # Limpiar productos existentes en el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        for producto in productos:
            self.tree.insert('', 'end', values=producto)

    def limpiar_campos(self):
        self.entry_crear.delete(0, tk.END)
        self.entry_editar.delete(0, tk.END)
        self.entry_eliminar.delete(0, tk.END)
        self.entry_listar.delete(0, tk.END)
        
    def editar_producto(self):
        # Obtener el item seleccionado en el Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            print("Por favor, seleccione un producto para editar.")
            return

        # Obtener los valores del item seleccionado
        values = self.tree.item(selected_item)['values']

        # Almacenar temporalmente los valores editados
        self.valores_editados = values

        # Eliminar la fila seleccionada del Treeview
        self.tree.delete(selected_item)

        # Mostrar los valores en los campos de entrada para su edición
        self.entry_crear.delete(0, tk.END)
        self.entry_crear.insert(0, self.valores_editados[1])

        self.entry_editar.delete(0, tk.END)
        self.entry_editar.insert(0, self.valores_editados[2])

        self.entry_eliminar.delete(0, tk.END)
        self.entry_eliminar.insert(0, self.valores_editados[3])

        self.entry_listar.delete(0, tk.END)
        self.entry_listar.insert(0, self.valores_editados[4])

       
        # Mostrar el botón "Guardar" y ocultar "Editar"
        self.boton_guardar.grid()
        self.boton_editar.grid_remove()

    def guardar_edicion(self):
        # Verificar si hay valores editados almacenados
        if self.valores_editados:
            # Obtener los valores actualizados
            crear = self.valores_editados[0]
            editar = self.entry_nombre.get()
            eliminar = self.entry_descripcion.get()
            listar = self.entry_cantidad.get()
           

            # Actualizar la base de datos
            self.actualizar_producto(crear, editar, eliminar, listar)

            # Limpiar los valores editados y mostrar el botón "Editar"
            self.valores_editados = None
            self.boton_editar.grid()

        # Resto de tu código...

    def actualizar_producto(self, crear, editar, eliminar, listar):
        cursor = self.conexion.cursor()
        cursor.execute("UPDATE productos SET nombre=?, descripcion=?, cantidad=?, proveedor=?, id_producto=?, id_cliente=? WHERE id=?",
                       (crear, editar, eliminar, listar))
        self.conexion.commit()
        print("Producto actualizado correctamente.")
        self.cargar_productos()

    def eliminar_producto(self):
        # Obtener el item seleccionado en el Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Por favor, seleccione un producto para eliminar.")
            return

        # Obtener el ID del producto seleccionado
        producto_id = self.tree.item(selected_item)['values'][0]

        # Confirmar la eliminación
        confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este producto?")
        if confirmacion:
            # Eliminar el producto de la base de datos
            cursor = self.conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE id=?", (producto_id,))
            self.conexion.commit()

            # Eliminar el producto del Treeview
            self.tree.delete(selected_item)

            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")




if __name__ == "__main__":
    root = tk.Tk()
    app = Mantenimiento_de_vehiculos(root)
    root.mainloop()

       
