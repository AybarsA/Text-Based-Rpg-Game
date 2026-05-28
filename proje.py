import random
import time
import json

# -----Başlangıç Statlar--------------------------------------------------- 
karakter = {"can": 100, "max can": 100, "altın": 200}
canta = []
kullanilan = {"silah": None, "zirh": None}

items = {
    "Hançer": {"tur": "silah", "fiyat": 50, "mindmg": 8, "maxdmg": 12},
    "Demir Kılıç": {"tur": "silah", "fiyat": 200, "mindmg": 14, "maxdmg": 38},
    "Demir Gürz": {"tur": "silah", "fiyat": 200, "mindmg": 24, "maxdmg": 28},
    "Dragon Slayer": {"tur": "silah", "fiyat": 500, "mindmg": 50, "maxdmg": 90},

    "Deri Ceket": {"tur": "zirh", "fiyat": 100, "koruma": 20, "maxhp": 20},
    "Metal Zırh": {"tur": "zirh", "fiyat": 200, "koruma": 45, "maxhp": 50},
    "Büyülü Zırh": {"tur": "zirh", "fiyat": 400, "koruma": 90, "maxhp": 100},

    "Can İksiri": {"tur": "tuketilebilir", "fiyat": 40, "heal": 40},
    "Büyük Can İksiri": {"tur": "tuketilebilir", "fiyat": 80, "heal": 100}
}

zirhlar = ["Deri Ceket", "Metal Zırh", "Büyülü Zırh"]
silahlar = ["Hançer", "Demir Kılıç", "Demir Gürz", "Dragon Slayer"]

#-----Kaydetme--------------------------------------------------- 
def kaydet(karaktersozluk, cantaliste, kullanilanlarsozluk):
    kayit_verisi = {
        "karakter": karaktersozluk,
        "canta": cantaliste,
        "kullanilan": kullanilanlarsozluk
    }
    
    with open("kayit.json", "w", encoding="utf-8") as dosya:
        json.dump(kayit_verisi, dosya, ensure_ascii=False, indent=4)
        
    print("\n---Oyun başarıyla kaydedildi!---")

def yukle():
    try:
        with open("kayit.json", "r", encoding="utf-8") as dosya:
            kayit_verisi = json.load(dosya)
            
        print("\n***Kayıtlı oyun başarıyla yüklendi!***") 
        return kayit_verisi["karakter"], kayit_verisi["canta"], kayit_verisi["kullanilan"]
        
    except FileNotFoundError:
        print("\n[!] Kayıt dosyası bulunamadı! Daha önce oyunu kaydetmemiş olabilirsin.")
        return None, None, None

#-----Savaş Fonksiyonları---------------------------------------------------
def dmg(kullanilanlarsozluk):
    vurulanhasar = random.randint(18, 22)
    aktifsilah = kullanilanlarsozluk["silah"]
    
    if aktifsilah != None:
        min_dmg = items[aktifsilah]["mindmg"]
        max_dmg = items[aktifsilah]["maxdmg"]
        vurulanhasar += random.randint(min_dmg, max_dmg)
    return vurulanhasar

def dmgtkn(kullanilanlarsozluk):
    alinanhasar = random.randint(28, 36)
    aktifzirh = kullanilanlarsozluk["zirh"]
    
    if aktifzirh != None:
        alinanhasar -= items[aktifzirh]["koruma"]
        
    if alinanhasar < 0:
        alinanhasar = 0
    return alinanhasar

def iksir_ic(karaktersozluk, cantaliste):
    print("\n1- Can İksiri\n2- Büyük Can İksiri\n3- Çıkış")
    
    try:
        secim = int(input("Seçiminiz: "))
    except ValueError:
        print("[!] Sadece sayı giriniz!")
        return False
        
    if secim == 1:
        if "Can İksiri" in cantaliste:
            cantaliste.remove("Can İksiri")
            karaktersozluk["can"] += items["Can İksiri"]["heal"]
            
            if karaktersozluk["can"] > karaktersozluk["max can"]:
                karaktersozluk["can"] = karaktersozluk["max can"]
                
            print("[+] Can İksiri içtin! Canın yenilendi.")
            return True
        else:
            print("[!] Çantanda Can İksiri yok!")
            return False
        
    elif secim == 2:
        if "Büyük Can İksiri" in cantaliste:
            cantaliste.remove("Büyük Can İksiri")
            karaktersozluk["can"] += items["Büyük Can İksiri"]["heal"]
            
            if karaktersozluk["can"] > karaktersozluk["max can"]:
                karaktersozluk["can"] = karaktersozluk["max can"]
                
            print("[+] Büyük Can İksiri içtin! Canın yenilendi.")
            return True
        else:
            print("[!] Çantanda Büyük Can İksiri yok!")
            return False
            
    elif secim == 3:
        return False
    else:
        print("Yanlış bir tuşa bastın.")
        return False

