from __future__ import with_statement
from accepts_block import accepts_block

@accepts_block
def bmap(arr, block):
  return map(block, arr)

with bmap([1,2,3]) as zootrope:
  def foo(x):
    return (float(x) + 1) / 2
print "should be [1.0, 1.5, 2.0]", zootrope

#Chris Siebenmann has pointed out to me that this technique doesn't work
#when the with statement is inside a function; in this case f_locals is
#a read-only dictionary. I'm not quite clear on when f_locals is read-only
#and when it's not, so please clarify it for me if you know.
def test():
  with bmap([1,2,3]) as zootrope:
    def foo(x):
      return (float(x) + 1) / 2
  print "should be [1.0, 1.5, 2.0], but is None:", zootrope
test()

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
