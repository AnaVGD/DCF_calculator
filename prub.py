import requests
headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"}
res=requests.get("https://finance.yahoo.com/quote/AAPL/financials?p=AAPL",headers=headers)
res.status_code

print(res.text)