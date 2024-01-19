# Djinni Job Vacancies Scraping and Analysis

## Overview

Welcome to the Djinni Job Vacancies Scraping and Analysis Project! 
This project focuses on developing robust way of scraping Python job openings from Djinni and
conducting an in-depth analysis of vacancies.

### Features
- Web Scraping: Utilizes Scrapy to crawl and extract relevant information from job postings.

- Data Analysis: Provides statistical analysis on the collected data, including information on vacancies, views, and reviews.

- Experience Requirement: Analyzes and presents insights into the experience required for Python developer positions.

- Location Insights: Offers statistics and trends related to the geographical locations of job vacancies.

- Technology Trends: Identifies and presents the most commonly mentioned technologies in job postings.


## How to Use

Follow these simple steps to get started with the project:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/Familenko/djinni_statistic.git
    ```
   
2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
   
3. **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```

4. **Install Requirements:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Web Scraping Script:**
    ```bash
    scrapy crawl jobs -O jobs.csv
    ```

6. **Run the Analysis Script:**
    ```bash
    python analize/analyze_job_market.ipynb
    ```

