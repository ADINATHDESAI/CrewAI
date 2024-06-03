from crewai import Agent
from crewai import Task
from crewai_tools import tool
from crewai import Crew, Process
import requests
import json
from dotenv import load_dotenv

load_dotenv()

url = '<apiurl>'

input_json = json.dumps({
    "notificationDetails": {
        "incidentDate": [
            2023,
            5,
            10
        ],
        "incidentTypeCode": "ACCIDENT",
        "notificationDate": [
            2023,
            5,
            20
        ],
        "locationOfIncidentCode": "HOSPITAL",
        "policyDetails": [
            {
                "policyNumber": "PA000789"
            }
        ],
        "claimantRoles": [
            {
                "claimantRefId": "2a34bcfe-f45d-55f2-8721-6789",
                "roleCode": "BENEFICIARY"
            }
        ],
        "notifierRoleCode": "FRIEND",
        "causeOfIncidentCode": "ACCIDENTAL",
        "notifierRelationship": "Friend",
        "insuredPersonName": "Ravi Sharma",
        "insuredPersonDOB": [
            1985,
            11,
            12
        ]
    },
    "clientDetails": [
        {
            "clientId": "2a34bcfe-f45d-55f2-8721-6789",
            "clientCategoryCode": "INDIVIDUAL",
            "personDetails": {
                "givenName": "Raj",
                "birthDate": 501113400000,
                "identificationList": [
                    {
                        "idTypeCode": "AADHAR",
                        "idNumber": "123456789012"
                    }
                ]
            },
            "addressList": [
                {
                    "addressLine": "Main Street",
                    "cityCode": "Mumbai",
                    "stateCode": "Maharashtra",
                    "postalCode": "400001"
                }
            ],
            "contactDetailsList": [
                {
                    "contactTypeCode": "EMAIL",
                    "contactValue": "raj.sharma@example.com"
                }
            ],
            "emailList": [
                {
                    "emailAddress": "raj.sharma@companyname.com"
                }
            ]
        }
    ]
})

#Tools
@tool("Post_API_Call")
def Post_API_Call(input_json, url):
    """Post_API_Call Tool"""
    # "Parse the input JSON"
    data = json.loads(input_json)
    
    # "Set the headers to specify content type as application/json"
    headers = {
        'Content-Type': 'application/json'
    }

    """Make the POST API call with headers"""
    response = requests.post(url, json=data, headers=headers)
    print(response)

    # "Check the response status code"
    if response.status_code == 200:
        print(response)
        # return f"POST API call successful. Response: {response.json()}"
        return json.dumps(response.json(), indent=2)
    else:
        print(response)
        # return f"Error making POST API call. Status code: {response.status_code}"
        return json.dumps({"error": "API request failed", "status_code": response.status_code}, indent=2)




#Agent
API_Post_Call_Agent = Agent(

    role = " Expert POST API Call Maker  ",
    goal = " Make POST API call successful with input_json = {input_json} and url = {url} ",
    backstory = "You know how to make POST API call.",
    verbose= True,
    # memory = True,
    tools = [Post_API_Call],
    allow_delegation = False
)

#Task
POST_API_call_Task = Task(
    description =   "Take only input_json = {input_json} , url = {url} as input and make a POST API call.",
    expected_output = "POST API Call must be successful",
    tools = [Post_API_Call],
    agent = API_Post_Call_Agent,
    # context = [Text_to_JSON_Task ]
)


crew = Crew(
    agents= [API_Post_Call_Agent ],
    tasks= [ POST_API_call_Task ],
    # process=Process.sequential,
    # memory=True
    # cache=True,
)
result = crew.kickoff(inputs={'input_json': input_json, 'url': url })

print(result)


