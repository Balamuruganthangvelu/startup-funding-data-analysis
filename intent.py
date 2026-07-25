def detect_intent(question):
    q = question.lower()

    if "highest" in q and "industry" in q:
        return "highest_industry"

    elif "highest" in q and "startup" in q:
        return "highest_startup"

    elif "top" in q and "investor" in q:
        return "top_investors"

    elif "city" in q and "highest" in q:
        return "highest_city"

    elif "average" in q:
        return "average"

    return "llm"