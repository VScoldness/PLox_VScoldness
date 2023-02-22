import sys
sys.path.append("../src")
from pLox import PLox


input_txt = "input1.txt"

p = PLox()
p.run(input_txt)
