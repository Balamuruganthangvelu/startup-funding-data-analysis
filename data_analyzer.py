import pandas as pd

def analyze(df, intent):

    if intent == "highest_industry":

        result = (
            df.groupby("Industry")["InvestmentAmount_USD"]
            .sum()
            .sort_values(ascending=False)
            .head(1)
        )

        industry = result.index[0]
        amount = result.iloc[0]

        return {
            "industry": industry,
            "amount": amount
        }

    return None