import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

class MainView:
    def __init__(self, master, car_controller, rental_controller):
        #constructor method
        self.master = master # RentalApp instance
        self.car_controller = car_controller
        self.rental_controller = rental_controller
        self.arayuz_olustur()
        
    def arayuz_olustur(self):
        # Grid yapısını ayarlama
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=0)

        self.sidebar_olustur()
        self.arac_tablo_olustur()
        self.form_olustur()

    def sidebar_olustur(self):
        # Sol taraftaki menüyü oluşturur.
        self.sidebar_frame = ctk.CTkFrame(self.master, corner_radius=10)
        self.sidebar_frame.grid(row=0 , column=0 ,rowspan=2 ,sticky="nsew" ,padx=10 ,pady=10)
        
        ctk.CTkLabel(self.sidebar_frame ,text="KONTROL PANELİ" ,font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15 ,padx=20)

        ctk.CTkLabel(self.sidebar_frame, text="ARAÇ DURUMU FİLTRELE",font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(5, 0), padx=20)
        self.filter_options = ["Tümü", "Kirada", "Müsait"]
        self.filter_combobox = ctk.CTkComboBox(self.sidebar_frame, values=self.filter_options, command=self.araba_filtrele)
        self.filter_combobox.set("Tümü")
        self.filter_combobox.pack(pady=(0, 20), padx=20, fill="x")

        ctk.CTkLabel(self.sidebar_frame ,text="TEMA AYARLARI" ,font=ctk.CTkFont(size=12, weight="bold")).pack(padx=20)
        self.tema_degis = ctk.CTkOptionMenu(self.sidebar_frame,values=["Light","Dark"],command=self.master.tema_degistir)
        self.tema_degis.set(ctk.get_appearance_mode())
        self.tema_degis.pack(pady=(0,10))


        self.rapor_frame = ctk.CTkFrame(self.sidebar_frame, corner_radius=10, fg_color=("#F5F5F5", "#3A3A3A"))
        self.rapor_frame.pack(pady=(10, 15), padx=15, fill="x")
   
        ctk.CTkLabel(self.rapor_frame, text="GENEL DURUM", font=ctk.CTkFont(size=12, weight="bold"), anchor="w").pack(pady=(10, 0), padx=10, fill="x")
        self.istatistik_text = ctk.CTkLabel(self.rapor_frame, justify="left", anchor="w", font=ctk.CTkFont(size=11,weight="bold"))
        self.istatistik_text.pack(pady=(0, 5), padx=10, fill="x")
      
        self.progress_frame = ctk.CTkFrame(self.rapor_frame, fg_color="transparent")
        self.progress_frame.pack(pady=(0, 10), padx=10, fill="x")
        self.progress_frame.grid_columnconfigure(0, weight=1)
        
        self.durum_cubuk = ctk.CTkProgressBar(self.progress_frame, height=10, corner_radius=5)
        self.durum_cubuk.grid(row=0, column=0, sticky="ew")
       
        ctk.CTkLabel(self.rapor_frame, text="RAPORLAR", font=ctk.CTkFont(size=12, weight="bold"), anchor="w").pack(pady=(10, 0), padx=10, fill="x")
        self.toplam_gelir = ctk.CTkLabel(self.rapor_frame, anchor="w", font=ctk.CTkFont(size=11, weight="bold"))
        self.toplam_gelir.pack(pady=(0, 2), padx=10, fill="x")

        self.en_cok_kiralanan = ctk.CTkLabel(self.rapor_frame, anchor="w", font=ctk.CTkFont(size=11, weight="bold"))
        self.en_cok_kiralanan.pack(pady=(0, 10), padx=10, fill="x")
        
        self.btn_kaydet = ctk.CTkButton(self.sidebar_frame, text="Verileri Kaydet" ,command= self.master.kapat_kaydet)
        self.btn_kaydet.pack(pady=10 ,padx=20 ,side="bottom" ,fill="x")
        
        self.btn_gecmis = ctk.CTkButton(self.sidebar_frame, text="Kiralama Geçmişi", command=self.rental_controller.gecmisi_goster)
        self.btn_gecmis.pack(pady=(10, 0) ,padx=20 ,fill="x",side="bottom")

       
    def arac_tablo_olustur(self):
        # Arac tablosunu oluşturan ve styling yapan method
        self.table_frame = ctk.CTkFrame(self.master)
        self.table_frame.grid(row=0 ,column=1, padx=(0,10) ,pady=(10,0) , sticky="nsew" ,columnspan=2)
        columns = ("Plaka" ,"Marka" ,"Model" ,"Günlük Ücret" ,"Durum","Kiralayan","Başlangıç","Bitiş")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#4CAF86",foreground="white")
        style.configure("Treeview", rowheight=25)
        style.map("Treeview.Heading",background=[("active", "#4CAF86")])

        self.arac_tablo = ttk.Treeview(self.table_frame , columns=columns ,show='headings')
        self.arac_tablo.bind("<<TreeviewSelect>>", self.secimi_doldur)
        for col in columns:
            self.arac_tablo.heading(col,text=col)
            self.arac_tablo.column(col, width=120 ,anchor="center")

        scroll = ctk.CTkScrollbar(self.table_frame, command=self.arac_tablo.yview)
        self.arac_tablo.configure(yscrollcommand= scroll.set)
        scroll.pack(side="right",fill="y")
        self.arac_tablo.pack(expand=True ,fill="both" ,padx=(10,0),pady=10)
        
    def form_olustur(self):
        # Araç ekle guncelle sil formu
        self.form_box = ctk.CTkFrame(self.master,corner_radius=10)
        self.form_box.grid(row=1 ,column=1 ,padx=(0,5) ,pady=(10,10), sticky="nsew")
        ctk.CTkLabel(self.form_box, text="Araç Ekleme ve Düzenleme", font=ctk.CTkFont(size=14 , weight="bold")).pack(pady=(10,5))
        
        self.plaka_input = self.input_olustur(self.form_box,"Plaka:") 
        self.marka_input = self.input_olustur(self.form_box,"Marka:") 
        self.model_input = self.input_olustur(self.form_box,"Model:") 
        self.ucret_input = self.input_olustur(self.form_box,"Günlük Ücret:") 

        btn_frame1 = ctk.CTkFrame(self.form_box, fg_color="transparent")
        btn_frame1.pack(pady=10 ,padx=(10,5),fill="x",expand=True)
        self.btn_ekle = ctk.CTkButton(btn_frame1 ,text="Ekle" ,command=self.car_controller.add_car)
        self.btn_ekle.pack(side="left" ,padx=5 ,pady=10)
        self.btn_guncelle = ctk.CTkButton(btn_frame1, text="Güncelle",command=self.car_controller.update_car)
        self.btn_guncelle.pack(side="left",padx=5 ,expand=True)
        self.btn_sil = ctk.CTkButton(btn_frame1 ,text="Sil" ,command=self.car_controller.delete_car ,fg_color="#D32F2F",hover_color="#B71C1C")
        self.btn_sil.pack(side="left" ,padx=5 ,expand=True)

        # Kiralama başlat ve iade et formu
        self.kiralama_box = ctk.CTkFrame(self.master ,corner_radius=10)
        self.kiralama_box.grid(row=1 ,column=2 ,padx=(5,10) ,pady=(10,10), sticky="nsew")
        ctk.CTkLabel(self.kiralama_box, text="Kiralama ve İade İşlemleri", font=ctk.CTkFont(size=14,weight="bold")).pack(pady=(10,5))

        self.kiralayan_input = self.input_olustur(self.kiralama_box, "Müşteri Adı:")
        self.baslangic_input = self.takvim_olustur(self.kiralama_box,"Başlangıç Tarihi:")
        self.bitis_input = self.takvim_olustur(self.kiralama_box,"Bitiş Tarihi:")

        btn_frame2 = ctk.CTkFrame(self.kiralama_box ,fg_color="transparent")
        btn_frame2.pack(pady=10, fill="x" ,padx=10)
        self.btn_kirala = ctk.CTkButton(btn_frame2 ,text="Kiralama Başlat" ,command=self.rental_controller.kirala)
        self.btn_kirala.pack(side="left" ,padx=5 ,expand=True)
        self.btn_iade = ctk.CTkButton(btn_frame2, text="Aracı İade Et", command=self.rental_controller.iade_et)
        self.btn_iade.pack(side="left", padx=5, expand=True)


    def takvim_olustur(self, parent, label_text):
        #takvim oluşturan metod
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=5, padx=10, fill="x")

        ctk.CTkLabel(frame, text=label_text, width=150, anchor="w").pack(side="left", padx=5)

        date_input = DateEntry(frame,date_pattern="dd-mm-yyyy",background="#4CAF86", foreground="white",borderwidth=2, width=18)
        date_input.pack(side="left", fill="x", expand=True, padx=5)
        return date_input

    def input_olustur(self,parent ,label_text):
        #input alanlarını oluşturan method
        frame = ctk.CTkFrame(parent ,fg_color="transparent")
        frame.pack(pady=5, padx=10, fill="x")

        ctk.CTkLabel(frame ,text=label_text,width=150 ,anchor="w").pack(side="left" ,padx=5)
        entry = ctk.CTkEntry(frame)
        entry.pack(side="left" , fill="x" , expand=True ,padx=5)
        return entry

    def istatistik_guncelle(self): 
        # Rapor ve genel durum 
        istatistik = self.master.system.istatistik_hesapla()
        toplam_gelir= self.master.system.toplam_gelir_hesapla()
        marka , sayi = self.master.system.en_cok_kiralanan_marka()
        istatistik_text =f"Toplam Araç: {istatistik['toplam_arac']}   Kirada: {istatistik['kirada_sayisi']}    Müsait: {istatistik['müsait_sayisi']}"
        self.istatistik_text.configure(text = istatistik_text )
    
        toplam = istatistik['toplam_arac']
        kirada = istatistik['kirada_sayisi']
    
        if toplam > 0:
            kirada_orani = kirada / toplam
            self.durum_cubuk.set(kirada_orani)
            if kirada > 0:
                self.durum_cubuk.configure(fg_color="#D32F2F") 
            else:
                self.durum_cubuk.configure(fg_color="#4CAF86")
        else:
            self.durum_cubuk.set(0)

        self.toplam_gelir.configure(text = f"Toplam Gelir: {toplam_gelir:,.0f} TL")
        self.en_cok_kiralanan.configure(text = f"En Çok Kiralanan: {marka} ({sayi} kez)")
    
    def araba_filtrele(self, secim):
        #arabaları filtereleme secimini küçük harfe çevirerek aracları_yukle metoduna gönderir
        if secim == "Tümü":
            filtre_secim ="Tümü"
        else:
            filtre_secim = secim.lower()
        self.araclari_yukle(filtre_secim)

    def araclari_yukle(self ,filter_secim="Tümü"):
        #aracları fitreler ve tabloya yükler
        for item in self.arac_tablo.get_children():
            self.arac_tablo.delete(item)

        araclar = self.master.system.araclari_filtrele(filter_secim)
        for arac in araclar:
            values = (arac.plaka.upper(), arac.marka.capitalize() , arac.model.capitalize(), f"{arac.ucret:.0f} TL",
                      arac.durum.capitalize(), arac.kiralayan.capitalize(),arac.baslangic_tarihi,arac.bitis_tarihi)
            if arac.durum == "kirada":
                tag = 'kirada'
            else :
                tag = 'müsait'
            self.arac_tablo.insert("", "end" ,values=values , tags=(tag,)) 

        self.arac_tablo.tag_configure('kirada',background="#ffcccc", foreground="#000000") 
        self.arac_tablo.tag_configure('müsait', background="#CCFFCC", foreground="#000000")
        self.istatistik_guncelle()
    
    def secimi_doldur(self,event):
        # secilen aracı forma doldurur
        secilen = self.arac_tablo.selection()
        if not secilen:
            return
        plaka = self.arac_tablo.item(secilen[0],'values')[0]
        arac = self.master.system.arac_bul(plaka)

        if arac :
            self.form_temizle(mode='arac_yonetim')
            self.form_temizle(mode='kiralama')
            self.plaka_input.insert(0,arac.plaka)
            self.marka_input.insert(0,arac.marka)
            self.model_input.insert(0,arac.model)
            self.ucret_input.insert(0,f"{arac.ucret:.0f}")

    def form_temizle(self,mode):
        # Tarih seçici temizleme eklendi
        if mode=='arac_yonetim':
            self.plaka_input.delete(0,tk.END)
            self.marka_input.delete(0,tk.END)
            self.model_input.delete(0,tk.END)
            self.ucret_input.delete(0,tk.END)
        elif mode == 'kiralama':
            self.kiralayan_input.delete(0,tk.END)
            self.baslangic_input.set_date(datetime.now())
            self.bitis_input.set_date(datetime.now())