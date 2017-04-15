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
        ans = '_design/{0}'.format(dirname)
        assert doc.get_id() == ans


class testCreate(object):
    def setUp(self):
        self.dir = mkdtemp()

    def tearDown(self):
        rmtree(self.dir)

    def exists(self, filename):
        return os.path.exists(os.path.join(self.dir, filename))

    def test_create(self):
        doc = LocalDoc(self.dir, create=True)

        assert self.exists('.couchapprc')
        assert self.exists('.couchappignore')

    def test_create_nothing(self):
        # .couchapprc already exists
        path = os.path.join(self.dir, '.couchapprc')
        with open(path, 'w') as f:
            f.write('{}')

        doc = LocalDoc(self.dir, create=True)

        assert self.exists('.couchapprc')
        assert not self.exists('.couchappignore')


def test_check_ignore():
    f = check_check_ignore

    ignores = ['.*\.bak']
    yield f, ignores, 'magic.bak', True
    yield f, ignores, 'magicbak', False
    yield f, ignores, 'bar/magic.bak', True

    ignores = ['bar']
    yield f, ignores, 'bar', True
    yield f, ignores, 'bar/', True
    yield f, ignores, 'bar.txt', False
    yield f, ignores, 'magic_bar', False

    yield f, ignores, 'foo/bar', True
    yield f, ignores, 'foo/qaz/bar', True
    yield f, ignores, 'foo/bar/app.js', True

    yield f, ignores, 'bar/app.js', True
    yield f, ignores, 'bar/foo.txt', True

    yield f, ignores, 'magic_bar/app.js', False
    yield f, ignores, 'bar_magic/app.js', False

    # the result should be same as ``['bar']``,
    # the ``$`` is include by default
    ignores = ['bar$']
    yield f, ignores, 'bar', True
    yield f, ignores, 'bar/', True
    yield f, ignores, 'bar.txt', False
    yield f, ignores, 'magic_bar', False

    yield f, ignores, 'foo/bar', True
    yield f, ignores, 'foo/qaz/bar', True
    yield f, ignores, 'foo/bar/app.js', True

    yield f, ignores, 'bar/app.js', True
    yield f, ignores, 'bar/foo.txt', True

    yield f, ignores, 'magic_bar/app.js', False
    yield f, ignores, 'bar_magic/app.js', False

    ignores = ['foo/bar']
    yield f, ignores, 'foo/bar', True
    yield f, ignores, 'qaz/foo/bar', True

    yield f, ignores, 'foo/bar/', True
    yield f, ignores, 'qaz/foo/bar/', True

    yield f, ignores, 'foo/bar/app.js', True
    yield f, ignores, 'qaz/foo/bar/app.js', True

    ignores = ['foo/.*bar']
    yield f, ignores, 'foo/magic_bar', True
    yield f, ignores, 'foo/magic_bar/', True
    yield f, ignores, 'foo/magic_bar/app.js', True

    yield f, ignores, 'foo/magic/bar/', True
    yield f, ignores, 'foo/magic/bar/app.js', True

    yield f, ignores, 'foo/magic/long/long/bar', True
    yield f, ignores, 'foo/magic/long/long/bar/app.js', True

    yield f, ignores, 'foobar', False

    yield f, ignores, 'qaz/foo/magic_bar', True
    yield f, ignores, 'qaz/foo/magic_bar/', True
    yield f, ignores, 'qaz/foo/magic_bar/app.js', True

    yield f, ignores, 'qaz/foo/magic/bar/', True
    yield f, ignores, 'qaz/foo/magic/bar/app.js', True

    yield f, ignores, 'qaz/foo/magic/long/long/bar', True
    yield f, ignores, 'qaz/foo/magic/long/long/bar/app.js', True

    yield f, ignores, 'qaz_foo/magic_bar', False
    yield f, ignores, 'qaz_foo/magic_bar/', False
    yield f, ignores, 'qaz_foo/magic_bar/app.js', False

    yield f, ignores, 'qaz_foo/magic/bar/', False
    yield f, ignores, 'qaz_foo/magic/bar/app.js', False

    yield f, ignores, 'qaz_foo/magic/long/long/bar', False
    yield f, ignores, 'qaz_foo/magic/long/long/bar/app.js', False

    yield f, ignores, 'foo/magic_bar_', False
    yield f, ignores, 'foo/magic_bar_/', False
    yield f, ignores, 'foo/magic_bar_/app.js', False

    yield f, ignores, 'foo/magic/bar_/', False
    yield f, ignores, 'foo/magic/bar_/app.js', False

    yield f, ignores, 'foo/magic/long/long/bar_', False
    yield f, ignores, 'foo/magic/long/long/bar_/app.js', False

    ignores = ['foo/.*/bar']
    yield f, ignores, 'foo/magic_bar', False
    yield f, ignores, 'foo/magic_bar/', False
    yield f, ignores, 'foo/magic_bar/app.js', False

    yield f, ignores, 'foo/magic/bar/', True
    yield f, ignores, 'foo/magic/bar/app.js', True

    yield f, ignores, 'foo/magic/long/long/bar', True
    yield f, ignores, 'foo/magic/long/long/bar/app.js', True

    yield f, ignores, 'foobar', False

    yield f, ignores, 'qaz/foo/magic_bar', False
    yield f, ignores, 'qaz/foo/magic_bar/', False
    yield f, ignores, 'qaz/foo/magic_bar/app.js', False

    yield f, ignores, 'qaz/foo/magic/bar/', True
    yield f, ignores, 'qaz/foo/magic/bar/app.js', True

    yield f, ignores, 'qaz/foo/magic/long/long/bar', True
    yield f, ignores, 'qaz/foo/magic/long/long/bar/app.js', True

    yield f, ignores, 'qaz_foo/magic_bar', False
    yield f, ignores, 'qaz_foo/magic_bar/', False
    yield f, ignores, 'qaz_foo/magic_bar/app.js', False

    yield f, ignores, 'qaz_foo/magic/bar/', False
    yield f, ignores, 'qaz_foo/magic/bar/app.js', False

    yield f, ignores, 'qaz_foo/magic/long/long/bar', False
    yield f, ignores, 'qaz_foo/magic/long/long/bar/app.js', False

    yield f, ignores, 'foo/magic/bar_', False
    yield f, ignores, 'foo/magic/bar_/', False
    yield f, ignores, 'foo/magic/bar_/app.js', False

    yield f, ignores, 'foo/magic/long/long/bar_', False
    yield f, ignores, 'foo/magic/long/long/bar_/app.js', False

    ignores = ['/foo/bar']
    yield f, ignores, 'foo/bar', True
    yield f, ignores, 'foo/bar/app.js', True

    yield f, ignores, 'qaz/foo/bar', False
    yield f, ignores, 'qaz/foo/bar/app.js', False

    ignores = [u'測試']  # unicode testing
    yield f, ignores, u'測試', True
    yield f, ignores, u'測 試', False
    yield f, ignores, u'測試/app.js', True
    yield f, ignores, u'測試資料夾', False
    yield f, ignores, u'測試.txt', False

    yield f, ignores, u'foo/測試', True
    yield f, ignores, u'foo/測 試', False
    yield f, ignores, u'foo/測試/app.js', True
    yield f, ignores, u'foo/測試資料夾', False
    yield f, ignores, u'foo/測試.txt', False


