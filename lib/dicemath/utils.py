from . import PROJ_PATH


def file_from_name(folder, filename):
    file_ = PROJ_PATH.joinpath("out", folder)
    try:
        file_.mkdir()
    except FileExistsError:
        pass
    return file_.joinpath("{}.png".format(filename))
