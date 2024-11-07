#STEP 1: Importing Libraries
import http.client #used to make HTTP request to the game server
import json #handle JSON data
import random #used to generate random number and choices
import pprint #used to print data structures in readable format

#STEP 2: Setting up variables
game_url = "api.considition.com" #URL of the game server
api_key = "36635d27-7098-440e-abd6-cfafce58e1f5" # API-key is sent in mail inbox
map_file = "Map-Almhult.json" # Change map here, the file containing map data for the game
awards_file = "Awards.json"
personalities_file = "personalities.json"

#STEP 3: Loading the map data
with open(map_file, "r") as file: #this opens the map file and loads its content into the obj variable as a dictionary
    map_file = json.load(file) 
#with open(awards_file, "r") as awardsfile:
#   awards_data = json.load(awardsfile)
#with open(personalities_file, "r") as file:
#    personalities_data = json.load(file)
#STEP 4: Initializing game input
game_input = {                       #this is a dictionary to store the game data, including map name, loan proposals, and iterations of actions
    "MapName": "Almhult",
    "Proposals": [],
    "Iterations": []
}
#STEP 5: Defining the Loan Assessment Function
def assess_loan_approval(customer):
    monthly_income = customer["income"]
    monthly_expenses = customer["monthlyExpenses"]
    loan_amount = customer["loan"]["amount"]
     # Check to prevent division by zero
    if monthly_income == 0:
        return False
    
    debt_to_income_ratio = (monthly_expenses + loan_amount / map_file["gameLengthInMonths"]) / monthly_income
   
    # Criteria for loan approval
    if debt_to_income_ratio < 0.4 and customer["capital"] > loan_amount:
        return True
    else:
        return False

# Assess each customer
for customer in map_file["customers"]:
    approval = assess_loan_approval(customer)
    #print(f"Loan approval for {customer['name']}: {'Approved' if approval else 'Denied'}")

#STEP 6: Creating Loan Proposals
for customer in map_file["customers"]:          #this loop goes through each customer in the map data, assesses their loan application, adds approved proposals to the game_input
    game_input["Proposals"].append({
        "CustomerName": customer["name"],
        "MonthsToPayBackLoan": map_file["gameLengthInMonths"],
        "YearlyInterestRate": 0.05
    })

#STEP 7: Defining action types and rewards
action_types = ["Award", "Skip"]         #possible actions for each customer (either give an award or skip)
#award_types = list(awards_data["Awards"].keys())
award_types = ["IkeaFoodCoupon", "IkeaDeliveryCheck", "IkeaCheck", "GiftCard", "HalfInterestRate", "NoInterestRate"] #different types of awards that can be given to customers
#STEP 8: Generating iteration of actions
for index in range(map_file["gameLengthInMonths"]):         #this loop creates a series of actions for each month of the game. 
  customer_actions_dict = {}
  for customer in map_file['customers']:
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