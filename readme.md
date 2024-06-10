
# CoinMarketCap Data Scrapping

The goal is to basically make a script to scrape some data from a website exposed as a django rest framework API.
https://coinmarketcap.com/


This application takes in a list of valid crypto coin acronyms and scrapes data from the website and return back the JSON response.

Libraries used:
 - DjangoRestFramework
 - Celery
 - Requests
 - Selenium

Overview:
 - There are two end-points
    - api/taskmanager/start_scraping/
    - api/taskmanager/scraping_status/<job_id>/
 - The input to this API is validated: If a payload like ```[1, “DUKO”, 3]``` is provided, it throws relevant response.
 - The APIs is generalized i.e, it works with any valid input coins available on CoinMarketCap.

### Starting Page
![image](https://github.com/lokeswar-gahir/CoinMarketCap-scrapping/blob/master/images/image-1(start).png?raw=true)

### Getting Job ID from Celery
![image](https://github.com/lokeswar-gahir/CoinMarketCap-scrapping/blob/master/images/image-2_getting_UUID.png?raw=true)

### Showing Results using Job ID
![image](https://github.com/lokeswar-gahir/CoinMarketCap-scrapping/blob/master/images/image-3_getting_results.png?raw=true)

### All Jobs on Admin Panel
Latest jobs are on top
![image](https://github.com/lokeswar-gahir/CoinMarketCap-scrapping/blob/master/images/image-4_showing_job.png?raw=true)

### Job Detail
![image](https://github.com/lokeswar-gahir/CoinMarketCap-scrapping/blob/master/images/image-5_showing_job_detail.png?raw=true)

### All Tasks on Admin Panel
latest tasks are on top
![image](https://github.com/lokeswar-gahir/CoinMarketCap-scrapping/blob/master/images/image-6_showing_task.png?raw=true)

### Task Detail
![image](https://github.com/lokeswar-gahir/CoinMarketCap-scrapping/blob/master/images/image-7_showing_task_detail.png?raw=true)

### Response on Invalid Input
![image](https://github.com/lokeswar-gahir/CoinMarketCap-scrapping/blob/master/images/image-8_on_invalid_input.png?raw=true)

### Generalized Performance
1. Input
![image](https://github.com/lokeswar-gahir/CoinMarketCap-scrapping/blob/master/images/image-9_generalized_coin_input.png?raw=true)

2. Output
![image](https://github.com/lokeswar-gahir/CoinMarketCap-scrapping/blob/master/images/image-10_generalized_coin_output.png?raw=true)
