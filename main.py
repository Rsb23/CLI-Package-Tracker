import requests
from bs4 import BeautifulSoup
import sys
from json_data_handling import JsonDataHandler as jdh


def get_tracking_information(tracking_num, shipper):
    timeline_info = ""

    if shipper == 'ups':
        url = f"https://www.bing.com/packagetrackingv2?packNum={tracking_num}&carrier=UPS"
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
        r = requests.get(url, headers={'User-Agent': user_agent})

        if r.headers != 200:  # invalid response, perhaps package does not exist or 
            return -1, "", "", ""
        
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
        
        return 0, package_status, estimated_delivery, timeline_info


while True:
    try:
        while True:
            shipper_choice = input("Choose Shipper (fedex, dhl, ups, or usps) OR 'saved': ")
            if shipper_choice == "fedex":
                pass
            elif shipper_choice == "dhl":
                pass            
            elif shipper_choice == "ups":
                ups_tracking_num = input("UPS Tracking Number: ")
                response, package_status, estimated_delivery, timeline_info = get_tracking_information(ups_tracking_num, 'ups')
                if response == 0:
                    print(f"\n{package_status}\n{estimated_delivery}\n\n{timeline_info}")
                else:
                    print("Cannot Find Package!")
            elif shipper_choice == "usps":
                pass            
            elif shipper_choice == "saved":
                data_handler = jdh("saved_tracking_number_data.json")
                while True:
                    saved_choice = input("v to view, a to add, r to remove, or h to go back home: ")
                    if saved_choice in ['v', 'a', 'r']:
                        if saved_choice == 'v':
                            saved_shipper_choice = input("Choose a shipper (fedex, dhl, ups, usps): ")
                            for num in data_handler.get_numbers(saved_shipper_choice):
                                get_tracking_information(num, saved_shipper_choice)
                        elif saved_choice == 'a':
                            saved_shipper_choice = input("Choose a shipper (fedex, dhl, ups, usps): ")
                            num = input("Enter The Tracking Number: ")
                            data_handler.add_number(num, saved_shipper_choice)
                        elif saved_choice == 'r':
                            saved_shipper_choice = input("Choose a shipper (fedex, dhl, ups, usps): ")
                            num = input("Enter The Tracking Number: ")
                            data_handler.remove_number(num, saved_shipper_choice)
                        elif saved_choice == 'h':
                            break
                    else:
                        print("Invalid Option!")
                    break
            else:
                print("Invalid Option!")
    except KeyboardInterrupt:
        print("\nGoodbye...")
        sys.exit(0)