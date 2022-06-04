from .nodegraph import BaseNode


class PipelineStepNode(BaseNode):

    __identifier__ = 'pipeline'

    NODE_NAME = 'Pipeline Step'

    def __init__(self):
        super(PipelineStepNode, self).__init__()
        self.set_port_deletion_allowed(True)

        self.add_combo_menu('program', "Program", ["Test 1", "Test 2"])
        program_wgt = self.get_widget('program')
        program_wgt.value_changed.connect(self._program_changed)

    def _program_changed(self, name, data):
        print(f"Selected Program: {data}")


class PipelineAssetImportNode(BaseNode):

    __identifier__ = 'asset_import'

    NODE_NAME = 'Asset Import'

    def __init__(self):
        super(PipelineAssetImportNode, self).__init__()
        self.set_port_deletion_allowed(True)

        self.add_combo_menu('pipeline', "Pipeline", ["Pipeline 01", "Pipeline 02"])
        pipline_wgt = self.get_widget('pipeline')
        pipline_wgt.value_changed.connect(self._pipeline_changed)

    def _pipeline_changed(self, name, data):
        print(f"Selected Pipeline: {data}")


class PipelineEngineExportNode(BaseNode):

    __identifier__ = 'engine_export'

    NODE_NAME = 'Engine Export'

    def __init__(self):
        super(PipelineEngineExportNode, self).__init__()
        self.set_port_deletion_allowed(True)

        self.add_combo_menu('engine', "Engine", ["Unity", "Unreal", "CryEngine"])
        engine_wgt = self.get_widget('engine')
        engine_wgt.value_changed.connect(self._engine_changed)

    def _engine_changed(self, name, data):
        print(f"Selected Engine: {data}")