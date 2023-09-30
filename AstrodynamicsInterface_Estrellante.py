########################################################################################        
#################################### INTERFAZ ##########################################
########################################################################################
from numpy import array,zeros,floor,linspace,cos,sin,arccos,pi,append,insert
from spiceypy import oscltx, conics
from astropy.time import Time
from scipy.integrate import odeint
import matplotlib.pyplot as plt
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
import mariadb
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
deg = pi/180

class interfaz():
    def __init__(self,ventana):
        self.graph=False
        self.gal = False
        self.sis = False
        C="gray12"
        D="white"
        self.ventana=ventana
        self.ventana.title("IVICU")
        ventana.geometry("900x700")
        ventana.configure(bg=C)
        
        #r=mb.showinfo(message="Para ingresar un nuevo cuerpo seleccione antes una galaxia y un sistema.\nNota: Recuerde que las unidades son del SI y la epoca seleccionada para los cuerpos es J2000",
        #           title="Bienvenido a IVICU!")
        
        
        ###################### Marco Galaxia  ######################################
        ############################################################################
        
        marco=LabelFrame(self.ventana,text="Galaxia",fg=D)
        marco.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.07)
        marco.configure(bg=C)
        #marco1.grid(row=0,column=0,columnspan=20,pady=10)
        
        Label(marco,text="Nombre",fg=D,bg=C).place(relx=0, rely=0.05, relwidth=0.06, relheight=0.6)
        self.nombregal=Entry(marco)
        self.nombregal.place(relx=0.06, rely=0.05, relwidth=0.14, relheight=0.6)
        self.nombregal.focus()
        
        Label(marco,text="Radio",fg=D,bg=C).place(relx=0.19, rely=0.05, relwidth=0.04, relheight=0.6)
        self.tamgal=Entry(marco)
        self.tamgal.place(relx=0.23, rely=0.05, relwidth=0.14, relheight=0.6)

        Label(marco,text="Masa",fg=D,bg=C).place(relx=0.37, rely=0.05, relwidth=0.04, relheight=0.6)
        self.masagal=Entry(marco)
        self.masagal.place(relx=0.41, rely=0.05, relwidth=0.14, relheight=0.6)
        
        self.tipogal = StringVar(self.ventana)
        self.tipogal.set("Galaxia")

        Label(marco,text="Tipo",fg=D,bg=C).place(relx=0.55, rely=0.05, relwidth=0.04, relheight=0.6)
        self.optiontipo = OptionMenu(marco,self.tipogal,"Espiral","Elíptica","Irregular","Lenticular","Peculiar")
        self.optiontipo.config(fg=D,bg=C)
        self.optiontipo["menu"].config(fg=D,bg=C)
        self.optiontipo.place(relx=0.59, rely=0.05, relwidth=0.1, relheight=0.8)
        
        self.creargal=Button(marco,text="Nuevo",fg=D,bg="green",state="normal",command=self.NuevaGalaxia)
        self.creargal.place(relx=0.7, rely=0.03, relwidth=0.07, relheight=0.7)
        
        
        self.buscargal=Button(marco,text="Cargar",fg=D,bg="gold3",state="normal",command=self.CargarGalaxia)
        self.buscargal.place(relx=0.775, rely=0.03, relwidth=0.07, relheight=0.7)
        

        self.actualizargal=Button(marco,text="Actualizar",fg=D,bg="blue",state="normal",command=self.ActualizarGalaxia)
        self.actualizargal.place(relx=0.85, rely=0.03, relwidth=0.07, relheight=0.7)
        
        
        self.borrargal=Button(marco,text="Borrar",fg=D,bg="red",state="normal", command=self.BorrarGalaxia)
        self.borrargal.place(relx=0.925, rely=0.03, relwidth=0.07, relheight=0.7)
        
        ###################### Marco sistema  ######################################
        ############################################################################
        
        marco1=LabelFrame(self.ventana,text="Sistema",fg=D)
        marco1.place(relx=0.01, rely=0.1, relwidth=0.49, relheight=0.11)
        marco1.configure(bg=C)
        #marco1.grid(row=0,column=0,columnspan=20,pady=10)
        
        Label(marco1,text="Nombre",fg=D,bg=C).grid(row=0,column=0,columnspan=2)
        self.nombresis=Entry(marco1)
        self.nombresis.grid(row=0,column=3,columnspan=2)
        
        Label(marco1,text="Distancia",fg=D,bg=C).grid(row=0,column=5,columnspan=2)
        self.distsis=Entry(marco1)
        self.distsis.grid(row=0,column=7,columnspan=2)
        
        self.crearsis=Button(marco1,text="Nuevo",fg=D,bg="green",state="disabled",command=self.NuevoSistema)
        self.crearsis.place(relx=0.12, rely=0.5, relwidth=0.15, relheight=0.4)
        
        
        self.buscarsis=Button(marco1,text="Cargar",fg=D,bg="gold3",state="disabled",command=self.CargarSistema)
        self.buscarsis.place(relx=0.3, rely=0.5, relwidth=0.15, relheight=0.4)
        

        self.actualizarsis=Button(marco1,text="Actualizar",fg=D,bg="blue",state="disabled",command=self.ActualizarSistema)
        self.actualizarsis.place(relx=0.48, rely=0.5, relwidth=0.15, relheight=0.4)
        
        
        self.borrarsis=Button(marco1,text="Borrar",fg=D,bg="red",state="disabled",command=self.BorrarSistema)
        self.borrarsis.place(relx=0.66, rely=0.5, relwidth=0.15, relheight=0.4)
        
        
        ###################### Marco Grafica  ######################################
        ############################################################################
        
        marcoparams=LabelFrame(self.ventana,text="Gráfica")
        #marcoparams.grid(row=1,column=0,columnspan=20,pady=20,sticky=N+S)
        marcoparams.place(relx=0.01, rely=0.22, relwidth=0.49, relheight=0.12)
        marcoparams.configure(fg=D,bg=C)
        
        Label(marcoparams,text="Tiempo inicio",fg=D,bg=C).grid(row=0,column=0,columnspan=2)
        self.tiempoi=Entry(marcoparams)
        self.tiempoi.grid(row=0,column=3,columnspan=2,pady=5,sticky=N)
        #self.nombresis.focus()
        
        Label(marcoparams,text="Tiempo fin",fg=D,bg=C).grid(row=0,column=5,columnspan=2)
        self.tiempof=Entry(marcoparams)
        self.tiempof.grid(row=0,column=7,columnspan=2,pady=5,sticky=N)

        self.checkgrid_value = BooleanVar(self.ventana)        
        self.checkgrid = Checkbutton(marcoparams,text="Cuadricula", variable=self.checkgrid_value)#, onvalue=1, offvalue=0)
        self.checkgrid.grid(row=1,column=3,columnspan=2,pady=5)
        self.checkgrid.configure(fg=D,bg=C,selectcolor="black")
        
        self.creargrafica=Button(marcoparams,text="Graficar",fg="White",bg="green",state="disabled",command=self.Graficar)
        self.creargrafica.grid(row=1,column=6,columnspan=2,pady=5,sticky=W+E)
        
        
        Label(marco1,text="Distancia",fg=D,bg=C).grid(row=0,column=5,columnspan=2)
        self.distsis=Entry(marco1)
        self.distsis.grid(row=0,column=7,columnspan=2)
        self.distsis.focus()
        
        self.mensaje = Label(self.ventana,text="Bienvenido",font=(11),fg=D,bg=C)
        self.mensaje.place(relx=0.01, rely=0.34, relwidth=0.49)#,relheight=0.15)
        
        self.marcograph=LabelFrame(self.ventana)#,text="Gráfica")
        self.marcograph.place(relx=0.01, rely=0.38, relwidth=0.49, relheight=0.49)
        self.marcograph.configure(fg=D,bg=C)

        self.state = "Status: "
        self.status = Label(self.ventana, text=self.state,fg=D,bg=C)
        self.status.place(relx=0.01, rely=0.89)#,relheight=0.15)
        
        ###################### Marco cuerpo  ######################################
        ############################################################################
        
        marco2=LabelFrame(self.ventana,text="Cuerpo",fg=D)
        marco2.place(relx=0.51, rely=0.1, relwidth=0.48, relheight=0.11)
        marco2.configure(bg=C)
        #marco2.grid(row=0,column=22,columnspan=20,pady=20)
        
        
        #marco3.grid(row=1,column=22,columnspan=20,pady=20)
        
        Label(marco2,text="Nombre",fg=D,bg=C).grid(row=0,column=0,columnspan=2)
        self.nombrebody=Entry(marco2)
        self.nombrebody.grid(row=0,column=3,columnspan=2)

        self.option_var = StringVar(ventana)
        self.option_var.set("Cuerpo")
        
        Label(marco2,text="Tipo",fg=D,bg=C).grid(row=0,column=5,columnspan=2)
        self.w = OptionMenu(marco2,self.option_var,"Estrella","Planeta","Asteroide","Cometa","Luna","Satelite")
        self.w.config(fg=D,bg=C)
        self.w["menu"].config(fg=D,bg=C)
        self.w.place(relx=0.485, rely=0.02, relwidth=0.25, relheight=0.35)#grid(row=0,column=7,columnspan=2,sticky=W+E)
        
        Label(marco2,text="Radio",fg=D,bg=C).grid(row=1,column=0,columnspan=2)
        self.radiobody=Entry(marco2)
        self.radiobody.grid(row=1,column=3,columnspan=2)
        
        Label(marco2,text="Masa",fg=D,bg=C).grid(row=1,column=5,columnspan=2)
        self.masabody=Entry(marco2)
        self.masabody.grid(row=1,column=7,columnspan=2)

        self.buscarbodys=Button(marco2,text="Cargar\nTodos",fg=D,bg="gold3",state="disabled",command=self.CargarBodys)
        self.buscarbodys.place(relx=0.82, rely=0.1, relwidth=0.13, relheight=0.7)
        
                
        ###################### Marco parametros  ######################################
        ############################################################################
        
        marco3=LabelFrame(self.ventana,text="Parametros",fg=D)
        marco3.place(relx=0.51, rely=0.22, relwidth=0.48, relheight=0.23)
        marco3.configure(bg=C)

        Label(marco3,text="Semieje",fg=D,bg=C).grid(row=0,column=0,columnspan=2,pady=3)
        self.semieje=Entry(marco3)
        self.semieje.grid(row=0,column=3,columnspan=2)
        
        
        Label(marco3,text="Excentricidad",fg=D,bg=C).grid(row=1,column=0,columnspan=2,pady=3)
        self.ecc=Entry(marco3)
        self.ecc.grid(row=1,column=3,columnspan=2)
        
        
        Label(marco3,text="Inclinación",fg=D,bg=C).grid(row=2,column=0,columnspan=2,pady=3)
        self.inc=Entry(marco3)
        self.inc.grid(row=2,column=3,columnspan=2)
        
        
        Label(marco3,text="Argumento",fg=D,bg=C).grid(row=0,column=5,columnspan=2,pady=3)
        self.arg=Entry(marco3)
        self.arg.grid(row=0,column=7,columnspan=2)
        
        Label(marco3,text="RAAN",fg=D,bg=C).grid(row=1,column=5,columnspan=2,pady=3)
        self.raan=Entry(marco3)
        self.raan.grid(row=1,column=7,columnspan=2)
        
        Label(marco3,text="Anomalia",fg=D,bg=C).grid(row=2,column=5,columnspan=2,pady=3)
        self.ta=Entry(marco3)
        self.ta.grid(row=2,column=7,columnspan=2)

        Label(marco3,text="Cuerpo primario",fg=D,bg=C).grid(row=3,column=0,columnspan=4,pady=3)
        self.primario=Entry(marco3)
        self.primario.grid(row=3,column=4,columnspan=3)
        
        self.crearbody=Button(marco3,text="Nuevo",fg=D,bg="green",state="disabled",command=self.NuevoBody)
        self.crearbody.place(relx=0.2, rely=0.78, relwidth=0.15, relheight=0.16)
        
        
        self.buscarbody=Button(marco3,text="Cargar",fg=D,bg="gold3",state="disabled",command=self.CargarBody)
        self.buscarbody.place(relx=0.38, rely=0.78, relwidth=0.15, relheight=0.16)
        

        self.actualizarbody=Button(marco3,text="Actualizar",fg=D,bg="blue",state="disabled",command=self.ActualizarBody)
        self.actualizarbody.place(relx=0.56, rely=0.78, relwidth=0.15, relheight=0.16)
        
        
        self.borrarbody=Button(marco3,text="Borrar",fg=D,bg="red",state="disabled",command=self.BorrarBody)
        self.borrarbody.place(relx=0.74, rely=0.78, relwidth=0.15, relheight=0.16)
        
        
        ###################### Marco Tabla  ######################################
        ############################################################################
                
        #self.tabla_frame = LabelFrame(ventana)
        #self.tabla_frame.place(relx=0.51, rely=0.4, relwidth=0.48, relheight=0.4)
        #self.tabla_frame.configure(bg=C)
        self.cuadro=ttk.Treeview(ventana)
        
        self.cuadro['columns'] = ('Nombre','Masa','Radio','Tipo')
        #self.cuadro.grid(row=6,columnspan=2,sticky=W+E)
        #self.cuadro.bind("<Double-Button-1>",self.dobleclick)
        colwidth = 110
        self.cuadro.heading("#0",text="Nombre",anchor=CENTER)
        self.cuadro.column("#0",anchor=CENTER,width=colwidth, stretch=NO)
        self.cuadro.heading("#1",text="Masa",anchor=CENTER)
        self.cuadro.column("#1",anchor=CENTER,width=colwidth, stretch=NO)
        self.cuadro.heading("#2",text="Radio",anchor=CENTER)
        self.cuadro.column("#2",anchor=CENTER,width=colwidth, stretch=NO)
        self.cuadro.heading("#3",text="Tipo",anchor=CENTER)
        self.cuadro.column("#3",anchor=CENTER,width=colwidth, stretch=NO)
            
        style = ttk.Style(ventana)
        # set ttk theme to "clam" which support the fieldbackground option
        style.theme_use("clam")
        style.configure("Treeview", background=C,fieldbackground=C, foreground=D)
        style.configure('Treeview.Heading', background="PowderBlue")
        self.cuadro.place(relx=0.51, rely=0.47, relwidth=0.48, relheight=0.33)
        
        ############################# Marco Lista  #################################
        ############################################################################
        
        frame2 = Frame(ventana,bg=C)
        # Crear una barra de deslizamiento con orientación vertical.
        scrollbar = ttk.Scrollbar(frame2, orient=VERTICAL)
        # Vincularla con la lista.
        self.listbox = Listbox(frame2, yscrollcommand=scrollbar.set,selectmode=EXTENDED)
        scrollbar.config(command=self.listbox.yview)
        # Ubicarla a la derecha.
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.place(relwidth=0.85, relheight=1)
        frame2.place(relx=0.61, rely=0.81, relwidth=0.1, relheight=0.15)
        
        self.eliminarbody=Button(ventana,text="Eliminar\ndel modelo",fg="black",bg="red",state="disabled",command=self.EliminarBody)
        self.eliminarbody.place(relx=0.73, rely=0.84, relwidth=0.08, relheight=0.06)

        self.checkbodys_value = BooleanVar(self.ventana)        
        self.checkbodys = Checkbutton(ventana,text="Graficar seleccionados", variable=self.checkbodys_value)
        self.checkbodys.place(relx=0.73, rely=0.91, relwidth=0.17, relheight=0.035)
        self.checkbodys.configure(fg=D,bg=C,selectcolor="black")
        
        
    ################################ GALAXIA ###################################
    ############################################################################    
    def NuevaGalaxia(self):
        try:
            gall = [self.nombregal.get(),self.tamgal.get(),self.masagal.get(),self.tipogal.get()]
            if(((len(gall[0])!=0 and len(gall[1])!=0) and len(gall[2])!=0) and gall[3] != "Galaxia"):
                Guardar(gall,[],"galaxia")
                self.mensaje["text"]="La galaxia se ha ingresado con exito"
                self.nombregal.delete(0,END)
                self.tamgal.delete(0,END)
                self.masagal.delete(0,END)
                self.tipogal.set("Galaxia")
                self.nombregal.focus()
            else:
                self.mensaje["text"]="Ingrese todos los valores de la galaxia"
        except:
            self.mensaje["text"]="Ingrese valores validos"

    def ActualizarGalaxia(self):
        try:
            gall = [self.nombregal.get(),self.tamgal.get(),self.masagal.get(),self.tipogal.get()]
            if(((len(gall[0])!=0 and len(gall[1])!=0) and len(gall[2])!=0) and gall[3] != "Galaxia"):
                try:
                    Actualizar(gall,[],"galaxia",)
                    self.mensaje["text"]="La galaxia se ha actualizado con exito"
                    self.nombregal.delete(0,END)
                    self.tamgal.delete(0,END)
                    self.masagal.delete(0,END)
                    self.tipogal.set("Galaxia")
                    self.nombregal.focus()
                except:
                    self.mensaje["text"]="La galaxia no existe"
            else:
                self.mensaje["text"]="Ingrese todos los valores de la galaxia"
        except:
            self.mensaje["text"]="Ingrese valores validos"
    
    def CargarGalaxia(self):
        try:
            gall = [self.nombregal.get(),self.tamgal.get(),self.masagal.get(),self.tipogal.get()]
            if(((len(gall[0])!=0 and len(gall[1])==0) and len(gall[2])==0) and gall[3] == "Galaxia"):
                G = list(Buscar("galaxia",["id_Galaxia","Radio","Masa","Tipo"],["Nombre"], [gall[0]]))
                self.Galaxy = Galaxia(gall[0],G)
                self.mensaje["text"]="Galaxia seleccionada con exito"
                self.nombregal.delete(0,END)
                self.tamgal.delete(0,END)
                self.tipogal.set("Galaxia")
                self.nombregal.focus()
                self.state=f"Status:      Galaxia = {self.Galaxy.nombre}   radio: {self.Galaxy.radio:.2E} yl   masa: {self.Galaxy.masa:.2E} msol   tipo: {self.Galaxy.tipo}"#"Status:      Galaxia = "+str(Galaxy.nombre)+"   radio: "+str(Galaxy.radio)+" yl   masa: "+str(Galaxy.masa)+" msol"
                self.status["text"]=self.state
                self.stateButtons("sistema","normal")
                self.gal = True
                
            else:
                self.mensaje["text"]="Solo ingrese el Nombre de la galaxia"
        except:
            self.mensaje["text"]="Ingrese un nombre valido o existente"
    
    def BorrarGalaxia(self):
        try:            
            gall = [self.nombregal.get(),self.tamgal.get(),self.masagal.get(),self.tipogal.get()]
            if(((len(gall[0])!=0 and len(gall[1])==0) and len(gall[2])==0) and gall[3] == "Galaxia"):
                try:
                    Buscar("galaxia",["Masa"],["Nombre"], [gall[0]]) #  tipo(str)   params(list) condicion(list) value(list
                    respuesta=mb.askyesno("Cuidado", "¿Quiere borrar la galaxia "+str(gall[0])+"?")
                    if respuesta == True:
                        Borrar("galaxia",gall[0],[])
                        self.mensaje["text"]="La galaxia se ha borrado con exito"
                        self.nombregal.delete(0,END)
                        self.tamgal.delete(0,END)
                        self.tipogal.set("Galaxia")
                        self.nombregal.focus()
                        if self.gal == True:
                            if gall[0] == self.Galaxy.nombre:
                                self.status["text"]="Status: "
                                self.stateButtons("sistema","disabled")
                                self.gal == False
                            else: pass
                        else: pass
                    else: pass
                except:
                    self.mensaje["text"]="Nombre de galaxia incorrecto"
            else:
                self.mensaje["text"]="Solo ingrese el Nombre de la galaxia"
        except:
            self.mensaje["text"]="Ingrese un valor valido"

    ################################ SISTEMA ###################################
    ############################################################################

    def NuevoSistema(self):
        try:
            gall = [self.nombresis.get(),self.distsis.get()]
            if(len(gall[0])!=0 and len(gall[1])!=0):
                Guardar([gall[0],0,0,gall[1],self.Galaxy.id_Galaxia],[],"sistema")
                self.mensaje["text"]="El sistema se ha ingresado con exito"
                self.nombresis.delete(0,END)
                self.distsis.delete(0,END)
                self.nombresis.focus()
                self.MostrarTabla([],[])
            else:
                self.mensaje["text"]="Ingrese todos los valores del sistema"
        except:
            self.mensaje["text"]="Ingrese valores validos"

    def ActualizarSistema(self):
        try:
            gall = [self.nombresis.get(),self.distsis.get()]
            if(len(gall[0])!=0 and len(gall[1])!=0):
                try:
                    Actualizar([gall[0],"Distancia",gall[1]],[],"sistema",)
                    self.System.distancia = gall[1]
                    self.mensaje["text"]="El sistema se ha actualizado con exito"
                    self.nombresis.delete(0,END)
                    self.distsis.delete(0,END)
                    self.nombresis.focus()
                    if self.sis == True:
                        if gall[0] == self.System.nombre:
                            self.status["text"]=self.state+f"\nSistema = {self.System.nombre}   Estrellas: {self.System.estrellas}    Planetas: {self.System.planetas}    Distancia: {self.System.distancia:.2E} yl"#"Status:      Galaxia = "+str(Galaxy.nombre)+"   radio: "+str(Galaxy.radio)+" yl   masa: "+str(Galaxy.masa)+" msol"
                except:
                    self.mensaje["text"]="El sistema no existe"
            else:
                self.mensaje["text"]="Ingrese todos los valores del sistema"
        except:
            self.mensaje["text"]="Ingrese valores validos"
    
    def CargarSistema(self):
        try:
            gall = [self.nombresis.get(),self.distsis.get()]
            if(len(gall[0])!=0 and len(gall[1])==0):
                G = list(Buscar("sistema",["id_Sistema","Estrellas","Planetas","Distancia"],["Nombre","id_Galaxia"], [gall[0],self.Galaxy.id_Galaxia]))
                self.System = Sistema(gall[0],G)
                self.mensaje["text"]="Sistema seleccionado con exito"
                self.nombresis.delete(0,END)
                self.nombresis.focus()
                #self.state
                self.status["text"]=self.state+f"\nSistema = {self.System.nombre}   Estrellas: {self.System.estrellas}    Planetas: {self.System.planetas}    Distancia: {self.System.distancia:.2E} yl"#"Status:      Galaxia = "+str(Galaxy.nombre)+"   radio: "+str(Galaxy.radio)+" yl   masa: "+str(Galaxy.masa)+" msol"
                self.stateButtons("cuerpo","normal")
                self.stateButtons("grafica","normal")
                self.sis=True
                self.MostrarTabla([],[])
                                    
            else:
                self.mensaje["text"]="Solo ingrese el Nombre del sistema"
        except:
            self.mensaje["text"]="Ingrese un nombre valido o existente"
    
    def BorrarSistema(self):
        try:            
            gall = [self.nombresis.get(),self.distsis.get()]
            if(len(gall[0])!=0 and len(gall[1])==0):
                try:
                    Buscar("sistema",["Distancia"],["Nombre"], [gall[0]]) #  tipo(str)   params(list) condicion(list) value(list
                    respuesta=mb.askyesno("Cuidado", "¿Quiere borrar el sistema "+str(gall[0])+"?")
                    if respuesta == True:
                        Borrar("sistema",gall[0],["galaxia",self.Galaxy.id_Galaxia])
                        
                        self.nombresis.delete(0,END)
                        self.distsis.delete(0,END)
                        self.nombresis.focus()
                        if self.sis == True:
                            if gall[0] == self.System.nombre:
                                self.status["text"]=self.state
                                self.stateButtons("cuerpo","disabled")
                                self.sis=False
                                del self.System
                                self.MostrarTabla([],[])
                            else: pass
                        else: pass
                        self.mensaje["text"]="El sistema se ha borrado con exito"
                except:
                    self.mensaje["text"]="Nombre de sistema incorrecto"
            else:
                self.mensaje["text"]="Solo ingrese el Nombre del sistema"
        except:
            self.mensaje["text"]="Ingrese un valor valido"

    ################################ CUERPOS ###################################
    ############################################################################

    def CargarBodys(self):
        """if len(self.System.nombres) > 0:
            copianames = self.System.nombres
            print(copianames)
            for i in copianames:
                self.System.borrar(i)
                print(self.System.nombres)"""
        #limpiar
        if self.System.planetas > 0 or self.System.estrellas > 0:
            for cuerpo in ['planeta','estrella','asteroide','cometa','satelite']:
                try:
                    #Y = list(Buscar(cuerpo,['id_'+cuerpo.capitalize(),'Nombre','Masa','Radio'],['id_Sistema'], [str(self.System.id_Sistema)]))
                    Y = list(querys("SELECT `id_"+cuerpo.capitalize()+"`,`Nombre`,`Masa`,`Radio` FROM `"+cuerpo+"` WHERE `id_Sistema` = "+str(self.System.id_Sistema)+";"))
                    
                    if type(Y[0]) != int:                                
                        for i in Y:
                            
                            cparams = list(Buscar("cuerpo",['id_Cuerpo','Semieje','Excentricidad','Inclinacion','Argumento','RAAN','Anomalia'],['id_'+cuerpo.capitalize()], [str(i[0])]))
                            # = list(Buscar("parametros",['id_cuerpo'],['id_'cuerpo.capitalize()], [str(i[0])]))
                            
                            self.System.nuevo(i[1],cuerpo,[i[0],cparams[0]],i[3],[i[2]]+cparams[1:])
                    else:
                        cparams = list(Buscar("cuerpo",['id_Cuerpo','Semieje','Excentricidad','Inclinacion','Argumento','RAAN','Anomalia'],['id_'+cuerpo.capitalize()], [str(Y[0])]))
                        
                        self.System.nuevo(Y[1],cuerpo,[Y[0],cparams[0]],Y[3],[Y[2]]+cparams[1:])
                except:
                    pass
            self.MostrarTabla(self.System.nombres,self.System.table)
        else:
            self.mensaje["text"]="No hay cuerpos que cargar"
                    
            
    
    def NuevoBody(self):
        try:
            gall = [self.nombrebody.get(),self.radiobody.get(),self.masabody.get(),self.option_var.get(),self.semieje.get(),self.ecc.get(),self.inc.get(),self.arg.get(),self.raan.get(),self.ta.get()]
            if ((((((((len(gall[0])!=0 and len(gall[1])!=0) and len(gall[2])!=0) and gall[3] != "Cuerpo") and len(gall[4])!=0) and len(gall[5])!=0) and len(gall[6])!=0) and len(gall[7])!=0) and len(gall[8])!=0) and len(gall[9])!=0:
                Guardar([str(self.System.id_Sistema),'sistema',gall[0],gall[2],gall[1],gall[4]],gall[4:]+[0],gall[3])
                #Guardar(caracts,params,tipo)
                self.mensaje["text"]="El cuerpo se ha ingresado con exito"
                self.nombrebody.delete(0,END)
                self.radiobody.delete(0,END)
                self.masabody.delete(0,END)
                self.option_var.set("Cuerpo")
                self.semieje.delete(0,END)
                self.ecc.delete(0,END)
                self.inc.delete(0,END)
                self.arg.delete(0,END)
                self.raan.delete(0,END)
                self.ta.delete(0,END)
                if gall[3] in ["Planeta","Estrella"]:
                    if gall[3]=="Planeta":
                        self.System.planetas += 1
                        Actualizar([self.System.nombre,"Planetas",self.System.planetas],[],"sistema")
                    else:
                        self.System.estrellas += 1
                        Actualizar([self.System.nombre,"Estrellas",self.System.estrellas],[],"sistema")
                self.nombrebody.focus()
                self.status["text"]=self.state+f"\nSistema = {self.System.nombre}   Estrellas: {self.System.estrellas}    Planetas: {self.System.planetas}    Distancia: {self.System.distancia:.2E} yl"
            else:
                self.mensaje["text"]="Ingrese todos los valores del cuerpo"
        except:
            self.mensaje["text"]="Ingrese valores validos"

    def ActualizarBody(self):
        try:
            gall = [self.nombrebody.get(),self.radiobody.get(),self.masabody.get(),self.option_var.get(),self.semieje.get(),self.ecc.get(),self.inc.get(),self.arg.get(),self.raan.get(),self.ta.get()]
            if ((((((((len(gall[0])!=0 and len(gall[1])!=0) and len(gall[2])!=0) and gall[3] != "Cuerpo") and len(gall[4])!=0) and len(gall[5])!=0) and len(gall[6])!=0) and len(gall[7])!=0) and len(gall[8])!=0) and len(gall[9])!=0:
                try:
                    Actualizar([gall[0],"Masa",gall[2],"Radio",gall[1],"Distancia",gall[4]],gall[4:]+[0],gall[3])
                    self.System.actualizar(gall[0],[gall[2],gall[1],gall[4]],gall[4:]+[0],gall[3])
                    self.mensaje["text"]="El cuerpo se ha actualizado con exito"
                    self.nombrebody.delete(0,END)
                    self.radiobody.delete(0,END)
                    self.masabody.delete(0,END)
                    self.option_var.set("Cuerpo")
                    self.semieje.delete(0,END)
                    self.ecc.delete(0,END)
                    self.inc.delete(0,END)
                    self.arg.delete(0,END)
                    self.raan.delete(0,END)
                    self.ta.delete(0,END)
                    self.MostrarTabla(self.System.nombres,self.System.table)
                    self.nombrebody.focus()
                    if self.sis == True:
                        
                        self.status["text"]=self.state+f"\nSistema = {self.System.nombre}   Estrellas: {self.System.estrellas}    Planetas: {self.System.planetas}    Distancia: {self.System.distancia:.2E} yl"#"Status:      Galaxia = "+str(Galaxy.nombre)+"   radio: "+str(Galaxy.radio)+" yl   masa: "+str(Galaxy.masa)+" msol"
                except:
                    self.mensaje["text"]="El sistema no existe"
            else:
                self.mensaje["text"]="Ingrese todos los valores del sistema"
        except:
            self.mensaje["text"]="Ingrese valores validos"
    
    def CargarBody(self):
        try:
            gall = [self.nombrebody.get(),self.radiobody.get(),self.masabody.get(),self.option_var.get(),self.semieje.get(),self.ecc.get(),self.inc.get(),self.arg.get(),self.raan.get(),self.ta.get()]
            if ((((((((len(gall[0])!=0 and len(gall[1])==0) and len(gall[2])==0) and gall[3] != "Cuerpo") and len(gall[4])==0) and len(gall[5])==0) and len(gall[6])==0) and len(gall[7])==0) and len(gall[8])==0) and len(gall[9])==0:
                
                G = list(Buscar(str(gall[3]).lower(),["id_"+str(gall[3]),"Masa","Radio","Distancia"],["Nombre","id_Sistema"], [gall[0],str(self.System.id_Sistema)]))
                F = list(Buscar("cuerpo",["id_Cuerpo","Semieje","Excentricidad","Inclinacion","Argumento","RAAN","Anomalia"],["id_"+str(gall[3])], [str(G[0])]))
                self.System.nuevo(gall[0],gall[3],[G[0],F[0]],G[2],[G[1]]+F[1:])
                self.mensaje["text"]="Cuerpo seleccionado con exito"
                self.nombrebody.delete(0,END)
                self.option_var.set("Cuerpo")
                self.nombresis.focus()
                #self.state
                #self.status["text"]=self.state+f"\nSistema = {self.System.nombre}   Estrellas: {self.System.estrellas}    Planetas: {self.System.planetas}    Distancia: {self.System.distancia:.2E} yl"#"Status:      Galaxia = "+str(Galaxy.nombre)+"   radio: "+str(Galaxy.radio)+" yl   masa: "+str(Galaxy.masa)+" msol"
                self.MostrarTabla(self.System.nombres,self.System.table)
                self.sis=True
            else:
                self.mensaje["text"]="Ingrese solo el Nombre y el tipo de cuerpo"
        except:
            self.mensaje["text"]="Ingrese un nombre valido o existente"
    
    def BorrarBody(self):
        try:            
            gall = [self.nombrebody.get(),self.radiobody.get(),self.masabody.get(),self.option_var.get(),self.semieje.get(),self.ecc.get(),self.inc.get(),self.arg.get(),self.raan.get(),self.ta.get()]
            if ((((((((len(gall[0])!=0 and len(gall[1])==0) and len(gall[2])==0) and gall[3] != "Cuerpo") and len(gall[4])==0) and len(gall[5])==0) and len(gall[6])==0) and len(gall[7])==0) and len(gall[8])==0) and len(gall[9])==0:
                try:
                    Buscar(gall[3],["Distancia"],["Nombre"], [gall[0]]) #  tipo(str)   params(list) condicion(list) value(list
                    respuesta=mb.askyesno("Cuidado", "¿Quiere borrar el cuerpo "+str(gall[0])+"?")
                    if respuesta == True:
                        #Borrar("sistema",gall[0],["galaxia",self.Galaxy.id_Galaxia])
                        #Borrar(gall[3].lower(),gall[0],["sistema",self.System.id_Sistema])
                        Borrar(gall[3].lower(),gall[0],["sistema",self.System.id_Sistema])
                        
                        self.nombrebody.delete(0,END)
                        self.option_var.set("Cuerpo")
                        if gall[0] in self.System.nombres:
                            self.System.borrar(gall[0])
                            self.MostrarTabla(self.System.nombres,self.System.table)
                        else: pass
                        if gall[3] in ["Planeta","Estrella"]:
                            if gall[3]=="Planeta":
                                self.System.planetas -= 1
                                Actualizar([self.System.nombre,"Planetas",self.System.planetas],[],"sistema")
                            else:
                                self.System.estrellas -= 1
                                Actualizar([self.System.nombre,"Estrellas",self.System.estrellas],[],"sistema")
                        self.nombrebody.focus()
                        self.status["text"]=self.state+f"\nSistema = {self.System.nombre}   Estrellas: {self.System.estrellas}    Planetas: {self.System.planetas}    Distancia: {self.System.distancia:.2E} yl"
                    
                        self.mensaje["text"]="El cuerpo se ha borrado con exito"
                except:
                    self.mensaje["text"]="Valores incorrectos"
            else:
                self.mensaje["text"]="Ingrese solo el Nombre y el tipo de cuerpo"
        except:
            self.mensaje["text"]="Ingrese un valor valido" 

    def EliminarBody(self):
        try:            
            indices = self.listbox.curselection()
            if len(indices)>0:
                try:
                    respuesta=mb.askyesno("Cuidado", "¿Quiere borrar del modelo el/los cuerpo(s) seleccionados?")
                    if respuesta == True:
                        for i in indices:
                            self.System.borrar(self.listbox.get(i))
                            self.MostrarTabla(self.System.nombres,self.System.table)
                        self.mensaje["text"]="El cuerpo se ha borrado con exito"
                    else: pass
                except:
                    self.mensaje["text"]="Ocurrio un problema"
            else:
                self.mensaje["text"]="No hay cuerpos seleccionados"
        except:
            self.mensaje["text"]="Ocurrio un problema"
            
    def stateButtons(self,buttons,state):
        if buttons == "sistema":
            self.crearsis["state"]=state
            self.actualizarsis["state"]=state
            self.buscarsis["state"]=state
            self.borrarsis["state"]=state
        elif buttons == "cuerpo":
            self.crearbody["state"]=state
            self.actualizarbody["state"]=state
            self.buscarbody["state"]=state
            self.borrarbody["state"]=state
            self.buscarbodys["state"]=state
            self.eliminarbody["state"]=state
        elif buttons == "grafica":
            self.creargrafica["state"]=state
      
    def MostrarTabla(self,nombres,cuerpos):
        registros=self.cuadro.get_children()
        self.listbox.delete(0,END)
        self.cuadro.delete(*self.cuadro.get_children())
        for i in range(len(nombres)):
            self.cuadro.insert('',0,text=nombres[i],values=cuerpos[i])
            self.listbox.insert(END, nombres[i])
    
    def Graficar(self):
        ## codigo condensado para gráficar
        gl = [self.tiempoi.get(),self.tiempof.get()]
        if len(gl[0])>0 and len(gl[1])>0:
            if len(self.System.nombres) > 0:
                ti = Time(gl[0], format='iso', scale='utc')
                tf = Time(gl[1], format='iso', scale='utc')
                self.System.tiempo((float(ti.jd)-2451544.5)*86400,(float(tf.jd)-2451544.5)*86400)
                if self.System.tiempoi < self.System.tiempof:
                    indices = self.listbox.curselection()
                    if len(indices) > 0 and self.checkbodys_value.get() == True: 
                        self.cuerposgraph = []
                        for i in indices:
                            self.cuerposgraph.append(self.listbox.get(i))
                        BG = self.cuerposgraph
                        self.System.Solucionar(BG,self.checkgrid_value.get(),[20,-60])
                        canvas = FigureCanvasTkAgg(self.System.fig, self.marcograph)
                        canvas.draw()
                        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
                        self.graph = True
                    elif len(indices) == 0 and self.checkbodys_value.get() == True:
                        #BG = self.System.nombres
                        self.mensaje['text'] = "No hay cuerpos seleccionados"
                    else:
                        BG = self.System.nombres
                        self.System.Solucionar(BG,self.checkgrid_value.get(),[20,-60])
                        canvas = FigureCanvasTkAgg(self.System.fig, self.marcograph)
                        canvas.draw()
                        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
                        self.graph = True
                else:
                    self.mensaje['text'] = "Ingrese tiempos de integración validos"
            else:
                self.mensaje['text'] = "No hay cuerpos en el sistema para modelar"
        else:
            self.mensaje['text'] = "Ingrese tiempos de integración"
    
        
        
