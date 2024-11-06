#STEP 1: Importing Libraries
import http.client #used to make HTTP request to the game server
import json #handle JSON data
import random #used to generate random number and choices
import pprint #used to print data structures in readable format

#STEP 2: Setting up variables
game_url = "api.considition.com" #URL of the game server
api_key = "" # API-key is sent in mail inbox
map_file = "Map-Gothenburg.json" # Change map here, the file containing map data for the game
awards_file = "Awards.json"
personalities_file = "personalities.json"

#STEP 3: Loading the map data
with open(map_file, "r") as file: #this opens the map file and loads its content into the obj variable as a dictionary
    obj = json.load(file) 
#with open(awards_file, "r") as awardsfile:
#   awards_data = json.load(awardsfile)
#with open(personalities_file, "r") as file:
#    personalities_data = json.load(file)
#STEP 4: Initializing game input
game_input = {                       #a dictionary to store the game data, including map name, loan proposals, and iterations of actions
    "MapName": "Gothenburg",
    "Proposals": [],
    "Iterations": []
}
#STEP 5: Defining the Loan Assessment Function
def assess_loan(customer):
   credit_score = customer.get("credit_score",0)
   debt_to_income_ratio = customer.get("debt_to_income_ratio", 0)
   if credit_score < 600:                    #decides whether to approve or reject a loan based on the customer's credit score and debt-to-income ratio
      return "Reject"
   if debt_to_income_ratio > 0.4:
      return "Reject"
   return "Approve"
#STEP 6: Creating Loan Proposals
for customer in obj["customers"]:          #this loop goes through each customer in the map data, assesses their loan application, adds approved proposals to the game_input
    game_input["Proposals"].append({
        "CustomerName": customer["name"],
        "MonthsToPayBackLoan": obj["gameLengthInMonths"],
        "YearlyInterestRate": 0.05
    })

#STEP 7: Defining action types and rewards
action_types = ["Award", "Skip"]         #possible actions for each customer (either give an award or skip)
#award_types = list(awards_data["Awards"].keys())
award_types = ["IkeaFoodCoupon", "IkeaDeliveryCheck", "IkeaCheck", "GiftCard", "HalfInterestRate", "NoInterestRate"] #different types of awards that can be given to customers
#STEP 8: Generating iteration of actions
for index in range(obj["gameLengthInMonths"]):         #this loop creates a series of actions for each month of the game. 
  customer_actions_dict = {}
  for customer in obj['customers']:
    random_index = random.randint(0, len(action_types) - 1)    #it randomly decides whether to give an award or skip, and if giving an award, it randomly selects one customer
    random_type = action_types[random_index];
    random_award = "None" if random_type == "Skip" else random.choice(award_types)
    customer_actions_dict[customer["name"]] = {
        "Type": random_type,
        "Award": random_award
    }
  game_input["Iterations"].append(customer_actions_dict)

#STEP 9: Sending game data to the server
# Uncomment this to preview game
# pprint.pprint(game_input)
# This part sends the game_input data to the server using HTTP POST request
conn = http.client.HTTPSConnection(game_url)  #conn establishes a connection to the game server
headers = {                                   #set the content type to JSON and includes the API key for authentification
    "Content-Type": "application/json",
    "x-api-key": api_key
}

conn.request("POST", "/game", json.dumps(game_input), headers)   #conn.request sends the game data to the server
response = conn.getresponse()                                    # receives the server response
body = response.read().decode()

if response.status == 200:               #print the response of the request is successful
    pprint.pprint(json.loads(body))
else:
    print(f"Error: {response.status} - {body}")

conn.close()         #close the connection to the server