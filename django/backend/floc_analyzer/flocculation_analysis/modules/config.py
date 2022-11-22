import pandas as pd

# paths
imp_path = r"sustainable-drinking-water-treatment-plant\flocculation_analysis\data\analysis.txt"
exp_path = r"sustainable-drinking-water-treatment-plant\flocculation_analysis\data\actualvpredicted.txt"
db_path = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=sustainable-drinking-water-treatment-plant\flocculation_analysis\data\220630_flocculation.accdb;')

pipe_savepath = r"sustainable-drinking-water-treatment-plant\flocculation_analysis\data\flocculation_analysis_pipeline"
pipe_loadpath = pipe_savepath

# random state train_test_split
rand_state = 11

# test dataset size
test_dataset_size = 0.05

# evaluation number of algorithm optimizer
alg_num = 10

# evaluation number of input features optimizer
feature_num = 1000

# weight of penalties for input optimizer
pen_ftur = 0.25
pen_per = 0.25
pen_fpH = 0.25
pen_fEC = 0.25