########################################################################################        
################################# PROPAGACIÓN ########################################
########################################################################################
        
class Galaxia():
    def __init__(self, nombre, H):#[id_Galaxia, radio, masa, tipo]
        self.id_Galaxia = H[0]
        self.nombre = nombre
        self.radio = H[1]
        self.masa = H[2]
        self.tipo = H[3]
        

class Sistema():
  
    def __init__(self, nombre, H): #[id_Sistema,estrellas, planetas,distancia]
        
        self.nombre = nombre
        self.id_Sistema = H[0]
        self.estrellas = H[1]
        self.planetas = H[2]
        self.distancia = H[3]
        self.cuerpos = []
        self.tipos = []
        self.ids = []
        self.nombres = []
        self.table = []
    def nuevo(self,ncuerpo,tipo,idd,radio,parametros): #parametros es una lista
        self.nombres.append(ncuerpo)
        self.tipos.append(tipo)
        self.ids.append(idd)
        self.cuerpos.append(parametros)
        self.table.append([parametros[0],radio,tipo])
    def actualizar(self,ncuerpo,newcaracts,newparams): #parametros es un lista
        indx = self.nombres.index(ncuerpo)
        #self.nombres.drop(indx)
        self.cuerpos[indx] = newparams
        self.table[indx] = [newparams[0],newcaracts[1],self.tipos[indx]]
    def borrar(self,ncuerpo): 
        indx = self.nombres.index(ncuerpo)
        self.nombres.pop(indx)
        self.tipos.pop(indx)
        self.ids.pop(indx)
        self.cuerpos.pop(indx)
        self.table.pop(indx)
    def limpiar(self):
        self.cuerpos = []
        self.tipos = []
        self.ids = []
        self.nombres = []
        self.table = []

    def tiempo(self, tiempoi,tiempof):
        self.tiempoi = tiempoi#el valor del cuadro
        self.tiempof = tiempof

    def sistema_a_Y(self):
        mus=[]
        r0s=[]
        v0s=[]
        N=0
        for particula in self.canonics:
            m=particula['m']
            if m>0:
                mus+=[m]
                r0s+=list(particula["r"])
                v0s+=list(particula["v"])
                N+=1

        Y0s=array(r0s+v0s)
        mus=array(mus)
        return N,mus,Y0s
    
    def CanonicasConversion(self):
        cuerpos = array(self.cuerpos)
        UM = max(list(cuerpos[:,0]))# kg
        UL = max(list(cuerpos[:,1]))# km
        UT = (float(UL*1000)**3/(6.67308e-11*float(UM)))**0.5 #OJO G en SI: convertir km a m
        
        UV = UL/UT
        sis = []
        for i in range(len(cuerpos)):
            if cuerpos[i,2] == 0:
                sis.append(dict(m=cuerpos[i,0]/UM,r=[0,0,0],v=[0,0,0]))
            else:
                state=conics([float(cuerpos[i,1])/(1-float(cuerpos[i,2]))/UL]+[cuerpos[i,2]]+list(cuerpos[i,3:]*deg)+[0,1],0)#[0,1] son la epoca y el mu
                sis.append(dict(m=cuerpos[i,0]/UM,r=list(array(state[:3])),v=list(array(state[3:]))))
                
        self.tiempoi = self.tiempoi/UT#el valor del cuadro
        self.tiempof = self.tiempof/UT
        self.canonics=sis
        self.UT = UT
        
    def Solucionar(self,cuerposs,griid,vista):
        self.CanonicasConversion()
        N,mus,Yo = self.sistema_a_Y()
        #Tiempo de integración
        Nt = 2
        ts = linspace(0.0,self.tiempoi,Nt,endpoint=True)
        # Solución al sistema de ecuaciones diferenciales
        solucion = odeint(edm_ncuerpos,Yo,ts,args=(N,mus))
        rs,vs = solucion_a_estado(solucion,N,Nt)
        Yf = zeros(N*6)
        for i in range(N):
            for j in range(3): 
                Yf[3*i+j]=rs[i,-1,j]
                Yf[N*3+(3*i+j)]=vs[i,-1,j]
        #Tiempo de integración
        Nt = (self.tiempof-self.tiempoi)*self.UT/86400 if (self.tiempof-self.tiempoi)*self.UT > 10*86400 else 100
        ts = linspace(0,self.tiempof-self.tiempoi,int(Nt),endpoint=True)
        # Solución al sistema de ecuaciones diferenciales
        solucion = odeint(edm_ncuerpos,list(Yf),ts,args=(N,mus))
        rs,vs = solucion_a_estado(solucion,N,int(Nt))
        # Componente gráfica del algoritmo
        self.fig = plot_ncuerpos_3d(rs,self.nombres,cuerposs,griid,vista,lw=1)

