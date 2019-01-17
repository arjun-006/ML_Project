import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import StratifiedKFold
from scipy.stats import randint as sp_randint
from scipy.stats import uniform as sp_uniform
import numpy as np
import pickle

x = np.load("/home/arjun/PycharmProjects/ML_proj/scripts/dataset.npy")
y = np.load("/home/arjun/PycharmProjects/ML_proj/scripts/outcome.npy")



n_iter = 1000
k_fold = 5
cv = StratifiedKFold(n_splits=k_fold,shuffle=True)

GB = xgb.XGBClassifier()

param_grid = {'max_depth': sp_randint(1, 90),
              'learning_rate': sp_uniform(loc=0e0, scale=1e0),
              'objective': ['multi:softprob'],
              'nthread': [8],
              'missing': [np.nan],
              'reg_alpha': [0.01, 0.017782794, 0.031622777, 0.056234133, \
                            0.1, 0.17782794, 0.31622777, 0.56234133, 1., 1.77827941, \
                            3.16227766, 5.62341325, 10., \
                            17.7827941, 31.6227766, 56.2341325, 100.],
              'colsample_bytree': sp_uniform(loc=0.2e0, scale=0.8e0),
              'subsample': sp_uniform(loc=0.2e0, scale=0.8e0),
              'n_estimators': sp_randint(50, 200)}

search_GB = RandomizedSearchCV(GB,param_grid,\
               n_iter=n_iter,cv=cv,verbose=True).fit(x,y)
print (' ', search_GB.best_score_)
print(' ', search_GB.best_params_)
# save the results
# %%
f_name = open('xgboost_RSCV.dat','w')
pickle.dump([search_GB.cv_results_],f_name)
f_name.close()