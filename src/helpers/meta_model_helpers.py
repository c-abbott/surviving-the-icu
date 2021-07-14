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

def print_metrics_table(training_scores, val_scores, names):
    """
    Prints accuracy, AUROC, recall, F1 score and cross entropy loss metrics as a table
    for training and validation set comparison.

    Input:
        training_scores: list of 5 dictionaries - Set of training scores
        val_scores: list of 5 dictionaries      - Set of validation scores
        names: list of strings                  - Names of classifiers you are training

    Output:
        None
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