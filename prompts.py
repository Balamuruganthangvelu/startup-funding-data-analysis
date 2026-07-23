import pandas as pd


class Executor:

    def __init__(self, df):
        self.df = df.copy()


    def execute(self, plan):

        operation = plan.get("operation")

        try:

            if operation == "groupby":

                return self.groupby_operation(plan)

            elif operation == "summary":

                return self.summary_operation(plan)

            elif operation == "filter":

                return self.filter_operation(plan)

            elif operation == "top":

                return self.top_operation(plan)

            elif operation == "count":

                return self.count_operation(plan)

            elif operation == "unique":

                return self.unique_operation(plan)

            else:

                return {
                    "success": False,
                    "message": f"Unsupported operation: {operation}"
                }

        except Exception as e:

            return {
                "success": False,
                "message": str(e)
            }


    # ---------------------------------------------------

    def groupby_operation(self, plan):

        group_column = plan["group_column"]
        value_column = plan["value_column"]
        aggregation = plan.get("aggregation", "sum")
        top = plan.get("top", 10)

        result = (
            self.df
            .groupby(group_column)[value_column]
            .agg(aggregation)
            .sort_values(ascending=False)
            .head(top)
            .reset_index()
        )

        return {
            "success": True,
            "result": result
        }


    # ---------------------------------------------------

    def summary_operation(self, plan):

        column = plan["column"]

        result = {
            "count": self.df[column].count(),
            "mean": self.df[column].mean(),
            "min": self.df[column].min(),
            "max": self.df[column].max(),
            "sum": self.df[column].sum()
        }

        return {
            "success": True,
            "result": result
        }


    # ---------------------------------------------------

    def filter_operation(self, plan):

        column = plan["column"]
        value = plan["value"]

        result = self.df[
            self.df[column] == value
        ]

        return {
            "success": True,
            "result": result
        }


    # ---------------------------------------------------

    def top_operation(self, plan):

        column = plan["column"]
        top = plan.get("top", 10)

        result = (
            self.df
            .sort_values(
                by=column,
                ascending=False
            )
            .head(top)
        )

        return {
            "success": True,
            "result": result
        }


    # ---------------------------------------------------

    def count_operation(self, plan):

        return {
            "success": True,
            "result": len(self.df)
        }


    # ---------------------------------------------------

    def unique_operation(self, plan):

        column = plan["column"]

        result = self.df[column].unique().tolist()

        return {
            "success": True,
            "result": result
        }