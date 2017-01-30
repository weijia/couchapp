# -*- coding: utf-8 -*-

import os

from shutil import rmtree
from tempfile import mkdtemp

from couchapp.localdoc import LocalDoc


def test_load_ignores_non_exist():
    doc = LocalDoc('/mock/app', create=False)
    assert doc.ignores == []


class testIgnores(object):
    def setUp(self):
        self.dir = mkdtemp()

    def tearDown(self):
        rmtree(self.dir)

    def test_load_ignore(self):
        func = self.check_ignore

        yield func, '[42]', [42]

        yield func, '["foo", "bar"]', ['foo', 'bar']

        content = '''
            [
                "magic", // comments are allowed
                "answer"
            ]
            '''
        yield func, content, ['magic', 'answer']

        content = '''
            [
                "magic", /* comments are allowed */
                "answer"
            ]
            '''
        yield func, content, ['magic', 'answer']

        content = '''
            [
                "magic", /* comments are allowed */
                "answer"  // remix
            ]
            '''
        yield func, content, ['magic', 'answer']

        content = '''
            [
                "magic"
                /*
                "answer"
                */
            ]
            '''
        yield func, content, ['magic']

        content = '''
            [
                "^regex$", /* comment */
                "answer"
            ]
            '''
        yield func, content, ['^regex$', 'answer']

        content = '''
            [
                "/*regex", /* comment */
                "answer//"  // comment
            ]
            '''
        yield func, content, ['/*regex', 'answer//']

    def check_ignore(self, content, ans):
        # prepare ignore file
        path = os.path.join(self.dir, '.couchappignore')
        with open(path, 'w') as f:
            f.write(content)

        doc = LocalDoc(self.dir, create=False)
        assert doc.ignores == ans
