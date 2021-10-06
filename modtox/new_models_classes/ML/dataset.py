from abc import ABC, abstractmethod
from typing import Dict
from modtox.modtox.new_models_classes.ML.selector import FeaturesSelector

import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

class DataSet:
    """Represents a combination of features. Is dynamically 
    modified by FeaturesSelector subclasses, so all attributes
    are set as properties."""

    df: pd.DataFrame

    def __init__(self, df: pd.DataFrame, y_col_name="Activity", external_col_name="is_external") -> None:
        self.df = df
        self.y_col_name = y_col_name
        self.external_col_name = external_col_name
        
        self.is_external = df[external_col_name]
        self.activity = df[y_col_name]
        
        self.impute()

    def impute(self):
        """Imputes self.df in place"""
        imputer = SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=0)
        X_imputed = imputer.fit_transform(self.df)
        self.df = pd.DataFrame(X_imputed, columns = self.df.columns, dtype="float32")

    @property    
    def y_train(self):
        train_df = self.df.loc[self.df[self.external_col_name] == True]
        y_train = train_df[self.y_col_name]
        le = LabelEncoder()
        y_train = le.fit_transform(y_train)
        return y_train

    @property 
    def y_ext(self):
        external_df = self.df.loc[self.df[self.external_col_name] == True]
        y_ext = external_df[self.y_col_name]
        le = LabelEncoder()
        y_ext = le.fit_transform(y_ext)
        return y_ext

    @property
    def X_train(self):
        train_df = self.df.loc[self.df[self.external_col_name] == False]
        X_train = train_df.drop([self.y_col_name, self.external_col_name], axis=1, inplace=True)
        return X_train

    @property
    def X_ext(self):
        train_df = self.df.loc[self.df[self.external_col_name] == True]
        X_train = train_df.drop([self.y_col_name, self.external_col_name], axis=1, inplace=True)
        return X_train
    
    @property
    def X(self):
        df = self.df.copy()
        X = df.drop([self.y_col_name, self.external_col_name], axis=1, inplace=True)
        return X

    def select_features(selector: FeaturesSelector): 
        ds_new_shape = selector.select()

