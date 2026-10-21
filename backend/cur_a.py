# -*- coding: utf-8 -*-
"""Weeks 1-7 of the Introduction to Data Science Python curriculum."""

SNIPPETS_A = [
    # ---------------------------------------------------------------- WEEK 1
    dict(
        id="w01-01", week=1, difficulty=1,
        title="Variables and print",
        topic="Variables & print",
        prompt='Create a variable name set to the text "Ada" and a variable age set to 28, then print both on a single line.',
        hint="print(name, age) accepts two arguments and separates them with a space.",
        code='name = "Ada"\nage = 28\nprint(name, age)',
    ),
    dict(
        id="w01-02", week=1, difficulty=1,
        title="Check the type of a value",
        topic="Data types",
        prompt="Assign an integer 10 to x, a float 3.14 to y and the text value to z, then print type() for each in one print call.",
        hint="type(value) returns the data type; pass all three inside a single print().",
        code='x = 10\ny = 3.14\nz = "text"\nprint(type(x), type(y), type(z))',
    ),
    dict(
        id="w01-03", week=1, difficulty=1,
        title="Index into a list",
        topic="Lists",
        prompt="Store three temperatures 21.5, 23.0 and 19.8 in a list called temperatures, then print the first element.",
        hint="Python lists are zero-indexed, so the first element is [0].",
        code='temperatures = [21.5, 23.0, 19.8]\nprint(temperatures[0])',
    ),
    dict(
        id="w01-04", week=1, difficulty=1,
        title="Read a value from a dictionary",
        topic="Dictionaries",
        prompt='Create a dictionary student with keys "name" (value "Ada") and "score" (value 95), then print the score using square-bracket lookup.',
        hint='Use student["score"] with the key in double quotes.',
        code='student = {"name": "Ada", "score": 95}\nprint(student["score"])',
    ),
    dict(
        id="w01-05", week=1, difficulty=1,
        title="Arithmetic and averages",
        topic="Operators",
        prompt="Compute 10 + 5 * 2 into total, then divide total by 3 into mean and print mean.",
        hint="Multiplication binds tighter than addition, so no brackets are needed.",
        code="total = 10 + 5 * 2\nmean = total / 3\nprint(mean)",
    ),
    dict(
        id="w01-06", week=1, difficulty=2,
        title="Branch with if / elif / else",
        topic="Control flow",
        prompt='Set score to 82. Assign grade "A" when score is at least 90, "B" when at least 80, otherwise "C". Print grade.',
        hint="Use if / elif / else and the >= operator, then print(grade).",
        code=(
            'score = 82\n'
            'if score >= 90:\n'
            '    grade = "A"\n'
            'elif score >= 80:\n'
            '    grade = "B"\n'
            'else:\n'
            '    grade = "C"\n'
            'print(grade)'
        ),
    ),
    dict(
        id="w01-07", week=1, difficulty=2,
        title="Loop over a range",
        topic="Loops",
        prompt="Loop i from 0 to 4 with range(5) and print i raised to the power 2 on each iteration.",
        hint="Indent the body four spaces and use the exponent operator **.",
        code="for i in range(5):\n    print(i ** 2)",
    ),
    dict(
        id="w01-08", week=1, difficulty=2,
        title="Define a reusable mean function",
        topic="Functions",
        prompt="Define a function mean(values) that returns the sum divided by the length, then print the mean of the list [2, 4, 6].",
        hint="Use sum() and len() inside a return statement; leave one blank line before the print.",
        code="def mean(values):\n    return sum(values) / len(values)\n\nprint(mean([2, 4, 6]))",
    ),
    dict(
        id="w01-09", week=1, difficulty=1,
        title="Collect rows in a list",
        topic="Lists & loops",
        prompt="Create an empty list called rows, then loop over the names Ada, Grace and Alan and append each name to rows. Print the list.",
        hint="Start with rows = [] and use a for loop over the literal list.",
        code='rows = []\nfor name in ["Ada", "Grace", "Alan"]:\n    rows.append(name)\nprint(rows)',
    ),

    # ---------------------------------------------------------------- WEEK 2
    dict(
        id="w02-01", week=2, difficulty=2,
        title="Clone a repository and enter it",
        topic="Git basics",
        prompt="In the terminal, clone the repository https://github.com/user/project.git and then move into the project directory.",
        hint="Two commands: git clone <url> followed by cd project.",
        code="git clone https://github.com/user/project.git\ncd project",
    ),
    dict(
        id="w02-02", week=2, difficulty=2,
        title="Stage and commit a file",
        topic="Git staging",
        prompt='Stage the file data.csv and commit it with the message "Add raw dataset".',
        hint='git add <file> then git commit -m "<message>" — keep the message in double quotes.',
        code='git add data.csv\ngit commit -m "Add raw dataset"',
    ),
    dict(
        id="w02-03", week=2, difficulty=1,
        title="Push to the remote",
        topic="Git remotes",
        prompt="Push the current commits to the remote called origin on the branch main.",
        hint="git push <remote> <branch>.",
        code="git push origin main",
    ),
    dict(
        id="w02-04", week=2, difficulty=2,
        title="Inspect repository state",
        topic="Git status & log",
        prompt="Show the working tree status, then display the last five commits in one-line format.",
        hint="git status, then git log with the --oneline flag and -5.",
        code="git status\ngit log --oneline -5",
    ),
    dict(
        id="w02-05", week=2, difficulty=2,
        title="Install a package in Google Colab",
        topic="Colab environment",
        prompt="In a Google Colab cell, install pandas with pip using the shell escape, then import it with the alias pd.",
        hint="Prefix the shell command with ! and import with the as alias.",
        code="!pip install pandas\nimport pandas as pd",
    ),
    dict(
        id="w02-06", week=2, difficulty=2,
        title="Mount Google Drive in Colab",
        topic="Colab filesystem",
        prompt='Mount your Google Drive in Colab by importing drive from google.colab and calling drive.mount on the path "/content/drive".',
        hint='from google.colab import drive, then drive.mount("/content/drive").',
        code='from google.colab import drive\ndrive.mount("/content/drive")',
    ),

    # ---------------------------------------------------------------- WEEK 3
    dict(
        id="w03-01", week=3, difficulty=2,
        title="Send a GET request",
        topic="REST APIs",
        prompt='Import requests and fetch https://api.example.com/data with requests.get, storing the result in response. Print its status_code.',
        hint="Two lines of setup plus the call; leave a blank line before the request.",
        code=(
            "import requests\n"
            "\n"
            'response = requests.get("https://api.example.com/data")\n'
            "print(response.status_code)"
        ),
    ),
    dict(
        id="w03-02", week=3, difficulty=2,
        title="Query parameters and error checking",
        topic="REST APIs",
        prompt='Request the url stored in the variable url with the query parameter page set to 2, then raise an error for bad status codes.',
        hint='Pass params={"page": 2} and call response.raise_for_status().',
        code='response = requests.get(url, params={"page": 2})\nresponse.raise_for_status()',
    ),
    dict(
        id="w03-03", week=3, difficulty=2,
        title="Parse a JSON response",
        topic="JSON",
        prompt="Import json, parse response.text into a variable called payload, then print the first element of its items list.",
        hint='json.loads() converts text to Python objects; index with payload["items"][0].',
        code='import json\npayload = json.loads(response.text)\nprint(payload["items"][0])',
    ),
    dict(
        id="w03-04", week=3, difficulty=2,
        title="Serialise a dict to JSON",
        topic="JSON",
        prompt='Given a dictionary body with name "Ada" and score 95, print it as indented JSON with 2 spaces of indentation.',
        hint="json.dumps(body, indent=2).",
        code=(
            'body = {"name": "Ada", "score": 95}\n'
            "print(json.dumps(body, indent=2))"
        ),
    ),
    dict(
        id="w03-05", week=3, difficulty=2,
        title="POST JSON to an API",
        topic="REST APIs",
        prompt="Send the dictionary body to the variable url using requests.post as JSON, then print the parsed JSON reply from the response.",
        hint="Use the json= keyword argument, then response.json().",
        code="response = requests.post(url, json=body)\nprint(response.json())",
    ),
    dict(
        id="w03-06", week=3, difficulty=3,
        title="Parse HTML with BeautifulSoup",
        topic="Web scraping",
        prompt='Import BeautifulSoup from bs4, parse the html string with the "html.parser" parser into soup, then print the page title text.',
        hint="soup.title.get_text() extracts the text of the title tag.",
        code=(
            "from bs4 import BeautifulSoup\n"
            'soup = BeautifulSoup(html, "html.parser")\n'
            "print(soup.title.get_text())"
        ),
    ),
    dict(
        id="w03-07", week=3, difficulty=3,
        title="Extract table rows",
        topic="Web scraping",
        prompt='Loop over every tr element in soup and build a list of the stripped text of each td cell inside that row.',
        hint="Use find_all(\"tr\") then a list comprehension over row.find_all(\"td\") with get_text(strip=True).",
        code=(
            'for row in soup.find_all("tr"):\n'
            '    cells = [c.get_text(strip=True) for c in row.find_all("td")]'
        ),
    ),
    dict(
        id="w03-08", week=3, difficulty=2,
        title="Cache API results to disk",
        topic="File I/O",
        prompt='Write the payload dictionary to data.json as indented JSON with 2-space indentation, using a with block and a file handle named f.',
        hint='Open with open("data.json", "w") and use json.dump(payload, f, indent=2).',
        code='with open("data.json", "w") as f:\n    json.dump(payload, f, indent=2)',
    ),

    # ---------------------------------------------------------------- WEEK 4
    dict(
        id="w04-01", week=4, difficulty=2,
        title="Tidy rows as a list of dicts",
        topic="Tidy data",
        prompt='Build a list called rows holding two dictionaries: city "KL" with temp 32, and city "SG" with temp 30. Then print the city of the first row.',
        hint="One dictionary per line, trailing comma between them.",
        code=(
            "rows = [\n"
            '    {"city": "KL", "temp": 32},\n'
            '    {"city": "SG", "temp": 30},\n'
            "]\n"
            'print(rows[0]["city"])'
        ),
    ),
    dict(
        id="w04-02", week=4, difficulty=2,
        title="Pull one column into a list",
        topic="Comprehensions",
        prompt='Using a list comprehension over rows, collect every row\'s "temp" value into temps, then print the average of temps.',
        hint="[row[\"temp\"] for row in rows], then sum(temps) / len(temps).",
        code=(
            'temps = [row["temp"] for row in rows]\n'
            "print(sum(temps) / len(temps))"
        ),
    ),
    dict(
        id="w04-03", week=4, difficulty=2,
        title="Column-oriented storage",
        topic="Data structures",
        prompt="Build a dictionary called columns mapping the key city to the list [\"KL\", \"SG\"] and temp to the list [32, 30], then print the number of cities.",
        hint='len(columns["city"]).',
        code=(
            'columns = {"city": ["KL", "SG"], "temp": [32, 30]}\n'
            'print(len(columns["city"]))'
        ),
    ),
    dict(
        id="w04-04", week=4, difficulty=2,
        title="Unique values with a set",
        topic="Sets",
        prompt='Create a set called cities containing "KL", "SG" and a repeated "KL", then print how many unique values it holds.',
        hint="Sets drop duplicates automatically; use len().",
        code='cities = {"KL", "SG", "KL"}\nprint(len(cities))',
    ),
    dict(
        id="w04-05", week=4, difficulty=1,
        title="Tuple unpacking",
        topic="Tuples",
        prompt="Unpack the tuple (1, 2) into variables first and second, then print their sum.",
        hint="first, second = (1, 2) on a single line.",
        code="first, second = (1, 2)\nprint(first + second)",
    ),
    dict(
        id="w04-06", week=4, difficulty=3,
        title="Count categories with defaultdict",
        topic="Collections",
        prompt='Import defaultdict from collections, create counts with int as the default factory, count the values in the list ["KL", "SG", "KL"] by incrementing counts[city], then print counts.',
        hint="defaultdict(int) starts every missing key at 0.",
        code=(
            "from collections import defaultdict\n"
            "\n"
            "counts = defaultdict(int)\n"
            'for city in ["KL", "SG", "KL"]:\n'
            "    counts[city] += 1\n"
            "print(counts)"
        ),
    ),
    dict(
        id="w04-07", week=4, difficulty=2,
        title="Sort rows by a column",
        topic="Sorting",
        prompt='Sort the list rows in place by the "temp" key in descending order using a lambda key function.',
        hint='rows.sort(key=lambda r: r["temp"], reverse=True).',
        code='rows.sort(key=lambda r: r["temp"], reverse=True)',
    ),

    # ---------------------------------------------------------------- WEEK 5
    dict(
        id="w05-01", week=5, difficulty=2,
        title="Load a CSV into a DataFrame",
        topic="Pandas I/O",
        prompt='Import pandas as pd, load "data.csv" into a DataFrame called df, then print its shape.',
        hint="pd.read_csv() then df.shape.",
        code='import pandas as pd\n\ndf = pd.read_csv("data.csv")\nprint(df.shape)',
    ),
    dict(
        id="w05-02", week=5, difficulty=1,
        title="Preview the top and bottom rows",
        topic="Pandas inspection",
        prompt="Print the first five rows of df, then the last three rows.",
        hint="df.head() defaults to five rows; df.tail(3) gives three.",
        code="print(df.head())\nprint(df.tail(3))",
    ),
    dict(
        id="w05-03", week=5, difficulty=1,
        title="Inspect schema and dtypes",
        topic="Pandas inspection",
        prompt="Print a concise schema summary of df that shows column names, non-null counts and dtypes.",
        hint="df.info() prints exactly that summary.",
        code="df.info()",
    ),
    dict(
        id="w05-04", week=5, difficulty=2,
        title="Select a column",
        topic="Pandas selection",
        prompt='Store the "temp" column of df in temps, then print its maximum value.',
        hint='df["temp"] selects a Series; .max() reduces it.',
        code='temps = df["temp"]\nprint(temps.max())',
    ),
    dict(
        id="w05-05", week=5, difficulty=2,
        title="Filter rows with a condition",
        topic="Pandas filtering",
        prompt='Keep only the rows of df where "temp" is greater than 30, store them in hot, then print the first five rows of hot.',
        hint='df[df["temp"] > 30].head().',
        code='hot = df[df["temp"] > 30]\nprint(hot.head())',
    ),
    dict(
        id="w05-06", week=5, difficulty=3,
        title="Combine two filter conditions",
        topic="Pandas filtering",
        prompt='Select the rows of df where "temp" is above 30 AND "city" equals "KL", wrapping each condition in brackets and joining them with an ampersand.',
        hint='df[(df["temp"] > 30) & (df["city"] == "KL")].',
        code='hot = df[(df["temp"] > 30) & (df["city"] == "KL")]',
    ),
    dict(
        id="w05-07", week=5, difficulty=2,
        title="Count missing values",
        topic="Missing data",
        prompt="Print the number of missing values per column in df, then drop every row that contains a missing value and reassign the result to df.",
        hint="df.isna().sum(), then df = df.dropna().",
        code="print(df.isna().sum())\ndf = df.dropna()",
    ),
    dict(
        id="w05-08", week=5, difficulty=3,
        title="Impute missing values with the mean",
        topic="Missing data",
        prompt='Fill the missing values in the "temp" column of df with that column\'s mean, assigning the result back to the column.',
        hint='df["temp"].fillna(df["temp"].mean()).',
        code='df["temp"] = df["temp"].fillna(df["temp"].mean())',
    ),
    dict(
        id="w05-09", week=5, difficulty=3,
        title="Label and positional indexing",
        topic="Pandas indexing",
        prompt='Print the "temp" value of the first row using .loc with labels, then print the first five rows of the first column using .iloc.',
        hint='df.loc[0, "temp"] and df.iloc[:5, 0].',
        code='print(df.loc[0, "temp"])\nprint(df.iloc[:5, 0])',
    ),

    # ---------------------------------------------------------------- WEEK 6
    dict(
        id="w06-01", week=6, difficulty=3,
        title="Review: load, clean, filter",
        topic="Mid-term review",
        prompt='Load "data.csv" into df, drop missing rows, then keep rows where "sales" exceeds 100 and print the shape of the result.',
        hint="Three steps chained over three statements; use df.shape at the end.",
        code=(
            'import pandas as pd\n'
            '\n'
            'df = pd.read_csv("data.csv")\n'
            "df = df.dropna()\n"
            'big = df[df["sales"] > 100]\n'
            "print(big.shape)"
        ),
    ),
    dict(
        id="w06-02", week=6, difficulty=3,
        title="Review: API response to DataFrame",
        topic="Mid-term review",
        prompt='Fetch https://api.example.com/sales, raise for errors, convert the JSON reply to a DataFrame and print its columns as a list.',
        hint="requests.get(...).raise_for_status(), then pd.DataFrame(response.json()), then list(df.columns).",
        code=(
            "import requests\n"
            "import pandas as pd\n"
            "\n"
            'response = requests.get("https://api.example.com/sales")\n'
            "response.raise_for_status()\n"
            "df = pd.DataFrame(response.json())\n"
            "print(list(df.columns))"
        ),
    ),
    dict(
        id="w06-03", week=6, difficulty=3,
        title="Review: scraped rows to DataFrame",
        topic="Mid-term review",
        prompt='Parse the html string into soup, build a list called rows of dictionaries with keys "name" and "price" from each div with class "product", then print the DataFrame length.',
        hint="Use find_all(\"div\", class_=\"product\") inside a comprehension, then pd.DataFrame(rows).",
        code=(
            "from bs4 import BeautifulSoup\n"
            "import pandas as pd\n"
            "\n"
            'soup = BeautifulSoup(html, "html.parser")\n'
            'rows = [\n'
            '    {"name": d.find("h2").get_text(), "price": d.find("span").get_text()}\n'
            '    for d in soup.find_all("div", class_="product")\n'
            "]\n"
            "print(len(pd.DataFrame(rows)))"
        ),
    ),
    dict(
        id="w06-04", week=6, difficulty=2,
        title="Review: value counts as a dictionary",
        topic="Mid-term review",
        prompt='Using a dictionary comprehension over the set of cities in the list cities, count occurrences with the .count method.',
        hint="{c: cities.count(c) for c in set(cities)}.",
        code="counts = {c: cities.count(c) for c in set(cities)}\nprint(counts)",
    ),
    dict(
        id="w06-05", week=6, difficulty=3,
        title="Review: loop over DataFrame rows",
        topic="Mid-term review",
        prompt='Iterate over df with iterrows, unpacking index and row, and print the "city" value of each row.',
        hint="for index, row in df.iterrows(): then print(row[\"city\"]).",
        code='for index, row in df.iterrows():\n    print(row["city"])',
    ),
    dict(
        id="w06-06", week=6, difficulty=3,
        title="Review: selective CSV load",
        topic="Mid-term review",
        prompt='Read only the columns "city" and "temp" from "data.csv", forcing the "temp" column to the float dtype.',
        hint='pd.read_csv with usecols and dtype as dictionaries.',
        code=(
            'df = pd.read_csv(\n'
            '    "data.csv",\n'
            '    usecols=["city", "temp"],\n'
            '    dtype={"temp": float},\n'
            ")"
        ),
    ),

    # ---------------------------------------------------------------- WEEK 7
    dict(
        id="w07-01", week=7, difficulty=2,
        title="Group and aggregate",
        topic="GroupBy",
        prompt='Group df by "city", take the "temp" column and print the mean temperature per city.',
        hint='df.groupby("city")["temp"].mean().',
        code='print(df.groupby("city")["temp"].mean())',
    ),
    dict(
        id="w07-02", week=7, difficulty=3,
        title="Multiple aggregations per group",
        topic="GroupBy",
        prompt='Group df by "city" and produce both the mean and the maximum of the "temp" column in one aggregation call.',
        hint='.agg({"temp": ["mean", "max"]}).',
        code='summary = df.groupby("city").agg({"temp": ["mean", "max"]})\nprint(summary)',
    ),
    dict(
        id="w07-03", week=7, difficulty=3,
        title="Merge two DataFrames",
        topic="Joins",
        prompt='Left-join the orders DataFrame with customers on the key "customer_id" and store the result in merged.',
        hint="pd.merge(..., on=..., how=\"left\").",
        code='merged = pd.merge(orders, customers, on="customer_id", how="left")',
    ),
    dict(
        id="w07-04", week=7, difficulty=3,
        title="Stack rows with concat",
        topic="Concatenation",
        prompt="Vertically stack df1 and df2 into full, rebuilding the index instead of keeping the original labels.",
        hint="pd.concat([df1, df2], ignore_index=True).",
        code="full = pd.concat([df1, df2], ignore_index=True)",
    ),
    dict(
        id="w07-05", week=7, difficulty=2,
        title="Sort a DataFrame",
        topic="Sorting",
        prompt='Sort df by "temp" in descending order, assigning the sorted frame back to df, then print the first five rows.',
        hint='df.sort_values("temp", ascending=False).head().',
        code='df = df.sort_values("temp", ascending=False)\nprint(df.head())',
    ),
    dict(
        id="w07-06", week=7, difficulty=1,
        title="Count category frequencies",
        topic="Pandas inspection",
        prompt='Print how many times each distinct value appears in the "city" column of df.',
        hint='df["city"].value_counts().',
        code='print(df["city"].value_counts())',
    ),
    dict(
        id="w07-07", week=7, difficulty=3,
        title="Create a derived column",
        topic="Feature engineering",
        prompt='Add a column "fahrenheit" to df computed from "temp" with the lambda t: t * 9 / 5 + 32 applied through .apply.',
        hint='df["fahrenheit"] = df["temp"].apply(lambda t: ...).',
        code='df["fahrenheit"] = df["temp"].apply(lambda t: t * 9 / 5 + 32)',
    ),
    dict(
        id="w07-08", week=7, difficulty=3,
        title="Pivot table",
        topic="Reshaping",
        prompt='Build a pivot table called pivot with "city" as the index, "month" as the columns, mean of "temp" as values.',
        hint="df.pivot_table(index=..., columns=..., values=..., aggfunc=\"mean\").",
        code=(
            "pivot = df.pivot_table(\n"
            '    index="city",\n'
            '    columns="month",\n'
            '    values="temp",\n'
            '    aggfunc="mean",\n'
            ")"
        ),
    ),
]