class Cuerpo():
    def __init__(self,nombre,masa,radio,distancia,tipo,parametros):
        self.nombre = nombre
        self.masa = masa
        self.radio = radio
        self.distancia = distancia
        self.tipo = tipo
        self.parametros


###############################################################
####################### FUNCIONES #############################
def elo2vest(Y,mu):
        a,e,i,O,w,v = Y
        p = a*(1-e**2)
        r=p/(1+e*cos(v))


        x=r*(cos(O)*cos(w+v)-cos(i)*sin(O)*sin(w+v))
        y=r*(sin(O)*cos(w+v)+cos(i)*cos(O)*sin(w+v))
        z=r*(cos(v)*sin(w)*sin(i)+sin(v)*cos(w)*sin(i))

        muh=mu/((p*mu)**0.5)
        vx=muh*(-cos(O)*sin(w+v)-cos(i)*sin(w)*cos(w+v))-muh*e*(cos(O)*sin(w)+cos(w)*cos(i)*sin(w))
        vy=muh*(-sin(O)*sin(w+v)+cos(i)*cos(w)*cos(w+v))+muh*e*(-sin(O)*sin(w)+cos(w)*cos(i)*cos(w))
        vz=muh*(sin(i)*cos(w+v)+e*cos(w)*sin(i))
        return array([x,y,z,vx,vy,vz])


