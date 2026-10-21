# -*- coding: utf-8 -*-
"""Plain-language explanations for weeks 1-7.

`explain` = what the snippet does and why, in one short paragraph.
`notes`   = one note per source line ("" for blank lines).
`gotcha`  = the mistake students usually make.
"""

EX_A = {
    # ---------------------------------------------------------------- WEEK 1
    "w01-01": dict(
        explain=(
            "Stores two pieces of information in named variables and then prints both at once. "
            "`name` holds text (a string) and `age` holds a whole number (an int). "
            "Passing two arguments to print separates the output with a single space: `Ada 28`."
        ),
        notes=[
            'Creates a variable `name` and assigns it the string "Ada". The quotes are part of the syntax, not the value.',
            "Creates `age` and assigns the integer 28 — no quotes, so Python treats it as a number.",
            "print() can take several arguments; it prints them separated by spaces, so this outputs: Ada 28",
        ],
        gotcha='Writing `age = "28"` makes it text, and `age + 1` would then fail with a TypeError.',
    ),
    "w01-02": dict(
        explain=(
            "Shows how Python classifies values. `10` is an int, `3.14` a float and `\"text\"` a str. "
            "`type()` reports the class of a value, so this prints three `<class ...>` objects and is the fastest way "
            "to debug a column that refuses to do maths."
        ),
        notes=[
            "An integer literal: a whole number, no decimal point.",
            "A float literal: the decimal point makes it floating point.",
            'A string literal: text inside quotes.',
            "type() returns the data type of each value, all printed on one line.",
        ],
        gotcha="`type` needs the parentheses — `print(type(x))` works, `print(type x)` is a syntax error.",
    ),
    "w01-03": dict(
        explain=(
            "Creates a list of three temperatures and prints the first one. "
            "Lists keep items in order and are written in square brackets. Indexing starts at 0, so `[0]` is the "
            "first element, `[1]` the second and `[-1]` the last."
        ),
        notes=[
            "A list literal: three floats in square brackets, separated by commas.",
            "Square brackets after the list name select an element; 0 means the first item, so this prints 21.5.",
        ],
        gotcha="`temperatures[3]` raises IndexError — the valid positions here are 0, 1 and 2.",
    ),
    "w01-04": dict(
        explain=(
            "Builds a dictionary that maps keys to values and looks one value up by its key. "
            "Dictionaries are the Python shape of a single table row: field name → field value."
        ),
        notes=[
            'A dict literal with two key/value pairs: "name" → "Ada" and "score" → 95.',
            'Look values up with dict[key], so this prints 95. The key must be spelled and quoted exactly.',
        ],
        gotcha='`student[score]` without quotes looks for a variable named `score` and raises NameError.',
    ),
    "w01-05": dict(
        explain=(
            "Demonstrates operator precedence and division. Multiplication happens before addition, so "
            "`10 + 5 * 2` is 20, not 30. Single `/` always returns a float, so the mean is 6.666…"
        ),
        notes=[
            "`5 * 2` is evaluated first, then added to 10 — total becomes 20.",
            "Single `/` performs true division and always returns a float.",
            "Prints 6.666666666666667 rather than a rounded value.",
        ],
        gotcha="Use `//` for floor division or `round(x, 2)` when you want a tidy number in a report.",
    ),
    "w01-06": dict(
        explain=(
            "Classifies a score into a letter grade using a chain of conditions. Python tests `if` first, then each "
            "`elif` in order, and runs only the first branch that is True; `else` is the fallback. "
            "The indented blocks are what makes each branch belong to its condition."
        ),
        notes=[
            "The value being tested. Change it to 95 and the grade becomes A.",
            "First test: is the score at least 90?",
            'Runs only when the test above was True. Four spaces of indentation define the block.',
            "Checked only if the first test failed; `>=` includes exactly 80.",
            "80–89 lands here.",
            "Catch-all branch when nothing above matched.",
            "Scores below 80 get a C.",
            "Printing outside the indented blocks shows the single grade that was assigned.",
        ],
        gotcha="Using `=` instead of `==` inside a condition is an assignment and raises a SyntaxError.",
    ),
    "w01-07": dict(
        explain=(
            "Repeats a block of code five times. `range(5)` yields 0, 1, 2, 3, 4 — five numbers, stopping before 5. "
            "Each pass binds the next number to `i`, and `**` raises it to the power of 2."
        ),
        notes=[
            "Loop header: `i` takes each value from range(5) in turn, and the colon opens the block.",
            "The indented body runs once per value, printing 0, 1, 4, 9, 16 on separate lines.",
        ],
        gotcha="`range(5)` gives 5 values starting at 0 — it does not include 5 itself.",
    ),
    "w01-08": dict(
        explain=(
            "Defines a reusable function that computes an average, then calls it once. "
            "`def` names the function and lists its parameters; `return` sends a value back to the caller instead of "
            "printing it, which is what makes the function composable."
        ),
        notes=[
            "Function definition: the name `mean` and one parameter, `values`.",
            "sum() adds the numbers, len() counts them, and the division returns the average to the caller.",
            "",
            "Calls the function with the list [2, 4, 6]; the printed result is 4.0.",
        ],
        gotcha="Forgetting `return` makes the function hand back `None`, so `print` would show None.",
    ),
    "w01-09": dict(
        explain=(
            "Grows a list one item at a time — the pattern behind building a table from scratch. "
            "It starts empty, loops over three names and appends each one, which is exactly how rows get "
            "accumulated before being turned into a DataFrame."
        ),
        notes=[
            "Starts with an empty list so append() has somewhere to add items.",
            "Loops over a list literal of three names.",
            "append() adds one item to the end of the list, growing it each pass.",
            "Prints the completed list: ['Ada', 'Grace', 'Alan'].",
        ],
        gotcha="`rows = rows.append(name)` sets rows to None — append changes the list in place and returns nothing.",
    ),

    # ---------------------------------------------------------------- WEEK 2
    "w02-01": dict(
        explain=(
            "Two terminal commands that get a project onto your machine: `git clone` downloads the repository "
            "together with its full commit history into a new folder, and `cd` moves your shell into that folder so "
            "later git commands act on it."
        ),
        notes=[
            "Downloads the repository from the URL into a new local folder named after the repo (`project`).",
            "Changes the working directory into that new folder.",
        ],
        gotcha="Run `git status` after `cd` to confirm you are inside a repository before committing.",
    ),
    "w02-02": dict(
        explain=(
            "The two-step save in git: `git add` stages the change (puts it in the next snapshot), and `git commit` "
            "records that snapshot with a message. Nothing is saved to history until the commit happens."
        ),
        notes=[
            "Stages `data.csv` — the file is now in the index, waiting to be committed.",
            'Creates a commit of everything staged, labelled with the message "Add raw dataset". The -m flag takes the message inline.',
        ],
        gotcha="`git commit` alone commits staged files only — a file you never `add`ed stays out of the snapshot.",
    ),
    "w02-03": dict(
        explain=(
            "Uploads local commits to the remote repository. The first argument is the remote name (`origin`, the "
            "default alias for the URL you cloned from) and the second is the branch you are pushing (`main`)."
        ),
        notes=[
            "Sends the current branch's commits to the remote called origin, branch main.",
        ],
        gotcha="If the remote has newer commits, the push is rejected — pull or rebase first.",
    ),
    "w02-04": dict(
        explain=(
            "Read-only inspection. `git status` shows which files are modified, staged or untracked, and "
            "`git log --oneline -5` shows the five most recent commits in a compact one-line-per-commit format."
        ),
        notes=[
            "Reports the working tree state: staged, modified and untracked files.",
            "--oneline compresses each commit to one line and -5 limits the output to the last five.",
        ],
        gotcha="`git log` can trap you in a pager — press q to return to the shell prompt.",
    ),
    "w02-05": dict(
        explain=(
            "In a Colab cell, a leading `!` runs the rest of the line as a shell command, so pip installs into the "
            "notebook's runtime. The import that follows uses `as` to give the library the conventional short alias."
        ),
        notes=[
            "The `!` escape runs this as a shell command on the Colab VM, not as Python.",
            "Imports pandas under the alias pd, the alias every tutorial and the rest of this course uses.",
        ],
        gotcha="The pip install is not needed on a fresh Colab VM — pandas ships with it, so the line is often a no-op.",
    ),
    "w02-06": dict(
        explain=(
            "Connects Colab to your Google Drive so files persist between sessions. `drive.mount` asks for "
            "authorisation and exposes your Drive under `/content/drive`, after which you can read CSVs with normal "
            "paths such as `/content/drive/MyDrive/data.csv`."
        ),
        notes=[
            "Imports just the `drive` helper from the google.colab package.",
            'Mounts your Drive at the given path; Colab shows a consent prompt the first time.',
        ],
        gotcha="Without mounting, the Colab VM is temporary — files you write disappear when the runtime resets.",
    ),

    # ---------------------------------------------------------------- WEEK 3
    "w03-01": dict(
        explain=(
            "Performs the simplest HTTP GET call. `requests.get` sends the request and returns a Response object; "
            "`status_code` is the HTTP status, where 200 means success and 4xx/5xx mean failure. "
            "Nothing is parsed yet — the body is still raw."
        ),
        notes=[
            "Imports the third-party requests library, which wraps HTTP in one-line calls.",
            "",
            "Sends a GET request to the URL and stores the whole Response object in `response`.",
            "Prints the HTTP status code — 200 for a successful request.",
        ],
        gotcha="A 404 or 500 does not raise an exception by default; you must check the status or call raise_for_status().",
    ),
    "w03-02": dict(
        explain=(
            "Sends query parameters and fails loudly on a bad response. `params=` builds `?page=2` for you and "
            "handles URL-encoding; `raise_for_status()` converts any 4xx/5xx status into an exception so broken data "
            "never silently flows into your pipeline."
        ),
        notes=[
            'Passes the dict as query parameters, producing url?page=2 in the request.',
            "Raises an HTTPError if the server answered with a client or server error status.",
        ],
        gotcha="Never hand-build `url + '?page=2'` — encoding breaks as soon as a value contains a space or an ampersand.",
    ),
    "w03-03": dict(
        explain=(
            "Turns the JSON text returned by an API into real Python objects. `json.loads` means “load string” and "
            "produces dicts and lists, which you then index like any other Python data — here the first element of "
            "the `items` list."
        ),
        notes=[
            "Imports the standard-library json module (no installation needed).",
            "Parses the response body text into Python dicts/lists. Note the s: loads = string in.",
            'Indexes the parsed dict by key, then takes element 0 of that list.',
        ],
        gotcha="`json.load` (no s) expects an already-open file object; `json.loads` expects text.",
    ),
    "w03-04": dict(
        explain=(
            "Goes the other way: converts a Python dict into a JSON string. `indent=2` pretty-prints with two spaces "
            "per level, which makes the payload readable in logs or before POSTing it somewhere."
        ),
        notes=[
            "A normal Python dict — JSON objects and Python dicts look alike but are not the same thing.",
            "json.dumps serialises it to text; indent=2 adds newlines and indentation for readability.",
        ],
        gotcha='Tuples become arrays and `None` becomes `null`; sets and DataFrames cannot be serialised directly.',
    ),
    "w03-05": dict(
        explain=(
            "Sends data to an API rather than asking for it. The `json=` keyword serialises the dict, sets the "
            "Content-Type header to application/json and attaches it as the request body. `response.json()` parses "
            "the reply straight into Python objects."
        ),
        notes=[
            "POSTs the dict as a JSON body — do not json.dumps it yourself when using the json= keyword.",
            "Parses the response body in one step instead of calling json.loads(response.text).",
        ],
        gotcha="Using `data=body` sends form-encoded text, not JSON, which many APIs reject with 415 or 400.",
    ),
    "w03-06": dict(
        explain=(
            "Parses an HTML page into a searchable tree. BeautifulSoup needs the markup plus a parser name; after "
            "that you navigate with `.title`, `.find` and `.find_all` instead of regexes. `get_text()` strips the "
            "tags and returns just the visible text."
        ),
        notes=[
            "Imports only the BeautifulSoup class from the bs4 package.",
            "Parses the HTML string and returns a navigable tree; html.parser is the built-in, dependency-free parser.",
            "Walks to the title tag and prints its inner text without any markup.",
        ],
        gotcha="BeautifulSoup does not fetch pages — pass it `requests.get(url).text` first.",
    ),
    "w03-07": dict(
        explain=(
            "Walks an HTML table. `find_all(\"tr\")` returns every table row, and for each row a list comprehension "
            "collects the text of its `td` cells. `strip=True` removes the surrounding whitespace and newlines that "
            "HTML formatting leaves behind, which is essential for clean data."
        ),
        notes=[
            "Loops over every table-row element in the document.",
            "List comprehension: for each cell in this row, take the stripped text, producing one string per column.",
        ],
        gotcha="Without `strip=True` you get values like '\\n    42\\n  ' which break numeric conversion later.",
    ),
    "w03-08": dict(
        explain=(
            "Caches an API payload as a local JSON file so you do not re-fetch it every run. `with open(...)` closes "
            "the file automatically even if an error occurs, and `json.dump` writes the Python object straight into "
            "that open file handle."
        ),
        notes=[
            'Opens data.json for writing ("w" overwrites) and binds the handle to `f` for the indented block.',
            "json.dump (no s) writes into the open file object, pretty-printed with two spaces.",
        ],
        gotcha='`json.dump` writes to a file handle; `json.dumps` returns a string — mixing them up corrupts the file.',
    ),

    # ---------------------------------------------------------------- WEEK 4
    "w04-01": dict(
        explain=(
            "The canonical tidy-data shape: a list where every dictionary is one row and every key is one column. "
            "All rows share the same keys, which is exactly what `pd.DataFrame(rows)` expects, and you address a "
            "single cell as `rows[row_index][column_name]`."
        ),
        notes=[
            "Opens a list literal; the entries are dictionaries, one per row.",
            'First row: city "KL" with temp 32.',
            'Second row, same keys in the same order — consistent keys are what makes it tidy.',
            "Closes the list.",
            'Row 0, then the "city" key of that row, printing KL.',
        ],
        gotcha="Rows with different key names become NaN-filled columns once converted to a DataFrame.",
    ),
    "w04-02": dict(
        explain=(
            "Extracts one column out of the row list, then summarises it. The list comprehension visits each row and "
            "keeps only the `temp` value, turning row-oriented data into a plain list you can run maths on."
        ),
        notes=[
            'Comprehension: for every row, take row["temp"] — result is [32, 30].',
            "sum()/len() is the manual way to compute a mean; the printed result is 31.0.",
        ],
        gotcha="A comprehension already builds the list — do not wrap it in another pair of square brackets.",
    ),
    "w04-03": dict(
        explain=(
            "The column-oriented alternative to a list of rows: one dict, one key per column, each value a list of "
            "that column's entries. Arrow-style tools and APIs often hand data back in this shape, and NumPy/pandas "
            "love it because each column is contiguous."
        ),
        notes=[
            'Two columns: "city" holds two strings, "temp" holds two numbers, positionally aligned.',
            'Counts the entries in the city column, printing 2.',
        ],
        gotcha="The lists must be the same length — a short column silently produces misaligned rows.",
    ),
    "w04-04": dict(
        explain=(
            "Sets store only unique values, so duplicates collapse on creation. This is the quickest way to answer "
            "“how many distinct categories are in this column?” without loading pandas."
        ),
        notes=[
            '"KL" appears twice in the literal but the set keeps it once, so the set is {"KL", "SG"}.',
            "len() on a set counts unique members, printing 2.",
        ],
        gotcha="Sets are unordered, so you cannot index them with [0] — use `sorted(cities)[0]` instead.",
    ),
    "w04-05": dict(
        explain=(
            "Unpacks a tuple into named variables in a single assignment. Python matches positions on the left to "
            "values on the right, which is the same mechanism `for index, row in df.iterrows()` relies on."
        ),
        notes=[
            "Two targets, two values — first gets 1, second gets 2.",
            "Adds them and prints 3.",
        ],
        gotcha="The counts must match: three names for a two-item tuple raises ValueError.",
    ),
    "w04-06": dict(
        explain=(
            "Counts how often each value occurs without an `if key in counts` check. `defaultdict(int)` invents a "
            "default of 0 the first time a key is seen, so `+= 1` always works. This is the manual version of "
            "`df[\"city\"].value_counts()`."
        ),
        notes=[
            "Imports defaultdict from the standard-library collections module.",
            "",
            "A dict whose missing keys default to int() — that is, 0.",
            'Loops over three city values, one of which repeats.',
            "First sighting of a key starts at 0, so this becomes 1; the repeat reaches 2.",
            "Prints defaultdict(<class 'int'>, {'KL': 2, 'SG': 1}).",
        ],
        gotcha="A plain `{}` raises KeyError on `counts[city] += 1` the first time a value appears.",
    ),
    "w04-07": dict(
        explain=(
            "Sorts the row list in place by a field. `key=` names the value to sort on (here a lambda that pulls "
            "`row[\"temp\"]`), and `reverse=True` puts the largest first. `list.sort()` mutates the list and returns "
            "None, unlike `sorted()` which returns a new list."
        ),
        notes=[
            'Sorts rows by the "temp" value, highest first. The lambda receives one row and returns its sort key.',
        ],
        gotcha="`rows = rows.sort(...)` assigns None — either call sort() alone or use sorted(rows, ...).",
    ),

    # ---------------------------------------------------------------- WEEK 5
    "w05-01": dict(
        explain=(
            "The entry point of nearly every pandas workflow: read a CSV into a DataFrame. "
            "`pd.read_csv` infers column names from the header and dtypes from the values; `df.shape` then reports "
            "(rows, columns), the fastest sanity check that the file loaded as expected."
        ),
        notes=[
            "Imports pandas under the universal alias pd.",
            "",
            'Reads data.csv from the working directory into a DataFrame called df.',
            "shape is a tuple (n_rows, n_cols), e.g. (1000, 5).",
        ],
        gotcha="A FileNotFoundError here almost always means the notebook's working directory is not where the CSV lives.",
    ),
    "w05-02": dict(
        explain=(
            "Sneak-peeks the frame. `head()` shows the first five rows and `tail(3)` the last three — useful for "
            "checking that the column names parsed correctly and that totals or trailing junk are not sitting at the "
            "end of the file."
        ),
        notes=[
            "First five rows, with the index on the left and every column across.",
            "Passing 3 overrides the default of five, giving the last three rows.",
        ],
        gotcha="head()/tail() only display — they do not modify df.",
    ),
    "w05-03": dict(
        explain=(
            "Prints a compact schema report: index range, every column name, how many non-null values it has and its "
            "dtype, plus memory usage. It is the one call that tells you whether a column is numeric or accidentally "
            "text, and whether gaps exist."
        ),
        notes=[
            "Prints the schema summary. Read the Dtype column: `object` means text, so maths will fail.",
        ],
        gotcha="If a numeric column shows `object`, some value in it is text — often a comma or a blank string.",
    ),
    "w05-04": dict(
        explain=(
            "Selects a single column, which pandas returns as a Series (one dimension), then reduces it to a single "
            "number with `.max()`. `df[\"temp\"]` with one pair of brackets is a column; `df[[\"temp\"]]` with two "
            "would return a one-column DataFrame."
        ),
        notes=[
            'Single brackets select the column named "temp" and return a Series.',
            "max() reduces that whole Series to its largest value.",
        ],
        gotcha="`df[temp]` without quotes looks for a variable named temp and raises NameError.",
    ),
    "w05-05": dict(
        explain=(
            "Boolean filtering: `df[\"temp\"] > 30` produces a True/False Series, and using that inside `df[...]` "
            "keeps only the rows where it is True. Chain `.head()` to eyeball the survivors instead of printing "
            "thousands of rows."
        ),
        notes=[
            'The comparison builds a boolean mask; df[mask] returns only the rows where it is True.',
            "Shows the first five matching rows.",
        ],
        gotcha="The mask must come from the same DataFrame and the same index — compare df to df, not to a filtered copy.",
    ),
    "w05-06": dict(
        explain=(
            "Combines two conditions with `&` (element-wise AND). Each condition needs its own parentheses because "
            "`&` binds tighter than `>` and `==`, and Python's `and` cannot be used on Series at all."
        ),
        notes=[
            'Both masks are bracketed, then combined with & — rows must be above 30 AND in "KL" to survive.',
        ],
        gotcha='`and` raises “truth value of a Series is ambiguous”; always use `&`, `|` with parentheses.',
    ),
    "w05-07": dict(
        explain=(
            "Measures and then removes missing data. `isna()` marks every missing cell True and `.sum()` counts those "
            "per column; `dropna()` then removes any row containing at least one missing value. "
            "Check the counts first — dropping rows can quietly destroy most of a dataset."
        ),
        notes=[
            "isna() gives a True/False frame, sum() adds the Trues per column, so you see missing counts per column.",
            "Drops every row with at least one NaN and rebinds df to the result (dropna is not in place by default).",
        ],
        gotcha="`df.dropna()` without reassignment changes nothing — the result must be stored or passed inplace=True.",
    ),
    "w05-08": dict(
        explain=(
            "Imputes missing numbers with the column mean instead of deleting rows, preserving sample size. "
            "The right-hand side computes the mean of the non-missing values, `fillna` replaces the NaNs, and the "
            "result is assigned back into the same column."
        ),
        notes=[
            'Computes the mean of "temp" ignoring NaNs, fills each NaN with it, then overwrites the original column.',
        ],
        gotcha="This shrinks the column's variance and hides uncertainty — mention it as a limitation in any report.",
    ),
    "w05-09": dict(
        explain=(
            "Contrasts label-based and position-based indexing. `.loc[row_label, column_name]` works with names, "
            "while `.iloc[row_position, column_position]` works with integer offsets. "
            "Here `.loc` grabs one cell and `.iloc` grabs the first five rows of the first column."
        ),
        notes=[
            'Label-based: row with index label 0, column named "temp". Prints a single scalar.',
            "Position-based: rows 0-4 (stop 5 excluded) from column position 0. Returns a Series.",
        ],
        gotcha="With a non-default index, `df.loc[0]` may not be the first row — that is exactly why iloc exists.",
    ),

    # ---------------------------------------------------------------- WEEK 6
    "w06-01": dict(
        explain=(
            "A five-line mini-pipeline that reviews Weeks 2–5: import, load, clean, filter, report. "
            "Each step is a separate statement so you can inspect the frame in between — this is how you should build "
            "every analysis before collapsing it into one chain."
        ),
        notes=[
            "Import the one library the snippet needs.",
            "",
            "Load the raw file.",
            "Drop the incomplete rows before any counting.",
            'Keep only rows where "sales" beats 100.',
            "Report the surviving size as (rows, columns).",
        ],
        gotcha="Filtering before dropping NaNs and after gives different counts — always clean first, then filter.",
    ),
    "w06-02": dict(
        explain=(
            "Moves data from the web into pandas in one pass: fetch, check, decode, tabulate. "
            "`response.json()` produces a list of dicts, `pd.DataFrame(...)` turns it into a table, and "
            "`list(df.columns)` confirms the API's field names arrived as columns."
        ),
        notes=[
            "Imports for the HTTP call.",
            "Imports pandas for the table.",
            "",
            "Fetches the endpoint.",
            "Raises immediately if the status is 4xx/5xx.",
            "Converts the decoded JSON (a list of dicts) into a DataFrame — keys become columns.",
            "Prints the column names as a plain Python list.",
        ],
        gotcha="If the JSON is nested (records under a key), build the frame from `response.json()[\"items\"]` instead.",
    ),
    "w06-03": dict(
        explain=(
            "Scraping straight into a table. For each product card, a dict is built from the two nested elements that "
            "hold the name and price; the resulting list of dicts becomes a DataFrame. "
            "This is the standard “parse repeated blocks into rows” recipe."
        ),
        notes=[
            "HTML parser import.",
            "pandas import for the final table.",
            "",
            "Parses the page markup into a searchable tree.",
            "Starts the rows list; each entry will be one product.",
            'Per card: find the h2 for the name and the span for the price, taking text from each.',
            'Drives the comprehension — every div whose class is "product" contributes one row.',
            "Closes the list.",
            "Builds the DataFrame and prints its row count.",
        ],
        gotcha="If a card lacks an h2, `.find(...)` returns None and `.get_text()` raises AttributeError — guard with a try or `if`.",
    ),
    "w06-04": dict(
        explain=(
            "Counts occurrences of each distinct value using a dict comprehension. `set(cities)` gives the unique "
            "names and `list.count` counts each one, producing the same dict as `value_counts().to_dict()` but "
            "without pandas."
        ),
        notes=[
            "For each unique city, map it to how many times it appears — the comprehension builds the whole dict.",
            "Prints something like {'KL': 2, 'SG': 1}.",
        ],
        gotcha="This rescans the list once per unique value — fine for small lists, O(n²) for large ones.",
    ),
    "w06-05": dict(
        explain=(
            "Iterates a DataFrame row by row. `iterrows()` yields an (index, Series) pair per row, which is why two "
            "names go on the left. It is readable but slow — vectorised column operations are the preferred default."
        ),
        notes=[
            "Unpacks each row into its label and a Series of that row's values.",
            'Prints the "city" field of the current row.',
        ],
        gotcha="Values may be upcast when a row mixes dtypes, so iterrows can silently turn ints into floats.",
    ),
    "w06-06": dict(
        explain=(
            "Reads only what you need. `usecols` skips unwanted columns at parse time (much faster on wide files) and "
            "`dtype` forces a column's type so IDs keep leading zeros and numeric columns already behave like numbers."
        ),
        notes=[
            "Opens the read_csv call; arguments are split across lines for readability.",
            "The path to the file.",
            "Keeps only these two columns, discarding the rest while reading.",
            'Forces "temp" to float — useful when the raw column contains blanks or text.',
            "Trailing comma and close bracket — valid formatting.",
        ],
        gotcha='Read most ID-like columns as `str`, otherwise pandas strips leading zeros from values such as "007".',
    ),

    # ---------------------------------------------------------------- WEEK 7
    "w07-01": dict(
        explain=(
            "Split-apply-combine in a single line: `groupby(\"city\")` forms one group per distinct city, selecting "
            "`[\"temp\"]` narrows to that column, and `.mean()` collapses each group to one number. "
            "The result is a Series indexed by city."
        ),
        notes=[
            'Groups rows by city, keeps the temp column, averages within each group and prints the Series.',
        ],
        gotcha="groupby drops NaN keys by default — add dropna=False if missing categories matter.",
    ),
    "w07-02": dict(
        explain=(
            "Produces several statistics per group at once with `.agg({column: [functions]})`. "
            "The output has a MultiIndex column header (temp → mean, temp → max), which is why the result is often "
            "flattened before charting or exporting."
        ),
        notes=[
            'One aggregation call returning both the mean and the maximum of "temp" per city.',
            "Prints a two-level column table, one row per city.",
        ],
        gotcha="After .agg with a list you get MultiIndex columns — use `.columns = ['_'.join(c) for c in ...]` to flatten.",
    ),
    "w07-03": dict(
        explain=(
            "Joins two tables on a shared key. `how=\"left\"` keeps every row of `orders` and attaches matching "
            "customer fields where available, leaving NaN where there is no match — the safe default when the left "
            "table is your primary data."
        ),
        notes=[
            'Matches rows where customer_id is equal in both frames; keeps all orders even without a customer match.',
        ],
        gotcha='An inner join silently drops unmatched orders — check `merged["customer_id"].isna().sum()` after a left join.',
    ),
    "w07-04": dict(
        explain=(
            "Stacks DataFrames vertically, one on top of the other, useful for combining monthly exports that share "
            "columns. `ignore_index=True` renumbers rows 0..n so the original labels do not repeat and confuse `.loc`."
        ),
        notes=[
            "Concatenates the two frames row-wise; ignore_index rebuilds a clean 0..n-1 index.",
        ],
        gotcha="Without ignore_index you get duplicate index values, and later `.loc[0]` returns several rows.",
    ),
    "w07-05": dict(
        explain=(
            "Orders rows by a column's values. `ascending=False` puts the largest first; the sorted frame is assigned "
            "back to `df` because `sort_values` returns a new object rather than sorting in place."
        ),
        notes=[
            "Sorts by temp, biggest first, and rebinds df to the sorted copy.",
            "Confirms the new order with the first five rows.",
        ],
        gotcha="`.sort(inplace=True)` is deprecated for DataFrames — use `.sort_values(...)` and reassign.",
    ),
    "w07-06": dict(
        explain=(
            "Counts how often each distinct value appears in a column and returns it sorted from most to least "
            "frequent. The result is a Series indexed by the category, which is the quickest categorical profile you "
            "can run on a new dataset."
        ),
        notes=[
            'Tallies each distinct value in "city", descending by count.',
        ],
        gotcha="Add `normalize=True` to get proportions, or `dropna=False` to include missing values in the tally.",
    ),
    "w07-07": dict(
        explain=(
            "Adds a new computed column by applying a function element-wise. The lambda converts each temperature to "
            "Fahrenheit and the result is assigned to a new column name — the standard feature-engineering move "
            "before modelling."
        ),
        notes=[
            '"temp" goes through the lambda t: t*9/5+32 for every row, and the outputs become a new column.',
        ],
        gotcha="Vectorised arithmetic (`df[\"temp\"] * 9 / 5 + 32`) is the same result and much faster than apply.",
    ),
    "w07-08": dict(
        explain=(
            "Reshapes long data into a matrix: one row per city, one column per month, and the mean temperature in "
            "the cells. Pivot tables are how you turn tidy records into a comparison grid for a heatmap or report."
        ),
        notes=[
            "Starts the pivot_table call, wrapped across lines.",
            "Cities become the row labels.",
            "Months become the column headers.",
            "The numbers filling the grid come from the temp column.",
            "Where several rows share a cell, average them — this is the aggregation step.",
            "Closes the call; the result is a DataFrame indexed by city.",
        ],
        gotcha="Without aggfunc, duplicate city/month pairs raise a ValueError instead of being summarised.",
    ),
}
