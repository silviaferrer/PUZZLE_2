import code
import threading
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk


class LabelWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="rfid_gtk.py")
        self.set_border_width(10)

        self.box = Gtk.Box(spacing=6)
        self.box.set_homogeneous(False)
        
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        self.add(self.box)
        
        self.evbox = Gtk.EventBox()
        self.evbox.override_background_color(0, Gdk.RGBA(0,0,8,1))

        self.box.pack_start(self.box, True, True, 0)

        self.label = Gtk.Label('<span foreground="white" size="x-large">Please login with your university card</span>')
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_use_markup(True)
        self.label.set_name("Inicial_label")
        self.label.set_size_request(400,100)
        self.box.pack_start(self.label, True, True, 0)
        
        self.evbox.add(self.label)
        
        self.button = Gtk.Button(label="Clear")
        self.button.connect("clicked", self.clicked)
        self.box.pack_start(self.button, True, True, 0)
        
        thread = threading.Thread(target=self.read_uid)
        thread.setDaemon(True)
        thread.start()
        
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()
    
    def clicked (self, widget):
        self.label.set_label('<span foreground="white" size="x-large">Please login with your university card</span>')
        self.evbox.override_background_color(0, Gdk.RGBA(0,0,8,1))
        
        thread = threading.Thread(target=self.read_uid)
        thread.start()
        
    def read_uid (self):
        p1 = code.puzzle_1()
        uid = p1.read_card()
        
        self.label.set_label('<span foreground="white" size="x-large">uid:'+uid+'</span>')
        self.evbox.override_background_color(0, Gdk.RGBA(8,0,0,1))
        
w = LabelWindow()       
