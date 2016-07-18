class Stack(object):
    def __init__(self):
        self._stack = []

    def peek(self):
        return self._stack[-1]

    def pop(self):
        return self._stack.pop()

    def push(self, event):
        self._stack.append(event)

    def is_empty(self):
        if self._stack:
            return False
        else:
            return True

    def view(self):
        stack = list(self._stack)
        stack.reverse()
        return stack
