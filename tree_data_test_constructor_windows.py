import unittest
from tree_data import FileSystemTree

DIR_PATH = "Testing\\"


class Test_File_System(unittest.TestCase):

    @staticmethod
    def get_names(fs):
        if fs.is_empty():
            return []

        string_list = [fs._root]
        for tree in fs._subtrees:
            string_list.append(Test_File_System.get_names(tree))
        return string_list

    def check_color(self, fs):
        if fs.is_empty():
            return

        for val in fs.colour:
            self.assertGreaterEqual(val, 0)
            self.assertLessEqual(val, 255)
        for tree in fs._subtrees:
            self.check_color(tree)

    def check_parent(self, fs):
        if fs.is_empty():
            return False

        if len(fs._subtrees) == 0:
            if fs._parent_tree is None:
                return True
            return False

        print(fs._root)

        for subtree in fs._subtrees:
            if subtree._parent_tree != fs:
                return False

            if len(subtree._subtrees) > 0:
                if self.check_parent(subtree) is False:
                    return False
        return True

    # MAIN TESTING IS BELOW ==========================

    def test_constructor_filenames(self):
        filesystem = FileSystemTree(DIR_PATH + "Birds.txt")
        lst = Test_File_System.get_names(filesystem)
        self.assertEqual(lst, ['Birds.txt'])
        self.assertEqual(filesystem.data_size, 22)
        self.assertEqual(filesystem._parent_tree, None)
        self.check_color(filesystem)
        self.assertTrue(self.check_parent(filesystem))

    def test_constructor_emptyfolder_names(self):
        filesystem = FileSystemTree(DIR_PATH + "Empty Folder")
        lst = Test_File_System.get_names(filesystem)
        answer = ['Empty Folder']
        self.assertEqual(lst, answer)
        self.assertEqual(filesystem.data_size, 0)
        self.assertEqual(filesystem._parent_tree, None)
        self.check_color(filesystem)
        self.assertTrue(self.check_parent(filesystem))

    def test_constructor_multiple_empty_folders(self):
        filesystem = FileSystemTree(DIR_PATH + "Nested empty folder")
        lst = Test_File_System.get_names(filesystem)
        answer = ['Nested empty folder', ['Nested empty folder',
                                          ['Nested empty folder']]]
        self.assertEqual(lst, answer)
        self.assertEqual(filesystem.data_size, 0)
        self.assertEqual(filesystem._parent_tree, None)
        self.assertEqual(filesystem._subtrees[0]._parent_tree, filesystem)
        self.assertEqual(filesystem._subtrees[0]._subtrees[0]._parent_tree, filesystem._subtrees[0])
        self.check_color(filesystem)
        self.assertTrue(self.check_parent(filesystem))

    def test_constructor_one_folder(self):
        filesys = FileSystemTree(DIR_PATH + "One folder")
        lst = Test_File_System.get_names(filesys)
        answer = ["One folder", ["One folder"]]
        self.assertEqual(lst, answer)
        self.assertEqual(filesys.data_size, 0)
        self.assertEqual(filesys._subtrees[0].data_size, 0)
        self.assertEqual(filesys._subtrees[0]._parent_tree, filesys)
        self.assertEqual(filesys._parent_tree, None)
        self.check_color(filesys)
        self.assertTrue(self.check_parent(filesys))

    def test_constructor_depth_1_2(self):
        filesystem = FileSystemTree(DIR_PATH + "Depth 1-2")
        lst = Test_File_System.get_names(filesystem)
        answer = ['Depth 1-2', ['City.jpg'], ['Earth.jpg'], ['Empty Folder'],
                                  ['Stuff', ['Nature.jpg'], ['Squirrel.jpg']]]
        self.assertEqual(lst, answer)
        self.check_color(filesystem)
        self.assertTrue(self.check_parent(filesystem))

    def test_constructor_depth_2(self):
        filesystem = FileSystemTree(DIR_PATH + "Depth 2")
        lst = Test_File_System.get_names(filesystem)
        answer = ['Depth 2', ['Random 1', ['Bank.xlsx'], ['Bird Courses.txt']], ['Random 2', ['COG.docx'], ['sadsad.txt']]]
        self.assertEqual(lst, answer)
        self.check_color(filesystem)
        self.assertTrue(self.check_parent(filesystem))

    def test_four_files_with_folder(self):
        filesys = FileSystemTree(DIR_PATH + "Four files with a folder")
        lst = Test_File_System.get_names(filesys)
        answer = ['Four files with a folder', ['birds 10bytes.txt'], ['New folder', ['birds 1byte.txt'], ['birds 2bytes.txt'], ['birds 3bytes.txt']]]
        self.assertEqual(lst, answer)
        self.assertEqual(filesys.data_size, 16)
        self.assertEqual(filesys._subtrees[0].data_size, 10)
        self.assertEqual(filesys._subtrees[1]._subtrees[0].data_size, 1)
        self.assertEqual(filesys._subtrees[1]._subtrees[1].data_size, 2)
        self.assertEqual(filesys._subtrees[1]._subtrees[2].data_size, 3)
        for i in range(0, 2):
            self.assertEqual(filesys._subtrees[i]._parent_tree, filesys)
        for i in range(0, 3):
            self.assertEqual(filesys._subtrees[1]._subtrees[i]._parent_tree, filesys._subtrees[1])
        self.assertTrue(self.check_parent(filesys))

if __name__ == '__main__':
    unittest.main()
