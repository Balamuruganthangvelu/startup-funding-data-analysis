import pandas as pd


def analyze(df, intent):

    if df is None or df.empty:
        return "No data available"


    # Highest Industry Funding
    if intent == "highest_industry":

        if "Industry" not in df.columns or "InvestmentAmount_USD" not in df.columns:
            return "Required columns not available"

        result = (
            df.groupby("Industry")["InvestmentAmount_USD"]
            .sum()
            .sort_values(ascending=False)
            .head(1)
        )

        return {
            "industry": result.index[0],
            "amount": result.iloc[0]
        }


    # Highest City Funding
    elif intent == "highest_city":

        if "City" not in df.columns or "InvestmentAmount_USD" not in df.columns:
            return "Required columns not available"

        result = (
            df.groupby("City")["InvestmentAmount_USD"]
            .sum()
            .sort_values(ascending=False)
            .head(1)
        )

        return {
            "city": result.index[0],
            "amount": result.iloc[0]
        }


    # Highest Funded Startup
    elif intent == "highest_startup":

        if "Startup" not in df.columns or "InvestmentAmount_USD" not in df.columns:
            return "Required columns not available"

        result = (
            df.groupby("Startup")["InvestmentAmount_USD"]
            .sum()
            .sort_values(ascending=False)
            .head(1)
        )

        return {
            "startup": result.index[0],
            "amount": result.iloc[0]
        }


    # Total Funding
    elif intent == "total_funding":

        if "InvestmentAmount_USD" not in df.columns:
            return "Funding column not available"

        return {
            "total_funding": df["InvestmentAmount_USD"].sum()
        }


    # Average Funding
    elif intent == "average_funding":

        if "InvestmentAmount_USD" not in df.columns:
            return "Funding column not available"

        return {
            "average_funding": df["InvestmentAmount_USD"].mean()
        }


    # Top 10 Startups
    elif intent == "top_startups":

        if "Startup" not in df.columns or "InvestmentAmount_USD" not in df.columns:
            return "Required columns not available"

        result = (
            df.groupby("Startup")["InvestmentAmount_USD"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        return result.to_dict()


    return "I cannot analyze this request yet"