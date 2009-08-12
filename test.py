from __future__ import with_statement
from accepts_block import accepts_block

@accepts_block
def bmap(arr, block):
  return map(block, arr)

with bmap([1,2,3]) as zootrope:
  def foo(x):
    return (float(x) + 1) / 2
print zootrope

#make sure it works if we don't use a with block
print bmap([1,2,3], lambda x: (float(x)+1)/2)

@accepts_block
def each(iterable, block):
  for i in iterable: block(i)

with each(["twelve", "fourteen", "sixteen"]):
  def _(x):
    print x

#XXX: this doesn't work, because _ is not redefined. Need a "def".
with each(["twelve", "fourteen", "sixteen"]):
  _

each(["twelve", "fourteen", "sixteen"], _)

#let's try and fool len(interesting) == 2
with bmap([1,2,3]):
  result = 12
  y = lambda x:x

#result is [1,2,3], but it should probably still be 12
print result
