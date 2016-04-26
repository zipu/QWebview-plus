from PyQt5.Qt import QProcess, QProcessEnvironment

PORT = "5000"


if __name__ == "__main__":

    process = QProcess()
    env = QProcessEnvironment.systemEnvironment()
    env.insert("QTWEBENGINE_REMOTE_DEBUGGING", PORT)
    process.setProcessEnvironment(env)
    process.start("python wnd.py")
