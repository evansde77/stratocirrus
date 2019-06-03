
import subprocess


ENCODING='UTF-8'


def output_to_str(outp, split=True):
    """
    helper to convert shell output into strings/lists
    """
    outp = outp.decode('utf-8').strip()
    if split:
        outp = [x.strip() for x in outp.split() if x.strip()]
    return outp


def command_output(command, split=True):
    """
    run command in shell and return stdout as a string
    :param command: list of command line elements
    :return: stdout as string
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    outp, err = process.communicate()
    if process.returncode:
        return None
    return output_to_str(outp, split=split)


def shell_command_output(command, split=True):
    """
    run a command in shell mode

    :param command:  string containing shell command
    :return:
    """
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True
    )
    stdout, _ = process.communicate()
    stdout = output_to_str(stdout, split=split)
    if process.returncode != 0:
        raise RuntimeError(stdout)
    else:
        if not split:
            return "\n".join(stdout.splitlines())
        return stdout