def kac(karaktersozluk):
    print("Canını zar zor kurtarmaya çalışıyorsun...")
    time.sleep(2) # Bekleme süresini oynanış akıcılığı için 2'ye düşürdüm
    kacma = random.randint(1, 10)
    if kacma in [3, 9, 7]:
        a = random.randint(10, 25)   
        karaktersozluk["can"] -= a
        print("Kaçarken", a, "hasar yedin!")
    else:
        print("Başarıyla kaçtın...")

def sorgu(dusman):
    if dusman > 0:
        return True
    else:
        return False

#-----Combat fonksiyonu---------------------------------------------------
def Combat(karaktersozluk, cantaliste, kullanilanlarsozluk):
    print("\n*** SAVAŞ BAŞLADI ***")
    dusmancani = random.randint(60, 100)

    while karaktersozluk["can"] > 0 and dusmancani > 0:
        print(f"\nCan = {karaktersozluk['can']} ***** Düşman Canı = {dusmancani}")
        
        try:
            savas = int(input("1- Saldır\n2- Savunarak Saldır\n3- İksirler\n4- Kaç\nSeçim: "))
        except ValueError:
            print("Lütfen bir sayı girin!")
            continue
            
        if savas == 1:
            damage = dmg(kullanilanlarsozluk)
            dusmancani -= damage
            print(f"-> {damage} HASAR VERDİN!\n----------------")
            if sorgu(dusmancani) == False:
                break
            damagetaken = dmgtkn(kullanilanlarsozluk)
            karaktersozluk["can"] -= damagetaken 
            print(f"<- {damagetaken} HASAR ALDIN!")

        elif savas == 2:
            damage = dmg(kullanilanlarsozluk) // 2
            print(f"-> (Savunma) {damage} HASAR VERDİN!\n----------------")
            dusmancani -= damage
            if sorgu(dusmancani) == False:
                break
            damagetaken = dmgtkn(kullanilanlarsozluk) // 2
            karaktersozluk["can"] -= damagetaken
            print(f"<- (Savunma) {damagetaken} HASAR ALDIN!")

        elif savas == 3:
            iksir = iksir_ic(karaktersozluk, cantaliste)
            if iksir == True:
                damagetaken = dmgtkn(kullanilanlarsozluk)
                karaktersozluk["can"] -= damagetaken
                print(f"<- Sen iksir içerken {damagetaken} HASAR ALDIN!")

        elif savas == 4:
            kac(karaktersozluk)
            break

    if karaktersozluk["can"] > 0 and dusmancani <= 0:
        kazanilanaltin = random.randint(30, 60)
        karaktersozluk["altın"] += kazanilanaltin
        print(f"\nTEBRİKLER! Düşmanı yendin ve {kazanilanaltin} Altın kazandın!")
    elif karaktersozluk["can"] <= 0:
        print("\n                      ---- ÖLDÜN ----\n")

