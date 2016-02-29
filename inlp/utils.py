# -*- coding: utf-8 -*-
#  
#
# Author: Igor
import subprocess

from nltk import compat


def ltp_cmd(cmd, stdin=None, stdout=None, stderr=None, blocking=True):
    '''
    Execute the given ltp command, by opening a subprocess that calls
    ltp.
    执行ltp的命令
    :param cmd: The ltp command that should be called, formatted as
        a list of strings.
    :type cmd: list(str)

    :param stdin, stdout, stderr: Specify the executed programs'
        standard input, standard output and standard error file
        handles, respectively.  Valid values are ``subprocess.PIPE``,
        an existing file descriptor (a positive integer), an existing
        file object, and None.  ``subprocess.PIPE`` indicates that a
        new pipe to the child should be created.  With None, no
        redirection will occur; the child's file handles will be
        inherited from the parent.  Additionally, stderr can be
        ``subprocess.STDOUT``, which indicates that the stderr data
        from the applications should be captured into the same file
        handle as for stdout.

    :param blocking: If ``false``, then return immediately after
        spawning the subprocess.  In this case, the return value is
        the ``Popen`` object, and not a ``(stdout, stderr)`` tuple.

    :return: If ``blocking=True``, then return a tuple ``(stdout,
        stderr)``, containing the stdout and stderr outputs generated
        by the ltp command if the ``stdout`` and ``stderr`` parameters
        were set to ``subprocess.PIPE``; or None otherwise.  If
        ``blocking=False``, then return a ``subprocess.Popen`` object.

    :raise OSError: If the ltp command returns a nonzero return code.
    '''
    if stdin == 'pipe': stdin = subprocess.PIPE
    if stdout == 'pipe': stdout = subprocess.PIPE
    if stderr == 'pipe': stderr = subprocess.PIPE
    if isinstance(cmd, compat.string_types):
        raise TypeError('cmd should be a list of strings')

    # Construct the full command string.
    cmd = list(cmd)

    # Call ltp via a subprocess
    p = subprocess.Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr)
    if not blocking: return p
    (stdout, stderr) = p.communicate()

    # Check the return code.
    if p.returncode != 0:
        print(stderr)
        raise OSError('ltp command failed : ' + str(cmd))

    return (stdout, stderr)