def edm_ncuerpos(Y,t,N=2,mus=[]):
    dYdt=zeros(6*N)
    
    #Primer conjunto de ecuaciones
    dYdt[:3*N]=Y[3*N:]
    
    #Segundo conjunto de ecuaciones
    for k in range(3*N,6*N):
        l=k%3
        i=int(floor((k-3*N)/3))
        for j in range(N):
            if j==i:continue
            rij=(Y[3*i]-Y[3*j])**2+\
                (Y[3*i+1]-Y[3*j+1])**2+\
                (Y[3*i+2]-Y[3*j+2])**2
            dYdt[k]+=-mus[j]*(Y[3*i+l]-Y[3*j+l])/rij**1.5
    return dYdt

def solucion_a_estado(solucion,Nparticulas,Ntiempos):
    rs=zeros((Nparticulas,Ntiempos,3))
    vs=zeros((Nparticulas,Ntiempos,3))
    for i in range(Nparticulas):
        rs[i]=solucion[:,3*i:3*i+3]
        vs[i]=solucion[:,3*Nparticulas+3*i:3*Nparticulas+3*i+3]
    return rs,vs
  
def plot_ncuerpos_3d(rs,cuerpos,nombres,griid,view=[20,-60],**opciones):
    #Número de partículas
    #N=rs.shape[0]
    N=len(nombres)
    fig=plt.figure()
    ax=fig.add_subplot(111,projection="3d")
    for i in range(N):
      indx = cuerpos.index(nombres[i])
      ax.plot(rs[indx,:,0],rs[indx,:,1],rs[indx,:,2],**opciones);
      #ax.plot(rs[i,0,:],rs[i,1,:],rs[i,2,:],label=names[i+1],linewidth=1)
      ax.scatter(rs[indx,-1,0],rs[indx,-1,1],rs[indx,-1,2],label='_nolegend_')
      ax.text(rs[indx,-1,0],rs[indx,-1,1],rs[indx,-1,2]+0.01,s=nombres[i],c="white",fontsize=7)
    
    fig.set_facecolor('black');
    ax.set_facecolor('black');
    ax.grid(griid); 
    ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0));
    ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0));
    ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0));
    ax.set_box_aspect([1,1,1]);
    ax.axis("equal");
    fig.tight_layout()
    ax.view_init(view[0],view[1])
    return fig
    
