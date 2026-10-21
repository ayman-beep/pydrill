# -*- coding: utf-8 -*-
"""Plain-language explanations for weeks 8-14."""

EX_B = {
    # ---------------------------------------------------------------- WEEK 8
    "w08-01": dict(
        explain=(
            "Creates a NumPy array, the container pandas is built on. Unlike a list, an array has one dtype, a fixed "
            "shape and supports fast element-wise maths. `shape` reports its dimensions — a one-dimensional array of "
            "three numbers shows as (3,)."
        ),
        notes=[
            "Imports NumPy under the conventional alias np.",
            "",
            "np.array converts the Python list into a typed, vectorised array.",
            "shape is a tuple of dimensions; here (3,) means three elements in one dimension.",
        ],
        gotcha="A trailing comma in (3,) is what makes it a shape tuple — (3) is just the number 3.",
    ),
    "w08-02": dict(
        explain=(
            "Vectorisation: the arithmetic is applied to every element at once, with no loop. "
            "`(temps - 32) * 5 / 9` is the Fahrenheit→Celsius formula evaluated element-wise, and NumPy returns a new "
            "array of the same shape."
        ),
        notes=[
            "Subtracts 32 from every element, multiplies by 5 and divides by 9 — all in one expression, no loop.",
        ],
        gotcha="Never loop over an array for this; vectorised operations are orders of magnitude faster.",
    ),
    "w08-03": dict(
        explain=(
            "Boolean masking filters an array. `temps > 22` produces an array of True/False, and indexing with it "
            "keeps only the positions that are True. The filtered array is shorter, so it can be reduced immediately "
            "with `.mean()`."
        ),
        notes=[
            "The comparison builds a boolean mask; temps[mask] keeps only the entries that are True.",
            "Averaging the survivors — a conditional mean in two lines.",
        ],
        gotcha="The mask must have the same length as the array, or NumPy raises an IndexError.",
    ),
    "w08-04": dict(
        explain=(
            "Summarises a distribution with two numbers: the mean (centre) and the standard deviation (spread). "
            "Both are single function calls on the array, and both are computed on all elements at once."
        ),
        notes=[
            "Prints the average and then the standard deviation, separated by a space.",
        ],
        gotcha="np.std uses the population formula (ddof=0); pandas' `.std()` uses ddof=1 — they differ slightly.",
    ),
    "w08-05": dict(
        explain=(
            "Builds and reshapes a grid. `np.arange(12)` makes the numbers 0–11 and `.reshape(3, 4)` reinterprets "
            "them as 3 rows by 4 columns — no data is copied, the shape changes. "
            "This is the mental model you need before touching any matrix or image data."
        ),
        notes=[
            "arange(12) produces 0..11, and reshape(3, 4) arranges them into 3 rows of 4 columns.",
        ],
        gotcha="The total element count must match: reshape(3, 5) on 12 values raises ValueError.",
    ),
    "w08-06": dict(
        explain=(
            "One call that profiles every numeric column: count, mean, standard deviation, minimum, the three "
            "quartiles and the maximum. Comparing the mean with the median here immediately reveals skew, and the "
            "min/max reveal impossible outliers."
        ),
        notes=[
            "Prints the eight-row summary table for all numeric columns of df.",
        ],
        gotcha="Non-numeric columns are ignored — add `include=\"all\"` to see object columns too.",
    ),
    "w08-07": dict(
        explain=(
            "Compares the mean with the median of the same column. When they are close the distribution is roughly "
            "symmetric; when the mean is pulled far above the median, the tail is long on the right and the median is "
            "the more honest summary."
        ),
        notes=[
            'Prints the mean and the median of "temp" side by side for comparison.',
        ],
        gotcha="Both skip NaN by default — a large gap between the values can also come from many missing entries.",
    ),

    # ---------------------------------------------------------------- WEEK 9
    "w09-01": dict(
        explain=(
            "Draws a line chart of a column against its row order. `plt.plot` creates the line, `plt.title` labels "
            "it, and `plt.show()` renders the figure and clears the canvas — without it, plots can pile up or not "
            "appear in scripts."
        ),
        notes=[
            "Imports Matplotlib's pyplot interface under the conventional alias plt.",
            "",
            'Plots the "temp" column as a line, x = row index, y = value.',
            "Adds a title above the axes.",
            "Renders the figure — the point at which the plot actually appears.",
        ],
        gotcha="In a plain script nothing is drawn until `plt.show()` runs.",
    ),
    "w09-02": dict(
        explain=(
            "A scatter plot puts one numeric column on each axis so you can see the relationship between two "
            "variables — the visual step before fitting a regression. `plt.xlabel` names the horizontal axis; "
            "`plt.ylabel` is the usual companion."
        ),
        notes=[
            'x = "temp", y = "sales" — each row becomes one dot.',
            "Labels the horizontal axis so the chart is readable out of context.",
            "Displays the plot.",
        ],
        gotcha="Always label both axes and note units; an unlabelled scatter is unreadable a week later.",
    ),
    "w09-03": dict(
        explain=(
            "A histogram bins one numeric column and draws a bar per bin, revealing the distribution's shape "
            "(centre, spread, skew, gaps). `bins=20` controls the resolution: too few hides structure, too many turns "
            "the chart into noise."
        ),
        notes=[
            'Splits "temp" into 20 equal-width bins and draws how many rows fall in each.',
            "Shows the figure.",
        ],
        gotcha="Changing `bins` changes the apparent shape — try a couple of values before concluding anything.",
    ),
    "w09-04": dict(
        explain=(
            "Seaborn plots straight from a DataFrame using column names, and `hue` adds a third dimension by "
            "colouring points per category. This makes it easy to see whether one group sits apart from the others."
        ),
        notes=[
            "Imports Seaborn, which builds on Matplotlib and adds the data= interface.",
            "",
            'x and y name columns of df; hue shatters the points by city with a legend.',
            "show() is still Matplotlib's job — Seaborn draws onto the same canvas.",
        ],
        gotcha="With many categories `hue` becomes an unreadable rainbow — facet with `col=` or group instead.",
    ),
    "w09-05": dict(
        explain=(
            "A box plot compares a numeric distribution across categories: the box is the interquartile range, the "
            "line inside is the median, and the whiskers/points show spread and outliers. This is the fastest way to "
            "compare groups side by side."
        ),
        notes=[
            'One box per city, each summarising that city\'s sales distribution.',
            "Renders the figure.",
        ],
        gotcha="Box plots hide sample size — a wide box can come from 3 rows or 3000, so count groups too.",
    ),
    "w09-06": dict(
        explain=(
            "Computes pairwise Pearson correlation for all numeric columns, giving a value from -1 to +1 per pair. "
            "Use it to spot features that move together (multicollinearity) and to pick candidates for a scatter "
            "plot or a model."
        ),
        notes=[
            "numeric_only=True keeps text columns out; the output is a symmetric matrix with 1.0 on the diagonal.",
        ],
        gotcha="Correlation only measures linear association — a strong curved relationship can show r ≈ 0.",
    ),
    "w09-07": dict(
        explain=(
            "Uses the object-oriented Matplotlib API: create a figure and an axes first, draw on the axes, then save "
            "the whole figure. This is required once you have more than one panel, and it lets you export a "
            "publication-quality PNG instead of only showing it."
        ),
        notes=[
            "fig is the whole canvas, ax is the single plotting area inside it; figsize is inches.",
            "Draws a bar per category using the axes object rather than the global plt state.",
            'Writes plot.png at 150 dpi — call this before show(), which clears the figure.',
        ],
        gotcha="savefig after show() gives a blank image, because show() clears the canvas.",
    ),

    # ---------------------------------------------------------------- WEEK 10
    "w10-01": dict(
        explain=(
            "Splits features (X) and target (y) into a training set and a held-out test set. "
            "`test_size=0.2` holds back 20% for honest evaluation and `random_state=42` makes the split reproducible. "
            "The order of the four returned objects is fixed, so the names must match that order."
        ),
        notes=[
            "Imports only the splitting helper from scikit-learn.",
            "",
            "Four outputs in a fixed order: X_train, X_test, y_train, y_test.",
            "20% held out for testing, seeded so every run splits identically.",
            "Closes the call — the four names above now receive the split data.",
        ],
        gotcha="Swapping the order silently gives you a model trained on y — check shapes if scores look absurd.",
    ),
    "w10-02": dict(
        explain=(
            "Instantiates and fits a linear regression. `LinearRegression()` creates an unfitted object; "
            "`.fit(X_train, y_train)` learns one coefficient per feature plus an intercept, minimising squared error. "
            "The object now holds the model and can predict."
        ),
        notes=[
            "Imports the linear regression estimator.",
            "",
            "Creates the estimator with default settings — still unfitted at this point.",
            "Learns the coefficients from the training rows.",
        ],
        gotcha="fit() takes (features, target) in that order — passing y first raises a confusing shape error.",
    ),
    "w10-03": dict(
        explain=(
            "Applies the fitted model to unseen rows. `predict` takes a feature matrix shaped like the training data "
            "and returns one prediction per row; slicing `[:5]` just keeps the output readable."
        ),
        notes=[
            "Runs the model on the held-out features and stores one number per row.",
            "Shows the first five predictions.",
        ],
        gotcha="Passing a single row without the column structure (`X_test.iloc[0]`) triggers a feature-count error.",
    ),
    "w10-04": dict(
        explain=(
            "Inspects what the model learned. `coef_` holds one slope per feature — the change in the target per "
            "one-unit change in that feature, all else equal — and `intercept_` is the prediction when every feature "
            "is zero. These are the numbers you interpret in a report."
        ),
        notes=[
            "Prints the coefficient array followed by the intercept.",
        ],
        gotcha="A trailing underscore means “learned during fit” — reading coef_ before fit() raises an error.",
    ),
    "w10-05": dict(
        explain=(
            "Scores the predictions with R²: the fraction of the target's variance the model explains. "
            "1.0 is perfect, 0.0 is no better than always predicting the mean, and negative values mean the model is "
            "worse than that baseline. Both metrics are imported, but only R² is printed here."
        ),
        notes=[
            "Imports two metrics; mean_squared_error is available but unused in this snippet.",
            "",
            "Prints R², computed from the true test values and the predictions.",
        ],
        gotcha="Evaluating on X_train instead of X_test gives an optimistic score that hides overfitting.",
    ),
    "w10-06": dict(
        explain=(
            "Defines the modelling inputs. `X` is the feature matrix — note the double brackets, which keep it "
            "two-dimensional — and `y` is the one-dimensional target vector. Every scikit-learn estimator expects "
            "exactly this (n_samples, n_features) shape."
        ),
        notes=[
            "Double brackets select two columns as a DataFrame; single brackets would return a Series and break fit().",
            'The target column as a Series of numbers to predict.',
        ],
        gotcha='`df["temp", "humidity"]` is wrong syntax for columns — you need `df[["temp", "humidity"]]`.',
    ),
    "w10-07": dict(
        explain=(
            "Standardises features to mean 0 and standard deviation 1 so no column dominates because of its scale. "
            "`fit_transform` learns the mean/σ from X and applies them in one step; the printed mean of the output "
            "should be effectively 0, which is a quick correctness check."
        ),
        notes=[
            "Imports the standard scaler.",
            "",
            "Creates the scaler; nothing is learned yet.",
            "Computes mean and σ from X, then returns the standardised array.",
            "Prints a value at (or very near) zero, confirming the transformation worked.",
        ],
        gotcha="Fit on training data only, then `transform` the test set — fitting on both leaks information.",
    ),

    # ---------------------------------------------------------------- WEEK 11
    "w11-01": dict(
        explain=(
            "Builds a classification tree. `max_depth=3` caps how many splits deep the tree may go, which is the main "
            "guard against overfitting, and `random_state=42` makes the tie-breaking reproducible. "
            "`fit` then grows the tree by choosing the most informative split at each node."
        ),
        notes=[
            "Imports the classification tree estimator.",
            "",
            "Caps depth at 3 levels and fixes the random seed.",
            "Grows the tree on the training rows.",
        ],
        gotcha="With no max_depth a tree will memorise the training set and score near-perfectly on train, badly on test.",
    ),
    "w11-02": dict(
        explain=(
            "Measures classification performance. `accuracy_score` is the share of correct labels, computed here on "
            "the test set with fresh predictions. The confusion matrix is imported for the follow-up question: which "
            "classes get mixed up?"
        ),
        notes=[
            "Imports accuracy and the confusion matrix; only accuracy is used here.",
            "",
            "Predicts on X_test and compares to y_test, printing the fraction correct.",
        ],
        gotcha="Accuracy is misleading on imbalanced data — a 95%-negative dataset scores 0.95 by always saying no.",
    ),
    "w11-03": dict(
        explain=(
            "Renders the learned tree as a diagram. `feature_names` labels each split with the column actually used "
            "and `filled=True` colours nodes by the majority class, so you can read the decision rules straight off "
            "the chart."
        ),
        notes=[
            "Imports the plotting helper for trees.",
            "",
            "Draws the tree: each split shows the feature, threshold and impurity; feature_names come from X's columns.",
            "Displays the drawing.",
        ],
        gotcha="On a deep tree the figure is unreadable — cap max_depth or pass `max_depth=3` to plot_tree.",
    ),
    "w11-04": dict(
        explain=(
            "The regression variant predicts a number instead of a class. Trees split until each leaf is as pure as "
            "possible; `max_depth=4` keeps it shallow, and the printed predictions are the mean of the training "
            "targets that landed in each leaf."
        ),
        notes=[
            "Imports the regression tree estimator.",
            "",
            "Creates a tree limited to four levels of splits.",
            "Fits it to the training data.",
            "Predicts on the test set and prints just the first three numbers.",
        ],
        gotcha="Use the regressor for continuous targets and the classifier for labels — the wrong one fails at fit().",
    ),
    "w11-05": dict(
        explain=(
            "Turns the tree's `feature_importances_` array into a readable, sorted Series. Each value is the share of "
            "the model's impurity reduction attributable to that feature, and sorting ascending puts the weakest "
            "feature first so the strongest ones stand out at the end."
        ),
        notes=[
            "pandas is needed to build the labelled Series.",
            "",
            "Wraps the multi-line expression.",
            "Pairs each importance with its column name from X, then sorts from least to most important.",
            "Closes the print call.",
        ],
        gotcha="Importances sum to 1 but are not causal — and correlated features split the credit between them.",
    ),
    "w11-06": dict(
        explain=(
            "Estimates performance more reliably by training and testing k times. `cv=5` splits the data into five "
            "folds, trains on four and tests on the fifth, rotating each time, and returns five scores whose mean is a "
            "much steadier estimate than one split."
        ),
        notes=[
            "Imports the cross-validation scorer.",
            "",
            "Runs five-fold cross-validation on the full X and y — no manual train/test split needed.",
            "Prints the average of the five fold scores.",
        ],
        gotcha="Pass the model and the full data — cross_val_score does its own splitting, so do not hand it X_train.",
    ),

    # ---------------------------------------------------------------- WEEK 12
    "w12-01": dict(
        explain=(
            "Defines a small feed-forward network. `Sequential` stacks layers in order; the first `Dense` layer has 16 "
            "neurons with a ReLU activation and must declare the input shape (4 features); the final single-unit "
            "layer is the regression output."
        ),
        notes=[
            "Imports the Keras high-level API from TensorFlow.",
            "Imports the layer classes separately.",
            "",
            "Sequential means data flows through the listed layers in order.",
            "Hidden layer: 16 neurons, relu activation, and input_shape tells Keras the 4 features per row.",
            "Output layer: one neuron, no activation, because we are predicting a single number.",
            "Closes the list of layers.",
        ],
        gotcha="Drop input_shape and the model is not built — you cannot call summary() or fit() until it knows the inputs.",
    ),
    "w12-02": dict(
        explain=(
            "Compiles the network, which fixes how it will learn. `optimizer=\"adam\"` is the update rule, "
            "`loss=\"mse\"` is what it minimises (appropriate for regression), and `metrics=[\"mae\"]` is only "
            "reported for humans — it does not affect training."
        ),
        notes=[
            "Sets optimiser, loss and reporting metric; must run before fit().",
        ],
        gotcha="MSE loss with a classification problem will train but produce meaningless probabilities — match loss to task.",
    ),
    "w12-03": dict(
        explain=(
            "Trains the network. `epochs=20` means 20 passes over the data, `batch_size=32` means weights update every "
            "32 rows, and `validation_split=0.2` holds back 20% of the training rows to report validation loss each "
            "epoch. The returned `history` records those curves."
        ),
        notes=[
            "fit returns a History object, which stores the per-epoch loss/metric curves.",
            "Inputs first: the training features and targets.",
            "Twenty full passes over the training data.",
            "Update the weights after every 32 samples.",
            "Report validation metrics on the last 20% of X_train, so overfitting becomes visible.",
            "Closes the fit call; training starts when the statement executes.",
        ],
        gotcha="validation_split carves from the data you pass in — it does not replace your separate test set.",
    ),
    "w12-04": dict(
        explain=(
            "Scores the trained network and then uses it. `evaluate` returns one number per compiled metric — here "
            "loss and MAE, unpacked in that order — and `predict` returns raw numbers, sliced to three rows for "
            "readability."
        ),
        notes=[
            "Returns one value per compiled metric, in order: loss first, then mae.",
            "Predicts for the first three test rows.",
        ],
        gotcha="evaluate returns a list, so unpacking into the wrong number of names raises ValueError.",
    ),
    "w12-05": dict(
        explain=(
            "Converts a regression network into a three-class classifier. The final layer has one unit per class with "
            "`softmax` (turning scores into probabilities that sum to 1) and the loss becomes sparse categorical "
            "cross-entropy, which expects integer class labels."
        ),
        notes=[
            "Adds a new output layer: 3 units, softmax turns them into probabilities.",
            "Recompiles with a classification loss; 'sparse' means labels are integers 0,1,2 rather than one-hot vectors.",
        ],
        gotcha="Keep the old single-unit output layer and you get two outputs — rebuild the model, do not just add.",
    ),
    "w12-06": dict(
        explain=(
            "Prints the architecture and the size of the model. `summary()` lists every layer with its output shape "
            "and parameter count; `count_params()` gives the total, which is what tells you whether the model is "
            "unreasonably large for the data."
        ),
        notes=[
            "Table of layers, output shapes and parameter counts.",
            "Total learnable weights as a single number.",
        ],
        gotcha="Params = (inputs × units) + units per Dense layer — a huge count relative to rows means overfitting risk.",
    ),

    # ---------------------------------------------------------------- WEEK 13
    "w13-01": dict(
        explain=(
            "A whole supervised-learning pipeline end to end: import, load and clean, define features and target, "
            "split reproducibly, fit, and score on the held-out data. "
            "This is the shape of every analysis you will be asked to reproduce in the final exam."
        ),
        notes=[
            "Data handling library.",
            "Splitting helper.",
            "The estimator.",
            "",
            "Load and drop incomplete rows in one chained expression.",
            "Two-column feature matrix (double brackets keep it 2-D).",
            "Single target column.",
            "Split reproducibly — 80% train, 20% test.",
            "test_size 0.2 and a fixed seed.",
            "Closes the split call.",
            "Instantiate and fit in one line; fit() returns the model.",
            "R² on the held-out test set — the honest score.",
        ],
        gotcha="Reporting `model.score(X_train, y_train)` here would flatter the model; always score X_test.",
    ),
    "w13-02": dict(
        explain=(
            "An API-to-DataFrame cleaning pipeline. The JSON body becomes a table, the inconsistently capitalised "
            "column is renamed to a predictable snake_case name, and missing values are counted before any analysis."
        ),
        notes=[
            "HTTP client.",
            "pandas for the table.",
            "",
            "Fetch the endpoint.",
            "Decode the JSON body straight into a DataFrame.",
            'Rename the badly cased "Temp" column to "temp" so later code is consistent.',
            "Report missing counts per column before deciding how to handle them.",
        ],
        gotcha="Renaming with the wrong case does nothing silently — check `df.columns` afterwards.",
    ),
    "w13-03": dict(
        explain=(
            "A compact numeric profile. `select_dtypes(include=\"number\")` filters to numeric columns so text columns "
            "cannot raise errors, and the loop prints each column next to its mean — enough to spot scale differences "
            "and suspicious values quickly."
        ),
        notes=[
            'Loops only over numeric columns — "object" dtype columns are skipped.',
            "Prints the column name and its mean on one line.",
        ],
        gotcha="Means ignore NaN, so a column that is mostly missing still prints a confident-looking average.",
    ),
    "w13-04": dict(
        explain=(
            "Persists a trained model so you do not retrain for every prediction. `joblib.dump` serialises the fitted "
            "object to disk and `joblib.load` restores it, coefficients and all, ready for `.predict`."
        ),
        notes=[
            "joblib is the recommended serialiser for scikit-learn models.",
            "",
            "Writes the fitted model to a single binary file.",
            "Reads it back into a new variable, identical in behaviour to the original.",
        ],
        gotcha="A model file is tied to the library versions that created it — unpickling under another sklearn version may fail.",
    ),
    "w13-05": dict(
        explain=(
            "Produces a tidy summary table. `groupby` forms the groups, `.agg` computes a different statistic per "
            "column, and `.reset_index()` promotes the group keys out of the index into ordinary columns so the frame "
            "is flat and export-ready. The outer parentheses let one expression span several lines."
        ),
        notes=[
            "Opening parenthesis makes the multi-line expression valid Python.",
            "Group rows by city.",
            'Aggregate: average sales, count non-missing temp per city.',
            "Moves city from the index into a normal column.",
            "Closes the expression and assigns the flat frame to summary.",
        ],
        gotcha="Without reset_index the city names stay in the index and vanish from a CSV export or a plot's x axis.",
    ),

    # ---------------------------------------------------------------- WEEK 14
    "w14-01": dict(
        explain=(
            "Packages the standard training workflow into a reusable function: split, fit, score, return. "
            "Every value it needs arrives as a parameter and nothing is hard-coded, so the same function works for any "
            "feature matrix that shares the column layout."
        ),
        notes=[
            "Defines the function and its two inputs: features and target.",
            "Splits reproducibly inside the function so callers cannot skew the evaluation.",
            "test_size and random_state keep every call identical.",
            "Closes the split call.",
            "Creates an unfitted estimator.",
            "Learns the coefficients.",
            "Predicts on the test split and returns R² straight to the caller.",
        ],
        gotcha="Rebuilding the model inside the function means you cannot inspect it afterwards — return it too if needed.",
    ),
    "w14-02": dict(
        explain=(
            "Compares two candidate models on identical folds. Each entry runs `cross_val_score` with `cv=5` on the "
            "same X and y and stores the mean, making the dict a fair side-by-side scoreboard for model selection."
        ),
        notes=[
            "One dict, one key per candidate model.",
            "Five-fold CV mean for the tree model.",
            "Same folds and data for the linear model — the only thing that changes is the estimator.",
            "Closes the dict.",
        ],
        gotcha="Comparing scores from different folds or different data makes the comparison meaningless.",
    ),
    "w14-03": dict(
        explain=(
            "Builds a two-panel figure for a report. `plt.subplots(1, 2)` returns the figure plus an array of axes; "
            "you then draw on each axes object individually, which is the correct way to combine charts."
        ),
        notes=[
            "One row, two columns of axes, 12 by 4 inches; returns fig and the axes array.",
            "Left panel: distribution of sales.",
            "Right panel: relationship between temp and sales.",
            "Renders both panels at once.",
        ],
        gotcha="Calling `plt.hist` then `plt.scatter` without axes draws both onto the same panel and mixes them.",
    ),
    "w14-04": dict(
        explain=(
            "Scores brand-new observations. A list of dicts is converted into a DataFrame whose keys become columns — "
            "they must match the training feature names and order — and the fitted model returns one prediction per "
            "row."
        ),
        notes=[
            'Converts the new records to a DataFrame; keys "temp" and "humidity" must match the training columns.',
            "One predicted value per new row.",
        ],
        gotcha="Extra or missing keys cause a feature-name mismatch error at predict time.",
    ),
    "w14-05": dict(
        explain=(
            "The reproducibility header every notebook should start with: the three standard imports, a fixed random "
            "seed so splits and initialisations repeat, and the inline magic so figures render inside the notebook."
        ),
        notes=[
            "NumPy for arrays and maths.",
            "pandas for tabular data.",
            "Matplotlib's pyplot for charts.",
            "",
            "Pins NumPy's global random state so random operations are repeatable.",
            "%matplotlib inline is a notebook magic, not Python — it renders figures in the output cell.",
        ],
        gotcha="The seed only fixes NumPy; also pass random_state= to scikit-learn estimators for full reproducibility.",
    ),
}
