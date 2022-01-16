from extensions.super.precursor import precursor, precursor_of


class Foo:
    def bar(self):
        print('Foo.bar() called')

    def bar1(self, x):
        print(f'Foo.bar1({x}) called')


class Baz:
    pass


class Bar(Foo):
    def bar(self):
        precursor_of(Foo)()
        precursor()

    def bar1(self):
        precursor(1)

    def bar_x(self):
        precursor()


def test_prec1():
    """
    >>> b = Bar()
    >>> b.bar()
    Foo.bar() called
    Foo.bar() called
    >>> b.bar1()
    Foo.bar1(1) called
    >>> b.bar_x()
    Traceback (most recent call last):
    Exception: Method bar_x does not exist in superclass Foo
    """


# See: Stroustroup: The C++ Programming Language 2/e, p.206
# See: Betrand Meyer: Object-Oriented Software Construction 2/e, p. 557
class Window:
    def draw(self):
        print('Window.draw()')


class WindowWithBorder(Window):
    def draw_border(self):
        print('WindowWithBorder.draw_border()')

    def draw(self):
        print('WindowWithBorder.draw()')
        precursor()
        self.draw_border()


class WindowWithMenu(Window):
    def draw_menu(self):
        print('WindowWithMenu.draw_menu()')

    def draw(self):
        print('WindowWithMenu.draw()')
        precursor()
        self.draw_menu()


class WindowWithBorderAndMenu(WindowWithBorder, WindowWithMenu):
    def draw(self):
        print('WindowWithBorderAndMenu.draw()')
        precursor_of(Window)()
        self.draw_border()
        self.draw_menu()


def test_window_with_border():
    """
    >>> wb = WindowWithBorder()
    >>> wb.draw()
    WindowWithBorder.draw()
    Window.draw()
    WindowWithBorder.draw_border()
    """


def test_window_with_menu():
    """
    >>> wm = WindowWithMenu()
    >>> wm.draw()
    WindowWithMenu.draw()
    Window.draw()
    WindowWithMenu.draw_menu()
    """


def test_window_with_border_and_menu():
    """
    >>> wbm = WindowWithBorderAndMenu()
    >>> wbm.draw()
    WindowWithBorderAndMenu.draw()
    Window.draw()
    WindowWithBorder.draw_border()
    WindowWithMenu.draw_menu()
    """


class A:
    def hello(self, x):
        print(f'A: {x}')


class B(A):
    pass


class C(B):
    def hello(self, x):
        print(f'C: {x}')
        precursor(x)


class D(C):
    def hello(self, x):
        print(f'D: {x}')
        precursor(x)


def test_jump():
    """
    >>> C().hello('world')
    C: world
    A: world
    """


def test_double_precursor():
    """
    >>> D().hello('world')
    D: world
    C: world
    A: world
    """


class LocalInheritance:
    class A:
        def hello(self, x):
            print(f'A: {x}')

    class B(A):
        pass

    class C(B):
        def hello(self, x):
            print(f'C: {x}')
            precursor(x)

    class D(C):
        def hello(self, x):
            print(f'D: {x}')
            precursor(x)

    @staticmethod
    def run_test():
        LocalInheritance.D().hello('world')


def test_local_inheritance():
    """
    >>> LocalInheritance.run_test()
    D: world
    C: world
    A: world
    """


class R1:
    def r(self, x):
        return x + 1


class R2(R1):
    def r(self, x):
        return 3 * precursor(2 * x)


def test_precursor_return():
    """
    >>> R2().r(10)
    63
    """


if __name__ == '__main__':
    from doctest import testmod

    testmod()
