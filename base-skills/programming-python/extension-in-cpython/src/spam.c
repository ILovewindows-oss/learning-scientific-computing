// Make "s#" use Py_ssize_t rather than int.
#define PY_SSIZE_T_CLEAN

// Include Python.h before any standard headers are included
#include <Python.h>

/////////////////////////////////////////////////////////////////////////////
// Python API
/////////////////////////////////////////////////////////////////////////////

// Static object representing a custom exception type.
// In initialization the new exception is called `spam.error`.
static PyObject *SpamError;

//! Provides the call to default system's `system` function.
// 
// Parameters
// ----------
// *self: PyObject
//     Pointer to the present module object and allows for accesing
//     module level functions (not exported to Python API).
// *args: PyObject
//     Pointer to Python tuple containing the arguments. These are
//     Python objects and must be converted to C values.
static PyObject *
spam_system(
    PyObject *self, 
    PyObject *args
)
{
    const char *command;
    int sts;

    // Parse arguments to C-objects. It is not necessary to provide
    // an exception before returning because PyArg_ParseTuple has
    // already done it if parsing failed.
    if (!PyArg_ParseTuple(args, "s", &command)) {
        return NULL;
    }

    // Use system function.
    sts = system(command);

    // Illustration of a basic exception setting.
    if (sts < 0) {
        PyErr_SetString(SpamError, "System command failed");
        return NULL;
    }

    // Return the value as a Python object.
    return PyLong_FromLong(sts);
}

/////////////////////////////////////////////////////////////////////////////
// Exporting
/////////////////////////////////////////////////////////////////////////////

PyDoc_STRVAR(spam_doc, "This is a template module just for instruction.");


static PyMethodDef SpamMethods[] = {
    // Export `spam_system` as `system`.
    {"system",  spam_system, METH_VARARGS, "Execute a shell command."},
    // Sentinel (must be present to indicate end of table).
    {NULL, NULL, 0, NULL}  
};


static struct PyModuleDef spam = {
    PyModuleDef_HEAD_INIT,
    // name of module
    "spam",
    // module documentation, may be NULL  
    spam_doc,
    // size of per-interpreter state of the module, or -1 if the
    //module keeps state in global variables.
    -1,        
    // methods table
    SpamMethods
};

/////////////////////////////////////////////////////////////////////////////
// Initialization
/////////////////////////////////////////////////////////////////////////////

PyMODINIT_FUNC
PyInit_spam(void)
{
    PyObject *m;

    m = PyModule_Create(&spam);

    if (m == NULL) {
        return NULL;
    }

    SpamError = PyErr_NewException("spam.error", NULL, NULL);
    Py_XINCREF(SpamError);

    if (PyModule_AddObject(m, "error", SpamError) < 0) {
        Py_XDECREF(SpamError);
        Py_CLEAR(SpamError);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}

/////////////////////////////////////////////////////////////////////////////
// EOF
/////////////////////////////////////////////////////////////////////////////