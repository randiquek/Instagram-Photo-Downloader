## Instagram Photo Downloader

- It is for downloading your friend's photos with your acount.
- Your username and your password don't be stored.
- If you have two factor authentication in your Instagram account or not, it still works.
- It uses `Selenium` and two different browser which are `Chrome` and `PhantomJS`
    - The driver is being asked at the beginning of the program.
    - If you want to see what happens -> use `Chrome`
    - If you want the process at the background -> use `PhantomJs`

## Requirements

- Python 3
- Selenium
- PhantomJS
- Chrome Driver for Selenium

## How to install and run

1. Download and install `Python 3.6` in your computer.
	- [Python Download Page](https://www.python.org/downloads/ "Python Download Page")
2. Install `Pip`
	- [Pip Installation Page](https://pip.pypa.io/en/stable/installing/ "Pip Installation Page")
3. Install `Selenium`
	- `pip install selenium`
4. Install `Chrome Driver for Selenium`
	- `pip install chromedriver-installer`
5. Download and install `PhantomJs` 
    - For Linux
        - Do not use apt-get for downloading PhantomJs!
        - Wget the latest phantomjs (as per [PhatomJs Download Page](http://phantomjs.org/download.html "PhatomJs Download Page"))
            - `wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2`
        - Untar it
            - `tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2`
        - Moved the phantomjs executable to /usr/bin/ (may need sudo)
            - `cp /path/to/phantom/untar/bin/phantomjs /usr/bin/`
    - For Windows
        - Follow the rules below :
            - [PhatomJs Download Page](http://phantomjs.org/download.html "PhatomJs Download Page")
6. Download the source from Github
7. Run `Instagram_Photo_Donwloader.py`
	- `python Instagram_Photo_Donwloader.py`