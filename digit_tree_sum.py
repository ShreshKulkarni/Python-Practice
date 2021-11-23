#
# Binary trees are already defined with this interface:
# class Tree(object):
#   def __init__(self, x):
#     self.value = x
#     self.left = None
#     self.right = None
def solution(t):
    if not t:
        return 0
    
    from collections import deque 
    stack = deque()
    stack_pt = deque()
    
    num_list = []
    
    stack.append(t)
    stack_pt.append([t.value])
    
    while(True):
        if not stack:
            break
        
        isleaf = True
        e = stack.pop()  
        #num_list[-1].append(e.value)
        p = stack_pt.pop()
        
        if e.left:
            stack.append(e.left)
            stack_pt.append(p + [e.left.value])
            isleaf = False
        if e.right:
            stack.append(e.right)
            stack_pt.append(p + [e.right.value])
            isleaf = False
            
        if isleaf:
            num_list.append(p)
            
        print(num_list)

    def get_sum(l):
        l.reverse()
        return sum([d*(10**i) for i,d in enumerate(l)])
        
    return sum([get_sum(l) for l in num_list])
