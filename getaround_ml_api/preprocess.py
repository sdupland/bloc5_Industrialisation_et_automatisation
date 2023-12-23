import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
import joblib

def preparation_data(Features) :
    
    df = pd.DataFrame(dict(Features), index=[0])
    
    # grouping of certain values ​​on qualitative variables which are not enough present
    list_model_other = ["Maserati", "Suzuki", "Porsche", "Ford", 
                        "KIA Motors", "Alfa Romeo", "Fiat", 
                        "Lexus", "Lamborghini", "Mini", "Mazda",
                        "Honda","Yamaha"]
    list_fuel_other = ["hybrid_petrol", "electro"]
    list_color_other = ["green","orange"]

    df['model_key'] = df['model_key'].apply(lambda x: "others" if x in list_model_other else x)
    df['fuel'] = df['fuel'].apply(lambda x: "others" if x in list_fuel_other else x)
    df['paint_color'] = df['paint_color'].apply(lambda x: "others" if x in list_color_other else x)
    
    return df

def preprocessing_data(df) :
    
    """
    # Automatically detect names of numeric/categorical columns
    numeric_features = []
    categorical_features = []
    for i,t in df.dtypes.items() :
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
    
    X_val = preprocessor.transform(df.head())
    
    """
    preprocessor = joblib.load("prepro.joblib")
    X_val = preprocessor.transform(df.head())
    
    return X_val
    