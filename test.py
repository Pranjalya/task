import os
import requests

PATH = './sounds/samples/vi95kMQ65UeU7K1wae12D1GUeXd2'

for name in os.listdir(PATH):
    filename = os.path.join(PATH, name)
    files = {
        'file': (filename, open(filename, 'rb')),
    }
    response = requests.post('https://cough-detector.herokuapp.com/detect_coughs', files=files).json()
    print("File : {} and the Cough peaks occured at following seconds :".format(name))
    if len(response["peak_start"]) == 0:
        print("No cough was found in the audio")
        continue
    for i in response["peak_start"].values():
        print("{}".format(i), end=" ")
    print("\n")
