import json
from .arac import Arac

class DataManager:
    # her data manager bir obje olarak tanımlanıyor nedeni de her bir datamanager dosya
    # işlemlerini kendi içerisinde yapıyor başka yerler doğrudan dosya işlemleri yapılmıyor
    # yani encapsulation yapıyoruz
    def __init__(self, dosya_adi="./cars.json", gecmis_dosya_adi="./rental_history.json"):
        self.dosya_adi = dosya_adi
        self.gecmis_dosya_adi = gecmis_dosya_adi
        self.araclar = [] 
        self.kiralama_gecmisi = []
        
        self._verileri_yukle()
        self._gecmisi_yukle()

    def _verileri_yukle(self):
        # cars.json dosyasını okuyoruz ve araçları dict olacak şekilde arac_listesi'ne yerleştiriyoruz
        # ve en sonunda da datamanager nesnesinin içerisindeki araçlar listesine kaydediyoruz
        arac_listesi = []
        try:
            with open(self.dosya_adi, mode='r', newline='', encoding='utf-8') as json_file:
                json_data = json.load(json_file)
                for item in json_data:
                    arac_listesi.append(Arac(item["plaka"], item["marka"], item["model"], item["ucret"], item["durum"], item["kiralayan"], item["baslangic_tarihi"], item["bitis_tarihi"]))
            
            self.araclar = arac_listesi
            
        except FileNotFoundError:
            print(f"Uyarı: {self.dosya_adi} dosyası bulunamadı. Yeni boş dosya oluşturuluyor.")
            self.verileri_kaydet()
        except Exception as e:
            print(f"Hata: {self.dosya_adi} okuma hatası: {e}. Boş liste ile başlatılıyor.")

    def _gecmisi_yukle(self):
        # rental_history.json dosyasını okuyoruz ve kiralama geçmişini dict olacak şekilde gecmis_listesi'ne
        # yerleştiriyoruzve en sonunda da datamanager nesnesinin içerisindeki kiralama geçmişi listesine kaydediyoruz
        gecmis_listesi = []
        try:
            with open(self.gecmis_dosya_adi, mode='r', encoding='utf-8') as f:
                reader = json.load(f)
                for item in reader:
                    gecmis_listesi.append(item)
            
            self.kiralama_gecmisi = gecmis_listesi
            
        except FileNotFoundError:
            print(f"Uyarı: {self.gecmis_dosya_adi} bulunamadı. Boş geçmiş dosyası oluşturuluyor.")
            self.gecmisi_kaydet([])
            
        except Exception as e:
            print(f"Hata: Geçmiş okuma hatası: {e}.")

    def verileri_kaydet(self):
        # araçları dosyaya kaydeder
        try:
            with open(self.dosya_adi, mode='w', encoding='utf-8') as f:
                json.dump([arac.to_dict() for arac in self.araclar], f, indent=4)
            return True
        except Exception as e:
            print(f"Araçları kaydetme hatası: {e}.")
            return False
            
    def gecmisi_kaydet(self, gecmis_listesi):
        # kiralama geçmişini dosyaya kaydeder
        try:
            with open(self.gecmis_dosya_adi, mode='w', encoding='utf-8') as f:
                json.dump(gecmis_listesi, f, indent=4)
            return True
        except Exception as e:
            print(f"Geçmiş kaydetme hatası: {e}")
            return False