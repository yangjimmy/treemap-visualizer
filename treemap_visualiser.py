"""Assignment 2: Treemap Visualiser

=== CSC148 Fall 2016 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code to run the treemap visualisation program.
It is responsible for initializing an instance of AbstractTree (using a
concrete subclass, of course), rendering it to the user using pygame,
and detecting user events like mouse clicks and key presses and responding
to them.
"""
import pygame
from tree_data import FileSystemTree
from population import PopulationTree


# Screen dimensions and coordinates
ORIGIN = (0, 0)
WIDTH = 1024
HEIGHT = 768
FONT_HEIGHT = 30                       # The height of the text display.
TREEMAP_HEIGHT = HEIGHT - FONT_HEIGHT  # The height of the treemap display.

# Font to use for the treemap program.
FONT_FAMILY = 'Consolas'


def run_visualisation(tree):
    """Display an interactive graphical display of the given tree's treemap.

    @type tree: AbstractTree
        the tree to visualize
    @rtype: None
    """
    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # print(tree._root, tree.data_size)
    # Render the initial display of the static treemap.
    render_display(screen, tree, '')

    # Start an event loop to respond to events.
    event_loop(screen, tree)


def render_display(screen, tree, text):
    """Render a treemap and text display to the given screen.

    Use the constants TREEMAP_HEIGHT and FONT_HEIGHT to divide the
    screen vertically into the treemap and text comments.

    @type screen: pygame.Surface
        The display window
    @type tree: AbstractTree
        The tree to render
    @type text: str
        The text to render.
    @rtype: None
    """
    # First, clear the screen
    pygame.draw.rect(screen, pygame.color.THECOLORS['black'],
                     (0, 0, WIDTH, HEIGHT))

    rectangle_list = tree.generate_treemap((0, 0, WIDTH, TREEMAP_HEIGHT))
    if tree.data_size > 0:
        # if the data size is less than 0, the screen is black
        # draw each rectangle returned by generate_treemap
        for i in rectangle_list:
            pygame.draw.rect(screen, i[1], i[0])
        _render_text(screen, text)

    # This must be called *after* all other pygame functions have run.
    pygame.display.flip()


def _render_text(screen, text):
    """Render text at the bottom of the display.

    @type screen: pygame.Surface
        the display window
    @type text: str
        the text to render
    @rtype: None
    """
    # The font we want to use
    font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)
    text_surface = font.render(text, 1, pygame.color.THECOLORS['white'])

    # Where to render the text_surface
    text_pos = (0, HEIGHT - FONT_HEIGHT + 4)
    screen.blit(text_surface, text_pos)


def event_loop(screen, tree):
    """Respond to events (mouse clicks, key presses) and update the display.

    Note that the event loop is an *infinite loop*: it continually waits for
    the next event, determines the event's type, and then updates the state
    of the visualisation or the tree itself, updating the display if necessary.
    This loop ends when the user closes the window.

    @type screen: pygame.Surface
        the display window
    @type tree: AbstractTree
        the tree which to render
    @rtype: None
    """

    selected_leaf = None

    while True:
        # Wait for an event
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            return

        # render_display is called as data_sizes change, and
        # treemap and rectangles are updated
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # if user clicks left mouse button, select or deselect a leaf
            previous_leaf = selected_leaf
            selected_leaf = tree.find_leaf(event.pos, WIDTH, TREEMAP_HEIGHT)
            if selected_leaf is not None and previous_leaf is None:
                # selecting new leaf
                render_display(screen, tree,
                               selected_leaf.get_separator() + ' (' +
                               str(selected_leaf.data_size) + ')')
            elif selected_leaf is not None and previous_leaf != selected_leaf:
                # selecting new leaf
                render_display(screen, tree,
                               selected_leaf.get_separator() + ' (' +
                               str(selected_leaf.data_size) + ')')
            elif selected_leaf is not None and previous_leaf == selected_leaf:
                # deselecting leaf
                render_display(screen, tree, '')
                selected_leaf = None

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            # if user clicks right mouse button, delete the leaf
            to_be_deleted = tree.find_leaf(event.pos, WIDTH, TREEMAP_HEIGHT)
            if to_be_deleted is not None:
                # delete the leaf
                to_be_deleted.delete_leaf()
            if selected_leaf is None:
                # no selected leaf, don't display path
                render_display(screen, tree, '')
            elif selected_leaf.is_empty():
                # selected is an empty leaf, don't display path
                render_display(screen, tree, '')
            elif to_be_deleted == selected_leaf:
                # deleted the selected leaf, don't display path
                render_display(screen, tree, '')
            else:
                # selected leaf is not deleted, continue to display its path
                render_display(screen, tree,
                               selected_leaf.get_separator() + ' (' +
                               str(selected_leaf.data_size) + ')')

        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            # if up arrow key is pressed, selected leaf's size increases
            if selected_leaf is None:
                render_display(screen, tree, '')
            else:
                selected_leaf.increase_data_size()
                render_display(screen, tree, selected_leaf.get_separator() +
                               ' (' + str(selected_leaf.data_size) + ')')
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            # if down arrow key is pressed, selected leaf's size decreases
            if selected_leaf is None:
                render_display(screen, tree, '')
            else:
                selected_leaf.decrease_data_size()
                render_display(screen, tree, selected_leaf.get_separator() +
                               ' (' + str(selected_leaf.data_size) + ')')


def run_treemap_file_system(path):
    """Run a treemap visualisation for the given path's file structure.

    Precondition: <path> is a valid path to a file or folder.

    @type path: str
        the system path
    @rtype: None
    """
    file_tree = FileSystemTree(path)
    run_visualisation(file_tree)


def run_treemap_population():
    """Run a treemap visualisation for World Bank population data.

    @rtype: None
    """
    pop_tree = PopulationTree(True)
    run_visualisation(pop_tree)


if __name__ == '__main__':
    import python_ta
    # Remember to change this to check_all when cleaning up your code.
    python_ta.check_errors(config='pylintrc.txt')
    python_ta.check_all(config='pylintrc.txt')

    # To check your work for Tasks 1-4, try uncommenting the following function
    # call, with the '' replaced by a path like
    # 'C:\\Users\\David\\Documents\\csc148\\assignments' (Windows) or
    # '/Users/dianeh/Documents/courses/csc148/assignments' (OSX)

    run_treemap_file_system('C:\\Users\\jimmy\\Documents\\csc148')

    # To check your work for Task 5, uncomment the following function call.
    # run_treemap_population()