########################################################################################        
################################# BASE DE DATOS ########################################
########################################################################################
        
def querys(query):
        try:
            conn=mariadb.connect(
            host="localhost",
            user="root",
            password="",
            database="estrellantes",
            autocommit=True)
        except Exception as err:
            self.mensaje["text"]="No fue posible conectarse a la base de datos"
            
        cur=conn.cursor()
        cur.execute(query)
        return cur

def Guardar(caracts,params,tipo): #caracts(list)  params(list)   tipo(str)
    if tipo == "galaxia":
        querys("INSERT INTO `galaxia` (`id_Galaxia`,`Nombre`,`Radio`,`Masa`,`Tipo`) VALUES (NULL,'"+str(caracts[0])+"','"+str(caracts[1])+"','"+str(caracts[2])+"','"+str(caracts[3])+"');") 
    elif tipo == "sistema": #caracts: [nombre, estrellas, planetas,distancia, id]
        #ids = str(querys("SELECT `id_Galaxia` FROM `galaxia` WHERE `Nombre` = '"+str(caracts[0])+"';"))
        querys("INSERT INTO `sistema` (`id_Sistema`,`Nombre`,`Estrellas`,`Planetas`,`Distancia`,`id_Galaxia`) VALUES (NULL,'"+str(caracts[0])+"','"+str(caracts[1])+"','"+str(caracts[2])+"','"+str(caracts[3])+"','"+str(caracts[4])+"');")
    else:# (tipo != "galaxia" and tipo != "sistema"):
        #ids = str(querys("SELECT `id_"+caracts[1].capitalize()+"` FROM `"+caracts[1]+"` WHERE `Nombre` = '"+str(caracts[0])+"';").fetchall()[0][0])
        """desc = querys("DESCRIBE "+str(tipo)).fetchall()
        descs = [desc[i][0] for i in range(len(desc))]
        idscount = 0
        for i in descs:
            if "id_" in i:
                idscount += 1
        strr = "INSERT INTO `"+str(tipo)+"` (`"
        for i in range(len(desc)-idscount+1):
            strr += str(desc[i][0])+"`,`"""
        strr = "INSERT INTO `"+str(tipo)+"` (`id_"+str(tipo).capitalize()+"`,`Nombre`,`Masa`,`Radio`,`Distancia`,"
        """for i in range(len(desc)-idscount+1):
            strr += str(desc[i][0])+"`,`"""
        strr += "`id_"+caracts[1].capitalize()+"`) VALUES (NULL, '"
        for i in range(2,len(caracts)):
            strr += str(caracts[i])+"','" #if i != len(desc)-1 else ids+"');"
        strr += caracts[0]+"');"
        
        querys(strr)
        idd = str(querys("SELECT `id_"+tipo.capitalize()+"` FROM `"+tipo+"` WHERE `Nombre` = '"+str(caracts[2])+"';").fetchall()[0][0])
        querys("INSERT INTO `cuerpo` (`id_Cuerpo`,`id_"+tipo.capitalize()+"`,`semieje`,`Excentricidad`,`Inclinacion`,`Argumento`,`RAAN`,`Anomalia`,`Epoca`) VALUES (NULL,'"+str(idd)+"','"+str(params[0])+"','"+str(params[1])+"','"+str(params[2])+"','"+str(params[3])+"','"+str(params[4])+"','"+str(params[5])+"','"+str(params[6])+"');") 

