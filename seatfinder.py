import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

URL = 'add_url'

print("Script started...")

def get_available_spots(section_num):
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Check if the request was successful
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all class-section elements
    class_sections = soup.find_all('div', {'class': 'section delivery-f2f'})
    
    for section in class_sections:
        section_element = section.find('span', {'class': 'section-id'})
        if section_element and section_num in section_element.text:
            seats_info = section.find('span', {'class': 'open-seats'}).text.strip()
            # Extract the number of open seats
            open_seats = int(seats_info.split()[1].strip(','))
            return open_seats

    return None

def send_email(subject, body, to_email):
    # Email configuration
    from_email = "add_email"
    from_password = "add_app_password" # make sure to create an app password via gmail

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Connect to Gmail's SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

def main():
    section_num = "enter_sec_num"
    recipient_email = "add_email"
    while True:
        spots = get_available_spots(section_num)
        if spots is not None and spots > 0:
            subject = f"Available spots for section {section_num}"
            body = f"There are {spots} open spots available for section {section_num}."
            print(body)
            send_email(subject, body, recipient_email)
            print(f"email sent")
            time.sleep(30)
        else:
            print(f"email not sent")
            time.sleep(30)

if __name__ == "__main__":
    main()
