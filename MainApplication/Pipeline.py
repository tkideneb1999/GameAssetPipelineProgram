from enum import Enum

class PipelineStepTypes(Enum):
    MODELING = 0
    UVMAPPING = 1
    RIGGING = 2
    ANIMATION = 3
    TEXTURES = 4
    GAMEIMPORT = 5

class Pipeline:
    def __init__(self):
        self.pipelineSteps = []

    def load_pipeline_from_file(self, location):
        pass


class PipelineStep:
    def __init__(self, pipeline_step_type):
        self.pipelineStepType = pipeline_step_type
        self.program = "None"

    def set_program(self, program):
        self.program = program
