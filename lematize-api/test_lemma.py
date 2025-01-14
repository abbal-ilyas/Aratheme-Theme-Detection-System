import requests

url = 'http://localhost:5000/api/lemma'
text = 'يُشار إلى أن اللغة العربية'

payload = {'textinput': text}

response = requests.post(url, data=payload)

if response.status_code == 200:
    result = response.text
    print(f"Result: \n{result}")
else:
    print("Error during API request.")
