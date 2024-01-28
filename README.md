# sustainable drinking water treatment plant concepualizer
The conceptualizer provides support in the planning, construction, operation and maintenance of low-tech drinking water treatment plants. For water treatment, a selection of different processes is available, which, supported by various algorithms, can be dimensioned in an intuitive online interface using the simplest input parameters.
Currently the processes flocculation, biosand filtration (bsf) and solar disinfection (sodis) are supported. A wiki provides information about further processes, but there is no software-supported optimization for these.

# Getting started
To access the tool a [Webinterface](https://sustainable-water.de) is available. An [API](https://api.sustainable-water.de) is also provided
Alternatively, the entire components of the tool can be downloaded from this repository and installed in a suitable environment. Instructions on how to do this can be found in the [Installation](#installation) chapter.

The tool consists of four main components:
- A [PostgreSQL](https://www.postgresql.org/) database that contains all research data. These form the basis for the machine-learning algorithms used.
- In order to easily access the data as well as the algorithms, a [RESTful API](https://www.django-rest-framework.org/) was created using [Django](https://www.djangoproject.com/). Thus, the logical components of the tool can be used independently of the interface and integrated into other software.
- To produce the web interface, a website was created using the JavaScript library [svelte](https://svelte.dev/) to create an intuitive interface and present the data in a visually appealing way.
- For the neat presentation of the also provided knowledge base [wikijs](https://js.wiki/) was used. The software provides a complete wiki, which was included on the website to present the knowledge about the reprocessing methods in an orderly fashion.

# Installation
A [Raspberry Pi 4 Model B (4GB)](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) was used as the hardware base for the tool. With the help of the Raspberry Pi Imager, Ubuntu Server 22.04.1 LTS was installed. However, other hardware and operating systems based on Linux should also work.

After the successful start of the server, a remote access must be opened via SSH. To do this, determine the IP of the server and log in with the login data created during the installation of the OS. Afterwards, the installation of the components can be started.

## Visual Studio Code Server
The official [Quick Start](https://code.visualstudio.com/docs/remote/vscode-server#_quick-start) guide should be used to install VS Code Server. At the time of writing this readme, the installation was performed using the following command:
`wget -O- https://aka.ms/install-vscode-server/setup.sh | sh`

**Tip:** It is a good idea to use a versioning software (e.g. git) for backup.

## PostgreSQL
PostgreSQL can be installed via the Ubuntu package manager. The command for this is `apt-get install postgresql-12`

**Tip:** To create a new user and a new database the following commands must be used:
```
sudo -u postgres psql
postgres=# create database mydb;
postgres=# create user myuser with encrypted password 'mypass';
postgres=# grant all privileges on database mydb to myuser;
```

## wikijs
There are several options for installing wikijs. The easiest is probably to install it as a Docker container. However, for better integration with PostgreSQL, a manual installation is preferred. For this, the [official instructions](https://docs.requarks.io/install/linux) can be consulted. The recommended installation path is ./opt/wiki.

**Tip:** If there are problems installing or running the software due to lack of ownership, the folder "wiki" must be given to the user who starts the software (usually the default user "pi", if not changed). This can be achieved with the following command:
`sudo chown -cR pi:pi /opt/wiki`

## Django
For reference, the official [Quick Start Guide](https://docs.djangoproject.com/en/4.1/intro/install/) can be used.
Django is installed via the Ubuntu package manager (`python -m pip install Django`) and is the easiest way for most users.

**Tip:** To access the PostgreSQL database, [Psycopg2](https://www.psycopg.org/) is required. This is installed via the commands `sudo apt install python3-dev libpq-dev` and `pip install psycopg2`. The usage in Django can be found in the [PostgreSQL notes](https://docs.djangoproject.com/en/4.1/ref/databases/#postgresql-notes).

## Svelte
For Svelte to work, [Node.js](https://nodejs.org/en/) must be installed at the beginning. It can be installed via the package manager, but the packages are not necessarily up to date due to long-term support. It is recommended to install Node.js via NodeSource: `curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -` (The current version at the time of writing was _v18.12.1_). After that, Node,js can be installed via the command `sudo apt install nodejs` as usual.
Finally, a Svelte project can be created in the current folder using `npm create svelte@latest my-app`. It is also recommended to use ./opt/ as root folder. If Svelte is not installed yet, this will be done in the same process.

# Usage
The tool can be used in two ways:
1. via the [web interface](https://sustainable-water.de)
2. via the provided [RESTful API](https://api.sustainable-water.de).

The web interface provides a graphical interface to use all the functions of the tool in a neat order. Users can switch between a simple and advanced mode. In the simple mode, only organoleptic input parameters are requested, which can be detected purely by human senses without special analytics. Advanced mode provides more accurate results, but this requires the user to perform accurate analytics and enter the parameters.

Alternatively, the RESTful API can be used to bypass the web interface and directly access the provided methods. This is particularly useful if the functions are to be included elsewhere. The interface is provided openly, but it is assumed that only people with appropriate expertise will use this route.

## Provided Methods
### Flocculation
The API for predicting the cleaning performance of the flocculation process is divided into three parts. The first interface is used to predict the final turbidity, whereas the second interface predicts the final electrical conductivity. The third interface was set up to predict the final pH value, but the tests showed that the accuracy was only 50 %. The algorithm is therefore not able to deliver significant results and was therefore not implemented in the web application.
#### [Turbidity](https://api.sustainable-water.de/tur)
The API for predicting turbidity takes various input parameters, which are listed and briefly explained below:
- "print assessment" (boolean) can be used by developers to obtain assessment data of the algorithm.
- "load pipe" (boolean) is a boolean value that decides whether the existing model should be used or a new one trained.
- "surface water" (selection) is used to specifically select a surface water within the database. This allows the algorithm to be optimized for samples of the same water body.
- "initial pH" (), "initial EC" (µS/cm) and "initial turbidity" (NTU) are parameters of a required water sample.
- "flocculant" (selection) is used to select a specific flocculant to be used for treatment.
- "floc dose" (mg/l) is the amount of flocculant used in the process
- "floc saline molarity" (mol/l) and "floc cactus share" (%) are properties that relate specifically to the use of Moringa-based flocculants and can be specified optionally.
- Finally, the operating parameters such as stirring speed ("stirring speed coagulation phase" (rpm) and "stirring speed flocculation phase" (rpm)) and duration ("duration coagulation phase" (min), "duration flocculation phase" (min) and "duration sedimentation phase" (min)) of the various flocculation phases must be entered.
#### [EC](https://api.sustainable-water.de/ec)
The API for predicting electrical conductivity takes the following values:
- "print assessment" (boolean) can be used by developers to obtain assessment data of the algorithm.
- "load pipe" (boolean) is a boolean value that decides whether the existing model should be used or a new one trained.
- "initial EC" (µS/cm) is a value from the required water analysis
- "floc concentration" (g/l) is the concentration of the stock solution used
- "floc saline molarity" (mol/l) is an optional parameter
- "floc dose" (mg/l) is the amount of flocculant used in the process
#### [pH](https://api.sustainable-water.de/ph)
The API for predicting pH takes the following values:
- "print assessment" (boolean) can be used by developers to obtain assessment data of the algorithm.
- "load pipe" (boolean) is a boolean value that decides whether the existing model should be used or a new one trained.
- "initial pH" () is a value from the required water analysis
- "floc concentration" (g/l) is the concentration of the stock solution used
- "floc saline molarity" (mol/l) is an optional parameter
- "floc dose" (mg/l) is the amount of flocculant used in the process

As already mentioned, the interface does not provide any significant results and should therefore not be used. The interface was only included for the sake of completeness, as there is the possibility of achieving more reliable results in the future with a sufficient data basis (horizontal and vertical).

### [Biosand filtration](https://api.sustainable-water.de/bsf)
The API for predicting the cleaning performance of the biosand filtration process takes the following values:
- "print assessment" (boolean) can be used by developers to obtain assessment data of the algorithm.
- "load pipe" (boolean) is a boolean value that decides whether the existing model should be used or a new one trained.
- "diameter" (cm) is the diameter of the container used.
- "material height" (cm) is the height of the sand filled into the container and is used to calculate the filter volume
- "mean grain diameter" (mm) is a parameter that quantifies the fineness of the material used, on which the future cleaning performance depends.
- "mean flow" (l/h) refers to the flow rate.
- "mean pause" (h) is the time during which the filter is not used and the dirt cover can develop.
- "time dirt blanket" (d) is the age of the dirt blanket.
- "initial turbidity" (NTU) is the turbidity of the raw water used.

### [Activated Alumina Adsorption](https://api.sustainable-water.de/aaa)
The API for predicting the cleaning performance of the adsorption process takes the following values:
- "concentration" (mg/l) refers to the amount of fluoride contained in the water.
- "contact time" (min) is the time during which the water is in contact with the adsorbent.
- "concentration chloride", "concentration sulfate", "concentration bicarbonate", "concentration hydrogen phosphate", and "concentration arsenic" (all in mg/l) are concentrations of compounds that can inhibit the adsorption process through competitive adsorption.

### [SODIS](https://api.sustainable-water.de/sodis)
The API for predicting the cleaning performance of the solar disinfection process takes the following values:
- "latitude" () and "longitude" () are used to locate the place where SODIS (Solar Water Disinfection) is to be applied.
- "starting hour" (hh) is needed to fix the time at which the water to be treated is exposed to sunlight.
- "water temperature" (°C) is used to more accurately determine the thermal effects of SODIS.
- "target logdis" () is the desired level of purification. This uses the logarithmic scale. A disinfection level of 2 corresponds to 99% germ reduction, whereas a level of 4 corresponds to a 99.99% germ reduction.

# Support
If you find issues or have hints, you can open an issue here on this github project. Alternatively, you can extend the project in your own favor by forking the project and then making a merge request.

# Roadmap
- [x] get components up and running.
- [x] backend work
    - [x] create RESTful API
        - [x] add access to database (complete [CRUD](https://www.restapitutorial.com/lessons/httpmethods.html)!)
            - [x] [POST / Create](http://192.168.178.69:3001/flocdata/)
            - [x] [GET / Read](http://192.168.178.69:3001/flocdata/)
            - [x] [PUT,PATCH / Update](http://192.168.178.69:3001/flocdata/1001/ "Example (id 1001)")
            - [x] [DELETE / Delete](http://192.168.178.69:3001/flocdata/1001/ "Example (id 1001)")
        - [x] add access to functions (input/output)
            - [x] sodis
            - [x] flocculation
            - [x] bsf
            - [x] aaa
- [x] frontend work
    - [x] create web interface
        - [x] landing page
        - [x] input page
        - [x] results page
        - [x] ... see [figma](https://www.figma.com/proto/q2TWjgOTD9e2FJf0krhK3d/swtpc?node-id=1%3A10)
    - [x] fill wiki
        - [x] sodis/sopas
        - [x] bsf
        - [x] flocculation
        - [x] boiling
        - [x] chlorination
        - [x] [ceramic pot filtration](https://www.cdc.gov/healthywater/global/household-water-treatment.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fhealthywater%2Fglobal%2Fhousehold-water-treatment%2Fceramic-filtration.html)
        - [x] [WADI](https://www.helioz.org/en/wadi)
        - [x] [test strips](https://www.amazon.de/Wassertester-Wasserteststreifen-Teststreifen-Leitungswasser-Wasserqualit%C3%A4tstest/dp/B09F9W5BRP/ref=sr_1_4?keywords=wasser+teststreifen&qid=1669115134&sr=8-4)
    - [x] link sites
        - [x] [Affordable WASH services and products](https://sswm.info/sswm-solutions-bop-markets/affordable-wash-services-and-products)
        - [x] [Household Water Treatment and Safe Storage Products and Technologies](https://www.hwts.info/products-technologies)
- [x] write adequate documentation
    - [x] add technical functionality of REST API of algorithms
        - [x] sodis/sopas
        - [x] flocculation
        - [x] bsf
        - [x] aaa


# License
This project is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are **free to copy and redistribute** the material in any medium or format and remix, transform, and build upon the material for any purpose, **even commercially**.

**You must give appropriate credit**, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use. If you remix, transform, or build upon the material, you must **distribute your contributions under the same license** as the original.

**You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.**
