from sklearn.model_selection import RandomizedSearchCV

def perform_hyperparameter_tuning(model,pram_grid,X_train,y_train,scoring="f1",cv=5,n_iter=20):

    rs_cv = RandomizedSearchCV(
        estimator=model,
        param_distributions=pram_grid,
        n_iter=n_iter,
        cv=cv,
        scoring=scoring,
        verbose=1,
        n_jobs=-1,
        random_state=42
    ) 

    rs_cv.fit(X_train,y_train)

    return rs_cv.best_estimator_,rs_cv.best_params_,rs_cv.best_score_