#-----Ejderha Fonksiyonu---------------------------------------------------
def dungeon(karaktersozluk, cantaliste, kullanilanlarsozluk):
    print("\n" + "="*40)
    print("!!! KADİM EJDERHA UYANDI !!!")
    print("Kadim Ejderha ininden çıkıyor!")
    print("="*40)
    time.sleep(2)

    dusmancani = 250 

    while karaktersozluk["can"] > 0 and dusmancani > 0:
        print(f"\nCan = {karaktersozluk['can']}  ||  *** EJDERHA CANI = {dusmancani} ***")
        try:
            savas = int(input("1- Saldır\n2- Savunarak Saldır\n3- İksirler\n4- Kaç (Çok Zor!)\nSeçiminiz: "))
        except ValueError:
            continue
            
        if savas == 1:
            damage = dmg(kullanilanlarsozluk)
            dusmancani -= damage
            print(f"-> Kılıcını savurdun! Ejderhaya {damage} HASAR VERDİN!\n----------------")
            if not sorgu(dusmancani): break
                
            damagetaken = random.randint(40, 60)
            if kullanilanlarsozluk["zirh"] != None:
                damagetaken -= items[kullanilanlarsozluk["zirh"]]["koruma"]
            if damagetaken < 0: damagetaken = 0
            karaktersozluk["can"] -= damagetaken 
            print(f"<- EJDERHA ALEV PÜSKÜRTTÜ! {damagetaken} HASAR ALDIN!")

        elif savas == 2:
            damage = dmg(kullanilanlarsozluk) // 2
            dusmancani -= damage
            print(f"-> (Savunma) Ejderhaya {damage} HASAR VERDİN!\n----------------")
            if not sorgu(dusmancani): break
                
            damagetaken = random.randint(40, 60) // 2
            if kullanilanlarsozluk["zirh"] != None:
                damagetaken -= items[kullanilanlarsozluk["zirh"]]["koruma"]
            if damagetaken < 0: damagetaken = 0
            karaktersozluk["can"] -= damagetaken
            print(f"<- (Savunma) Ejderha pençe attı! {damagetaken} HASAR ALDIN!")

        elif savas == 3:
            iksir = iksir_ic(karaktersozluk, cantaliste)
            if iksir:
                damagetaken = random.randint(40, 60)
                if kullanilanlarsozluk["zirh"] != None:
                    damagetaken -= items[kullanilanlarsozluk["zirh"]]["koruma"]
                if damagetaken < 0: damagetaken = 0
                karaktersozluk["can"] -= damagetaken
                print(f"<- Sen iksir içerken Ejderha fırsat bildi! {damagetaken} HASAR ALDIN!")

        elif savas == 4:
            print("Ejderhadan kaçmak neredeyse imkansızdır...")
            time.sleep(2)
            kacma = random.randint(1, 10)
            if kacma == 5: 
                print("Mucize eseri ejderhanın alevlerinden kaçıp mağaradan çıktın!")
                return 
            else:
                damagetaken = random.randint(30, 50)
                karaktersozluk["can"] -= damagetaken
                print(f"Kaçamadın! Ejderha kuyruğuyla vurdu, {damagetaken} hasar yedin!")

    if karaktersozluk["can"] > 0 and dusmancani <= 0:
        kazanilanaltin = 500 
        karaktersozluk["altın"] += kazanilanaltin
        print("\n" + "*"*30)
        print("İNANILMAZ! KADİM EJDERHAYI KATLETTİN!")
        print(f"Ejderhanın inindeki {kazanilanaltin} Altını ele geçirdin!")
        print("*"*30 + "\n")
    elif karaktersozluk["can"] <= 0:
        print("\n         ---- KÜLE DÖNÜŞTÜN ----\n")

#-----Market ve Taverna Fonksiyonları---------------------------------------------------
def demirci(karaktersozluk, cantaliste, kullanilanlarsozluk):
    print("\n--- Demirciye Hoşgeldin ---")
    print("Satılan Silahlar:", silahlar)

    while True:
        secim = input("Ne almak istersin? (Çıkmak için 'q'): \n")

        if secim == "q":
            print("Demirciden Çıkıyorsun...")
            time.sleep(1)
            break    
        
        elif secim in items and items[secim]["tur"] == "silah":
            if secim in cantaliste or secim == kullanilanlarsozluk["silah"]:
                print(f"Zaten bir {secim} sahibisin! Aynısından almaya gerek yok...")
            elif karaktersozluk["altın"] >= items[secim]["fiyat"]:
                 karaktersozluk["altın"] -= items[secim]["fiyat"]
                 cantaliste.append(secim)
                 print(f"{secim} satın alındı! Kalan altın: {karaktersozluk['altın']}")
            else:
                print("Yeterli altının yok!")
        else:
            print("Böyle Bir Ürün Bulunmuyor veya Demircide Satılmıyor!\n")

