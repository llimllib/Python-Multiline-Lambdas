from __future__ import with_statement
from functools import partial
import inspect
 
def accepts_block(f):
  class _accepts_block(object):
    def __call__(self, *args, **kwargs):
      if len(args) == len(inspect.getargspec(f)[0]):
        return f(*args, **kwargs)
      self.thefunction = partial(f, *args, **kwargs)
      return self
 
    def __enter__(self):
      # keep track of all that's already defined BEFORE the `with`
      frame = inspect.currentframe(1)
      self.mustignore = dict(frame.f_locals)
 
    def __exit__(self, exc_type, exc_value, traceback):
      frame = inspect.currentframe(1)
      # see what's been bound anew in the body of the `with`
      interesting = dict()
      for n in frame.f_locals:
        newf = frame.f_locals[n]
        if n not in self.mustignore:
          interesting[n] = newf
          continue
        anf = self.mustignore[n]
        if id(newf) != id(anf):
          interesting[n] = newf
      if interesting:
        if len(interesting) > 2:
          raise "you are only allowed to define a single function inside this with block"
        elif len(interesting) == 1:
          block = list(interesting.itervalues())[0]
          if not isinstance(block, type(lambda:None)):
            raise "you must define a function inside this with block"
          self.thefunction(block)
        elif len(interesting) == 2:
          block = None
          savename = None
          for n,v in interesting.iteritems():
            if isinstance(v, type(lambda:None)): block = v
            else: savename = n
          if not savename or not isinstance(block, type(lambda:None)):
            raise "you must define a single function inside this with block"
          frame.f_locals[savename] = self.thefunction(block)
  return _accepts_block()
