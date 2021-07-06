import numpy as np
import statsmodels

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
    accepted_types = ['bool', 'int']
    if treatment_type not in accepted_types:
        error_msg = "Please specify a valid type for the treatment variable. Valid types are bool and int."
        raise TypeError(error_msg)
    else:
        # Separate patients who did and did not receive treatment
        df_treatment = df.loc[df[treatment] == 1]
        df_control = df.loc[df[treatment] == 0]

    # Conduct naive causal estimate
    naive_est = np.mean(df_treatment[outcome]) - np.mean(df_control[outcome])
    return naive_est

def print_estimate_comparison(naive_est, causal_est, estimation_method):
    """
    Input:
        naive_est (float64) - naive_causal.
        causal_est (dowhy.Causal estimate) - Causal estimate of identified estimand.
        estimation_method (str) - Estimation technique used to obtain causal estimate

    Output:
        Nothing. Prints comparison of causal estimate with naive estimate to the terminal
    """
    print("-------------- Causal Estimates -------------- ")
    print("Naive causal estimate is " + str(naive_est))
    print(f"{estimation_method} causal estimate is " + str(causal_est.value))
    print(f"Percentage change from naive_est: {round(((causal_est.value - naive_est) / naive_est) * 100, 3)}%")
    print("----------------------------------------------")

def linear_regression_estimator(model, estimand, ci=False, test_significance=False):
    """
    Input:
        model (dowhy.CausalModel) - Causal graph.
        estimand (dowhy.IdentifiedEstimand) - Causal estimand P(Y|do(T)) derived from model.
        ci (bool) - Confidence interval flag.
        test_significance - Get p-value of estimate flag.

    Output:
        lin_est (dowhy.CausalEstimate) - Linear regression causal estimate of identified estimand.
    """
    lin_est = model.estimate_effect(estimand, method_name="backdoor.linear_regression", 
                                    control_value=0, treatment_value=1, confidence_intervals=ci, 
                                    test_significance=test_significance)
    return lin_est

def bin_glm_estimator(model, estimand, ci=False, test_significance=False):
    """
    Input:
        model (dowhy.CausalModel) - Causal graph.
        estimand (dowhy.IdentifiedEstimand) - Causal estimand P(Y|do(T)) derived from model.
        ci (bool) - Confidence interval flag.
        test_significance - Get p-value of estimate flag.

    Output:
        glm_est (dowhy.CausalEstimate) - Binomial GLM causal estimate of identified estimand.
    """
    glm_est = model.estimate_effect(estimand, method_name="backdoor.generalized_linear_model", control_value=0, 
                                    treatment_value=1, confidence_intervals=ci, test_significance=test_significance,
                                    method_params={'glm_family':statsmodels.api.families.Binomial()})
    return glm_est
 
def plot_ipw_interpreter(est, confounder):
    """
    Input:
        est (dowhy.CausalEstimate) - Causal estimate from DoWhy
        confounder (str) - Confounder whose weights before and after IPW you'd like to visualize

    Output:
        Plot of weights associated with confounder before and after IPW is applied.
    """
    cols = est.estimator._observed_common_causes_names + est.estimator._treatment_name
    df = est.estimator._data[cols]
    treated = est.estimator._treatment_name[0]
    propensity = est.propensity_scores

    # add weight column
    df["weight"] = df[treated] * (propensity) ** (-1) + (1 - df[treated]) * (1 - propensity) ** (-1)

    # before weights are applied we count number rows in each category
    # which is equivalent to summing over weight=1
    barplot_df_before = df.groupby([confounder, treated]).size().reset_index(name="count")

    # # after weights are applied we need to sum over the given weights
    barplot_df_after = df.groupby([confounder, treated]).agg({'weight': np.sum}).reset_index()
    barplot_df_after.rename(columns={'weight': 'count'}, inplace=True)

    title1 = "Distribution of " + confounder + " before applying the weights"
    title2 = "Distribution of " + confounder + " after applying the weights"

    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    iterable = zip([barplot_df_before, barplot_df_after], [ax1, ax2], [title1, title2])
    for plot_df, ax, title in iterable:
        aggregated_not_treated = plot_df[plot_df["drain"] == False]
        aggregated_treated = plot_df[plot_df["drain"] == True]

        labels_not_treated = aggregated_not_treated[confounder]
        labels_treated = aggregated_treated[confounder]

        not_treated_counts = aggregated_not_treated['count']
        treated_counts = aggregated_treated['count']
    
        ax.grid(zorder=1)
        ax.bar(labels_not_treated - 0.35 / 2, not_treated_counts, 0.35, label='Untreated', zorder=2)
        ax.bar(labels_treated + 0.35 / 2, treated_counts, 0.35, label='Treated', zorder=2)
        ax.set_xlabel(confounder)
        ax.set_ylabel('Count')
        ax.set_title(title, fontsize=12)
        ax.set_xticks(labels_treated)
        ax.set_xticklabels(labels_treated)
        ax.legend()
    
    fig.tight_layout()
    plt.show()