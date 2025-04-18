
# Linkedin Company Data Scraper

This script based on property data scrap from https://www.linkedin.com/


## What you will get:

- All data in in a CSV file.
- Data points are- Company url, Company Name, Tagline, Service Summery, Followers, Employee, Website, Location, Overview, Industry, Company Size, Founded, Headquarter.


## Requirement

- Language: Python
- Libraries: datetime, pandas, selenium, webdriver_manager, Bs4, lxml, os


## Documentation

- Install python on your OS. You can install latest version of python.
- Now open your cmd/terminal from the script folder and run this command:
```bash
  pip install -r requirements.txt
```
- Now we can run the script using this command from that folder terminal/cmd:
```bash
python linkedin.py
```
- Before run the script you need to put your company names on my given company_name.csv file. I already put some company names, you can remove or add links on there. But don't remove the 'Name' header from that csv file.
- I set this script goes to maximum 5 pages for each search. You can edit page number from my code.
- After run the script, It will automaticaly go through all companies name search, scrap their links and scrap the data. Save the data in a CSV file.


## 🔗 Social Links

📧 mr.amitc55@gmail.com

✅ [@amitchakraborty123](https://www.github.com/amitchakraborty123)

✅ [Linkedin](https://www.linkedin.com/in/mrchamit/)
## 🚀 About Me
I'm a Data Analyst.


## License

[MIT License](https://choosealicense.com/licenses/mit/)
