import unittest

start_dir = r"C:\Python\SpectraTools"
pattern = "*_Tests.py"


TL = unittest.TestLoader()

tests = TL.discover(start_dir = start_dir, pattern = pattern)


result = unittest.TextTestRunner(verbosity=1).run(tests)

print(result)