# -*- coding: utf-8 -*-

from __future__ import absolute_import

from sentry.testutils import TestCase, fixture


class ExceptionTest(TestCase):
    def test_args_as_list(self):
        from sentry.interfaces import SingleException, Exception

        inst = Exception([{
            'type': 'ValueError',
            'value': 'hello world',
            'module': 'foo.bar',
        }])
        assert type(inst.values[0]) is SingleException
        assert inst.values[0].type == 'ValueError'
        assert inst.values[0].value == 'hello world'
        assert inst.values[0].module == 'foo.bar'

    def test_args_as_keyword_args(self):
        from sentry.interfaces import SingleException, Exception

        inst = Exception(values=[{
            'type': 'ValueError',
            'value': 'hello world',
            'module': 'foo.bar',
        }])
        assert type(inst.values[0]) is SingleException
        assert inst.values[0].type == 'ValueError'
        assert inst.values[0].value == 'hello world'
        assert inst.values[0].module == 'foo.bar'

    def test_args_as_old_style(self):
        from sentry.interfaces import SingleException, Exception

        inst = Exception(**{
            'type': 'ValueError',
            'value': 'hello world',
            'module': 'foo.bar',
        })
        assert type(inst.values[0]) is SingleException
        assert inst.values[0].type == 'ValueError'
        assert inst.values[0].value == 'hello world'
        assert inst.values[0].module == 'foo.bar'


class SingleExceptionTest(TestCase):
    @fixture
    def interface(self):
        from sentry.interfaces import SingleException

        return SingleException(
            type='ValueError',
            value='hello world',
            module='foo.bar',
        )

    def test_serialize_behavior(self):
        assert self.interface.serialize() == {
            'type': self.interface.type,
            'value': self.interface.value,
            'module': self.interface.module,
            'stacktrace': None,
        }

    def test_get_hash(self):
        assert self.interface.get_hash() == [
            self.interface.type,
            self.interface.value,
        ]

    def test_get_hash_without_type(self):
        self.interface.type = None
        assert self.interface.get_hash() == [
            self.interface.value,
        ]

    def test_get_hash_without_value(self):
        self.interface.value = None
        assert self.interface.get_hash() == [
            self.interface.type,
        ]
