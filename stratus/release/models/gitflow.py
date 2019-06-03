


from stratus.release.model import ReleaseModel


class Gitflow(ReleaseModel):

    def customize_parser_new(self, p):
        """hook to add parser options for new command"""
        g = p.add_mutually_exclusive_group()
        g.add_argument('--micro', action='store_true', dest='micro', default=False)
        g.add_argument('--minor', action='store_true', dest='minor', default=False)
        g.add_argument('--major', action='store_true', dest='major', default=False)
        p.add_argument('--stay-on-branch', action='store_true', default=False, help='stay on new release branch')

    def customize_parser_build(self, p):
        p.add_argument('--distribution', default=None)

    def new(self):
        print(vars(self.opts))

