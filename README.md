```
___  ___      _ _   _  ______                               _____ _          _ _ 
|  \/  |     | | | (_) | ___ \                             /  ___| |        | | |
| .  . |_   _| | |_ _  | |_/ /_____   _____ _ __ ___  ___  \ `--.| |__   ___| | |
| |\/| | | | | | __| | |    // _ \ \ / / _ \ '__/ __|/ _ \  `--. \ '_ \ / _ \ | |
| |  | | |_| | | |_| | | |\ \  __/\ V /  __/ |  \__ \  __/ /\__/ / | | |  __/ | |
\_|  |_/\__,_|_|\__|_| \_| \_\___| \_/ \___|_|  |___/\___| \____/|_| |_|\___|_|_|
                                                                                 
                                                                                 
```

## Description
**A multi-client reverse shell allowing multiple connections from target computers.**

<hr>


| | Description |
| ------------- | ------------- |
| :arrow_right: | Can be used by converting the **ReverseBackdoor** script to an exe extension using the **setup.py** script. |
| :arrow_right: | When **ReverseBackdoor.py** is converted to an exe, the persistence of **ReverseBackdoor** is ensured for Windows operating system only, thanks to the **persistent** method. |
| :arrow_right: | Thus, every time an operating system session starts, **ReverseBackdoor** disguises itself as a Windows file and begins to run. |
| :arrow_right: | The target computer where **ReverseBackdoor** is running continuously sends connection requests to the Hacker (**Listener**). The Hacker (**Listener**) establishes the connection as soon as it becomes active. As a result, the Hacker (**Listener**) can connect to the target computer at any time or disconnect the active connection. |
| :arrow_right: | Notifications are sent to the Hacker (**Listener**) when connection requests come from target computers. |
| :arrow_right: | File download and upload features allow for downloading and uploading files from/to the target computer. |




### Installation
**Module to install to run ReverseShell and Listener scripts**

* For Linux installation

```
python3 -m pip install termcolor==1.1.0
```

* For Windows installation

```
python -m pip install termcolor==1.1.0
```

**Module to install to use setup.py to convert ReverseBackdoor.py to exe extension**

* For Linux installation

```
python3 -m pip install PyInstaller==3.4
```

* For Windows installation

```
python -m pip install PyInstaller==3.4
```


### Usage
**Listener usage**

* For Linux usage

```
python3 Listener.py
```

* For Windows usage

```
 python Listener.py
```

**ReverseBackdoor.py script usage**

* For Linux usage
```
python3 ReverseBackdoor.py
```

* For Windows usage

```
 python ReverseBackdoor.py
```


#### Usage Commands

| | Usage Commands |
| ------------- | ------------- |
| **help** | Provides information about application usage. |
| **list** | Lists connected target computers. |
| **select** | Used to select connected computers. Selection is made according to the index numbers of the listed computers. |
| **quit** | Used to stop the connection from the active target computer being operated on. |
| **exit** | Stops the server from running. Exits the application. |
| **upload** | Enables uploading files to the selected target machine. This command runs after the target computer is selected. |
| **download** | Enables downloading files from the selected target machine. This command runs after the target computer is selected. |


#### Notes
* The scripts work on both Linux and Windows operating systems.
* Python version: 3.7.2
* The reason I did not convert ReverseBackdoor to exe using the **cx_Freeze** module in the setup script is that the ReverseBackdoor copied to the appdata folder for persistence with the persistent module does not run. Alternatively, I performed the conversion to exe with the **pyinstaller** module.
* The **setup.py** file converts ReverseBackdoor to an exe extension by using the pyinstaller exe conversion command with subprocess. For the pyinstaller module to work, the path to the pyinstaller module must be added to the Windows Paths.
* For more information, you can check the following 2 links:
    - [Add Python to the Windows Path](https://geek-university.com/python/add-python-to-the-windows-path)
    - [How to add to the PYTHONPATH in Windows, so it finds my modules/packages?](https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-so-it-finds-my-modules-packages)





### (Hacker) Listener Screenshots - On Kali Linux operating system
![3](https://user-images.githubusercontent.com/25087769/60386240-4503dc00-9a9b-11e9-86ea-c3d38383258f.PNG)


![4](https://user-images.githubusercontent.com/25087769/60386243-47663600-9a9b-11e9-8e18-08425c18e4bf.PNG)


![5](https://user-images.githubusercontent.com/25087769/60386386-e0498100-9a9c-11e9-82e1-60547c5c5350.PNG)




