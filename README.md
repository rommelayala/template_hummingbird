## Hummingbird

This project is based in Playwright-Phyton

## What is Playwright?

Playwright is a fairly new test automation framework from Microsoft.
It is open source, and it has bindings in TypeScript/JavaScript, Python, .NET, and Java.
Some of the nice features Playwright offers include:

* concise, readable calls
* easy out-of-the-box setup
* very fast execution times (compared to other browser automation tools)
* cross-browser and mobile emulation support
* automatic waiting
* screenshots and video capture
* built-in API calls

Microsoft is actively developing Playwright,

## Installation

### Requirements

* phyton V 3.10+ [Phyton Downloads](https://www.python.org/downloads/).

### Usage

1. Clone repository
2. Open in VSCode
3. Open a new terminal in VSCode
4. Execute

 ```
 $ python3 -m venv venv
 $ source venv/bin/activate
 
 The equivalent command for a Windows command line is:
 > venv\Scripts\activate.bat
 ```

5. Let's add some Python packages to our new virtual environment:

```
 $ pip3 install playwright
 $ pip3 install pytest
 $ pip3 install pytest-playwright
 $ playwright install (Debian)
 $ sudo playwright install-deps (Debian)
```

You can check all installed packages using pip3 freeze. They should look something like this:

```
 $ pip3 freeze
attrs==21.2.0
certifi==2021.10.8
charset-normalizer==2.0.8
greenlet==1.1.2
idna==3.3
iniconfig==1.1.1
packaging==21.3
playwright==1.19.1
pluggy==1.0.0
py==1.11.0
pyee==8.1.0
pyparsing==3.0.6
pytest==7.0.1
pytest-base-url==1.4.2
pytest-playwright==0.2.3
python-slugify==5.0.2
requests==2.26.0
text-unidecode==1.3
toml==0.10.2
tomli==2.0.1
urllib3==1.26.7
websockets==10.1
```

6. After the Python packages are installed, we need to install the browsers for Playwright. The playwright install
   command installs the latest versions of the three browsers that Playwright supports: Chromium, Firefox, and WebKit:

```
 $ playwright install
```

7. Run the init test

```
In order eecute all test to log data into elastic is necessary to run this command
$  export RUN_TYPE="manual" &&  python3 tests/test_veepee_privalia_es.py
```
Is possible to have issues if you are running this command
``` 
$ pytest tests/test_homepage_components.py
or
 $ python3 test_homepage_components.py
```

## Architecture

```
 ├── lib        (Utlility functions)
 │   ├── utilities
 │   ├── config_variables
 │   
 ├── reporting  (reporting functions)
 │   └──
 │ 
 ├── tests      (Testing functions)
 │   └── 
 │
 ├── integrations   (integrations with external tools )
 │   ├── slack
     ├── elastic

```

# Tests

This project will launch test for all veepee sites, actually there are 3/8 sites,

| Status | Country     | URL                    |
|--------|-------------|------------------------|
| DONE   | France      | https://www.veepee.fr/ |
| DONE   | Spain       | https://www.veepee.es/ |
| DONE   | Italy       | https://www.veepee.it/ |
| WIP    | Germany     | https://www.veepee.de/ |
| WIP    | Austria     | https://www.veepee.at/ |
| WIP    | Netherlands | https://www.veepee.nl/ |
| WIP    | Luxembourg  | https://www.veepee.lu/ |
| WIP    | Belgium     | https://www.veepee.be/ |

## France, Spain, Italy:

 [test_veepee_XX.py](tests%2Ftest_veepee_es.py) ( XX is the country i.e. fr france )
 1. check_campaign_link_is_not_dead_XX ( XX is the country i.e. fr france )
    - This test extract the url of the 'href' attribute then click on banner and check if href_url match with url_browser and inject in elastic search the resul, print in console time execution 
   
 2. check_picture_images_in_campaigns_XX ( XX is the country i.e. fr france )
    - This test extract the url of the 'srcset' attribute then open a new page using this link and check that the image is loaded correctly 

## Executing test
Go to /tests folder and execute
```
$ python3 test_campaigns.py
```
Is possible to execute test by country executing 
```
$ python3 test_veepee_fr.py (test will be executed only for veepee.fr)

$ python3 test_veepee_es.py (test will be executed only for veepee.es)

$ python3 test_veepee_it.py (test will be executed only for veepee.it)
```

### Release History

* 0.1.0

### Authors

* *Rommel Ayala* - *Initial work* 
