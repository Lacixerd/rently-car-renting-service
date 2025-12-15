import customtkinter as ctk
from tkinter import ttk

class RentalHistoryWindow(ctk.CTkToplevel):
    def __init__(self,master,gecmis_veri):
        super().__init__(master)
        self.title("Kiralama Geçmişi Kayıtları")
        self.geometry("1200x500")
        self.grab_set()
        self.gecmis_veri = gecmis_veri
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0 ,sticky="nsew", padx=10,pady=10)
        # Tablo başlık kurulumu
        columns = ("Plaka", "Marka", "Model", "Kiralayan", "Günlük Ücret", "Başlangıç", "Bitiş", "Toplam Ücret", "İade Tarihi")
        
        self.gecmis_tablo = ttk.Treeview(frame, columns=columns, show='headings')
        
        for col in columns:
            self.gecmis_tablo.heading(col, text=col)
            self.gecmis_tablo.column(col, width=100, anchor="center")

        # Scrollbar
        vscroll = ctk.CTkScrollbar(frame, command=self.gecmis_tablo.yview)
        self.gecmis_tablo.configure(yscrollcommand=vscroll.set)
        vscroll.pack(side="right", fill="y")
        self.gecmis_tablo.pack(expand=True, fill='both', padx=(10, 0), pady=10)

        self.gecmisi_yukle()
        
    def gecmisi_yukle(self):
        # Geçmiş listesindeki verileri tabloya yükler
        for kayit in self.gecmis_veri:
            values = (
                kayit.get('plaka', ''),
                kayit.get('marka', ''),
                kayit.get('model', ''),
                kayit.get('kiralayan', ''),
                f"{kayit.get('ucret', 0):.2f}",
                kayit.get('baslangic_tarihi', ''),
                kayit.get('bitis_tarihi', ''),
                f"{kayit.get('toplam_ucret', 0):.2f} TL",
                kayit.get('iade_tarihi', '')
            )
            self.gecmis_tablo.insert("", "end", values=values)
            
        self.gecmis_tablo.column("Toplam Ücret", width=120)
        self.gecmis_tablo.column("İade Tarihi", width=120)
        self.gecmis_tablo.column(0,width=120)