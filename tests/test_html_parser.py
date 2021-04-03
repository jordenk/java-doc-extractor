from src.html_parser import collect_html_file_paths
import os


def test_collect_html_file_paths():
    test_dir_path = os.path.join(os.path.dirname(__file__))
    test_data_path = os.path.join(test_dir_path, "resources", "html_parser_test_data", "nested_file_structure_data")

    actual = collect_html_file_paths(test_data_path, [])
    expected = {
        os.path.join(test_data_path, "test_top_b.html"),
        os.path.join(test_data_path, "test_top_c.html"),
        os.path.join(test_data_path, "nested_2a", "nested_3b", "test_2a_3b_a.html"),
        os.path.join(test_data_path, "nested_2a", "test_2a_a.html"),
        os.path.join(test_data_path, "nested_2a", "nested_3a", "test_2a_3a_a.html"),
        os.path.join(test_data_path, "nested_2b", "test_2b_a.html"),
        os.path.join(test_data_path, "test_top_a.html")
    }
    assert set(actual) == expected
