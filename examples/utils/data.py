import pandas as pd
import os
import zipfile
def load_ford(category: str = "A", input_length: int = 500):
    """
    Prepares train and test dataframes.

    Returns:

        x_train (np.ndarray): Train data in numpy format.
        x_test (np.ndarray): Test data in numpy format.
        y_train (np.ndarray): Train labels in numpy format.
        x_test (np.ndarray): Test labels in numpy format.
    """
    _dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(_dir, f'../data/Ford{category}.zip')

    with zipfile.ZipFile(data_file, 'r') as z:
        with z.open(f'Ford{category}_TRAIN.txt') as f:
            train = pd.read_csv(f, delim_whitespace=True, header=None)
        with z.open(f'Ford{category}_TEST.txt') as f:
            test = pd.read_csv(f, delim_whitespace=True, header=None)

    y_train = train.iloc[:, 0]
    x_train = train.iloc[:, 1:]
    x_test = test.iloc[:, 1:]
    y_test = test.iloc[:, 0]

    x_train = x_train.values.reshape(-1, input_length, 1)
    x_test = x_test.values.reshape(-1, input_length, 1)

    y_train[y_train == -1] = 0
    y_test[y_test == -1] = 0

    return x_train, x_test, y_train, y_test