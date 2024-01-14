import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests
from bs4 import BeautifulSoup


def get_html_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.prettify()

def extract_account_info(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all the email and password elements
    account_info_elements = soup.find_all("h4")
    email_elements = soup.find_all("input", {"id": "email"})
    password_elements = soup.find_all("input", {"id": "pass"})

    # Extract all the account info values and remove extra spaces and newlines
    account_infos = [' '.join(element.text.split()) for element in account_info_elements]
    emails = [element["value"] for element in email_elements]
    passwords = [element["value"] for element in password_elements]

    # Combine all the account infos, emails, and passwords into a list of tuples
    account_data = list(zip(account_infos, emails, passwords))

    return account_data

