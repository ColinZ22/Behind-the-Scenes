import os
import json

apiKeys = {"Spotify API Key": "",
               'Spotify API Secret': "",
               'Audd API Token': "",
               "ACRCloud API Access Key": "",
               "ACRCloud API Access Secret": "",
               "Rapid API Key": ""}

def getAPIKeys():

    apiFilePath = os.getcwd() + "\APIKeys.json"
    print("API Keys File Path " + apiFilePath)

    if os.path.exists(apiFilePath) and os.stat(apiFilePath).st_size != 0:
        print("API Keys File Exists")
        with open(apiFilePath, "r") as f:
            apiData = f.read()
        f.close()
        apiDict = json.loads(apiData)
        for apiKey in apiDict:
            if apiKeys[apiKey] == apiDict[apiKey] == "":
                print(f"Please enter your {apiKey}: ")
                apiKeys[apiKey] = input()
            else:
                apiKeys[apiKey] = apiDict[apiKey]
        with open(apiFilePath, 'w') as f:
            json.dump(apiKeys, f, indent=2)
        f.close()
    else:
        print("API Keys File Does Not Exist")
        with open(apiFilePath, 'w') as f:
            json.dump(apiKeys, f, indent=2)
        for apiKey in apiKeys:
            if apiKeys[apiKey] == "":
                print(f"Please enter your {apiKey}: ")
                apiKeys[apiKey] = input()
        with open(apiFilePath, 'w') as f:
            json.dump(apiKeys, f, indent=2)
        f.close()