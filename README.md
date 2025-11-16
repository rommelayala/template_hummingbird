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
 (deactivate venv
  rm -rf venv )
 $ python3 -m venv venv
 $ source venv/bin/activate
 
 The equivalent command for Caca-Windows command line is:
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
 $ pip install -r requirements.txt
 $ pip3 freeze

```

6. After the Python packages are installed, we need to install the browsers for Playwright. The playwright install
   command installs the latest versions of the three browsers that Playwright supports: Chromium, Firefox, and WebKit:

```
 $ playwright install
```

7. Run the init test

```
pytest 
pytest tests/test_login.py
!!! dont use python3 tests/test_login.py because we are using fixtures
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


### Release History

* 0.1.0

### Authors

* *Rommel Ayala* - *Initial work* 
