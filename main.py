import requests
from bs4 import BeautifulSoup
import sys


shippers = ["FedEx", "DHL", "UPS", "USPS"]


def get_ups_tracking_information(tracking_num):
    timeline_info = ""

    url = f"https://www.bing.com/packagetrackingv2?packNum={tracking_num}&carrier=UPS"
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
    headers = r = requests.get(url, headers={'User-Agent': user_agent})

    soup = BeautifulSoup(r.content, 'html.parser')

    estimated_delivery_data = soup.find_all('div', class_='b_focusTextSmall')
    for data in estimated_delivery_data:
        estimated_delivery = data.text

    package_status_data = soup.find_all('div', class_='pr-tr-currentState')
    for data in package_status_data:
        package_status = data.text

    timeline_data = soup.find('table', class_='rpt_se')
    for tr in timeline_data.contents:
        date_element = tr.find_next('td', class_='pt_Cell').contents[0]
        time_element = tr.find_next('td', class_='b_rTxt pt_Cell').contents[0]
        location_element = tr.find_next('td', class_='pt_location_cell pt_Cell').contents[0]
        status_element = tr.find_next('td', class_='rpt_se_rm pt_Cell').contents[0]

        timeline_info += f"{date_element} {time_element:>8}   {location_element:<50}   {status_element:>}\n"
    
    return package_status, estimated_delivery, timeline_info


while True:
    try:
        while True:
            shipper_choice = input("Please choose a shipper (FedEx, DHL, UPS, or USPS): ")
            if shipper_choice == "FedEx":
                pass
            elif shipper_choice == "DHL":
                pass            
            elif shipper_choice == "UPS":
                ups_tracking_num = input("UPS Tracking Number: ")
                package_status, estimated_delivery, timeline_info = get_ups_tracking_information(ups_tracking_num)
                print(f"\n{package_status}\n{estimated_delivery}\n\n{timeline_info}")
            elif shipper_choice == "USPS":
                pass            
            else:
                print("Invalid Option!")
    except KeyboardInterrupt:
        print("\nGoodbye...")
        sys.exit(0)