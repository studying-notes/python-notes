import subprocess

p = subprocess.Popen(
    [
        "cmd",
        "/c",
        "start",
        "cmd",
    ]
)

code = p.wait()