def Actualizar(caracts,params,tipo): #caracts(list) [nombre,masa,radio,distancia]  params(list)   tipo(str),idss(int ó str)
    if tipo =="galaxia":
        ids = str(querys("SELECT `id_Galaxia` FROM `galaxia` WHERE `Nombre` = '"+str(caracts[0])+"';").fetchall()[0][0])
        querys("UPDATE `galaxia` SET `Nombre`='"+str(caracts[0])+"',`Radio`='"+str(caracts[1])+"',`Masa`='"+str(caracts[2])+"',`Tipo`='"+str(caracts[3])+"' where `id_Galaxia`='"+str(ids)+"';") 
    if tipo == "sistema": #caracts=[key1,value1,key2,value2....]
        ids = str(querys("SELECT `id_Sistema` FROM `sistema` WHERE `Nombre` = '"+str(caracts[0])+"';").fetchall()[0][0])
        strr = "UPDATE `sistema` SET"
        for i in range(1,int(len(caracts))-2,2):
            strr += "`"+str(caracts[i])+"`='"+str(caracts[i+1])+"',"
        strr += "`"+str(caracts[-2])+"`='"+str(caracts[-1])+"' where `id_Sistema`='"+str(ids)+"';"
        querys(strr)
        #querys("UPDATE `sistema` SET `Nombre`='"+str(caracts[0])+"',Distancia`='"+str(caracts[3])+"' where `id_Sistema`='"+str(ids)+"';") 
    if tipo != "galaxia" and tipo != "sistema":
        ids = str(querys("SELECT `id_"+tipo.capitalize()+"` FROM `"+str(tipo)+"` WHERE `Nombre` = '"+str(caracts[0])+"';").fetchall()[0][0])
        """desc = querys("DESCRIBE "+str(tipo)).fetchall()
        descs = [desc[i][0] for i in range(len(desc))]
        idscount = 0
        for i in descs:
            if "id_" in i:
                idscount += 1"""
        #strr = "UPDATE `"+str(tipo)+"` SET `Masa` ="+caracts[1]+"`Radio` ="+caracts[2]+"`Distancia` ="+caracts[3]
        """for i in range(len(desc)-idscount):
            strr += str(desc[i+1][0])+"`='"+ str(caracts[i+2])+"',`" 
        #strr += "id_"+caracts[1].capitalize()+"`='"+str(ids)+"'"""
        #strr += " where `id_"+tipo.capitalize()+"`='"+str(ids)+"';"
        strr = "UPDATE `"+str(tipo)+"` SET"
        for i in range(1,int(len(caracts))-2,2):
            strr += "`"+str(caracts[i])+"`='"+str(caracts[i+1])+"',"
        strr += "`"+str(caracts[-2])+"`='"+str(caracts[-1])+"' where `id_Sistema`='"+str(ids)+"';"
        querys(strr)
        #idds = str(querys("SELECT `id_"+tipo.capitalize()+"` FROM `"+tipo+"` WHERE `Nombre` = '"+str(caracts[2])+"';").fetchall()[0][0])
        querys("UPDATE `cuerpo` SET `semieje`='"+str(params[0])+"',`Excentricidad`='"+str(params[1])+"',`Inclinacion`='"+str(params[2])+"',`Argumento`='"+str(params[3])+"',`RAAN`='"+str(params[4])+"',`Anomalia`='"+str(params[5])+"',`Epoca`='"+str(params[5])+"' where `id_"+tipo.capitalize()+"`='"+str(ids)+"';")
