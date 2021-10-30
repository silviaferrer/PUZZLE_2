import code
import threading
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib


class LabelWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="rfid_gtk.py")
        self.set_border_width(10)
        #creo el GtkBox
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=6)
        #afegeixo el GtkBox a la propia finestra (self)
        self.add(box)
        #creo la GtkLabel
        self.label = Gtk.Label(label="Please login with your university card")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_size_request(400,100)
        box.pack_start(self.label, True, True, 0)
        #creo el GtkButton
        self.button = Gtk.Button(label="Clear")
        self.button.connect("clicked", self.clicked)
        self.button.set_sensitive(False)
        box.pack_start(self.button, True, True, 0)
        #creo el Thread per a que la seva target sigui el mètode read_uid de la propia classe i l'inicialitzo
        self.thread = threading.Thread(target=self.read_uid)
        self.thread.setDaemon(True)
        self.thread.start()
        #carrego l'arxiu .css que proporciona els estils de la GtkLabel i inicialitzo afegint la classe "start"
        self.styles = Gtk.CssProvider()
        self.styles.load_from_path("style_prov/estilos.css")
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), self.styles, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.label.get_style_context().add_class("start")        
        #faig que es mostri la finestra
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()
    #mètode que es crida quan es clica el GtkButton
    def clicked (self, widget):
        self.label.set_text("Please login with your university card")
        self.label.get_style_context().remove_class("uid_screen")
        self.label.get_style_context().add_class("start")
        self.button.set_sensitive(False)
        #arrenco de nou el Thread existent
        self.thread = threading.Thread(target=self.read_uid)
        self.thread.start()
    #mètode que retorna la uid en hex amb el mètode del puzzle 1   
    def read_uid (self):
        p1 = code.puzzle_1()
        self.uid = p1.read_card()
        GLib.idle_add(self.update)
        
    #es neccessari cridar aquest mètode que està fora del Thread per actualitzar el label    
    def update (self):
        self.label.get_style_context().remove_class("start")
        self.label.get_style_context().add_class("uid_screen")
        self.label.set_text("uid: "+self.uid)
        self.button.set_sensitive(True)
        
w = LabelWindow()       
