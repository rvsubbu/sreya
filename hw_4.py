import ipytest
import traceback

#ipytest.autoconfig()
import pandas as pd
#import pdb; pdb.set_trace()
requests = pd.read_csv("http://storage.googleapis.com/python-public-policy/data/cleaned_311_data_hw2.csv.zip")
#print(type(requests))
#print(requests.columns.tolist())
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #print(requests)



def flag_graffiti(row):
    try:
       #print(row)
       if isinstance(row["complaint_type"], str) and "graffiti" in row["complaint_type"].lower():
           return True
       elif isinstance(row["descriptor"], str) and "graffiti" in row["descriptor"].lower():
           return True
       elif isinstance(row["resolution_description"], str) and "graffiti" in row["resolution_description"].lower():
           return True
       else:
           return False
    except Exception as e:
        print("Exception:", e)
    return False

requests["graffiti_flag"] = requests.apply(flag_graffiti, axis =1)
#print(requests.columns.tolist())

def test_complaint_type():
    test_row = pd.Series({
        "complaint_type": "graffiti",
        "descriptor": "",
        "resolution_description": ""
    })
    assert flag_graffiti(test_row) == True

def test_descriptor():
    test_row = pd.Series({
        "complaint_type": "",
        "descriptor": "graffiti",
        "resolution_description": ""
    })
    assert flag_graffiti(test_row) == True


def test_description():
    test_row = pd.Series({
        "complaint_type": "",
        "descriptor": "",
        "resolution_description": "graffiti"
    })
    assert flag_graffiti(test_row) == True


def test_none():
    test_row = pd.Series({
        "complaint_type": "",
        "descriptor": "",
        "resolution_description": ""
    })
    assert flag_graffiti(test_row) == False


def test_mixed_cases():
    test_row = pd.Series({
        "complaint_type": "GrafFiti",
        "descriptor": "",
        "resolution_description": ""
    })
    assert flag_graffiti(test_row) == True


def test_substring():
    test_row = pd.Series({
        "complaint_type": "",
        "descriptor": "there's graffiti on the wall",
        "resolution_description": ""
    })
    assert flag_graffiti(test_row) == True

def test_graffiti_flag(df):
    assert 'graffiti_flag' in df.columns, "column missing"
    assert df.dtypes['graffiti_flag'] == 'bool', "column should be booleans"

test_complaint_type()
test_descriptor()
test_description()
test_none()
test_mixed_cases()
test_substring()

test_graffiti_flag(requests)

df_graffiti = requests[ (requests["complaint_type"].str.contains("graffiti", case=False)) |
                        (requests["descriptor"].str.contains("graffiti", case=False)) |
                        (requests["resolution_description"].str.contains("graffiti", case=False))]

def test_all_have_graffiti():
    assert df_graffiti['graffiti_flag'].all(), "not all have graffiti_flag set to True"

test_all_have_graffiti()

community_boards = df_graffiti.groupby(by="community_board").size().reset_index()
print(community_boards)
#print(community_boards.columns.tolist())
max_community_board = community_boards.iloc[community_boards[0].idxmax()]
print("<", max_community_board['community_board'], "> has", max_community_board[0], "graffiti cases")
requests["graffiti_flag2"] = requests['complaint_type'].str.contains("graffiti", case=False)
print(requests["graffiti_flag2"])


# Flag whether a complaint is school related or not
requests["school_problem"] = requests['complaint_type'].str.contains("school", case=False)
print(requests["school_problem"])
