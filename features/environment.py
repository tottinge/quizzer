import tempfile


def before_scenario(context, _):
    context.temporary_directory = tempfile.TemporaryDirectory()
