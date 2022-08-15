# Extensions with default CPython modules

In this note we list the main points to remember when developing a pure CPython module. You can find more details in the official Python documentation on [extensions](https://docs.python.org/3/extending/extending.html). Also notice that an exemple module is provided by default in [CPython sources](https://github.com/python/cpython/blob/main/Modules/xxmodule.c).

Main takes:

- By convention a function `system` from module `spam` in C is called `spam_system`.
- Functions always have 2 (or 3 for kwargs) arguments, `self` and `args`, args, (and possibly `kwargs`) being parsed to C-objects.
- It is a convention to return `-1` or `NULL` when an error occurs on the C-side of module.
- To export a function it must be referenced in a method table of type `static PytMethodDef`.
- The method table is then used to create a module with `PyModuleDef` structure.
- To initialize `spam` module create a function `PyMODINIT_FUNC PyInit_spam(void)`.

Important API functions:

- [PyArg_ParseTuple](https://docs.python.org/3/c-api/arg.html#c.PyArg_ParseTuple)
- [PyArg_ParseTupleAndKeywords](https://docs.python.org/3/c-api/arg.html#c.PyArg_ParseTupleAndKeywords)
- [PyErr_SetString](https://docs.python.org/3/c-api/exceptions.html#c.PyErr_SetString)
- [PyErr_SetFromErrno](https://docs.python.org/3/c-api/exceptions.html#c.PyErr_SetFromErrno)
- [PyErr_SetObject](https://docs.python.org/3/c-api/exceptions.html#c.PyErr_SetObject)
- [PyErr_Occurred](https://docs.python.org/3/c-api/exceptions.html#c.PyErr_Occurred)
