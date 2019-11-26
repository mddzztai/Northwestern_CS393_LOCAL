BOARD_LENGTH=9

class Local_Exception(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class Remote_Exception(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)