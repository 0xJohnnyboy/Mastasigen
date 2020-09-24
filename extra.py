class Extra:

    def __init__(self, code_friendly: bool, fenced_code_blocks: bool,
            cuddled_lists: bool):
        self.code_friendly = code_friendly
        self.fenced_code_blocks = fenced_code_blocks
        self.cuddled_lists = cuddled_lists

    def get_extras(self):
        
        return [self.code_friendly, self.fenced_code_blocks,
                self.cuddled_lists]
