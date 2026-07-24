import pandas as pd


class Executor:

    def __init__(self, df):

        self.df = df.copy()



    def execute(self, plan):

        operation = plan.get("operation")
            # Check requested columns exist

        available_columns = self.df.columns.tolist()

        check_columns = []


        for key in [
            "column",
            "group_column",
            "value_column"
        ]:

            if key in plan:

                check_columns.append(
                    plan[key]
                )


        missing_columns = [
            col for col in check_columns
            if col not in available_columns
            ]
        if missing_columns:
            missing_columns = [str(col) for col in missing_columns if col is not None]

            return {
                "success": False,
                "error": "Missing columns: " + ", ".join(missing_columns)
                }
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


            elif operation == "columns":

                return self.columns_operation(plan)


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



    # ---------------- COLUMNS ----------------

    def columns_operation(self, plan):

        return {

            "success": True,

            "result": {

                "total_columns": len(self.df.columns),

                "columns": self.df.columns.tolist()

            }

        }



    # ---------------- COUNT ----------------

    def count_operation(self, plan):

        return {

            "success": True,

            "result": len(self.df)

        }



    # ---------------- SUMMARY ----------------

    def summary_operation(self, plan):

        column = plan["column"]


        return {

            "success": True,

            "result": {

                "count": int(self.df[column].count()),

                "mean": float(self.df[column].mean()),

                "min": float(self.df[column].min()),

                "max": float(self.df[column].max()),

                "sum": float(self.df[column].sum())

            }

        }



    # ---------------- FILTER ----------------

    def filter_operation(self, plan):

        column = plan["column"]

        value = plan["value"]


        result = self.df[
            self.df[column] == value
        ]

        return {
        "success": False,
        "result": None,
        "message": "No matching data found."
        }



    # ---------------- TOP ----------------

    def top_operation(self, plan):

        column = plan["column"]

        top = plan.get(
            "top",
            10
        )


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

            "result": result.to_dict(
                orient="records"
            )

        }



    # ---------------- GROUPBY ----------------

    def groupby_operation(self, plan):

        group_column = plan["group_column"]

        value_column = plan["value_column"]

        aggregation = plan.get(
            "aggregation",
            "sum"
        )


        result = (

            self.df

            .groupby(group_column)[value_column]

            .agg(aggregation)

            .sort_values(
                ascending=False
            )

            .head(
                plan.get("top",10)
            )

            .reset_index()

        )
        if result.empty:
            return {
                "success": False,
                "error": "No available data found for this query."
                }


        return {

            "success": True,

            "result": result.to_dict(
                orient="records"
            )

        }



    # ---------------- UNIQUE ----------------

    def unique_operation(self, plan):

        column = plan["column"]


        return {

            "success": True,

            "result": self.df[column]
            .unique()
            .tolist()

        }



# IMPORTANT:
# chatbot.py imports this function

def execute_plan(df, plan):

    executor = Executor(df)

    return executor.execute(plan)