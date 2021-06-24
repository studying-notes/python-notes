python -c "import os; f = open('f1', 'wb'); f.write(os.urandom(128 * 1024))"

python -c "import os; f = open('f1', 'wb'); f.write(os.urandom(8 * 1024 * 1024))"

python -c "import os; f = open('f1', 'wb'); f.write(os.urandom(512 * 1024 * 1024))"

time python -m timeit -s 'import shutil; p1 = "f1"; p2 = "f2"' 'shutil.copyfile(p1, p2)'
