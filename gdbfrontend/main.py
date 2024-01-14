from pygdbmi.gdbcontroller import GdbController


class GdbControllerInterface:
    gdbmi = GdbController()
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._initialized = True
        return cls._instance

    def __init__(self, filename):
        self.filename = filename

    def get_source_code(self):
        """Get source code of program using list command of gdb"""
        self.gdbmi.write(f'-file-exec-file {self.filename}')
        self.gdbmi.write(f'file {self.filename}')

        code_dict = {}
        source_code = self.gdbmi.write('list 1,999999')

        for line_num, response in enumerate(source_code, 1):
            code = response.get('payload')
            if code and code[0].isdigit():
                code_dict[line_num] = code

        return code_dict

    def __getattr__(self, item, *args, **kwargs):
        """Use attributes from GdbController instance"""
        try:
            return getattr(self.gdbmi, item)
        except AttributeError:
            print(f'Non-existent attribute: {item}')

