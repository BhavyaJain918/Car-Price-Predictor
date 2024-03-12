import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split

def regression(cur_year , kms , fuel , trans , own):
    dataset = pd.read_csv("")   # Name of the file that contians the dataset
    pd.set_option("future.no_silent_downcasting" , True)
    dataset.replace({"Fuel_Type" : {"Petrol" : 0 , "Diesel" : 1 , "CNG" : 2}} , inplace = True) 
    dataset.replace({"Transmission" : {"Manual" : 0 , "Automatic" : 1}} , inplace = True)
    dataset.replace({"Owner" : {"First" : 0 , "Second" : 1 , "Third" : 2}} , inplace = True)
    X = dataset.drop(["Car_Name" , "Selling_Price"] , axis = 1)
    Y = dataset["Selling_Price"]
    X_Train , X_Test , Y_Train , Y_Test = train_test_split(X , Y , test_size = 0.25 , random_state = 2)
    model_pre = Lasso()
    model_pre.fit(X_Train , Y_Train)
    values = [[cur_year , kms , fuel , trans , own]]
    val = np.array(values)
    dataset_pr = pd.DataFrame(data = val)
    dataset_pr.columns = ["Year" , "Dist_Driven" , "Fuel_Type" , "Transmission" , "Owner"]
    predicted_value = model_pre.predict(dataset_pr)
    print(predicted_value)

if __name__ == "__main__":
    regression(2015 , 30000 , 2 , 0 , 2)