def Borrar(tipo,name,padre): #  tipo(str)   name(str)   padre(list)
    #querys("DELETE from "+str(tipo)+" where `id_"+tipo.capitalize()+" ='"+str(idss)+"';")
    if tipo != "galaxia":
        #print("SELECT `id_"+tipo.capitalize()+"` FROM `"+str(tipo)+"` WHERE `Nombre` = '"+str(name)+"' AND `id_"+str(padre[0].capitalize())+"` = '"+str(padre[1])+"';")
        ids = querys("SELECT `id_"+tipo.capitalize()+"` FROM `"+str(tipo)+"` WHERE `Nombre` = '"+str(name)+"' AND `id_"+str(padre[0].capitalize())+"` = '"+str(padre[1])+"';").fetchall()[0][0]
        #print("DELETE from `"+str(tipo)+"` where `id_"+tipo.capitalize()+"` ='"+str(ids)+"';")
        querys("DELETE from `"+str(tipo)+"` where `id_"+tipo.capitalize()+"` ='"+str(ids)+"';")
    else:
        ids = querys("SELECT `id_"+tipo.capitalize()+"` FROM `"+str(tipo)+"` WHERE `Nombre` = '"+str(name)+"';").fetchall()[0][0]
        querys("DELETE from "+str(tipo)+" where id_"+str(tipo.capitalize())+" ='"+str(ids)+"';")
