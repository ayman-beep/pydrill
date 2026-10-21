# -*- coding: utf-8 -*-
"""Weeks 8-14 of the Introduction to Data Science Python curriculum."""

SNIPPETS_B = [
    # ---------------------------------------------------------------- WEEK 8
    dict(
        id="w08-01", week=8, difficulty=1,
        title="Create a NumPy array",
        topic="NumPy basics",
        prompt="Import numpy as np, build an array of 21.5, 23.0 and 19.8 called temps, then print its shape.",
        hint="np.array([...]) then temps.shape.",
        code="import numpy as np\n\ntemps = np.array([21.5, 23.0, 19.8])\nprint(temps.shape)",
    ),
    dict(
        id="w08-02", week=8, difficulty=2,
        title="Vectorised arithmetic",
        topic="NumPy basics",
        prompt="Convert the whole temps array from Fahrenheit to Celsius in one vectorised expression using (temps - 32) * 5 / 9.",
        hint="No loop and no brackets around the array are needed.",
        code="celsius = (temps - 32) * 5 / 9",
    ),
    dict(
        id="w08-03", week=8, difficulty=2,
        title="Boolean masking",
        topic="NumPy indexing",
        prompt="Keep only the entries of temps greater than 22, store them in hot, then print the mean of hot.",
        hint="temps[temps > 22] then .mean().",
        code="hot = temps[temps > 22]\nprint(hot.mean())",
    ),
    dict(
        id="w08-04", week=8, difficulty=2,
        title="Mean and standard deviation",
        topic="Descriptive statistics",
        prompt="Print the mean and the standard deviation of temps in a single print call using NumPy functions.",
        hint="np.mean(temps), np.std(temps).",
        code="print(np.mean(temps), np.std(temps))",
    ),
    dict(
        id="w08-05", week=8, difficulty=3,
        title="Build and reshape a grid",
        topic="NumPy shapes",
        prompt="Create a 3 by 4 array called grid from the integers 0 to 11 using arange and reshape.",
        hint="np.arange(12).reshape(3, 4).",
        code="grid = np.arange(12).reshape(3, 4)",
    ),
    dict(
        id="w08-06", week=8, difficulty=1,
        title="Five-number summary",
        topic="Descriptive statistics",
        prompt="Print the descriptive statistics table (count, mean, std, min, quartiles, max) for all numeric columns of df.",
        hint="df.describe() covers this in one call.",
        code="print(df.describe())",
    ),
    dict(
        id="w08-07", week=8, difficulty=2,
        title="Mean versus median",
        topic="Descriptive statistics",
        prompt='Print the mean and then the median of the "temp" column of df in a single print call, separated by a comma.',
        hint='df["temp"].mean(), df["temp"].median().',
        code='print(df["temp"].mean(), df["temp"].median())',
    ),

    # ---------------------------------------------------------------- WEEK 9
    dict(
        id="w09-01", week=9, difficulty=2,
        title="Line plot with Matplotlib",
        topic="Matplotlib",
        prompt='Import matplotlib.pyplot as plt, plot the "temp" column of df as a line, add the title "Temperature" and show the figure.',
        hint="plt.plot(), plt.title(), plt.show().",
        code=(
            "import matplotlib.pyplot as plt\n"
            "\n"
            'plt.plot(df["temp"])\n'
            'plt.title("Temperature")\n'
            "plt.show()"
        ),
    ),
    dict(
        id="w09-02", week=9, difficulty=2,
        title="Scatter plot with axis labels",
        topic="Matplotlib",
        prompt='Scatter "temp" against "sales" from df, label the x axis "Temp" and display the figure.',
        hint="plt.scatter(df[\"temp\"], df[\"sales\"]), plt.xlabel, plt.show().",
        code=(
            'plt.scatter(df["temp"], df["sales"])\n'
            'plt.xlabel("Temp")\n'
            "plt.show()"
        ),
    ),
    dict(
        id="w09-03", week=9, difficulty=2,
        title="Histogram of a column",
        topic="Matplotlib",
        prompt='Draw a histogram of the "temp" column of df using 20 bins, then show the figure.',
        hint="plt.hist with the bins keyword.",
        code='plt.hist(df["temp"], bins=20)\nplt.show()',
    ),
    dict(
        id="w09-04", week=9, difficulty=3,
        title="Seaborn scatter with hue",
        topic="Seaborn",
        prompt='Import seaborn as sns, draw a scatterplot of "temp" against "sales" from df coloured by "city", then show it.',
        hint='sns.scatterplot(data=df, x=..., y=..., hue=...).',
        code=(
            "import seaborn as sns\n"
            "\n"
            'sns.scatterplot(data=df, x="temp", y="sales", hue="city")\n'
            "plt.show()"
        ),
    ),
    dict(
        id="w09-05", week=9, difficulty=2,
        title="Compare distributions across groups",
        topic="Seaborn",
        prompt='Draw a boxplot of "sales" per "city" from df and show the figure.',
        hint='sns.boxplot(data=df, x="city", y="sales").',
        code='sns.boxplot(data=df, x="city", y="sales")\nplt.show()',
    ),
    dict(
        id="w09-06", week=9, difficulty=2,
        title="Correlation matrix",
        topic="EDA",
        prompt="Print the pairwise correlation matrix of df, considering only numeric columns.",
        hint="df.corr(numeric_only=True).",
        code="print(df.corr(numeric_only=True))",
    ),
    dict(
        id="w09-07", week=9, difficulty=3,
        title="Subplots and saving a figure",
        topic="Matplotlib",
        prompt='Create a figure and axes with a size of 8 by 5, draw a bar chart of "sales" per "city" on the axes, then save the figure as plot.png at 150 dpi.',
        hint="fig, ax = plt.subplots(figsize=(8, 5)), ax.bar(...), fig.savefig(...).",
        code=(
            "fig, ax = plt.subplots(figsize=(8, 5))\n"
            'ax.bar(df["city"], df["sales"])\n'
            'fig.savefig("plot.png", dpi=150)'
        ),
    ),

    # ---------------------------------------------------------------- WEEK 10
    dict(
        id="w10-01", week=10, difficulty=3,
        title="Split into train and test sets",
        topic="Model validation",
        prompt="Import train_test_split from sklearn.model_selection and split X and y with a 20 percent test size and random_state 42, unpacking into X_train, X_test, y_train, y_test.",
        hint="Four names on the left-hand side in that exact order.",
        code=(
            "from sklearn.model_selection import train_test_split\n"
            "\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y, test_size=0.2, random_state=42\n"
            ")"
        ),
    ),
    dict(
        id="w10-02", week=10, difficulty=2,
        title="Fit a linear regression",
        topic="Linear regression",
        prompt="Import LinearRegression, instantiate it into model and fit it on X_train and y_train.",
        hint="model = LinearRegression() then model.fit(X_train, y_train).",
        code=(
            "from sklearn.linear_model import LinearRegression\n"
            "\n"
            "model = LinearRegression()\n"
            "model.fit(X_train, y_train)"
        ),
    ),
    dict(
        id="w10-03", week=10, difficulty=1,
        title="Predict on unseen data",
        topic="Linear regression",
        prompt="Generate predictions for X_test with the fitted model, store them in predictions and print the first five.",
        hint="model.predict(X_test) then predictions[:5].",
        code="predictions = model.predict(X_test)\nprint(predictions[:5])",
    ),
    dict(
        id="w10-04", week=10, difficulty=2,
        title="Inspect learned coefficients",
        topic="Linear regression",
        prompt="Print the fitted model's coefficients and its intercept in a single print call.",
        hint="model.coef_, model.intercept_.",
        code="print(model.coef_, model.intercept_)",
    ),
    dict(
        id="w10-05", week=10, difficulty=3,
        title="Evaluate with R squared",
        topic="Model metrics",
        prompt="Import r2_score and mean_squared_error from sklearn.metrics, then print the R squared score of predictions against y_test.",
        hint="Only one of the two imported functions is needed for the print.",
        code=(
            "from sklearn.metrics import mean_squared_error, r2_score\n"
            "\n"
            "print(r2_score(y_test, predictions))"
        ),
    ),
    dict(
        id="w10-06", week=10, difficulty=2,
        title="Build the feature matrix and target",
        topic="Feature engineering",
        prompt='Create the feature matrix X from the columns "temp" and "humidity" of df, and the target vector y from the "sales" column.',
        hint="Double brackets keep the DataFrame shape for X.",
        code='X = df[["temp", "humidity"]]\ny = df["sales"]',
    ),
    dict(
        id="w10-07", week=10, difficulty=3,
        title="Scale features before fitting",
        topic="Preprocessing",
        prompt="Import StandardScaler, fit it on X, transform X into X_scaled and print the mean of X_scaled.",
        hint="scaler.fit_transform(X), then np.mean(X_scaled).",
        code=(
            "from sklearn.preprocessing import StandardScaler\n"
            "\n"
            "scaler = StandardScaler()\n"
            "X_scaled = scaler.fit_transform(X)\n"
            "print(np.mean(X_scaled))"
        ),
    ),

    # ---------------------------------------------------------------- WEEK 11
    dict(
        id="w11-01", week=11, difficulty=3,
        title="Train a decision tree classifier",
        topic="Decision trees",
        prompt="Import DecisionTreeClassifier, build a tree with maximum depth 3 and random_state 42, then fit it on X_train and y_train.",
        hint="DecisionTreeClassifier(max_depth=3, random_state=42).",
        code=(
            "from sklearn.tree import DecisionTreeClassifier\n"
            "\n"
            "model = DecisionTreeClassifier(max_depth=3, random_state=42)\n"
            "model.fit(X_train, y_train)"
        ),
    ),
    dict(
        id="w11-02", week=11, difficulty=3,
        title="Score a classifier",
        topic="Model metrics",
        prompt="Import accuracy_score and confusion_matrix, then print the accuracy of the model on X_test compared with y_test.",
        hint="accuracy_score(y_test, model.predict(X_test)).",
        code=(
            "from sklearn.metrics import accuracy_score, confusion_matrix\n"
            "\n"
            "print(accuracy_score(y_test, model.predict(X_test)))"
        ),
    ),
    dict(
        id="w11-03", week=11, difficulty=3,
        title="Visualise the tree structure",
        topic="Decision trees",
        prompt="Import plot_tree and draw the fitted model with the feature names taken from the columns of X and filled nodes, then show the figure.",
        hint="feature_names=list(X.columns), filled=True.",
        code=(
            "from sklearn.tree import plot_tree\n"
            "\n"
            'plot_tree(model, feature_names=list(X.columns), filled=True)\n'
            "plt.show()"
        ),
    ),
    dict(
        id="w11-04", week=11, difficulty=2,
        title="Decision tree regressor",
        topic="Decision trees",
        prompt="Import DecisionTreeRegressor, build tree with maximum depth 4, fit it on X_train and y_train, then print the first three predictions for X_test.",
        hint="tree.predict(X_test)[:3].",
        code=(
            "from sklearn.tree import DecisionTreeRegressor\n"
            "\n"
            "tree = DecisionTreeRegressor(max_depth=4)\n"
            "tree.fit(X_train, y_train)\n"
            "print(tree.predict(X_test)[:3])"
        ),
    ),
    dict(
        id="w11-05", week=11, difficulty=3,
        title="Rank feature importances",
        topic="Feature importance",
        prompt="Build a pandas Series from the model's feature_importances_ indexed by the columns of X, then print it sorted in ascending order.",
        hint="pd.Series(...).sort_values().",
        code=(
            "import pandas as pd\n"
            "\n"
            "print(\n"
            "    pd.Series(model.feature_importances_, index=X.columns).sort_values()\n"
            ")"
        ),
    ),
    dict(
        id="w11-06", week=11, difficulty=3,
        title="Cross-validate a model",
        topic="Model validation",
        prompt="Import cross_val_score, compute five-fold cross-validated scores for model on X and y, store them in scores and print the mean score.",
        hint="cv=5, then scores.mean().",
        code=(
            "from sklearn.model_selection import cross_val_score\n"
            "\n"
            "scores = cross_val_score(model, X, y, cv=5)\n"
            "print(scores.mean())"
        ),
    ),

    # ---------------------------------------------------------------- WEEK 12
    dict(
        id="w12-01", week=12, difficulty=3,
        title="Define a feed-forward network",
        topic="Neural networks",
        prompt='Import keras and layers from tensorflow, then build a Sequential model with a 16-unit relu Dense layer taking input_shape (4,) followed by a single-unit output layer.',
        hint="keras.Sequential([...]) with two layers.Dense entries.",
        code=(
            "from tensorflow import keras\n"
            "from tensorflow.keras import layers\n"
            "\n"
            "model = keras.Sequential([\n"
            '    layers.Dense(16, activation="relu", input_shape=(4,)),\n'
            "    layers.Dense(1),\n"
            "])"
        ),
    ),
    dict(
        id="w12-02", week=12, difficulty=2,
        title="Compile the network",
        topic="Neural networks",
        prompt='Compile the model with the adam optimiser, mean squared error loss and mean absolute error as the tracked metric.',
        hint='optimizer="adam", loss="mse", metrics=["mae"].',
        code='model.compile(optimizer="adam", loss="mse", metrics=["mae"])',
    ),
    dict(
        id="w12-03", week=12, difficulty=3,
        title="Train the network",
        topic="Neural networks",
        prompt="Train the model for 20 epochs with a batch size of 32 and 20 percent of the data held out for validation, saving the history object.",
        hint="model.fit(..., epochs=20, batch_size=32, validation_split=0.2).",
        code=(
            "history = model.fit(\n"
            "    X_train, y_train,\n"
            "    epochs=20,\n"
            "    batch_size=32,\n"
            "    validation_split=0.2,\n"
            ")"
        ),
    ),
    dict(
        id="w12-04", week=12, difficulty=2,
        title="Evaluate and predict",
        topic="Neural networks",
        prompt="Evaluate the trained model on X_test and y_test, unpacking into loss and mae, then print the model's predictions for the first three test rows.",
        hint="model.evaluate(...) then model.predict(X_test[:3]).",
        code=(
            "loss, mae = model.evaluate(X_test, y_test)\n"
            "print(model.predict(X_test[:3]))"
        ),
    ),
    dict(
        id="w12-05", week=12, difficulty=3,
        title="Multi-class output layer",
        topic="Neural networks",
        prompt='Add a dense output layer with 3 units and the softmax activation to the existing Sequential model, then compile it with the sparse categorical crossentropy loss.',
        hint="model.add(layers.Dense(...)) then compile with loss=\"sparse_categorical_crossentropy\".",
        code=(
            'model.add(layers.Dense(3, activation="softmax"))\n'
            'model.compile(optimizer="adam", loss="sparse_categorical_crossentropy")'
        ),
    ),
    dict(
        id="w12-06", week=12, difficulty=1,
        title="Inspect the architecture",
        topic="Neural networks",
        prompt="Print a summary of the model's layers and parameter counts, then print the number of trainable weights.",
        hint="model.summary() and model.count_params().",
        code="model.summary()\nprint(model.count_params())",
    ),

    # ---------------------------------------------------------------- WEEK 13
    dict(
        id="w13-01", week=13, difficulty=3,
        title="Capstone: end-to-end pipeline",
        topic="Capstone",
        prompt='Load "data.csv", drop missing values, split the features "temp" and "humidity" against the target "sales", fit a linear regression with train_test_split random_state 42 and print the test R squared.',
        hint="Load, clean, split, fit, score — five logical steps.",
        code=(
            "import pandas as pd\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.linear_model import LinearRegression\n"
            "\n"
            'df = pd.read_csv("data.csv").dropna()\n'
            'X = df[["temp", "humidity"]]\n'
            'y = df["sales"]\n'
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y, test_size=0.2, random_state=42\n"
            ")\n"
            "model = LinearRegression().fit(X_train, y_train)\n"
            "print(model.score(X_test, y_test))"
        ),
    ),
    dict(
        id="w13-02", week=13, difficulty=3,
        title="Capstone: API to clean frame",
        topic="Capstone",
        prompt='Fetch https://api.example.com/sales into response, convert the JSON body to a DataFrame, rename the column "Temp" to "temp" and print the missing value counts.',
        hint="requests.get, pd.DataFrame(response.json()), .rename(columns=...), .isna().sum().",
        code=(
            "import requests\n"
            "import pandas as pd\n"
            "\n"
            'response = requests.get("https://api.example.com/sales")\n'
            "df = pd.DataFrame(response.json())\n"
            'df = df.rename(columns={"Temp": "temp"})\n'
            "print(df.isna().sum())"
        ),
    ),
    dict(
        id="w13-03", week=13, difficulty=2,
        title="Capstone: quick EDA report",
        topic="Capstone",
        prompt='For each column in the numeric columns of df, print the column name together with its mean, using a loop over df.select_dtypes.',
        hint='Loop over df.select_dtypes(include="number").columns.',
        code=(
            'for col in df.select_dtypes(include="number").columns:\n'
            '    print(col, df[col].mean())'
        ),
    ),
    dict(
        id="w13-04", week=13, difficulty=3,
        title="Capstone: persist a trained model",
        topic="Capstone",
        prompt='Import joblib, save the fitted model to "model.joblib", then load it back into loaded_model.',
        hint="joblib.dump(model, ...) then joblib.load(...).",
        code=(
            "import joblib\n"
            "\n"
            'joblib.dump(model, "model.joblib")\n'
            'loaded_model = joblib.load("model.joblib")'
        ),
    ),
    dict(
        id="w13-05", week=13, difficulty=3,
        title="Capstone: report a group summary",
        topic="Capstone",
        prompt='Group df by "city", aggregate the mean of "sales" and the count of "temp", then reset the index so the result has default integer labels.',
        hint=".agg({...}).reset_index().",
        code=(
            "summary = (\n"
            '    df.groupby("city")\n'
            '    .agg({"sales": "mean", "temp": "count"})\n'
            "    .reset_index()\n"
            ")"
        ),
    ),

    # ---------------------------------------------------------------- WEEK 14
    dict(
        id="w14-01", week=14, difficulty=3,
        title="Final: reusable training function",
        topic="Final drills",
        prompt="Define a function train_model(X, y) that splits with test_size 0.2 and random_state 42, fits a LinearRegression and returns the r2_score on the test split.",
        hint="Define, split into four variables, fit with LinearRegression(), return r2_score(...).",
        code=(
            "def train_model(X, y):\n"
            "    X_train, X_test, y_train, y_test = train_test_split(\n"
            "        X, y, test_size=0.2, random_state=42\n"
            "    )\n"
            "    model = LinearRegression()\n"
            "    model.fit(X_train, y_train)\n"
            "    return r2_score(y_test, model.predict(X_test))"
        ),
    ),
    dict(
        id="w14-02", week=14, difficulty=3,
        title="Final: compare two models",
        topic="Final drills",
        prompt='Build a dictionary results mapping the names "tree" and "linear" to the five-fold cross-validation mean scores of the already-fitted model objects tree_model and linear_model.',
        hint="Two cross_val_score calls with cv=5 and .mean().",
        code=(
            "results = {\n"
            '    "tree": cross_val_score(tree_model, X, y, cv=5).mean(),\n'
            '    "linear": cross_val_score(linear_model, X, y, cv=5).mean(),\n'
            "}"
        ),
    ),
    dict(
        id="w14-03", week=14, difficulty=3,
        title="Final: two-panel visual report",
        topic="Final drills",
        prompt='Create a figure with 1 row and 2 columns of axes sized 12 by 4, draw a histogram of "sales" in the first panel and a scatter of "temp" against "sales" in the second, then show the figure.',
        hint="fig, axes = plt.subplots(1, 2, figsize=(12, 4)); use axes[0] and axes[1].",
        code=(
            "fig, axes = plt.subplots(1, 2, figsize=(12, 4))\n"
            'axes[0].hist(df["sales"], bins=20)\n'
            'axes[1].scatter(df["temp"], df["sales"])\n'
            "plt.show()"
        ),
    ),
    dict(
        id="w14-04", week=14, difficulty=2,
        title="Final: score new observations",
        topic="Final drills",
        prompt='Given the list new_rows of dictionaries with keys "temp" and "humidity", convert it to a DataFrame called new_X and print the model predictions.',
        hint="pd.DataFrame(new_rows) then model.predict(new_X).",
        code=(
            "new_X = pd.DataFrame(new_rows)\n"
            "print(model.predict(new_X))"
        ),
    ),
    dict(
        id="w14-05", week=14, difficulty=3,
        title="Final: reproducible run",
        topic="Final drills",
        prompt="Import numpy, pandas and matplotlib, then set the global random seed to 42 with NumPy and make the plots render inline with the matplotlib notebook magic.",
        hint="np.random.seed(42) and the %matplotlib inline magic comment.",
        code=(
            "import numpy as np\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n"
            "\n"
            "np.random.seed(42)\n"
            "%matplotlib inline"
        ),
    ),
]
