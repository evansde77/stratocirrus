"""
common utils for package creation


"""
import os


def validate_namespace_name(value):
    """
    ensure package names dont cause problems
    with bad characters
    """
    if "-" in value:
        raise ArgumentTypeError(
            "Package name: {} contains a - character".format(value)
        )
    if " " in value:
        raise ArgumentTypeError(
            "Package name: {} contains a space ".format(value)
        )
    return value


def validate_pypi_package_name(value):
    """
    ensure package names dont cause problems
    with bad characters
    """
    if " " in value:
        raise ArgumentTypeError(
            "Package name: {} contains a space ".format(value)
        )
    return value


def backup_file(filename):
    """
    if filename exists, make a .BAK copy of it to avoid clobbering
    any existing files.
    """
    if not os.path.exists(filename):
        return
    newfile = "{}.BAK".format(filename)
    with open(filename, 'r') as handle_in:
        content = handle_in.read()

    with open(newfile, 'w') as handle_out:
        handle_out.write(content)



def write_manifest(dirname, requirements_files=None, templates=None):
    """
    write the manifest file used for distribution
    """
    if requirements_files is None:
        requirements_files = []
    if isinstance(requirements_files, str):
        requirements_files = [requirements_files]

    if templates is None:
        templates = []
    if ininstance(templates, str):
        templates = [templates]

    manifest = os.path.join(dirname, 'MANIFEST.in')
    backup_file(manifest)
    lines = ["include setup.cfg"]
    lines.extend("include {}".format(x) for x in requirements_files)
    lines.extend("include {}".format(x) for x in templates)

    with open(manifest, 'w') as handle:
        for line in lines:
            handle.write("{}\n".format(line))
    return manifest