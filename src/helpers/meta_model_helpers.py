import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns
from sklearn.metrics import log_loss, recall_score, f1_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score

class MyRandInt():
    """
        Wrapper class to return multivariate rand ints"
    """
    
    def __init__(self, low, high, dim):
        self.low = low
        self.high = high
        self.dim = dim
    
    def rvs(self, random_state=None):
        # increase proba to sample most complex config (hack, don't take too seriously)
        if stats.bernoulli.rvs(0.1):
            return np.full(self.dim, self.high, dtype=int)
        else:
            return stats.randint.rvs(self.low, self.high, size=(1, self.dim), random_state=random_state)[0]

def train_and_validate_classifiers(Xtrain, ytrain, Xval, yval,  names, classifiers):
    """
    Trains and validates a set of binary classifiers on a training and held-out validation set. Metrics 
    used to evaluate classifier performance are: accuracy, AUROC, recall, F1 score and cross-entropy log-loss.

    Parameters
    ----------
        Xtrain: np.array of (n_samples, n_features)     - Training set
        ytrain: np.array of (n_samples,)                - Training labels
        Xval: np.array of (n_val_samples, n_features)   - Validation set
        yval: np.array of (n_val_samples,)              - Validation labels
        names: list of strings                          - Names of classifiers you are training
        classifiers: list of sklearn classifier objects - Set of classifiers you wish to train

    Output
    ----------
        training_scores: list of 5 dictionaries - Set of training scores
        val_scores: list of 5 dictionaries      - Set of validation scores
    """
    # Training 
    ca_train_score = {}  # Classification accuracy
    auroc_train_score = {} # AUROC
    recall_train_score = {} # Recall
    f1_train_score = {} # F1 Score
    ce_train_score = {}  # Cross-entropy

    # Validation
    ca_val_score = {}
    auroc_val_score = {}
    recall_val_score = {}
    f1_val_score = {}
    ce_val_score = {}

    for name, clf in zip(names, classifiers):
        clf.fit(Xtrain, ytrain) # Train classifiers

        # Get training scores
        ca_train_score[name] = clf.score(Xtrain, ytrain)
        auroc_train_score[name] = roc_auc_score(ytrain, clf.predict(Xtrain))
        recall_train_score[name] = recall_score(ytrain, clf.predict(Xtrain))
        f1_train_score[name] = f1_score(ytrain, clf.predict(Xtrain))
        ce_train_score[name] = log_loss(ytrain, clf.predict(Xtrain))
        
        # Get validation scores
        ca_val_score[name] = clf.score(Xval, yval)
        auroc_val_score[name] = roc_auc_score(yval, clf.predict(Xval))
        recall_val_score[name] = recall_score(yval, clf.predict(Xval))
        f1_val_score[name] = f1_score(yval, clf.predict(Xval))
        ce_val_score[name] = log_loss(yval, clf.predict(Xval))
    
    training_scores = [ca_train_score, auroc_train_score, recall_train_score, f1_train_score, ce_train_score]
    val_scores = [ca_val_score, auroc_val_score, recall_val_score, f1_val_score, ce_val_score]
    return training_scores, val_scores

def print_metrics_table(training_scores, val_scores, names):
    """
    Prints accuracy, AUROC, recall, F1 score and cross entropy loss metrics as a table
    for training and validation set comparison.

    Parameters
    ----------
        training_scores: list of 5 dictionaries - Set of training scores
        val_scores: list of 5 dictionaries      - Set of validation scores
        names: list of strings                  - Names of classifiers you are training
    """
    print('Classification performance on validation set: \n')
    print("{0:<10s}   {1:-^43s}   {2:-^43s}".format('','Validation', 'Training'))
    print("{0:<10s}{1:>9s}{2:>9s}{3:>9s}{4:>9s}{5:>9s}{6:>9s}{7:>9s}{8:>9s}{9:>9s}{10:>9s}".format(
        'Method', 'Acc\u2191', 'AUROC\u2191', 'Recall\u2191', 'F1\u2191', 'LL\u2193',
        'Acc\u2191', 'AUROC\u2191', 'Recall\u2191', 'F1\u2191', 'LL\u2193'))
    print("-"*(10+10*9))
    for clf in names:
        print ("{method:<10s}{val_accuracy:>9.3f}{val_auroc:>9.3f}{val_recall:>9.3f}{val_f1:>9.3f}{val_logloss:>8.3f}{train_accuracy:>9.3f}{train_auroc:>9.3f}{train_recall:>9.3f}{train_f1:>9.3f}{train_logloss:>9.3f}".format(
            method=clf, 
            val_accuracy = val_scores[0][clf],
            val_auroc = val_scores[1][clf],
            val_recall = val_scores[2][clf],
            val_f1 = val_scores[3][clf],
            val_logloss = val_scores[4][clf],
            train_accuracy = training_scores[0][clf], 
            train_auroc = training_scores[1][clf],
            train_recall = training_scores[2][clf],
            train_f1 = training_scores[3][clf],
            train_logloss=training_scores[4][clf]
            )
        )

