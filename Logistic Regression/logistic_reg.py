import math
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import numpy as np


class CustomLogisticRegression:
    def __init__(self, fit_intercept=True, l_rate=0.01, n_epoch=100):
        self.fit_intercept = fit_intercept
        self.l_rate = l_rate
        self.n_epoch = n_epoch
        self.log_loss = 0.0
        self.mse = 0.0
        self.def_score = 0.0
        self.coef_ = []
        self.log_loss_coef_ = []
        self.first_mse_error = []
        self.last_mse_error = []
        self.first_log_loss_error = []
        self.last_log_loss_error = []

    @staticmethod
    def sigmoid(t):
        return 1 / (1 + pow(math.e, -t))

    def predict_proba(self, row, coef_):
        if self.fit_intercept:
            t = coef_[0] + np.dot(row, coef_[1:])
        else:
            t = np.dot(row, coef_)
        return self.sigmoid(t)

    def default_logistic_reg(self, X_train, y_trains, X_test, y_tests):
        logistic_model = LogisticRegression(fit_intercept=self.fit_intercept)
        logistic_model.fit(X_train, y_trains)
        y_pred = logistic_model.predict(X_test)
        self.def_score = accuracy_score(y_tests, y_pred)

    @staticmethod
    def fit_mse_error(y_val, y_hat, n):
        return 1 / n * (y_val - y_hat) ** 2

    def fit_mse(self, X_train, y_trains):
        if self.fit_intercept:
            self.coef_ = (X_train.shape[1] + 1) * [0]
        else:
            self.coef_ = X_train.shape[1] * [0]

        for k in range(self.n_epoch):
            for i, row in enumerate(X_train):
                y_hat = self.predict_proba(row, self.coef_)
                if self.fit_intercept:
                    self.coef_[0] += (
                        -self.l_rate * (y_hat - y_trains[i]) * y_hat * (1 - y_hat)
                    )
                    for j in range(len(row)):
                        self.coef_[j + 1] += (
                            -self.l_rate
                            * (y_hat - y_trains[i])
                            * y_hat
                            * (1 - y_hat)
                            * row[j]
                        )
                else:
                    for j in range(len(row)):
                        self.coef_[j] += (
                            -self.l_rate
                            * (y_hat - y_trains[i])
                            * y_hat
                            * (1 - y_hat)
                            * row[j]
                        )
                if k == 0:
                    er_val = self.fit_mse_error(y_trains[i], y_hat, X_train.shape[0])
                    self.first_mse_error.append(er_val)
                if k == self.n_epoch - 1:
                    er_val = self.fit_mse_error(y_trains[i], y_hat, X_train.shape[0])
                    self.last_mse_error.append(er_val)

    @staticmethod
    def fit_log_loss_error(y_val, y_hat, n):
        return -1 / n * (y_val * math.log(y_hat) + (1 - y_val) * math.log(1 - y_hat))

    def fit_log_loss(self, X_train, y_trains):
        # stochastic gradient descent implementation
        if self.fit_intercept:
            self.log_loss_coef_ = (X_train.shape[1] + 1) * [0]
        else:
            self.log_loss_coef_ = X_train.shape[1] * [0]
        for k in range(self.n_epoch):
            for i, row in enumerate(X_train):
                y_hat = self.predict_proba(row, self.log_loss_coef_)
                if self.fit_intercept:
                    self.log_loss_coef_[0] += (
                        -self.l_rate * (y_hat - y_trains[i]) / len(X_train)
                    )
                    for j in range(len(row)):
                        self.log_loss_coef_[j + 1] += (
                            -self.l_rate * (y_hat - y_trains[i]) * row[j] / len(X_train)
                        )
                else:
                    for j in range(len(row)):
                        self.log_loss_coef_[j] += (
                            -self.l_rate * (y_hat - y_trains[i]) * row[j] / len(X_train)
                        )

                if k == 0:
                    func = self.fit_log_loss_error(y_trains[i], y_hat, len(X_train))
                    self.first_log_loss_error.append(func)
                if k == self.n_epoch - 1:
                    func = self.fit_log_loss_error(y_trains[i], y_hat, len(X_train))
                    self.last_log_loss_error.append(func)

    def predict_mse(self, X_test, cut_off=0.5):
        predictions = []
        for row in X_test:
            y_hat = self.predict_proba(row, self.coef_)
            if y_hat >= cut_off:
                predictions.append(1)
            else:
                predictions.append(0)
        return predictions

    def predict_log_loss(self, X_test, cut_off=0.5):
        predictions = []
        for row in X_test:
            y_hat = self.predict_proba(row, self.log_loss_coef_)
            if y_hat >= cut_off:
                predictions.append(1)
            else:
                predictions.append(0)
        return predictions

    def print_params(self):
        print(
            {
                "mse_accuracy": self.mse,
                "logloss_accuracy": self.log_loss,
                "sklearn_accuracy": self.def_score,
                "mse_error_first": self.first_mse_error,
                "mse_error_last": self.last_mse_error,
                "logloss_error_first": self.first_log_loss_error,
                "logloss_error_last": self.last_log_loss_error,
            }
        )


model = CustomLogisticRegression(fit_intercept=True, l_rate=0.01, n_epoch=1000)
data = load_breast_cancer(as_frame=True).frame
data_columns = ["worst concave points", "worst perimeter", "worst radius"]
target_column = ["target"]

scaler = StandardScaler()

x = data[data_columns]
y = data[target_column]
x = scaler.fit_transform(x)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, train_size=0.8, random_state=43
)

for dataset in [y_train, y_test]:
    dataset.reset_index(drop=True, inplace=True)

model.fit_mse(x_train, y_train["target"])
model.fit_log_loss(x_train, y_train["target"])
model.default_logistic_reg(x_train, y_train["target"], x_test, y_test["target"])
predicts = model.predict_mse(x_test)
predicts_log_loss = model.predict_log_loss(x_test)
model.log_loss = accuracy_score(predicts_log_loss, y_test["target"])
model.mse = accuracy_score(predicts, y_test["target"])
model.print_params()

print(
    """
Answers to the questions:
1) 0.00001
2) 0.00000
3) 0.00153
4) 0.00600
5) expanded
6) expanded"""
)
