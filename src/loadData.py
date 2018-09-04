import pandas as pd
import numpy as np
import random

def load_data(url):
    df = pd.read_excel(url)
    train = df[:].values.tolist()
    train = np.array(train)
    for i in range(200):
       m1 =random.randint(0,59)
       m2 = random.randint(0,59)
       train[[m1, m2], :] = train[[m2, m1], :]
    y = train[:, -1]

    train_data = train[:, 0:-1]
    # y1=np.array(y1)
    x_train = train_data[0:40].copy()
    x_test = train_data[40:].copy()
    y_train = y[0:40].copy()
    y_test = y[40:].copy()
    return x_train, y_train, x_test, y_test