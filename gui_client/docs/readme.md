# Thema06_GUI GUIDE/README
Gui_client is a Python module used in combination with the pipeline.

## Installation

Clone git repository 

```bash
git clone https://github.com/devalk96/Thema06.git
```
## Dependancies
Python 3.8+
Further dependencies available in requirements.txt
- Jinja2==2.11.2
- multiqc==1.9
- pandas==1.2.0
- paramiko==2.7.2
- Pillow==8.1.0
- pylatex==1.4.1
- PyQt5==5.15.2

## Usage
Run gui_client.py
```bash
gui_client.py
```

## Guide
**1. Run gui_client**.   
![Starting screen](https://i.imgur.com/Epryhmt.png "Starting screen"). 

**2. Select your connection mode**.   
![Connection mode](https://i.imgur.com/JgskLTD.png "Connection mode")    
SSH won't work if proxy's are used, where for example multiple SSH need to be completed in order to connect to the right host. For that we recommend to setup a [ssh tunnel](https://linuxize.com/post/how-to-setup-ssh-tunneling/ "ssh tunnel") and use the SSH Connection mode to connect to localhost. 

**3. Tool setup**.   
Add all paths to the tools. Examples can be found in the /saved_data/examples directory.  
If you want to use these, just copy them to the saved_data directory.   
Examples:     
./saved_data/default_run_local.json  
./saved_data/default_run_ssh.json  
etc..

![Tool screen](https://i.imgur.com/Lv5vx0j.png "Tool screen").   

**4. Create job**.   
![Job screen](https://i.imgur.com/HVseMff.png "Job screen"). 
-  Optimum amount of threads is 8. More won't make the pipeline faster
- Output path should be on the machine the script is run form. 
	1. Add files using the 'Add files' button
	2. Then press RUN pipeline
	3. Jobs will be added to queue 
![Job](https://i.imgur.com/X4voQQf.png "Job")

**5. View jobs**. 
1. Click 'Jobs' button on the sidebar.
- Save PDF button will appear when job is succesfully completed.
- Logs will be available after run, to view the run parameters along the stdout and stderr.

## Support
**author:** SJ Bouwman
**Contact:** sjbouwman@st.hanze.nl
