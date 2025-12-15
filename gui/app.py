import customtkinter as ctk
from models.rental_systems import RentalSystem
from controllers.car_controller import CarController
from controllers.rental_controller import RentalController
from view.main_view import MainView
from utils.feedback import FeedbackService 

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class RentalApp(ctk.CTk):
    #Ana uygulama, controller ve view'ı bağlayan yer
    def __init__(self):
        #constructor
        super().__init__()
        self.title("Araç Kiralama Sistemi")
        self.geometry("1200x700")
        self.system = RentalSystem()
        self.feedback = FeedbackService()
        self.car_controller = CarController(self, self.system)
        self.rental_controller = RentalController(self, self.system)
        self.main_view = MainView(self, self.car_controller, self.rental_controller) 
        self.main_view.araclari_yukle()
        self.protocol("WM_DELETE_WINDOW", self.kapat_kaydet)
        
    def tema_degistir(self, mode):
        #tema değiştirir.
        ctk.set_appearance_mode(mode)

    def kapat_kaydet(self):
        # uygulama kapatılırken kaydetme 
        if self.system.verileri_kaydet():
            print("Veriler başarıyla kaydedildi...")
        self.destroy()