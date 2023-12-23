# import necessary libraries
import joblib
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
# from sklearn.metrics import r2_score, mean_squared_error, accuracy_score
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
    if ('float' in str(t)) or ('int' in str(t)) :
        numeric_features.append(i)
    else :
        categorical_features.append(i)

# Create pipeline for numeric features
numeric_transformer = Pipeline(steps=[
    ("Imputer", SimpleImputer(strategy="median")), # not necessary but in case of
    ('scaler', StandardScaler())
])

# Create pipeline for categorical features
categorical_transformer = Pipeline(steps=[
    ("Imputer", SimpleImputer(strategy="most_frequent")), # not necessary but in case of
    ('encoder', OneHotEncoder(drop='first')) # first column will be dropped to avoid creating correlations between features
    ])

# Use ColumnTransformer to make a preprocessor object that describes all the treatments to be done
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=0)
X_train = preprocessor.fit_transform(X_train)
X_test = preprocessor.transform(X_test)

# Set your variables for your environment
EXPERIMENT_NAME="my-first-mlflow-experiment"

# instanciate your experiment
client=mlflow.tracking.MlflowClient()
mlflow.set_tracking_uri("https://getaround-mlflow-ed95616b9f3c.herokuapp.com/")

# Set experiment's info 
mlflow.set_experiment(EXPERIMENT_NAME)

# Get our experiment info
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

# Call mlflow autolog
mlflow.xgboost.autolog()

with mlflow.start_run(experiment_id = experiment.experiment_id):
 
    # Instanciate and fit the model 
    xgb_regressor = xgb.XGBRegressor(
    max_depth=4,
    learning_rate=0.1,
    n_estimators=250,
    random_state =0
    )
    xgb_regressor.fit(X_train, Y_train)

    # Store metrics 
    predicted_price = xgb_regressor.predict(X_test.values)
    score = xgb_regressor.score(X_test.values, Y_test.values)

    # Print results 
    print("XGBoost model")
    print("Score: {}".format(score))