def check_check_ignore(ignores, path, ans):
    doc = LocalDoc('/mock/app', create=False)
    doc.ignores = ignores
    assert doc.check_ignore(path) is ans


def test_meta_to_fields():
    f = check_meta_to_fields

    yield f, ({}, {}), ({'couchapp': {}}, {})

    yield f, ({}, []), ({'couchapp': {'meta': []}},
                        {'meta': []})
    yield f, ({}, [42]), ({'couchapp': {'meta': [42]}},
                          {'meta': [42]})
    yield f, ({}, 'magic'), ({'couchapp': {'meta': 'magic'}},
                             {'meta': 'magic'})

    yield f, ({}, {'signatures': 42}), ({'couchapp': {}}, {})
    yield f, ({}, {'manifest': 42}), ({'couchapp': {}}, {})
    yield f, ({}, {'objects': 42}), ({'couchapp': {}}, {})
    yield f, ({}, {'object': 42}), ({'couchapp': {'object': 42}},
                                    {'object': 42})
    yield f, ({}, {'length': 42}), ({'couchapp': {}}, {})

    yield (f,
           ({'couchapp': {'magic': 42}}, {'foo': 'bar'}),
           ({'couchapp': {'magic': 42, 'foo': 'bar'}}, {'foo': 'bar'}))


def check_meta_to_fields(input, ans):
    output = LocalDoc._meta_to_fields(*input)

    assert ans == output
    # check the is a copy of dict
    for i, o in zip(input, output):
        assert i is not o


class TestEncodeContent(object):
    def setUp(self):
        self.dir = mkdtemp()

    def tearDown(self):
        rmtree(self.dir)

    def test_json_suffix(self):
        f = self.check_json_suffix

        yield f, '{"magic": 42}', {'magic': 42}
        yield f, '"magic"', "magic"
        yield f, '[1, 2, 3]', [1, 2, 3]
        yield f, '{}{}', ''

    def check_json_suffix(self, content, ans):
        name = 'magic.json'
        p = os.path.join(self.dir, name)

        with open(p, 'w') as f:
            f.write(content)

        content = LocalDoc._encode_content(name, p)
        assert content == ans

    def test_text_file(self):
        f = self.check_text_file

        yield f, b'readme'
        yield f, b'readme\ntopic\n'
        yield f, b'readme\ntopic\n   '

        yield f, b'測試'
        yield f, b'測試\n測試\n'
        yield f, b'測試\n測試\n   '

    def check_text_file(self, ans):
        name = 'README.rst'
        p = os.path.join(self.dir, name)

        with open(p, 'wb') as f:
            f.write(ans)

        content = LocalDoc._encode_content(name, p)
        assert content == ans.decode('utf8'), content

    def test_bin_file(self):
        f = self.check_bin_file

        yield f, b'\xb4\xfa\xb8\xd5', 'tPq41Q=='
        yield f, b'\xb4\xfa\xb8\xd5\xb4', 'tPq41bQ='

    def check_bin_file(self, bits, ans):
        name = 'a.out'
        p = os.path.join(self.dir, name)

        with open(p, 'wb') as f:
            f.write(bits)

        content = LocalDoc._encode_content(name, p)
        assert content == 'base64-encoded;' + ans
