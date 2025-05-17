from dataclasses import dataclass
import os 
import json
# config.py

from dataclasses import dataclass

@dataclass
class ApiConfig:
    base_url: str = "/app/"
    create_user: str = base_url + "create_user"
    login: str = base_url + "login"
    post_apartment : str = base_url + "post_apartment"
    Apartments : str = base_url + "Apartments"
    apartment_images : str =  base_url + "upload_image"
    apartment_details : str = base_url + "apartment_details"
    update_apartment_status : str = base_url + "update_status"    
    # Firebase API URL
    firebase_base_url: str = "https://identitytoolkit.googleapis.com/v1/accounts:"
    firebase_signInWithPassword = f"{firebase_base_url}signInWithPassword?key="
    firebase_sendOobCode = f"{firebase_base_url}sendOobCode?key="
    firebase_api_key: str = ""
    cloud_apikey : str = ""
    cloud_apisecret : str = ""
    cloud_name : str = ""

 
    @classmethod
    def api_keys(cls):
        # Logic to get API Key from the service account JSON (you can store this securely)
        conf = cls()
        try :
            firebase_path = "secrets/firebase_api.json"
            cloud_path = "secrets/cloud.json"
            if os.path.exists(firebase_path):
                with open(firebase_path, "r", encoding="utf-8") as config_file:
                    print("opened")
                    data = json.load(config_file)
                    conf.firebase_api_key = data.get("apiKey")
            if os.path.exists(cloud_path):
                with open(cloud_path , "r" , encoding="utf-8") as cloud_secrets:
                    print("opened cloud_path")
                    data = json.load(cloud_secrets)
                    conf.cloud_apikey = data.get("cloud_apikey")
                    conf.cloud_apisecret = data.get("cloud_apisecret")
                    conf.cloud_name = data.get("cloud_name")
            return conf
        except Exception as e:
            return conf

routes = ApiConfig.api_keys()
