import tkinter as tk
from models.rental_systems import RentalSystem
from gui.view.history_view import RentalHistoryWindow

class RentalController:
    def __init__(self, app_instance, rental_system: RentalSystem):
        #constructor
        self.app = app_instance
        self.system = rental_system

    def kirala(self):
        #kiralama işlemini yapan method
        secilen = self.app.main_view.arac_tablo.selection()
        if not secilen:
            self.app.feedback.show(False, "Kiralamak için bir araç seçin")
            return
        plaka = self.app.main_view.arac_tablo.item(secilen[0], 'values')[0]
        kiralayan = self.app.main_view.kiralayan_input.get()
        baslangic_str = self.app.main_view.baslangic_input.get_date().strftime("%d-%m-%Y")
        bitis_str = self.app.main_view.bitis_input.get_date().strftime("%d-%m-%Y")

        success, message = self.system.kiralama_baslat(plaka, kiralayan, baslangic_str, bitis_str)
        self.app.feedback.show(success, message)

        if success:
            self.app.main_view.araclari_yukle()
            self.app.main_view.form_temizle(mode='kiralama')
            
    def iade_et(self):
        #iade etme işlemini gerçekleştiren metodu
        secilen = self.app.main_view.arac_tablo.selection()
        if not secilen:
            self.app.feedback.show(False, "İade edilecek bir araç seçin.")
            return
        plaka = self.app.main_view.arac_tablo.item(secilen[0], 'values')[0]

        if tk.messagebox.askyesno("Onay", f"'{plaka}' plakalı aracın iade işlemini onaylıyor musunuz?"):
            success, message = self.system.arac_iade_et(plaka)
            self.app.feedback.show(success, message)
            if success:
                self.app.main_view.araclari_yukle()
                self.app.main_view.form_temizle(mode='kiralama')
            else:
                self.app.feedback.show(False, "İade işlemi iptal edildi.")

    def gecmisi_goster(self): 
        #gecmisi kiralama kayıtlarını gosteren method
        gecmis = self.system.kiralama_gecmisi
        RentalHistoryWindow(self.app, gecmis)