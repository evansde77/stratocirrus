from stratus.release.model import ReleaseModel



class Train(ReleaseModel):

    def customize_parser_new(self, p):
        """hook to add parser options for new command"""

    def customize_parser_build(self, p):
        pass

    def new(self):
        print(vars(self.opts))



