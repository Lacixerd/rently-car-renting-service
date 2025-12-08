from datetime import datetime

class ValidationService:
    # bu classda static methodlar kullanıyoruz çünkü bu metodlar bi nesneye bağlı
    # değil yani nesne oluşturmadan direkt çağırabiliriz
    # class şeklinde oluşturmamızın nedeni ise hepsi validation işlemi olduğu için
    # daha organize bir yapı sağlıyor
    @staticmethod
    def validate_plaka(plaka):
        if not plaka or not plaka.strip():
            return False, "Plaka boş olamaz."
        
        if len(plaka.strip()) < 5:
            return False, "Plaka en az 5 karakter olmalıdır."
        
        return True, ""
    
    @staticmethod
    def validate_ucret(ucret):
        try:
            ucret_float = float(ucret)
            if ucret_float <= 0:
                return False, "Günlük ücret 0'dan büyük olmalıdır."
            return True, ucret_float
        except ValueError:
            return False, "Günlük ücret sayısal bir değer olmalıdır."
    
    @staticmethod
    def validate_tarih_araligi(baslangic_str, bitis_str):
        try:
            baslangic = datetime.strptime(baslangic_str, '%d-%m-%Y')
            bitis = datetime.strptime(bitis_str, '%d-%m-%Y')
            
            if bitis <= baslangic:
                return False, "Bitiş tarihi, başlangıç tarihinden sonra olmalıdır.", None, None
            
            return True, "", baslangic, bitis
            
        except ValueError:
            return False, "Tarih formatı DD-MM-YYYY olmalıdır.", None, None
    
    @staticmethod
    def validate_musteri_adi(ad):
        if not ad or not ad.strip():
            return False, "Müşteri adı boş olamaz."
        
        if len(ad.strip()) < 2:
            return False, "Müşteri adı en az 2 karakter olmalıdır."
        
        return True, ""