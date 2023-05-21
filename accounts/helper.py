import requests
from decouple import config

# Load the SMS API key from environment variables
api_key = config("SMS_API_KEY")

def send_otp(phone_number,otp):
    try:
        # URL for sending OTP
        url = f"https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}/Metabyte"

        # send a get request to the url
        response = requests.get(url)

        # Return True if the response is successful
        return True
    except:
        #Return False
        return False