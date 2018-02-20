"""
Tests delete method of AbstractTree
"""
from tree_data import *
from hypothesis import *
import unittest


class DeleteTest(unittest.TestCase):
    def test_delete_single(self):
        sub1 = AbstractTree('1', [], 1)
        sub1.delete_leaf()
        self.assertEqual(sub1._parent_tree, None)
        self.assertEqual(sub1.data_size, 0)
        self.assertEqual(sub1._subtrees, [])

    def test_del_one(self):
        sub1 = AbstractTree('1', [], 1)
        sub2 = AbstractTree('2', [], 2)
        sub3 = AbstractTree('3', [], 3)
        parent = AbstractTree('parent', [sub1, sub2, sub3])
        sub1.delete_leaf()
        self.assertEqual(sub1._parent_tree, None)
        self.assertEqual(sub1.data_size, 0)
        self.assertEqual(sub1._subtrees, [])

    def test_del_two(self):
        sub1 = AbstractTree('1', [], 1)
        sub2 = AbstractTree('2', [], 2)
        sub3 = AbstractTree('3', [], 3)
        parent = AbstractTree('parent', [sub1, sub2, sub3])
        parent2 = AbstractTree('parent2', [parent])
        sub1.delete_leaf()
        sub2.delete_leaf()
        self.assertEqual(sub1._parent_tree, None)
        self.assertEqual(sub1.data_size, 0)
        self.assertEqual(sub1._subtrees, [])
        self.assertEqual(sub2._parent_tree, None)
        self.assertEqual(sub2.data_size, 0)
        self.assertEqual(sub2._subtrees, [])
        self.assertEqual(parent.data_size, 3)
        self.assertEqual(parent2.data_size, 3)


if __name__ == '__main__':
    unittest.main()
