# Stocker
Stocker scrapes stock symobls and the stocks public market information to determine quickly if a stock is a good buy or a goodby.

## Intrinsic Value
Intrinsic value is calculated based on this online [TUTORIAL](http://web.archive.org/web/20191030205524/https://medium.com/popularengineering/how-to-calculate-the-intrinsic-value-of-stocks-like-warren-buffett-f9b97e3738ba)


# Setup

## Mac OS and Linux

### First Install Anaconda
Anaconda® is a package manager, an environment manager, a Python/R data science distribution.  In order to use some Machine learning and Data science libaries we can use the Andaconda installer to install Panda and SicPy stack (IPython, NumPy, Matplotlib,...).  After running the Anaconda® installer, users will have access to panda and the rest of the ScipPy stack without needing to install anything else, and with needing to wait for any software to complie. To install Anaconda® via the installer follow the instuctions on their website [here](https://docs.continuum.io/anaconda/install/mac-os/#). Refer to Anaconda-Starter-Guide.pdf as a cheat sheet.  Also, see the [user guide](https://docs.anaconda.com/anaconda/user-guide/)

After you install Anaconda® you may need to restart/refresh you terminal.

#### A Note for older Mac Machines
Numpy 1.18 isn't compatiable with older Mac CPU architecture. If you run into the following error: 
`Illegal instruction: 4`
Then you may need to downgrade numpy to version 1.16.4.

You may need to install through conda-forge [see](https://conda-forge.org), if you want to learn more about conda-forge.

To downgrade, run the following command:
`conda install -c conda-forge numpy=1.16.4`

### Install Pandas
Pandas should already be installed with Anaconda®, but if for some reason you need to reinstall it run the following command:
`conda install -c conda-forge pandas`

### Install Selenium
Install selenium to all for web browser automation
`conda install -c conda-forge selenium`

### Install Beautiful Soup
Install "Beautiful Soup" for html web scraping
`conda install -c conda-forge bs4`

### [LINUX ONLY] Install geckodrive for Linux to use Firefox
In order to use the Firefox driver make sure `geckodriver` is installed. [see](https://github.com/mozilla/geckodriver) for more information. 

To setup do the following:
1. Go to the [geckodriver releases page](https://github.com/mozilla/geckodriver/releases). Find the latest version of the driver for your platform and download it. For example:
`wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-<vXXXX>-linux64.tar.gz` - where `XXXX` is the desired version.

2. Extract the file with:
`tar -xvzf geckodriver*`

3. Make it executable:
`chmod +x geckodriver`

4. Move `geckodrive` to `/usr/local/bin/`:
`sudo mv geckodriver /usr/local/bin/`

### Allow Remote Automation
To allow Stocker to scrape the internet on Safari go into Preference -> Advanced and check box label `Show Develop menu in menu bar.  Then select Developer -> Allow Remote Automation.

### Done
In the words of the infamous Porky Pig, "That's all Folks!".  Your environment should be ready to use Stocker.

## Windows

# Unit Tests
Unit tests are setup to use Python's build in Unit testing framework.  Please refer [here](https://docs.python.org/2/library/unittest.html) for more information

## Run Unit Tests
In order to run you unit test they need to be run as modules/packages - use the -m argument.  See the example below to run as as terminal command at root:
`python -m Tests.stock_tests`

# Run Stocker
To run Stocker make sure you're at root and run the following command:
`python -m Classes.runner -d <web_driver_name> -i <input_file.txt>` 

In you input_file.txt list the stock symbols for Stocker to run.  If an input file isn't a global search for all stock symbols be will run.