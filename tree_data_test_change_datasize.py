import unittest
from tree_data import FileSystemTree
from tree_data_helper_test import print_directory

DIR_PATH = "Testing\\"

# THE CONTRACT:
""" Increases / decreases the datasize and its ascendents by an amount
       When <amount> is positive, it will increase the data_size and its
       ascendents by <amount>.
       When <amount> is negative, it will decrease the data_size and its
       ascendents by <amount>.
       Pre-condition: data_size > amount
       @type self: AbstractTree
       @rtype: None
"""


class Test_File_System(unittest.TestCase):

    def test_constructor_filenames(self):
        filesystem = FileSystemTree(DIR_PATH + "Birds.txt")
        self.assertEqual(filesystem.data_size, 22)
        filesystem.update_data_size(-10)
        self.assertEqual(filesystem.data_size, 12)

    def test_constructor_depth_1_2(self):
        filesystem = FileSystemTree(DIR_PATH + "Depth 1-2")
        print_directory(filesystem)
        print(filesystem._subtrees[3]._subtrees)
        a, b, c = filesystem.data_size, filesystem._subtrees[3].data_size, filesystem._subtrees[3]._subtrees[1].data_size
        filesystem._subtrees[3]._subtrees[1].update_data_size(-100000)
        self.assertEqual(filesystem.data_size, a - 100000)
        self.assertEqual(filesystem._subtrees[3].data_size, b - 100000)
        self.assertEqual(filesystem._subtrees[3]._subtrees[1].data_size, c - 100000)

    def test_constructor_depth_2(self):
        filesystem = FileSystemTree(DIR_PATH + "Depth 2")
        print_directory(filesystem)
        a = filesystem.data_size
        b1 = filesystem._subtrees[0].data_size
        b2 = filesystem._subtrees[1].data_size
        c = filesystem._subtrees[0]._subtrees[1].data_size

        filesystem._subtrees[0]._subtrees[1].update_data_size(-100)
        self.assertEqual(filesystem._subtrees[0]._subtrees[1].data_size, c - 100)
        self.assertEqual(filesystem._subtrees[0].data_size, b1 - 100)
        self.assertEqual(filesystem.data_size, a - 100)
        self.assertEqual(filesystem._subtrees[1].data_size, b2)

    def test_decrease_in_middle(self):
        filesystem = FileSystemTree(DIR_PATH + "Four files with a folder")
        print_directory(filesystem)
        a = filesystem.data_size
        b1 = filesystem._subtrees[0].data_size
        b2 = filesystem._subtrees[1].data_size
        c1 = filesystem._subtrees[1]._subtrees[0].data_size
        c2 = filesystem._subtrees[1]._subtrees[1].data_size
        c3 = filesystem._subtrees[1]._subtrees[2].data_size
        filesystem._subtrees[1].update_data_size(-5)
        self.assertEqual(filesystem.data_size, a - 5)
        self.assertEqual(b1, filesystem._subtrees[0].data_size)
        self.assertEqual(b2 - 5, filesystem._subtrees[1].data_size)
        self.assertEqual(c1, filesystem._subtrees[1]._subtrees[0].data_size)
        self.assertEqual(c2, filesystem._subtrees[1]._subtrees[1].data_size)
        self.assertEqual(c3, filesystem._subtrees[1]._subtrees[2].data_size)

    def test_decrease_root(self):
        filesystem = FileSystemTree(DIR_PATH + "Four files with a folder")
        print_directory(filesystem)
        a = filesystem.data_size
        b1 = filesystem._subtrees[0].data_size
        b2 = filesystem._subtrees[1].data_size
        c1 = filesystem._subtrees[1]._subtrees[0].data_size
        c2 = filesystem._subtrees[1]._subtrees[1].data_size
        c3 = filesystem._subtrees[1]._subtrees[2].data_size
        filesystem.update_data_size(-5)
        self.assertEqual(filesystem.data_size, a - 5)
        self.assertEqual(b1, filesystem._subtrees[0].data_size)
        self.assertEqual(b2, filesystem._subtrees[1].data_size)
        self.assertEqual(c1, filesystem._subtrees[1]._subtrees[0].data_size)
        self.assertEqual(c2, filesystem._subtrees[1]._subtrees[1].data_size)
        self.assertEqual(c3, filesystem._subtrees[1]._subtrees[2].data_size)

if __name__ == '__main__':
    unittest.main()
