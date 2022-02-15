import tempfile


def before_scenario(context, current_scenario):
    context.temporary_directory = tempfile.TemporaryDirectory()