def plot_confusion_matrix(cm, class_labels=None):
    """
    Plots a confusion matrix using seaborn's heatmap function
    
    Columns and rows are labelled with the strings provided in class_labels.
    
    Parameters
    ----------
    cm: array-like
        contains the confusion matrix
        
    class_labels: array-like, optional
        contains the string labels
            
    """
    
    # check whether we have count data or not
    if issubclass(cm.dtype.type, np.integer):
        fmt = 'd'
    else:
        fmt = '.2f'
        
    if class_labels is not None:
        plt.subplots(1, 1, figsize=(8,6))
        sns.heatmap(cm, cmap='viridis',xticklabels=class_labels, yticklabels=class_labels,\
                    annot=True, annot_kws={"fontsize":15},  fmt=fmt)  # controls the display of the numbers
    else:
        plt.subplots(1, 1, figsize=(8,6))
        sns.heatmap(cm, cmap='viridis', annot=True, annot_kws={"fontsize":15},  fmt=fmt)
        
    plt.ylabel('True label', fontsize=20)
    plt.xlabel('Predicted label', fontsize=20)
    
    # Format xtick and ttick labels
    plt.setp(plt.gca().get_xticklabels(),
         rotation_mode="anchor", fontsize=16)
    plt.setp(plt.gca().get_yticklabels(), fontsize=16)

def randomized_search_cv(Xtrain, ytrain, search_space, n_iter=100, score='roc_auc', cv=None, refit=True, verbose=False):
    """
    Maximises a cross-validation score (AUROC) by random search.
    
    Parameters
    ------------
    Xtrain : nd array, (n_samples, n_features)
        Features used for training
    
    ytrain: nd array, (n_samples,)
        Labels used for training
        
    search_space: list
        Each element of the list must be a tuple (id, classifier_object, param_distributions)
        - id is a string
        - classifier_object is an instance of a classifier
        - param_distributions is a dictionary defining the search space of the hyperparameters,
          the entries can either be lists, or objects implementing a rvs() method returning a
          random sample.
          
    n_iter: int
        Number of trials in the random search
    
    score: str
        Metric to maximise, see sklearn docs for valid strings
        
    cv: int, cross-validation generator or an iterable, default=None
        Determines the cross-validation splitting strategy, used with
        sklearn.model_selection.cross_val_score
        
    refit: bool
        Refit best estimator on the whole dataset
    
    verbose: bool
        Prints debug info
    
    Output
    --------
    cv_scores: list
        list with cv scores
    
    configs: list
        list with sampled configurations
        
    best_estimator: 
        refitted estimator (if refit=True, else None is returned)
    
    """
    # 5-fold cross validation as deafult
    if cv is None:
        cv = StratifiedKFold(n_splits=5, shuffle=True)                              

    if verbose:
        print("cv strategy", cv)
        
    # Number of classifiers
    L = len(search_space)
    # Random search
    cv_scores = []
    configs = []
    
    for trial in range(0, n_iter):
        if verbose:
            print("--"*20)
            print("Trial", trial)
            print("--"*20)
        # pick classifier
        index = np.random.choice(L)
        
        # sample a parameter configuration for the selected classifier   
        my_id = search_space[index][0]
        clf = search_space[index][1]
        param_distr = search_space[index][2]
        
        # sample hyperparameters
        param_dict = {}
        for k, v in param_distr.items():
            if isinstance(v, list):
                # sample from list
                param_dict[k] = np.random.choice(v)
            else:
                # sample from distribution
                param_dict[k] = v.rvs()

        # construct pipeline
        pipe = Pipeline([(my_id, clf)])
        pipe.set_params(**param_dict)
        if verbose:
            print("Parameters", param_dict)
            print("Pipeline:", pipe)
            
        # compute cv score
        scores_tmp = cross_val_score(pipe, Xtrain, ytrain, cv=cv, scoring=score, n_jobs=-1)
        if verbose:
            print("cv score:", scores_tmp)
                
        # store
        cv_scores.append(np.mean(scores_tmp))
        configs.append(pipe)
    
    # Refit best set of hyperparameters
    if refit:
        print("--"*20)
        print("Selecting and refitting best classifier")
        print("--"*20)
        best_index = np.argmax(cv_scores)
        best_score = cv_scores[best_index]
        best_estimator = configs[best_index]
        best_estimator.fit(Xtrain, ytrain)
        if verbose:
            print("best score:", best_score)
            print("best pipe:", best_estimator)
    else:
        best_estimator = None
        
    return cv_scores, configs, best_estimator

