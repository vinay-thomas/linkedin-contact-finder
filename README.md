
LinkedIn Contact Finder
==============================

What Is This?
-------------

This is a simple LinkedIn web scraping program that, given a list of companies, will find a mid-level employee, their role, and their e-mail for each company. The goal of this script is to find low-to-mid-level employees in venture capital firms, funds, debt providers, DFIs, etc. that are ideal for cold contact.


Installation
-------

1. Install [python3](https://www.python.org/downloads/)
2. Download this repo
3. Open the repo with a command line (`cd linkedin-contact-finder` )
	* Alternatively, open this folder with File Explorer, shift + right click, and select "Open with PowerShell window here"  
4. Create a python virtual environment `python -m venv venv`
5. Activate the python virtual environment `venv/Scripts/activate`
6. Install dependencies `python install -r requirements.txt`
7. Download a [Chromedriver](https://chromedriver.chromium.org/downloads) that matches your version of Chrome and move it into this directory

How To Use This
---------------

1. Create a new file called `.env` and paste the contents of the `.example.env` file into it.
2. Add your relevant information to each variable.
	 * Note: You must provide a list of companies in a string that is comma delimited. You must also provide a list of e-mail formats that correspond to the index of the companies, which are also comma delimited.  
	 * Variables:
		 * LINKEDIN_USERNAME - Username to login to your LinkedIn, usually an e-mail
		 * LINKEDIN_PASSWORD - Your LinkedIn password
		 * COMPANIES - A list of companies you want to find contacts for
		 * FORMATS - A list of e-mail formats that correspond to each company
3. Each time you want to run this script, you must first activate the python virtual environment by running `venv/Scripts/activate` and then run `python main.py`
4. Once the script is finished, a csv file called `contacts.csv` will open with the desired information.
