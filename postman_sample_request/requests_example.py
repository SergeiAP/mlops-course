from email import header
from urllib import response
import requests
import pandas as pd


test_df = pd.read_csv("../data/processed/test.csv")
x_holdout = test_df.drop("price", axis=1)
x_holdout = x_holdout[0:10]


headers = {"content-type": "application/json", "Accept": "text/plain"}
response = requests.post("http://127.0.0.1:5001/invocations",
                         data=x_holdout.to_json(orient="split"),
                         headers=headers)

print(response.content)
