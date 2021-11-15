import unittest

from snapshot import Snapshot


class TestSnapShot(unittest.TestCase):

    def test_by_names(self):
        class Some:
            snapshot = Snapshot('a', x='b')

            def __init__(self):
                self.a = 1
                self.b = 2

        snap = Some().snapshot
        assert isinstance(snap, Some.snapshot.tuple_type)
        assert snap.a == 1
        assert snap.x == 2

    def test_nested(self):
        class Some:
            snapshot = Snapshot(x='a.a')

            def __init__(self, a):
                self.a = a

        snap = Some(Some(1)).snapshot
        assert isinstance(snap, Some.snapshot.tuple_type)
        assert snap.x == 1

    def test_function(self):
        class Some:
            snapshot = Snapshot(x=lambda obj: obj.a**2)

            def __init__(self, a):
                self.a = a

        snap = Some(2).snapshot
        assert isinstance(snap, Some.snapshot.tuple_type)
        assert snap.x == 4

    def test_combined(self):
        class Some:
            snapshot = Snapshot('a', b='b', c=lambda obj: obj.c, s=lambda obj: obj.d ** 2, ea='e.a')

            def __init__(self, a, b=None, c=None, d=None, e=None):
                self.a = a
                self.b = b
                self.c = c
                self.d = d
                self.e = e

        snap = Some(1, 2, 3, 4, Some(5)).snapshot
        assert isinstance(snap, Some.snapshot.tuple_type)
        assert snap.a == 1
        assert snap.b == 2
        assert snap.c == 3
        assert snap.s == 16
        assert snap.ea == 5

    def test_call(self):
        class Some:
            snapshot = Snapshot(x='a')

            def __init__(self, a):
                self.a = a

        somes = [Some(i) for i in range(10)]
        snaps = Some.snapshot(somes)  # returns iterator
        assert [s.x for s in snaps] == list(range(10))

    def test_exceptions(self):
        with self.assertRaises(TypeError):
            Snapshot(a=())  # only string or callable

    # def test_mypy(self):
    #     import subprocess, os
    #     file_path = os.path.abspath(os.path.join(__file__, '../../snapshot.py'))
    #     mypy_path = os.path.abspath(os.path.join(__file__, '../../../venv/Scripts/mypy.exe'))
    #     if not os.path.exists(mypy_path):
    #         return
    #     completed = subprocess.run([mypy_path,
    #                                 file_path],
    #                                capture_output=True)
    #     completed.check_returncode()
    #     self.assertTrue('error' not in str(completed.stdout))


if __name__ == '__main__':
    unittest.main()







