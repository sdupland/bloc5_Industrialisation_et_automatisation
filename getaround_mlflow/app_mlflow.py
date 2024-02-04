# import necessary libraries
import pandas as pd

from sklearn.model_selection import train_test_split # used to split a dataset into training and testing sets.
from sklearn.pipeline import Pipeline # used to chain together multiple data processing steps
from sklearn.impute import SimpleImputer # used to impute (fill in) missing values in a dataset with a specified strategy (mean, median, etc.)
from sklearn.preprocessing import OneHotEncoder, StandardScaler # OneHotEncoder is used to convert categorical variables into a one-hot encoded format, StandardScaler is used to standardize features by removing the mean and scaling to unit variance.
from sklearn.compose import ColumnTransformer # used to apply different transformers to different columns of the input data.
import xgboost as xgb # used for gradient boosting

import mlflow # provides tools for tracking experiments, packaging code into reproducible runs, and sharing and deploying models

# import dataset saved as a csv file
dataset_price_clean = pd.read_csv("dataset_price_clean.csv")

# Separate target and features
X = dataset_price_clean.iloc[:,0:-1]
Y = dataset_price_clean.iloc[:,-1:]

# Automatically detect names of numeric/categorical columns (thanks to Jedha for this part of code)
numeric_features = []
categorical_features = []
# iterates over the items of X.dtypes. i represents the column name (index) and t represents the data type of the corresponding column.
for i,t in X.dtypes.items() :
    if ("float" in str(t)) or ("int" in str(t)) :
        numeric_features.append(i)
    else :
        categorical_features.append(i)

# Create pipeline for numeric features
numeric_transformer = Pipeline(steps=[
    ("Imputer", SimpleImputer(strategy="median")), # not necessary but in case of
    ("scaler", StandardScaler())
])

# Create pipeline for categorical features
categorical_transformer = Pipeline(steps=[
    ("Imputer", SimpleImputer(strategy="most_frequent")), # not necessary but in case of
    ("encoder", OneHotEncoder(drop="first")) # first column will be dropped to avoid creating correlations between features
    ])

# Use ColumnTransformer to make a preprocessor object that describes all the treatments to be done
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ])

# create two datasets from X and Y, with 80% for training and 20% for testing
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=0)

# preprocess features
X_train = preprocessor.fit_transform(X_train)
X_test = preprocessor.transform(X_test)

# Set your variables for your environment
EXPERIMENT_NAME="getaround-xgboost-v3"

# instanciate your experiment
client=mlflow.tracking.MlflowClient()
mlflow.set_tracking_uri("https://mlflow-apps-b1797a75bc7a.herokuapp.com")

# Set experiment"s info 
mlflow.set_experiment(EXPERIMENT_NAME)

# Get our experiment info
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

# Call mlflow autolog
mlflow.xgboost.autolog()

# create a loop in order to test different values for learning rate and max depth
# learning rate =  controls the contribution of each tree to the final prediction. A smaller learning rate generally requires more trees in the ensemble but can lead to a more robust model
# max_depth = sets the maximum depth of each tree in the ensemble. It controls the complexity of the individual trees. Smaller values can help prevent overfitting

for lr in [0.001, 0.01, 0.1,0.2,0.3] :
    for md in [3,5,10] :
        with mlflow.start_run(experiment_id = experiment.experiment_id):
        
            # Instanciate and fit the model
            # n_estimators = specifies the number of trees in the ensemble. It represents the total number of boosting rounds.
            # More trees generally improve the model's performance but come at the cost of increased computation.
            xgb_regressor = xgb.XGBRegressor(random_state=0,learning_rate=lr, max_depth=md, n_estimators=150)
            xgb_regressor.fit(X_train, Y_train)

            # Store metrics
            predicted_price = xgb_regressor.predict(X_test)
            score = xgb_regressor.score(X_test, Y_test)
            
            # Log Metric 
            mlflow.log_metric("Accuracy", score)
            
            # log best parameters
            #importance = model.best_params_(importance_type='weight')
            # mlflow.log_artifact(importance, 'feature_importance.json')
            
            # Log model 
            mlflow.sklearn.log_model(xgb_regressor, "model")

            # Print results 
            print("XGBoost model")
            print("Score: {}".format(score))