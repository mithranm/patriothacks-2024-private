from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pandas as pd
from prompt_library import single_prompt_llm
from pandas_loader import load_data_from_csv
import search_algorithm
import json

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

load_dotenv()

METRO_DATAFRAME, PROPERTY_DATAFRAME, ZIP_DATAFRAME = load_data_from_csv()

"""
Requirements
/house/search - this endpoint will use an llm with aggregated data as context to find the best house. (we choose model later)
/graph/historic_price - this endpoint will create a gradio or streamlit embedded within our react page
"""

class UserParameters(BaseModel):
    budget: int
    credit_score: int
    dist_from_public_transport: int # will be in miles.
    length_of_loan: int # will be in years.
    work_zipcode: int
    
class ChatRequest(BaseModel):
    prompt: str
"""
This endpoint will return the best ranking house with the given parameters from the frontend.
Frontend must form a POST request with the following json formatted body:
{
    "budget": int,
    "credit_score": int,
    "dist_from_public_transport": int,
    "length_of_loan": int
}
"""

@app.post("/house_search")
def search(user_params: UserParameters):
    # Steps for this function.
    budget: int = user_params.budget
    dist: int = user_params.dist_from_public_transport
    zipcode: int = user_params.work_zipcode 
    # We want to be able to use these two variables to rank the best real estate options.

    credit_score: int = user_params.credit_score
    length_of_loan: int = user_params.length_of_loan

    print(f"budget {budget}, preferred distence from public transport: {dist}, work zipcode: {zipcode}, credit score: {credit_score}, length of loan {length_of_loan}") # ensuring all values are being received.

    # Pass in budget, dist, zipcode into llm to get the best real estate.

    #response = chat_llm()
    #print(response["body"].read()) # This is how to get the response from the llm.

    pass

@app.get("/get_properties")
def get_property_dataframe_json(budget=5000, creditScore=0, maxDistance=2, loanTerm=0, workZip=22030):
    if budget=='':
        budget=5000
    if creditScore=='':
        creditScore=0
    if maxDistance=='':
        maxDistance=2
    if loanTerm=='':
        loanTerm=0
    if workZip=='':
        workZip=22030

    output = search_algorithm.run_search_algorithm(float(budget), float(maxDistance), int(workZip))
    return output

@app.post("/chat")
def chat(req: ChatRequest):
    response = single_prompt_llm(req.prompt)

    print(response["body"])

@app.get("/graph_historic_price")
def get_historic_price():


    # Code here (mithran)

    pass


if __name__ == "__main__":
    print(METRO_DATAFRAME["X"])