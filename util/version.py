import sys

version_major = "3"
version_minor = "5"

def check_version():
    global version_major, version_minor
    version_major = str(sys.version_info[0])
    version_minor = str(sys.version_info[1])
    return version_major + '.' + version_minor

check_version()
