# import necessary libraries
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
import xgboost as xgb

import mlflow

dataset_price_clean = pd.read_csv("dataset_price_clean.csv")

# Separate target and features
X = dataset_price_clean.iloc[:,0:-1]
Y = dataset_price_clean.iloc[:,-1:]

# Automatically detect names of numeric/categorical columns
numeric_features = []
categorical_features = []
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
EXPERIMENT_NAME="getaround-xgboost"

# instanciate your experiment
client=mlflow.tracking.MlflowClient()
mlflow.set_tracking_uri("https://mlflow-apps-b1797a75bc7a.herokuapp.com")

# Set experiment"s info 
mlflow.set_experiment(EXPERIMENT_NAME)

# Get our experiment info
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

# Call mlflow autolog
mlflow.xgboost.autolog()

with mlflow.start_run(experiment_id = experiment.experiment_id):
 
    # Instanciate and fit the model with gridsearchcv (cross validation + try of differents values of parameters, cf params_grid)
    xgb_regressor = xgb.XGBRegressor(random_state=0,learning_rate=0.1, max_depth=5, n_estimators=150)
    xgb_regressor.fit(X_train, Y_train)

    # Store metrics
    predicted_price = xgb_regressor.predict(X_test)
    score = xgb_regressor.score(X_test, Y_test)
    
    # Log Metric 
    # mlflow.log_metric("Accuracy", score)
    
    # log best parameters
    #importance = model.best_params_(importance_type='weight')
    # mlflow.log_artifact(importance, 'feature_importance.json')
    
    # Log model 
    # mlflow.sklearn.log_model(model, "model")

    # Print results 
    print("XGBoost model")
    print("Score: {}".format(score))