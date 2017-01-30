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


class testGetId(object):
    '''
    The test cases of ``LocalDoc.get_id``
    '''
    def setUp(self):
        self.dir = mkdtemp()

    def tearDown(self):
        rmtree(self.dir)

    def test_idfile(self):
        f = self.check_idfile

        yield f, 'magic_id', 'magic_id'
        yield f, 'magic_id', 'magic_id', 'wb'

        yield f, ' magic_id', 'magic_id'
        yield f, ' magic_id', 'magic_id', 'wb'
        yield f, 'magic_id ', 'magic_id'
        yield f, 'magic_id ', 'magic_id', 'wb'
        yield f, ' magic_id ', 'magic_id'
        yield f, ' magic_id ', 'magic_id', 'wb'

        yield f, 'magic_id\n', 'magic_id'
        yield f, 'magic_id\n', 'magic_id', 'wb'
        yield f, 'magic_id\n\r', 'magic_id'
        yield f, 'magic_id\n\r', 'magic_id', 'wb'
        yield f, 'magic_id\r', 'magic_id'
        yield f, 'magic_id\r', 'magic_id', 'wb'

        yield f, 'magic_id \n', 'magic_id'
        yield f, 'magic_id \n', 'magic_id', 'wb'
        yield f, 'magic_id \n\r', 'magic_id'
        yield f, 'magic_id \n\r', 'magic_id', 'wb'
        yield f, 'magic_id \r ', 'magic_id'
        yield f, 'magic_id \r ', 'magic_id', 'wb'

        f = self.check_not_idfile
        yield f, '\nmagic_id', 'magic_id'
        yield f, '\n\rmagic_id', 'magic_id'
        yield f, '\nmagic_id\n', 'magic_id'

    def check_idfile(self, content, ans, mode='w'):
        # create ``_id`` file
        p = os.path.join(self.dir, '_id')
        with open(p, mode) as idfile:
            idfile.write(content)

        doc = LocalDoc(self.dir, create=False)
        assert doc.get_id() == ans, doc.get_id()

    def check_not_idfile(self, content, ans, mode='w'):
        # create ``_id`` file
        p = os.path.join(self.dir, '_id')
        with open(p, mode) as idfile:
            idfile.write(content)

        doc = LocalDoc(self.dir, create=False)
        assert doc.get_id() != ans, doc.get_id()

    def test_dirname(self):
        '''
        If the ``_id`` file does not eixsts
        '''
        dirname = os.path.split(self.dir)[-1]
        doc = LocalDoc(self.dir, is_ddoc=False)
        assert doc.get_id() == dirname

        doc = LocalDoc(self.dir, is_ddoc=True)
        ans = '_design/{}'.format(dirname)
        assert doc.get_id() == ans
