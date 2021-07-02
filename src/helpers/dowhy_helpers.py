import numpy as np
import pandas as pd
import dowhy

def naive_estimate(df, treatment, outcome, treatment_type=None):
    """
        Input:
        df (pd.DataFrame) - Dataframe holding data in question.
        treatment (str) - Name of treatment variable. Must be binary.
        outcome (str) -  Name of outcome variable.
        treatment_type (str) - Type of treatment variable. Accepted types: bool, int.

        Output:
        naive_est (float64) - Causal estimate with no confounders adjusted for.
    """
    if treatment_type == None:
        error_msg = "Please specify the type of the treatment variable. Valid types are bool and int."
        raise ValueError(error_msg)
    elif treatment_type == 'bool':
        # separate patients who did and did not receive treatment
        df_treatment = df.loc[df[treatment] == True]
        df_control = df.loc[df[treatment] == False]
    elif treatment_type == 'int':
        # separate patients who did and did not receive treatment
        df_treatment = df.loc[df[treatment] == 1]
        df_control = df.loc[df[treatment] == 0]
    # conduct naive causal estimate
    naive_est = np.mean(df_treatment[outcome]) - np.mean(df_control[outcome])
    return naive_est