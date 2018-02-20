import unittest
from tree_data import FileSystemTree

DIR_PATH = "Testing\\"

class Test_Get_Separator(unittest.TestCase):
    """
            The get_separator() on the parent folder should be the parent folder's name
            The get_separator() on the subtree folders should be parent_folder's get_separator() / ... / folder's name
            The get_separator() on a file should be parent_folder's get_separator()/.../ filename.extension
    """

    def test_empty_folder(self):
        filesys = FileSystemTree(DIR_PATH + "Empty Folder")
        self.assertEqual(filesys.get_separator(), "Empty Folder")

    def test_nested_empty_folder(self):
        filesys = FileSystemTree(DIR_PATH + "Nested empty folder")
        self.assertEqual(filesys.get_separator(), "Nested empty folder")
        self.assertEqual(filesys._subtrees[0].get_separator(), "Nested empty folder\\Nested empty folder")
        self.assertEqual(filesys._subtrees[0]._subtrees[0].get_separator(),
                         "Nested empty folder\\Nested empty folder\\Nested empty folder")

    def test_one_file(self):
        filesys = FileSystemTree(DIR_PATH + "One file")
        self.assertEqual(filesys.get_separator(), "One file")
        self.assertEqual(filesys._subtrees[0].get_separator(), "One file\Birds.txt")

    def test_two_files(self):
        filesys = FileSystemTree(DIR_PATH + "Two files")
        self.assertEqual(filesys.get_separator(), "Two files")
        self.assertEqual(filesys._subtrees[0].get_separator(), "Two files\Birds 1.txt")
        self.assertEqual(filesys._subtrees[1].get_separator(), "Two files\Birds 2.txt")

    def test_four_files(self):
        filesys = FileSystemTree(DIR_PATH + "Four files")
        self.assertEqual(filesys.get_separator(), "Four files")
        self.assertEqual(filesys._subtrees[0].get_separator(), "Four files\\birds 10bytes.txt")
        self.assertEqual(filesys._subtrees[1].get_separator(), "Four files\\birds 1byte.txt")
        self.assertEqual(filesys._subtrees[3].get_separator(), "Four files\\birds 3bytes.txt")
        self.assertEqual(filesys._subtrees[2].get_separator(), "Four files\\birds 2bytes.txt")

    def test_four_files_with_folder(self):
        filesys = FileSystemTree(DIR_PATH + "Four files with a folder")
        self.assertEqual(filesys.get_separator(), "Four files with a folder")
        self.assertEqual(filesys._subtrees[0].get_separator(), "Four files with a folder\\birds 10bytes.txt")
        self.assertEqual(filesys._subtrees[1].get_separator(), "Four files with a folder\\New folder")
        self.assertEqual(filesys._subtrees[1]._subtrees[0].get_separator(), "Four files with a folder\\New folder\\birds 1byte.txt")
        self.assertEqual(filesys._subtrees[1]._subtrees[2].get_separator(), "Four files with a folder\\New folder\\birds 3bytes.txt")
        self.assertEqual(filesys._subtrees[1]._subtrees[1].get_separator(), "Four files with a folder\\New folder\\birds 2bytes.txt")

    def test_depth_1_2(self):
        filesys = FileSystemTree(DIR_PATH + "Depth 1-2")
        self.assertEqual(filesys.get_separator(), "Depth 1-2")
        self.assertEqual(filesys._subtrees[0].get_separator(), "Depth 1-2\\City.jpg")
        self.assertEqual(filesys._subtrees[1].get_separator(), "Depth 1-2\\Earth.jpg")
        self.assertEqual(filesys._subtrees[2].get_separator(), "Depth 1-2\\Empty Folder")
        self.assertEqual(filesys._subtrees[3].get_separator(), "Depth 1-2\\Stuff")
        self.assertEqual(filesys._subtrees[3]._subtrees[0].get_separator(), "Depth 1-2\\Stuff\\Nature.jpg")
        self.assertEqual(filesys._subtrees[3]._subtrees[1].get_separator(), "Depth 1-2\\Stuff\\Squirrel.jpg")

    def test_depth_2(self):
        filesys = FileSystemTree(DIR_PATH + "Depth 2")
        self.assertEqual(filesys.get_separator(), "Depth 2")
        self.assertEqual(filesys._subtrees[0].get_separator(), "Depth 2\\Random 1")
        self.assertEqual(filesys._subtrees[1].get_separator(), "Depth 2\\Random 2")
        self.assertEqual(filesys._subtrees[0]._subtrees[0].get_separator(), "Depth 2\\Random 1\\Bank.xlsx")
        self.assertEqual(filesys._subtrees[0]._subtrees[1].get_separator(), "Depth 2\\Random 1\\Bird Courses.txt")
        self.assertEqual(filesys._subtrees[1]._subtrees[0].get_separator(), "Depth 2\\Random 2\\COG.docx")
        self.assertEqual(filesys._subtrees[1]._subtrees[1].get_separator(), "Depth 2\\Random 2\\sadsad.txt")

if __name__ == "__main__":
    unittest.main()
