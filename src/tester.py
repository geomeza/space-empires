import sys
sys.path.append('Units')

from Units.Unit import Unit

Test = Unit([5,5],None,Unit,1)
print(Test.coords)