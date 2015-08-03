import nose, os
import pytem

def test():
  os.environ["PROMPT"] = "no"
  return pytem.main("template","in","out")

nose.main()
