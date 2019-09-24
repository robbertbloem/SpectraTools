import importlib

import unittest




import SpectraTools.Tests.CommonFunctions_ST_Tests
import SpectraTools.Tests.hitran_Tests
import SpectraTools.Tests.LinearSpectrum_Tests
import SpectraTools.Tests.MultiLinearSpectra_Tests
import SpectraTools.Tests.nist_import_jcamp_Tests
import SpectraTools.Tests.nist_Tests
import SpectraTools.Tests.RefractiveIndex_Tests
import SpectraTools.Tests.RI_read_yaml_Tests
import SpectraTools.Tests.UnitConversion_Tests


importlib.reload(SpectraTools.Tests.CommonFunctions_ST_Tests)
importlib.reload(SpectraTools.Tests.hitran_Tests)
importlib.reload(SpectraTools.Tests.LinearSpectrum_Tests)
importlib.reload(SpectraTools.Tests.MultiLinearSpectra_Tests)
importlib.reload(SpectraTools.Tests.nist_import_jcamp_Tests)
importlib.reload(SpectraTools.Tests.nist_Tests)
importlib.reload(SpectraTools.Tests.RefractiveIndex_Tests)
importlib.reload(SpectraTools.Tests.RI_read_yaml_Tests)
importlib.reload(SpectraTools.Tests.UnitConversion_Tests)

verbosity = 2

TS = unittest.TestSuite()

# TL = unittest.TestLoader()
# tests = TL.loadTestsFromModule(SpectraTools.Tests.CommonFunctions_ST_Tests)
# TS.addTests(tests)

# TL = unittest.TestLoader()
# tests = TL.loadTestsFromModule(SpectraTools.Tests.hitran_Tests)
# TS.addTests(tests)

# TL = unittest.TestLoader()
# tests = TL.loadTestsFromModule(SpectraTools.Tests.LinearSpectrum_Tests)
# TS.addTests(tests)

TL = unittest.TestLoader()
tests = TL.loadTestsFromModule(SpectraTools.Tests.MultiLinearSpectra_Tests)
TS.addTests(tests)

# TL = unittest.TestLoader()
# tests = TL.loadTestsFromModule(SpectraTools.Tests.nist_import_jcamp_Tests)
# TS.addTests(tests)

# TL = unittest.TestLoader()
# tests = TL.loadTestsFromModule(SpectraTools.Tests.nist_Tests)
# TS.addTests(tests)

# TL = unittest.TestLoader()
# tests = TL.loadTestsFromModule(SpectraTools.Tests.RefractiveIndex_Tests)
# TS.addTests(tests)

# TL = unittest.TestLoader()
# tests = TL.loadTestsFromModule(SpectraTools.Tests.RI_read_yaml_Tests)
# TS.addTests(tests)

# TL = unittest.TestLoader()
# tests = TL.loadTestsFromModule(SpectraTools.Tests.UnitConversion_Tests)
# TS.addTests(tests)

result = unittest.TestResult()
TS.run(result)

print(result)
