from .data_manager import DataManager
from .arac import Arac
from datetime import datetime
from services.validation_service import ValidationService

class RentalSystem:
    def __init__(self):
        self.manager = DataManager()
        self.araclar = self.manager.araclar
        self.kiralama_gecmisi = self.manager.kiralama_gecmisi

    def arac_bul(self, plaka):
        return next((a for a in self.araclar if a.plaka == plaka.upper()), None)
    
    def arac_ekle(self, plaka, marka, model, ucret):

        valid, mesaj = ValidationService.validate_plaka(plaka)
        if not valid:
            return False, f"Hata: {mesaj}"
        
        if self.arac_bul(plaka):
            return False, "Hata: Bu plaka zaten sistemde kayıtlı."
        
        valid_ucret, return_value = ValidationService.validate_ucret(ucret)
        if not valid_ucret:
            return False, f"Hata: {return_value}"
        
        ucret = return_value
        yeni_arac = Arac(plaka, marka, model, ucret)
        self.araclar.append(yeni_arac)
        return True, "Araç başarıyla eklendi."

    def arac_sil(self, plaka):
        arac = self.arac_bul(plaka)
        if not arac:
            return False, "Hata: Silinecek araç bulunamadı."
        
        if arac.durum == "kirada":
            return False, "Hata: Kirada olan bir araç silinemez!"

        self.araclar.remove(arac)
        return True, "Araç başarıyla sistemden kaldırıldı."
    
    def arac_guncelle(self, plaka, marka, model, ucret):
        arac = self.arac_bul(plaka)
        if not arac:
            return False, "Hata: Güncellenecek araç bulunamadı."
        
        valid_ucret, return_value = ValidationService.validate_ucret(ucret)
        if not valid_ucret:
            return False, f"Hata: {return_value}"

        arac.marka = marka
        arac.model = model
        arac.ucret = return_value
        return True, f"{plaka} plakalı araç başarıyla güncellendi."
    

    # ------------- kiralama işlemleri ------------------
    
    def kiralama_baslat(self, plaka, kiralayan, baslangic_str, bitis_str):
        arac = self.arac_bul(plaka)
        if not arac:
            return False, "Hata: Araç bulunamadı."
        if arac.durum != "müsait":
            return False, f"Hata: Araç şu anda '{arac.durum}' durumunda."

        valid_musteri_adi, mesaj = ValidationService.validate_musteri_adi(kiralayan)
        if not valid_musteri_adi:
            return False, f"Hata: {mesaj}"

        valid_tarih_araligi, mesaj, baslangic, bitis = ValidationService.validate_tarih_araligi(baslangic_str, bitis_str)
        if not valid_tarih_araligi:
            return False, f"Hata: {mesaj}"

        gun_farki = (bitis - baslangic).days
        toplam_ucret = arac.ucret_hesapla(gun_farki)
        
        arac.durum = "kirada"
        arac.kiralayan = kiralayan
        arac.baslangic_tarihi = baslangic_str
        arac.bitis_tarihi = bitis_str
        
        mesaj = f"Kiralama başarıyla tamamlandı.\nToplam Ücret: {toplam_ucret:.2f} TL ({gun_farki} gün)"
        return True, mesaj

    def arac_iade_et(self, plaka):
        arac = self.arac_bul(plaka)
        if not arac:
            return False, "Hata: İade edilecek araç bulunamadı."
        if arac.durum != "kirada":
            return False, f"Hata: Araç kirada değil, durumu '{arac.durum}'."
        
        try:
            baslangic = datetime.strptime(arac.baslangic_tarihi, '%d-%m-%Y')
            bitis = datetime.strptime(arac.bitis_tarihi, '%d-%m-%Y')
            gun_farki = (bitis - baslangic).days
            
            toplam_ucret = arac.ucret_hesapla(gun_farki) 
            iade_tarihi = datetime.now().strftime('%d-%m-%Y')
        except ValueError:
             return False, "Hata: Kayıtlı tarih formatında sorun var."

        gecmis_kaydi = {
            "plaka": arac.plaka,
            "marka": arac.marka,
            "model": arac.model,
            "ucret": arac.ucret,
            "kiralayan": arac.kiralayan,
            "baslangic_tarihi": arac.baslangic_tarihi,
            "bitis_tarihi": arac.bitis_tarihi,
            "toplam_ucret": toplam_ucret,
            "iade_tarihi": iade_tarihi
        }
        self.kiralama_gecmisi.append(gecmis_kaydi)
        self.manager.gecmisi_kaydet(self.kiralama_gecmisi) 

        arac.durum = "müsait"
        arac.kiralayan = ""
        arac.baslangic_tarihi = ""
        arac.bitis_tarihi = ""
        
        return True, f"Araç başarıyla iade edildi. Toplam Ücret: {toplam_ucret:.2f} TL"
    
    # ------------- istatistikler ------------------

    def toplam_gelir_hesapla(self):
        toplam_gelir = sum(kayit.get('toplam_ucret', 0) for kayit in self.kiralama_gecmisi)
        return toplam_gelir

    def en_cok_kiralanan_marka(self):
        marka_sayilari = {}
        for kayit in self.kiralama_gecmisi:
            marka = kayit.get('marka')
            if marka:
                marka_sayilari[marka] = marka_sayilari.get(marka, 0) + 1
        
        if not marka_sayilari:
            return "Kayıt Yok", 0

        en_cok_kiralanan = max(marka_sayilari, key=marka_sayilari.get)
        return en_cok_kiralanan, marka_sayilari[en_cok_kiralanan]

    def istatistik_hesapla(self):
        kirada_olanlar = [a for a in self.araclar if a.durum == "kirada"]
        return {
            "toplam_arac": len(self.araclar),
            "kirada_sayisi": len(kirada_olanlar),
            "müsait_sayisi": len(self.araclar) - len(kirada_olanlar),
        }
    
    def araclari_filtrele(self, durum_filtresi="Tümü"):
        if durum_filtresi == "Tümü":
            return self.araclar
        
        return [arac for arac in self.araclar if arac.durum == durum_filtresi]

    def verileri_kaydet(self):
        return self.manager.verileri_kaydet()