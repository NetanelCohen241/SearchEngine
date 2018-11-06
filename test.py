import time
import Parse

import re

# # r = Reader.ReadFile("D:\iretrival\corpus")
#
# r.startAction()

x=Parse.Parser()

# df = pandas.DataFrame({"original value ":z,"calcsize value":w})
# print(df)
#
# t= time.time()
print(x.parse("306 Dec NIHON KEIZAI SHIMBUN"))
# print(time.time()-t)
# print(re.split("[,\-!?:]+", "Hey, you - what are you doing here!?"))

