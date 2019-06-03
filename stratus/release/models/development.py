from stratus.release.model import ReleaseModel



class Development(ReleaseModel):


    def customize_parser_new(self, p):
        """hook to add parser options for new command"""
        p.add_argument('--branch', action='store_true', default=False, help='create a branch from the new release')
        p.add_argument('--tag-prefix', default='dev')

    def customize_parser_build(self, p):
        pass

    def new(self):
        print(vars(self.opts))