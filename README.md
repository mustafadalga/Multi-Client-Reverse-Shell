```
___  ___      _ _   _  ______                               _____ _          _ _ 
|  \/  |     | | | (_) | ___ \                             /  ___| |        | | |
| .  . |_   _| | |_ _  | |_/ /_____   _____ _ __ ___  ___  \ `--.| |__   ___| | |
| |\/| | | | | | __| | |    // _ \ \ / / _ \ '__/ __|/ _ \  `--. \ '_ \ / _ \ | |
| |  | | |_| | | |_| | | |\ \  __/\ V /  __/ |  \__ \  __/ /\__/ / | | |  __/ | |
\_|  |_/\__,_|_|\__|_| \_| \_\___| \_/ \___|_|  |___/\___| \____/|_| |_|\___|_|_|
                                                                                 
                                                                                 
```

## Açıklama
**Hedef bilgisayarlardan gelen birden fazla bağlantıya izin veren çoklu istemcili reverse shell.**

<hr>


|   | Açıklama |
| ------------- |  ------------- | 
| :arrow_right:  | **setup.py** scripti ile **ReverseBackdoor** exe uzantısına çevrilerek kullanılabilir.  |
|:arrow_right: | **ReverseBackdoor.py** , exe uzantısına çevrildiğinde , sadece Windows işletim sistemi için çalışacak olan **persistent** metodu sayesinde **ReverseBackdoor**'un kalıcılığı sağlanır.  |
|:arrow_right: | Böylece her işletim sistemi oturumu başladığında **ReverseBackdoor** kendini bir Windows dosyası olarak gösterip çalışmaya başlar. |
|:arrow_right: | **ReverseBackdoor**'in çalıştığı hedef bilgisayar sürekli Hacker'a(**Listener**) bağlantı isteği gönderir.Hacker(**Listener**) aktif olduğu anda bağlantıyı kurar.Sonuç olarak Hacker(**Listener**) , hedef bilgisayara istediği zaman bağlanabilir veya aktif bağlantıyı koparabilir. |
| :arrow_right: | Hedef bilgisayarlardan bağlantı istekleri geldiğinde Hacker'a(**Listener**) bildirimler gelir. |
| :arrow_right: | Dosya indirme ve yükleme özellikleri ile hedef bilgisayardan dosya indirme ve yükleme işlemi gerçekleştirilebilir. |





### Kurulum
**ReverseShell ve Listener scriptlerini çalıştırabilmek için kurulacak modül**

* Linux için kurulum 

```
python3 -m pip install termcolor==1.1.0
```

* Windows için kurulum 

```
python -m pip install termcolor==1.1.0
```

**ReverseBackdoor.py'i exe uzantısına çevirmek için kullanılan setup.py'i kullanabilmek için kurulacak modül** 

* Linux için kurulum 

```
python3 -m pip install PyInstaller==3.4
```

* Windows için kurulum 

```
python -m pip install PyInstaller==3.4
```


### Kullanım
**Listener kullanımı** 

* Linux için kullanım 

```
python3 Listener.py
```

* Windows için kullanım 

```
 python Listener.py
```

**ReverseBackdoor.py'in script olarak kullanımı** 

* Linux için kullanım 
```
python3 ReverseBackdoor.py
```

* Windows için kullanım 

```
 python ReverseBackdoor.py
```


#### Kullanım komutları
* **help** : Uygulama kullanımı hakkında bilgi verir.
* **list** : Bağlantı sağlayan hedef bilgisayarları listeler.
* **select** : Bağlantı sağlayan bilgisayarları seçmek için kullanılır.Seçim işlemi listelenen bilgisayarların index numaralarına göre yapılır.
* **quit** : Üzerinde işlem yapılan aktif hedef bilgisayardan bağlantıyı durdurmak için kullanılır.
* **exit** : Serverin çalışmasını durdurur.Uygulamadan çıkış yapar.
* **upload** : Seçilen hedef makineye dosya yüklenmesini sağlar.Hedef bilgisayar seçildikten sonra bu komut çalışır.
* **download** : Seçilen hedef makineden dosya indirilmesini sağlar.Hedef bilgisayar seçildikten sonra bu komut çalışır.



#### Notlar
* Scriptler hem Linux hem de Windows işletim sistemlerinde çalışmaktadır.
* Python versiyonu:3.7.2
* setup scriptinde **cx_Freeze** modülünü kullanarak ReverseBackdoor'u exe'ye dönüştürmememin sebebi , persistent modülü ile kalıcılık sağlanmak için appdata klasörüne kopyalanan ReverseBackdoor'u çalışmamasıdır.Alternatif olarak **pyinstaller** modülü ile exe'ye dönüştürme işlemini gerçekleştirdim.
* **setup.py** dosyası , ReverseBackdoor'u exe uzantısına dönüştürürken subprocess  ile pyinstaller exe'ye dönüştürme komutu kullanılarak yapılmaktadır.pyinstaller modülünün çalışması içinde, pyinstall modülü yolunun Windows Path'lerin içerisine eklenmiş olması gerekmektedir.
* Daha fazla bilgi için aşağıdaki 2 linki inceleyebilirsiniz:  
    1-)[Add Python to the Windows Path](https://geek-university.com/python/add-python-to-the-windows-path)  
    2-)[How to add to the PYTHONPATH in Windows, so it finds my modules/packages?](https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-so-it-finds-my-modules-packages)





### (Hacker) Listener Görüntüleri - Kali linux işletim sistemi üzerinde
![3](https://user-images.githubusercontent.com/25087769/60386240-4503dc00-9a9b-11e9-86ea-c3d38383258f.PNG)


![4](https://user-images.githubusercontent.com/25087769/60386243-47663600-9a9b-11e9-8e18-08425c18e4bf.PNG)


![5](https://user-images.githubusercontent.com/25087769/60386386-e0498100-9a9c-11e9-82e1-60547c5c5350.PNG)




