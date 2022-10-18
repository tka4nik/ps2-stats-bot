import datetime


class GeneralLogger:

    def __init__(self, path_cmd="log/cmd.log", path_err="log/err.log"):
        self.path_cmd = path_cmd
        self.path_err = path_err

    def LogCommand(self, input, format):
        with open(self.path_cmd, "a+") as f:
            f.write(datetime.datetime.now().strftime(format) + "\n")
            f.write(str(input) + "\n")

    def LogError(self, error, format):
        with open(self.path_err, "a+") as f:
            f.write(datetime.datetime.now().strftime(format) + "\n")
            f.write(str(error) + "\n")

    def LogInfo(self, info, format):
        with open(self.path_cmd, "a+") as f:
            f.write(datetime.datetime.now().strftime(format) + ": ")
            f.write(str(info) + "\n")
