import tempfile

def before_scenario(context, current_scenario):
    context.temporary_directory = tempfile.TemporaryDirectory()
    print(current_scenario)
    print(dir(current_scenario))
