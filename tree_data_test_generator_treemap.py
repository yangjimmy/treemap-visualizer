import unittest
from tree_data import FileSystemTree
from tree_data_helper_test import *

test_directory = "Testing\\"

class Test_TreeData_GenerateTreeMap(unittest.TestCase):

    # ==============================================================
    # If it is an empty directory, create an empty list
    # ==============================================================
    def test_empty_directory(self):
        global test_directory

        directory = test_directory + "Empty Folder"
        filesystem = FileSystemTree(directory)
        rects1 = filesystem.generate_treemap((0, 0, 500, 500))
        self.assertEqual(rects1, [])

    # ==============================================================
    # If it only has a single empty folder, create an empty list
    # ==============================================================
    def test_singlefolder(self):
        global test_directory

        directory = test_directory + "One folder"
        filesystem = FileSystemTree(directory)
        rects1 = filesystem.generate_treemap((0, 0, 500, 500))
        self.assertEqual(rects1, [])

    # ==============================================================
    # If it is a nested folder of empty folders, return an empty list
    # ==============================================================
    def test_nested_empty_folders(self):
        global test_directory

        filesys = FileSystemTree(test_directory + "Nested empty folder")
        rects1 = filesys.generate_treemap((0, 0, 500, 500))
        self.assertEqual(rects1, [])

    # ==============================================================
    # If it has one file create a rectangle that covers the entire screen
    # ==============================================================
    def test_single_file(self):
        global test_directory
        directory = test_directory + "One file"
        filesystem = FileSystemTree(directory)
        print_directory(filesystem)

        # If width == height
        rects1 = filesystem.generate_treemap((0, 0, 500, 500))
        self.assertEqual(rects1[0][0], (0, 0, 500, 500))
        self.assertEqual(len(rects1[0][1]), 3)
        self.assertEqual(len(rects1), 1)

        # If width < height
        rects2 = filesystem.generate_treemap((0, 0, 200, 500))
        self.assertEqual(len(rects2[0][1]), 3)
        self.assertEqual(rects2[0][0], (0, 0, 200, 500))
        self.assertEqual(len(rects2), 1)

        # If width > height
        rects3 = filesystem.generate_treemap((0, 0, 1200, 500))
        self.assertEqual(len(rects3[0][1]), 3)
        self.assertEqual(rects3[0][0], (0, 0, 1200, 500))
        self.assertEqual(len(rects3), 1)

    # ==============================================================
    # If two files have same size, return two rectangles with (width|height)/2
    # ==============================================================
    def test_two_same_files(self):
        global test_directory
        directory = test_directory + "Two files"
        filesystem = FileSystemTree(directory)
        print(print_directory(filesystem))

        # If width == height
        rects = filesystem.generate_treemap((0, 0, 200, 200))
        self.assertEqual(len(rects[0][1]), 3)
        self.assertEqual(rects[0][0], (0, 0, 200, 100))
        self.assertEqual(rects[1][0], (0, 100, 200, 100))
        self.assertEqual(len(rects), 2)

        # If width < height
        rects = filesystem.generate_treemap((0, 0, 100, 200))
        self.assertEqual(len(rects[0][1]), 3)
        self.assertEqual(rects[0][0], (0, 0, 100, 100))
        self.assertEqual(rects[1][0], (0, 100, 100, 100))
        self.assertEqual(len(rects), 2)

        # If width > height
        rects = filesystem.generate_treemap((0, 0, 300, 200))
        self.assertEqual(len(rects[0][1]), 3)
        self.assertEqual(rects[0][0], (0, 0, 150, 200))
        self.assertEqual(rects[1][0], (150, 0, 150, 200))
        self.assertEqual(len(rects), 2)

    # ==============================================================
    # If files have diff size, return rectangles with diff width/height
    # ==============================================================
    def test_diff_files(self):
        global test_directory
        directory = test_directory + "Four files"
        filesystem = FileSystemTree(directory)
        print_directory(filesystem)

        # If width <= height
        rects = filesystem.generate_treemap((0, 0, 200, 200))
        for i in range(0, 4):
            self.assertEqual(len(rects[i][1]), 3)
        self.assertEqual(rects[0][0], (0, 0, 200, 125))
        self.assertEqual(rects[1][0], (0, 125, 200, 12))
        self.assertEqual(rects[2][0], (0, 137, 200, 25))
        self.assertEqual(rects[3][0], (0, 162, 200, 38))

        # If width > height
        rects = filesystem.generate_treemap((0, 0, 200, 100))
        for i in range(0, 4):
            self.assertEqual(len(rects[i][1]), 3)
        self.assertEqual(rects[0][0], (0, 0, 125, 100))
        self.assertEqual(rects[1][0], (125, 0, 12, 100))
        self.assertEqual(rects[2][0], (137, 0, 25, 100))
        self.assertEqual(rects[3][0], (162, 0, 38, 100))
        self.assertEqual(len(rects), 4)

    # ==============================================================
    # Testing depth 1-2
    # ==============================================================
    def test_depth_one_two(self):
        global test_directory
        directory = test_directory + "Depth 1-2"
        filesys = FileSystemTree(directory)
        print_directory(filesys)

        # If width > height
        sys = FileSystemTree(directory)
        rects = sys.generate_treemap((0, 0, 500, 300))
        for i in range(0, 4):
            self.assertEqual(len(rects[i][1]), 3)
        self.assertEqual(rects[0][0], (0, 0, 36, 300))
        self.assertEqual(rects[1][0], (36, 0, 30, 300))
        self.assertEqual(rects[2][0], (66, 0, 25, 300))
        self.assertEqual(rects[3][0], (91, 0, 409, 300))
        self.assertEqual(len(rects), 4)

        # If width == height
        rects = sys.generate_treemap((0, 0, 100, 100))
        for i in range(0, 4):
            self.assertEqual(len(rects[i][1]), 3)
        self.assertEqual(rects[0][0], (0, 0, 100, 7))
        self.assertEqual(rects[1][0], (0, 7, 100, 6))
        self.assertEqual(rects[2][0], (0, 13, 5, 87))
        self.assertEqual(rects[3][0], (5, 13, 95, 87))
        self.assertEqual(len(rects), 4)

        # If width < height
        rects = sys.generate_treemap((0, 0, 5000, 4500))
        for i in range(0, 4):
            self.assertEqual(len(rects[i][1]), 3)
        self.assertEqual(rects[0][0], (0, 0, 361, 4500))
        self.assertEqual(rects[1][0], (361, 0, 308, 4500))
        self.assertEqual(rects[2][0], (669, 0, 4331, 265))
        self.assertEqual(rects[3][0], (669, 265, 4331, 4235))
        self.assertEqual(len(rects), 4)

    # ==============================================================
    # Testing depth 2
    # ==============================================================
    def test_depth_two(self):
        global test_directory
        directory = test_directory + "Depth 2"
        filesys = FileSystemTree(directory)
        print_directory(filesys)

        # If width < height
        rects = filesys.generate_treemap((0, 0, 5000, 4000))
        for i in range(0, 4):
            self.assertEqual(len(rects[i][1]), 3)
        self.assertEqual(rects[0][0], (0, 0, 2214, 3405))
        self.assertEqual(rects[1][0], (0, 3405, 2214, 595))
        self.assertEqual(rects[2][0], (2214, 0, 2786, 3896))
        self.assertEqual(rects[3][0], (2214, 3896, 2786, 104))
        self.assertEqual(len(rects), 4)

        # If width == height
        rects = filesys.generate_treemap((0, 0, 100, 100))
        for i in range(0, 4):
            self.assertEqual(len(rects[i][1]), 3)
        self.assertEqual(rects[0][0], (0, 0, 85, 44))
        self.assertEqual(rects[1][0], (85, 0, 15, 44))
        self.assertEqual(rects[2][0], (0, 44, 97, 56))
        self.assertEqual(rects[3][0], (97, 44, 3, 56))
        self.assertEqual(len(rects), 4)



if __name__ == '__main__':
    unittest.main()