def zirhci(karaktersozluk, cantaliste, kullanilanlarsozluk):
    print("\n--- Zırh Tüccarına Hoşgeldin ---")
    print("Satılan Zırhlar:", zirhlar)

    while True:
        secim = input("Ne almak istersin? (Çıkmak için 'q'): \n")

        if secim == "q":
            print("Zırh Tüccarından Çıkıyorsun...")
            time.sleep(1)
            break    
        
        elif secim in items and items[secim]["tur"] == "zirh":
            if secim in cantaliste or secim == kullanilanlarsozluk["zirh"]:
                print(f"Zaten bir {secim} sahibisin! Aynısından almaya gerek yok...")
            elif karaktersozluk["altın"] >= items[secim]["fiyat"]:
                 karaktersozluk["altın"] -= items[secim]["fiyat"]
                 cantaliste.append(secim)
                 print(f"{secim} satın alındı! Kalan altın: {karaktersozluk['altın']}")
            else:
                print("Yeterli altının yok!")
        else:
            print("Böyle Bir Ürün Bulunmuyor veya Zırhçıda Satılmıyor!\n")

def taverna(karaktersozluk, cantaliste):
    print("\n--- Tavernaya Hoşgeldin ---")
    while True:
        print(f"\nMevcut Can: {karaktersozluk['can']} | Max Can: {karaktersozluk['max can']} | Altın: {karaktersozluk['altın']}")
        print("1- Can İksiri Satın Al (40 Altın)")
        print("2- Büyük Can İksiri Satın Al (80 Altın)")
        print("3- Yemek Ye (+60 Can | 20 Altın)")
        print("4- Handa Uyu (Canı Fuller | 40 Altın)")
        print("5- Tavernadan Çık")
        
        try:
            secim = int(input("Seçiminiz: "))
        except ValueError:
            continue
            
        if secim == 1:
            if karaktersozluk["altın"] >= items["Can İksiri"]["fiyat"]:
                karaktersozluk["altın"] -= items["Can İksiri"]["fiyat"]
                cantaliste.append("Can İksiri")
                print("Çantana Can İksiri eklendi!")
            else:
                print("Yeterli altının yok!")
        elif secim == 2:
            if karaktersozluk["altın"] >= items["Büyük Can İksiri"]["fiyat"]:
                karaktersozluk["altın"] -= items["Büyük Can İksiri"]["fiyat"]
                cantaliste.append("Büyük Can İksiri")
                print("Çantana Büyük Can İksiri eklendi!")
            else:
                print("Yeterli altının yok!")
        elif secim == 3:
            if karaktersozluk["altın"] >= 20:
                karaktersozluk["altın"] -= 20
                karaktersozluk["can"] += 60
                if karaktersozluk["can"] > karaktersozluk["max can"]:
                    karaktersozluk["can"] = karaktersozluk["max can"]
                print(f"Yemek yedin! Güncel Can: {karaktersozluk['can']}")
            else:
                print("Yeterli altının yok!")
        elif secim == 4:
            if karaktersozluk["altın"] >= 40:
                karaktersozluk["altın"] -= 40
                karaktersozluk["can"] = karaktersozluk["max can"]
                print("Uyudun ve dinlendin! Canın Fullendi.")
            else:
                print("Yeterli altının yok!")
        elif secim == 5:
            print("Tavernadan çıkılıyor...")
            time.sleep(1)
            break

#-----Menü Seçenekleri---------------------------------------------------
def odulavi(karaktersozluk, cantaliste, kullanilanlarsozluk):
    print("\n-----------------\nÖdül avına çıkıyorsun...")
    time.sleep(1)
    print("Ödülü görüyorsun!")
    time.sleep(1)
    Combat(karaktersozluk, cantaliste, kullanilanlarsozluk)

