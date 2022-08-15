# -*- coding: utf-8 -*-
import spam


def test_system_call():
    assert spam.system("ls -l") == 0


def test_constant_flag():
    assert spam.SPAM_FLAG == 666


def test_macro_constant():
    assert spam.SPAM_MACRO == 256
