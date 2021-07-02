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
    # Variable type checking
    if (treatment_type != 'bool') or (treatment_type != 'int'):
        error_msg = "Please specify a valid type for the treatment variable. Valid types are bool and int."
        raise TypeError(error_msg)
    else:
        # separate patients who did and did not receive treatment
        df_treatment = df.loc[df[treatment] == 1]
        df_control = df.loc[df[treatment] == 0]
    # conduct naive causal estimate
    naive_est = np.mean(df_treatment[outcome]) - np.mean(df_control[outcome])
    return naive_est