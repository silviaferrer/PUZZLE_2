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

        self.box = Gtk.Box(spacing=6)
        self.box.set_homogeneous(False)
        
        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=6)
        
        self.add(self.box)
        
        self.box.pack_start(self.box, True, True, 0)

        self.label = Gtk.Label(label="Please login with your university card")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_size_request(400,100)
        self.box.pack_start(self.label, True, True, 0)
        
        self.button = Gtk.Button(label="Clear")
        self.button.connect("clicked", self.clicked)
        self.box.pack_start(self.button, True, True, 0)
        
        self.thread = threading.Thread(target=self.read_uid)
        self.thread.setDaemon(True)
        self.thread.start()
        
        self.styles = Gtk.CssProvider()
        self.styles.load_from_path("style_prov/estilos.css")
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), self.styles, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.label.get_style_context().add_class("start")        
        
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()
    
    def clicked (self, widget):
        self.label.set_text("Please login with your university card")
        self.label.get_style_context().remove_class("uid_screen")
        self.label.get_style_context().add_class("start")
        
        self.thread = threading.Thread(target=self.read_uid)
        self.thread.start()
        
    def read_uid (self):
        p1 = code.puzzle_1()
        self.uid = p1.read_card()
        GLib.idle_add(self.update)
        
        
    def update (self):
        self.label.get_style_context().remove_class("start")
        self.label.get_style_context().add_class("uid_screen")
        self.label.set_text("uid: "+self.uid)
        
w = LabelWindow()       