def kasaba(karaktersozluk, cantaliste, kullanilanlarsozluk):
    while True:
        try:
            town = int(input("\n--- KASABA MENUSU ---\n1- Tavernaya Git\n2- Demirciye Git\n3- Zırh Tüccarına Git\n4- Geri Dön\nSeçiminiz: "))
        except ValueError:
            continue
            
        if town == 1:
            taverna(karaktersozluk, cantaliste)
        elif town == 2:
            demirci(karaktersozluk, cantaliste, kullanilanlarsozluk)
        elif town == 3:
            zirhci(karaktersozluk, cantaliste, kullanilanlarsozluk)
        elif town == 4:
            break

def envanter(karaktersozluk, cantaliste, kullanilanlarsozluk):
    while True: 
        print("\nÇanta:", cantaliste)
        print("Kuşanılan Ekipman:", kullanilanlarsozluk)
        print("Durum:", karaktersozluk)
        
        secim = input("\nKullanmak İstediğin Eşyayı Yaz (Çıkış için 'q'): ")
        
        if secim == "q":
            break

        elif secim in cantaliste:
            tur = items[secim]["tur"]
            
            if tur == "silah":
                silah = kullanilanlarsozluk["silah"]
                if silah != None:
                    cantaliste.append(silah)
                    
                kullanilanlarsozluk["silah"] = secim
                cantaliste.remove(secim)
                print(f"\n{secim} kuşandın!")

            elif tur == "zirh":
                zirh = kullanilanlarsozluk["zirh"]
                
                if zirh != None:
                    cantaliste.append(zirh) 
                    
                    eski_bonus = items[zirh]["maxhp"]
                    karaktersozluk["max can"] -= eski_bonus
                    karaktersozluk["can"] -= eski_bonus
                
                    if karaktersozluk["can"] < 1:
                        karaktersozluk["can"] = 1
                        
                    if karaktersozluk["can"] > karaktersozluk["max can"]:
                        karaktersozluk["can"] = karaktersozluk["max can"]

                kullanilanlarsozluk["zirh"] = secim
                cantaliste.remove(secim)
                
                yeni_bonus = items[secim]["maxhp"]
                karaktersozluk["max can"] += yeni_bonus
                karaktersozluk["can"] += yeni_bonus 
                print(f"\n{secim} giydin!")
                
            elif tur == "tuketilebilir":
                print("\n[!] İksirleri savaşta kullanmalısın, buradan sadece ekipman kuşanabilirsin.")
        else:
            print("\nEnvanterde Böyle Bir Eşya Yok!")

#-----Main Fonksiyon---------------------------------------------------
print("      --- EN İYİ OYUN ---\n")

while True:
    try:
        anamenu = int(input("\n1- Yeni Oyuna Başla\n2- Kayıtlı Oyuna Devam Et\n3- Oyundan Çık\nSeçiminiz: "))
    except ValueError:
        print("Lütfen bir sayı girin!")
        continue
        
    oyun_aktif = False

    if anamenu == 1:
        karakter = {"can": 100, "max can": 100, "altın": 200}
        canta = []
        kullanilan = {"silah": None, "zirh": None}
        oyun_aktif = True
        
    elif anamenu == 2:
        geciciKarakter, geciciCanta, geciciKullanilan = yukle()
        
        if geciciKarakter != None:
            karakter = geciciKarakter
            canta = geciciCanta
            kullanilan = geciciKullanilan
            oyun_aktif = True
        else:
            continue 
            
    elif anamenu == 3:
        break
        
    if oyun_aktif:
        while True:
            if karakter["can"] <= 0:
                print("Maceran burada sona erdi...")
                break
                
            try:
                menu = int(input("\n--- ANA MENÜ ---\n1- Ödül Avına Çık\n2- Kasabada Gezin\n3- Envanterine ve Bilgilere Bak\n4- Oyunu Kaydet\n5- Ejderha Avı!\n6- Ana Menüye Dön\nSeçiminiz: "))      
            except ValueError:
                continue
                
            if menu == 1:
                odulavi(karakter, canta, kullanilan)
            elif menu == 2: 
                kasaba(karakter, canta, kullanilan)
            elif menu == 3:
                envanter(karakter, canta, kullanilan)
            elif menu == 4:
                kaydet(karakter, canta, kullanilan)
            elif menu == 5:
                dungeon(karakter, canta, kullanilan)
            elif menu == 6:
                break



























































































  


