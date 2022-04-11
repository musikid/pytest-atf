Pytest-atf - pytest atf wrapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The package is in a WIP state (for now!).

Usage
_____

There are two ways to invoke the wrapper.

With a ``main`` file 
####################

**main.py**

.. code-block:: python

    #!/usr/bin/env python

    atf_main_wrapper()

**Kyuafile**

.. code-block:: lua

    syntax(2)

    test_suite('test')

    atf_test_program{name='main.py'}


With ``atf-python`` as shebang
###################################


.. code-block:: shell

    #!/usr/bin/atf-python