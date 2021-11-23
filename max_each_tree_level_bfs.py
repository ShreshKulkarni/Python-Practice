#
# Binary trees are already defined with this interface:
class Tree(object):
   def __init__(self, x):
     self.value = x
     self.left = None
     self.right = No

def solution(t):
    if not t:
        return []
    
    ml = [[]]
    stack_c = []
    stack_n = []
    stack_c.append(t)
    
    while(True):
        if not stack_c:
            if stack_n:
                stack_c = stack_n
                stack_n = []
                ml.append([])
            else:
                break
        #traverse the left tree first and keep adding elements as
        #they come in the stack. They will be processed in LIFO order
        e = stack_c.pop(0)
        ml[-1].append(e.value)
        if e.left:
            stack_n.append(e.left)
        if e.right:
            stack_n.append(e.right)
            
    #print(ml)
    return [max(l) for l in ml]            
            
if __name__=='__main__':
  t = Tree(1)
  t.left = Tree(2)
  t.right = Tree(3)
  
  print(solution(t))

