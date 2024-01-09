from df_csv_excel.read_data import read_data_by_path, greet

def test_read_data_by_path():
    assert read_data_by_path('') == None
    assert read_data_by_path(None) == None


def test_greet():
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"