def Buscar(tipo,params,condicion, value): #  tipo(str)   params(list) condicion(list) value(list)
    strr="SELECT "
    for i in range(len(params)-1):
        strr +="`"+str(params[i])+"`,"
    strr += "`"+str(params[-1])+"` FROM `"+str(tipo)+"` where "
    for i in range(len(condicion)-1):
        strr +="`"+str(condicion[i])+"`='"+str(value[i])+"' AND " 
    strr +="`"+str(condicion[-1])+"`='"+str(value[-1])+"';"
    return querys(strr).fetchall()[0]

########################################################################################
########################################################################################
        
if __name__=="__main__":
    ventana=Tk()
    aplicacion=interfaz(ventana)
    #aplicacion.mostrar()
    ventana.mainloop()


"""sistema_ejemplo=array([[2e30,0,True,0,0,0,0],#[2e30,1.044432136480338E+06,2.694756167974767E-01,1.555730359764524E+00,1.036750662362893E+02,2.229947459632241E+02,2.346870976912870E+02],#[2e30,0,True,0,0,0,0]
                       [5.972e24,1.489157387174645E+08,1.519356354936738E-02,1.180412883841571E-02,8.994459355558011E+00,6.504439592195953E+01,2.626770133243085E+01],
                      [1.9e27,7.763722760560771E+08,4.775179786950577E-02,1.304275313560391E+00,1.004827571728605E+02,2.740954352407625E+02,2.168778040526353E+01]])

prueba = sys("system")
prueba.nuevo("cuerpo1",array(sistema_ejemplo[0]))
prueba.nuevo("cuerpo2",array(sistema_ejemplo[1]))

prueba.nuevo("cuerpo3",sistema_ejemplo[2])
prueba.tiempo(0,86400*365)
#prueba.tiempo(86400*365,86400*2*365)
prueba.Solucionar(["cuerpo1","cuerpo2","cuerpo3"],[20,-60])"""
