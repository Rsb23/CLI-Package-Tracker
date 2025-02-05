import json
import os


class JsonDataHandler():
    def __init__(self, filepath):
        self.filepath = filepath

        self.init_file()

    def init_file(self):
        default_data = {
            "shippers": {
                "fedex": [

                ],
                "dhl": [

                ],
                "ups": [

                ],
                "usps": [

                ]
            }
        }
        # check if file exists, create file in correct format if not
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as file:
                file.write(json.dumps(default_data, indent=4))
                file.close()
    
    def get_numbers(self, shipper):
        with open(self.filepath, "r") as file:
            json_obj = json.load(file)
            file.close()
        
        if shipper in ["fedex", "dhl", "ups", "usps"]:
            return json_obj["shippers"][shipper]
    
    def add_number(self, num, shipper):
        with open(self.filepath, 'r') as file:
            json_obj = json.load(file)
            file.close()
        
        if shipper in ["fedex", "dhl", "ups", "usps"]:
            json_obj["shippers"][shipper].append(num)
        
        with open(self.filepath, 'w') as file:
            json.dump(json_obj, file, indent=4)
            file.close()

    def remove_number(self, num, shipper):
        with open(self.filepath, 'r') as file:
            json_obj = json.load(file)
            file.close()
        
        if shipper in ["fedex", "dhl", "ups", "usps"]:
            json_obj["shippers"][shipper].remove(num)
        
        with open(self.filepath, 'w') as file:
            json.dump(json_obj, file, indent=4)
            file.close()