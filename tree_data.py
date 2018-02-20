"""Assignment 2: Trees for Treemap

=== CSC148 Fall 2016 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.

"""
import os
from random import randint
import math


class AbstractTree:
    """A tree that is compatible with the treemap visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you adding and implementing
    new public *methods* for this interface.

    === Public Attributes ===
    @type data_size: int
        The total size of all leaves of this tree.
    @type colour: (int, int, int)
        The RGB colour value of the root of this tree.
        Note: only the colours of leaves will influence what the user sees.

    === Private Attributes ===
    @type _root: obj | None
        The root value of this tree, or None if this tree is empty.
    @type _subtrees: list[AbstractTree]
        The subtrees of this tree.
    @type _parent_tree: AbstractTree | None
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.
    - colour's elements are in the range 0-255.

    - If _root is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.
    - _subtrees IS allowed to contain empty subtrees (this makes deletion
      a bit easier).

    - if _parent_tree is not empty, then self is in _parent_tree._subtrees
    """
    def __init__(self, root, subtrees, data_size=0):
        """Initialize a new AbstractTree.

        If <subtrees> is empty, <data_size> is used to initialize this tree's
        data_size.
        Otherwise, the <data_size> parameter is ignored, and this
        tree's data_size is computed from the data_sizes of the subtrees.

        If <subtrees> is not empty, <data_size> should not be specified.

        This method sets the _parent_tree attribute for each subtree to self.

        A random colour is chosen for this tree.

        Preconditions:
        data_size >= 0

        Representation invariants:
        if <root> is None, then parent is None, data_size is 0,
        and <subtrees> is an empty list.

        @type self: AbstractTree
        @type root: object
        @type subtrees: list[AbstractTree]
        @type data_size: int
        @rtype: None
        """
        self._root = root
        self._subtrees = subtrees
        self._parent_tree = None

        # 1. Initialize self.colour and self.data_size, according to the
        # docstring.

        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        if self._subtrees == []:
            self.data_size = data_size
        else:
            self.data_size = 0
            for i in subtrees:
                self.data_size += i.data_size

        # 2. Properly set all _parent_tree attributes in self._subtrees

        for st in self._subtrees:
            st._parent_tree = self

    def is_empty(self):
        """Return True if this tree is empty.

        @type self: AbstractTree
            AbstractTree which to check
        @rtype: bool
            Whether it's empty or not
            True if it is empty
            False if it isn't empty
        """
        return self._root is None

    def generate_treemap(self, rect):
        """Run the treemap algorithm on this tree and return the rectangles.

        Each returned tuple contains a pygame rectangle and a colour:
        ((x, y, width, height), (r, g, b)).

        One tuple should be returned per non-empty leaf in this tree.

        If the tree has size 0,
        return an empty list.

        If the tree is just a single leaf with positive size,
        return a list containing just the single rectangle that covers the
        whole display area, as well as the colour of that leaf.

        Otherwise,
        if the display area's width is greater than its height:
        divide the display area into vertical rectangles, one smaller
        rectangle per non-zero-sized subtree, in proportion to the sizes of
        the subtrees.

        If the height is greater than or equal to the width,
        then make horizontal rectangles instead of vertical
        ones, and do the analogous operations as above.

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @rtype: list[((int, int, int, int), (int, int, int))]
        """

        if self.is_empty():
            return []
        elif self.data_size == 0:
            return []
        elif self._subtrees == [] and self.data_size > 0:
            return [(rect, self.colour)]

        n_empty = self.get_non_empty_leaves()
        final_rect_pos = find_last(n_empty)
        lst = []
        x, y, width, height = rect
        if width > height:
            # divide the rectangle into vertical strips
            offset1 = 0
            for i in range(0, len(n_empty)):
                if n_empty[i].data_size > 0 and i != final_rect_pos:
                    fraction = n_empty[i].data_size / self.data_size
                    adj_width = int(math.floor(fraction * width))
                    lst += [n_empty[i].generate_treemap((x + offset1, y,
                                                         adj_width, height))]
                    offset1 += adj_width
                elif i == final_rect_pos:
                    # if it is the last one, make it cover the remaining area
                    adj_width = width - offset1
                    lst += [n_empty[i].generate_treemap((x + offset1, y,
                                                         adj_width, height))]
        else:
            # width <= height
            # divide the rectangle into horizontal strips
            offset2 = 0
            for i in range(0, len(n_empty)):
                if n_empty[i].data_size > 0 and i != final_rect_pos:
                    fraction = n_empty[i].data_size / self.data_size
                    adj_height = int(math.floor(fraction * height))
                    lst += [n_empty[i].generate_treemap((x, y + offset2,
                                                         width, adj_height))]
                    offset2 += adj_height
                elif i == final_rect_pos:
                    # if it is the last one, make it cover the remaining area
                    adj_height = height - offset2
                    lst += [n_empty[i].generate_treemap((x, y + offset2,
                                                         width, adj_height))]
        return extract_nested(lst)

    # Helpers used for treemap_visualizer =====================================
    def get_non_empty_leaves(self):
        """
        Finds all the non-empty leaves in self._subtrees and returns them in a
        list
        @type self: AbstractTree
        @rtype: list[AbstractTree]
        """
        result = []
        for i in self._subtrees:
            if not i.is_empty() and i.data_size != 0:
                result.append(i)
        return result

    def delete_leaf(self):
        """
        Deletes the leaf from the tree (i.e. make the leaf an empty tree) and
        updates the data_size attributes of all ancestors

        === Preconditions: ===
        self is a leaf

        @type self: AbstractTree
        @rtype: None
        """
        self.update_data_size(0 - self.data_size)
        self.data_size = 0
        self._parent_tree = None
        self._subtrees = []
        self._root = None

    def increase_data_size(self):
        """
        Increases the data size of the selected leaf by 1%
        Also applies changes to the data sizes of the leaf's ancestors

        @type self: AbstractTree
        @rtype: None
        """
        self.update_data_size(int(math.ceil(self.data_size * 0.01)))

    def decrease_data_size(self):
        """
        Decreases the data size of the selected leaf by 1% to a minimum of 1
        Also applies changes to the data sizes of the leaf's ancestors

        @type self: AbstractTree
        @rtype: None
        """
        new_data_size = self.data_size - math.ceil(self.data_size * 0.01)
        if new_data_size >= 1:
            self.update_data_size(0 - int(math.ceil(self.data_size * 0.01)))
        else:
            pass

    def update_data_size(self, size_increment):
        """
        Updates the data size of self and all of its ancestors

        === Representation invariants ===
        size_increment < 0, decrease size
        size > 0, increase size
        =================================

        @type self: AbstractTree
        @type size_increment: int
        @rtype: None
        """
        if self is None:
            pass
        elif self.is_empty():
            pass
        elif self._parent_tree is None:
            self.data_size += size_increment
        else:
            self.data_size += size_increment
            self._parent_tree.update_data_size(size_increment)

    def generate_leafmap(self, rect):
        """Run the treemap algorithm on this tree and return the leaves.
        Note: The leaves are in the exact same order as the rectangles.

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
            Rectangle which to draw the leaves onto
        @rtype: list[AbstractTree]
            List of leaves (in the same order as generate_treemap rectangles)
        """
        if self.is_empty():
            return []
        elif self.data_size == 0:
            return []
        elif self._subtrees == [] and self.data_size > 0:
            return [self]

        n_empty = self.get_non_empty_leaves()
        lst = []
        x, y, width, height = rect
        if width > height:
            offset1 = 0
            for i in range(0, len(n_empty)):
                if i < len(n_empty) - 1:
                    fraction = n_empty[i].data_size / self.data_size
                    adj_width = math.floor(fraction * width)
                    lst += [n_empty[i].generate_leafmap((x + offset1, y,
                                                         adj_width, height))]
                    offset1 += adj_width
                else:
                    adj_width = width - offset1
                    lst += [n_empty[i].generate_leafmap((x + offset1, y,
                                                         adj_width, height))]
        else:
            offset2 = 0
            for i in range(0, len(n_empty)):
                if i < len(n_empty) - 1:
                    fraction = self._subtrees[i].data_size / self.data_size
                    adj_height = math.floor(fraction * height)
                    lst += [n_empty[i].generate_leafmap((x, y + offset2,
                                                         width, adj_height))]
                    offset2 += adj_height
                else:
                    adj_height = height - offset2
                    lst += [n_empty[i].generate_leafmap((x, y + offset2,
                                                         width, adj_height))]
        return extract_nested(lst)

    def find_leaf(self, coordinates, width, height):
        """
        Finds the leaf containing the coordinates (specified by a tuple)

        @type self: AbstractTree
        @type coordinates: tuple(int, int)
        @type width: int
        @type height: int
        @rtype: AbstractTree
        """
        map_ = self.generate_treemap((0, 0, width, height))
        leaves_map = self.generate_leafmap((0, 0, width, height))
        x, y = coordinates
        for i in range(0, len(map_)):
            if map_[i][0][0] <= x and (map_[i][0][0] + map_[i][0][2]) >= x and \
                            map_[i][0][1] <= y and \
                            (map_[i][0][1] + map_[i][0][3]) >= y:
                # check if x and y coordinates are both inside the rectangle
                # find the fraction of the total area that this represents, and
                # based on that, find the corresponding file/folder
                return leaves_map[i]

    def __eq__(self, other):
        """
        Sees if two leaves are equal

        === Precondition: ===
        self is a leaf and self._subtrees is []
        other is a leaf and other._subtrees is []

        @type self: AbstractTree
            first leaf of two to be compared
        @type other: AbstractTree
            second leaf of two to be compared
        @rtype: bool
        """
        return self._root == other.get_root() and \
            self._parent_tree == other._parent_tree

    def get_root(self):
        """
        Gets the root of a tree without having to explicity access the private
        attribute
        @type self: AbstractTree
        @rtype: None
        """
        return self._root

    # ========================================================================

    # To be implemented in subclasses, do nothing here
    def get_separator(self):
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        This is overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.

        @type self: AbstractTree
        @rtype: str
        """
        raise NotImplementedError


class FileSystemTree(AbstractTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _root attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/David/csc148/assignments'

    The data_size attribute for regular files as simply the size of the file,
    as reported by os.path.getsize.

    === Inherited attributes ===
    @type _root: str
        Name of dir/file
    @type _subtrees: list[FileSystemTree]
        Everything inside dir (empty list for files)
    @type _data_size: int
        Size of everything contained in dir (file size for files)
    @type _parent_tree: FileSystemTree
        The parent FileSystemTree, aka the parent directory (automatically set)
    """
    def __init__(self, path):
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.

        @type self: FileSystemTree
        @type path: str
        @rtype: None
        """
        # # os.path.isdir
        # # os.listdir
        # # os.path.join
        # # os.path.getsize
        # # os.path.basename

        if not os.path.isdir(path):
            AbstractTree.__init__(self, os.path.basename(path), [],
                                  os.path.getsize(path))
        else:
            # don't specify size (auto calculated)
            subtrees = []
            for d in os.listdir(path):
                subtrees += [FileSystemTree(os.path.join(path, d))]
            AbstractTree.__init__(self, os.path.basename(path), subtrees)

    def get_separator(self):
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        === Preconditions: ===
        self is a leaf, self._subtrees = []

        @type self: FileSystemTree
            The leaf which to return the path of
        @rtype: str
            The path of the leaf
        """
        if self is None:
            return ''
        elif self._parent_tree is None:
            return self._root
        else:
            p = os.path.join(self._parent_tree.get_separator(), self._root)
            return p


# Helpers for AbstractTree ===================================================

def extract_nested(nested_lst):
    """
    Extract a list from a nested list. Does not mutate the original list
    @type nested_lst: list[object|list]
    @rtype: list[object]
    """
    if not isinstance(nested_lst, list):
        return nested_lst
    else:
        lst = []
        for i in range(0, len(nested_lst)):
            if isinstance(nested_lst[i], list):
                lst += extract_nested(nested_lst[i])
            else:
                lst += [nested_lst[i]]
        return lst


def find_last(lst):
    """
    Find the last non-zero sized leaf in a list of subtrees and
    return its position
    @type lst: list[AbstractTree]
    @rtype: int
    """
    result = len(lst)-1
    for i in range(len(lst)-1, -1):
        if lst[i].is_empty() or lst[i].data_size == 0:
            result = i
        else:
            return result
    return result

# ============================================================================

if __name__ == '__main__':
    import python_ta
    # Remember to change this to check_all when cleaning up your code.
    python_ta.check_errors(config='pylintrc.txt')
    python_ta.check_all(config='pylintrc.txt')
