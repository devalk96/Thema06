# Thema06_GUI
Gui_client is a Python module used in combination with the pipline.

## Installation

Clone git repository 

```bash
git clone https://github.com/devalk96/Thema06.git
```

## Usage
Run gui_client.py
```bash
gui_client.py
```

## Guide
**1. Run gui_client**
![Starting screen](https://i.imgur.com/Epryhmt.png "Starting screen"). 

**2. Select your connection mode**
![Connection mode](https://i.imgur.com/JgskLTD.png "Connection mode")  
SSH won't work if proxy's are used, where for example multiple SSH need to be completed in order to connect to the right host. For that we recommend to setup a [ssh tunnel](https://linuxize.com/post/how-to-setup-ssh-tunneling/ "ssh tunnel") and use the SSH Connection mode to connect to localhost. 

**3. Tool setup**
Add all paths to the tools.   
![Tool screen](https://i.imgur.com/Lv5vx0j.png "Tool screen"). 

**4. Create job**. 
![Job screen](https://i.imgur.com/HVseMff.png "Job screen"). 
-  Optimum amount of threads is 8. More won't make the pipeline faster
- Output path should be on the machine the script is run form. 
	1. Add files using the 'Add files' button
	2. Then press RUN pipeline
	3. Jobs will be added to queue 
![Job](https://i.imgur.com/X4voQQf.png "Job")

**5. View jobs**
1. Click 'Jobs' button on the sidebar.
- Save PDF button will appear when job is succesfully completed.
- Logs will be available after run, to view the run parameters along the stdout and stderr.

## Support
**author:** SJ Bouwman
**Contact:** sjbouwman@st.hanze.nl


