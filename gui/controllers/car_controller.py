import tkinter as tk
from models.rental_systems import RentalSystem

class CarController:
    def __init__(self, app_instance, rental_system: RentalSystem):
        #constructor method
        self.app = app_instance
        self.system = rental_system

    def add_car(self):
        #araba ekleme iişlemini gerçekleştiren method
        plaka = self.app.main_view.plaka_input.get()
        marka = self.app.main_view.marka_input.get()
        model = self.app.main_view.model_input.get()
        ucret = self.app.main_view.ucret_input.get()

        success, message = self.system.arac_ekle(plaka, marka, model, ucret)
        self.app.feedback.show(success, message)
        
        if success:
            self.app.main_view.araclari_yukle()
            self.app.main_view.form_temizle(mode='arac_yonetim')

    def update_car(self):
        #araba bilgilerini güncelleyen method
        plaka = self.app.main_view.plaka_input.get()
        marka = self.app.main_view.marka_input.get()
        model = self.app.main_view.model_input.get()
        ucret = self.app.main_view.ucret_input.get()

        success, message = self.system.arac_guncelle(plaka, marka, model, ucret)
        self.app.feedback.show(success, message)

        if success:
            self.app.main_view.araclari_yukle()
    
    def delete_car(self):
        #seçilen arabayı silen method
        secilen = self.app.main_view.arac_tablo.selection()
        if not secilen:
            self.app.feedback.show(False, "Silinecek araç seçilemedi")
            return
            
        plaka = self.app.main_view.arac_tablo.item(secilen[0] ,'values')[0]

        if tk.messagebox.askyesno("Onay", f"'{plaka}' plakalı aracı silmek istediğinizden emin misiniz?"):
            success, message = self.system.arac_sil(plaka)
            self.app.feedback.show(success, message)
            if success:
                self.app.main_view.araclari_yukle()
                self.app.main_view.form_temizle(mode='arac_yonetim')