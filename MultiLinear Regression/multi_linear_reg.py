import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import math


class CustomLinearRegression:
    def __init__(self, fit_intercept=False):
        self.fit_intercept = fit_intercept
        self.coefficient = []
        self.intercept = 0
        self.w_vector = []
        self.r2_score_val = 0
        self.rmse_val = 0
        self.reg_sci = None
        self.reg_sci_r2_score = None
        self.reg_sci_rmse = None

    def use_predefined_regression(self, x, y):
        reg_sci = LinearRegression(fit_intercept=True)
        reg_sci.fit(x, y)
        self.reg_sci_r2_score = r2_score(y, reg_sci.predict(x))
        self.reg_sci_rmse = mean_squared_error(y, reg_sci.predict(x))
        self.reg_sci = reg_sci

    def fit(self, x, y):
        if not self.fit_intercept:
            return
        x_array = np.matrix(x, dtype=np.float64)
        y_array = np.matrix(y, dtype=np.float64).transpose()
        x_transpose_self = np.matmul(x_array.transpose(), x_array)
        x_transpose_self_inverse = np.linalg.inv(x_transpose_self)
        x_transpose_y = x_array.transpose() * y_array
        self.w_vector = np.matmul(x_transpose_self_inverse, x_transpose_y)
        self.intercept = self.w_vector[0, 0]
        self.coefficient = [self.w_vector[i, 0] for i in range(1, len(self.w_vector))]

    def predict(self, x):
        transpose_df = x.transpose()
        transpose_df_dict = transpose_df.to_dict()
        final_res = []
        for item, value in transpose_df_dict.items():
            total = sum(
                v * self.w_vector[idx, 0] for idx, v in enumerate(value.values())
            )
            final_res.append(total)

        return np.array(final_res)

    def r2_score(self, y, yhat):
        y_values = np.array(y)
        yhat_val = np.array(yhat)
        up = 0
        down = 0
        for i in range(len(y_val)):
            up += (y_values[i] - yhat_val[i]) ** 2
            down += (y_values[i] - np.mean(y_values)) ** 2

        self.r2_score_val = 1 - up / down

    def rmse(self, y, yhat):
        y_values = np.array(y)
        yhat_val = np.array(yhat)
        up = sum((y_values[i] - yhat_val[i]) ** 2 for i in range(len(y_val)))
        self.rmse_val = np.sqrt(up / len(y_val))

    def print_result(self):
        print(
            {
                "Intercept": self.intercept,
                "Coefficient": np.array([self.coefficient]),
                "R2": self.r2_score_val,
                "RMSE": self.rmse_val,
            }
        )

    def print_predefined_result(self):
        print(
            {
                "Intercept": self.reg_sci.intercept_,
                "Coefficient": np.array([self.reg_sci.coef_]),
                "R2": self.reg_sci_r2_score,
                "RMSE": self.reg_sci_rmse,
            }
        )

    def print_differ(self):
        print(
            {
                "Intercept": self.reg_sci.intercept_ - self.intercept,
                "Coefficient": np.array([self.reg_sci.coef_])
                - np.array([self.coefficient]),
                "R2": self.reg_sci_r2_score - self.r2_score_val,
                "RMSE": math.sqrt(self.reg_sci_rmse) - self.rmse_val,
            }
        )


path = "data_stage4.csv"
df = pd.read_csv(path)
x_val = df.iloc[:, :3]
x_ones = np.ones((len(x_val), 1))
y_val = df["y"]
custom_x_val = np.concatenate((x_ones, x_val), axis=1)
custom_x_val_to_df = pd.DataFrame(custom_x_val)
linearRegression = CustomLinearRegression(fit_intercept=True)
linearRegression.use_predefined_regression(x_val, y_val)
linearRegression.fit(custom_x_val_to_df, y_val)
res = linearRegression.predict(custom_x_val_to_df)
linearRegression.r2_score(y_val, res)
linearRegression.rmse(y_val, res)
linearRegression.print_differ()
