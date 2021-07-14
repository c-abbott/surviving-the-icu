from sklearn.metrics import log_loss, recall_score, f1_score, roc_auc_score

def train_and_validate_classifiers(Xtrain, ytrain, Xval, yval,  names, classifiers):
    """
    Trains and validates a set of binary classifiers on a training and held-out validation set. Metrics 
    used to evaluate classifier performance are: accuracy, AUROC, recall, F1 score and cross-entropy log-loss.

    Input:
        Xtrain: np.array of (n_samples, n_features)     - Training set
        ytrain: np.array of (n_samples,)                - Training labels
        Xval: np.array of (n_val_samples, n_features)   - Validation set
        yval: np.array of (n_val_samples,)              - Validation labels
        names: list of strings                          - Names of classifiers you are training
        classifiers: list of sklearn classifier objects - Set of classifiers you wish to train

    Output:
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

def print_metrics_table(training_scores, validation_scores, names):
    """
    Prints a 

    """