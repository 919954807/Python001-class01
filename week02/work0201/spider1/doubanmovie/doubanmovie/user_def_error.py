class UserDefError(Exception):
    def __init__(self,ErrorInfo):
        super().__init__(self,ErrorInfo)
        self.errorinfo = ErrorInfo
    def __str__(self):
        return self.errorinfo



if __name__ == "__main__":
    userinput = 'a'

    try:
        if(not userinput.isdigit()):
            raise UserDefError("用户输入错误")
    except UserDefError as ue:
        print(ue)   