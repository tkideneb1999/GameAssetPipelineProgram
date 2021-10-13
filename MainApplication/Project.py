from Pipeline import Pipeline


class Project:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.assets = []
        self.default_pipeline = Pipeline()

    def create_asset(self, asset):
        self.assets.append(asset)

