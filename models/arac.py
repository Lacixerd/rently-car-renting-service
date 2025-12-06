import json
from datetime import datetime

class Arac:
    # her araç bir obje olarak tanımlanıyor
    def __init__(self, plaka, marka, model, ucret, durum="müsait", kiralayan="", baslangic_tarihi="", bitis_tarihi=""):
        # constructor method
        self.plaka = plaka.upper()
        self.marka = marka
        self.model = model
        try:
            self.ucret = float(ucret) 
        except ValueError:
            self.ucret = 0.0 
            
        self.durum = durum
        self.kiralayan = kiralayan
        self.baslangic_tarihi = baslangic_tarihi
        self.bitis_tarihi = bitis_tarihi

    def to_dict(self):
        # json dosyasına kaydederken ve diğer işlemlerde kullanırken kolaylık olsun diye **kwargs hale getiriyoruz
        return {
            "plaka": self.plaka,
            "marka": self.marka,
            "model": self.model,
            "ucret": self.ucret,
            "durum": self.durum,
            "kiralayan": self.kiralayan,
            "baslangic_tarihi": self.baslangic_tarihi,
            "bitis_tarihi": self.bitis_tarihi
        }

    def ucret_hesapla(self, gun_sayisi):
        # burada ücreti hesaplayıp döndürüyoruz
        return gun_sayisi * self.ucret