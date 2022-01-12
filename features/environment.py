import tempfile


def before_scenario(context, current_scenario):
    context.temporary_directory = tempfile.TemporaryDirectory()
    print(current_scenario)
    print("Temporary directory created",  context.temporary_directory)
