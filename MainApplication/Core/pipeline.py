from pathlib import Path
import json

# TODO(Pipeline): Presets for programs


class Pipeline:
    def __init__(self):
        # Data
        self.name = "Pipeline_1"
        self.pipeline_steps: list[PipelineStep] = []
        self.io_connections: dict[str, str] = {}
        self.step_id_counter = 0

    # -------------
    # Pipeline Step
    # -------------
    def add_step(self) -> tuple[str, str]:
        self.pipeline_steps.append(PipelineStep(f"s{self.step_id_counter}"))
        self.step_id_counter += 1
        if len(self.pipeline_steps) > 1:
            if self.pipeline_steps[-2].next_step == "":
                self.pipeline_steps[-2].set_next_step(self.pipeline_steps[-1].uid)
        return self.pipeline_steps[-1].uid, self.pipeline_steps[-1].name

    def remove_step(self, index: int) -> None:
        for i in self.pipeline_steps[index].inputs:
            self.delete_io_connection_if_exists(i.uid)
        deletion_output_uids = []
        wrangled_outputs = list(self.io_connections.values())
        for o in self.pipeline_steps[index].outputs:
            if o.uid in wrangled_outputs:
                deletion_output_uids.append(wrangled_outputs.index(o.uid))
        wrangled_inputs = list(self.io_connections.keys())
        for i in deletion_output_uids:
            del self.io_connections[wrangled_inputs[i]]

        del self.pipeline_steps[index]

    def set_program(self, step_index: int, program_name: str) -> None:
        self.pipeline_steps[step_index].set_program(program_name)
        print(
            f"{self.pipeline_steps[step_index].program} is set as a program for step {self.pipeline_steps[step_index].uid}")

    def set_additional_settings(self, step_index: int, additional_settings: dict) -> None:
        self.pipeline_steps[step_index].set_additional_settings(additional_settings)

    def get_additional_settings(self, step_index) -> dict:
        return self.pipeline_steps[step_index].additional_settings

    def set_config(self, step_index: int, config: str) -> None:
        self.pipeline_steps[step_index].set_config(config)

    def set_required_settings(self, step_index: int, required_settings: dict) -> None:
        self.pipeline_steps[step_index].has_set_outputs = required_settings["has_set_outputs"]
        self.pipeline_steps[step_index].export_all = required_settings["export_all"]
        self.pipeline_steps[step_index].is_plugin = required_settings["is_plugin"]

    # --------------
    # Inputs/Outputs
    # --------------
    def add_input(self, step: int) -> str:
        return self.pipeline_steps[step].add_input()

    def remove_input(self, step: int, index: int) -> str:
        uid = self.pipeline_steps[step].remove_input(index)
        self.delete_io_connection_if_exists(uid)
        return uid

    def add_output(self, step: int) -> tuple[str, str]:
        return self.pipeline_steps[step].add_output()

    def remove_output(self, step: int, index: int) -> str:
        uid = self.pipeline_steps[step].remove_output(index)
        output_list = list(self.io_connections.values())

        # Check if output is connected to any inputs
        if uid not in output_list:
            return uid

        # Get indices of connections
        indices = []
        for i in range(len(output_list)):
            if output_list[i] == uid:
                indices.append(i)

        # Delete connections
        inputs = list(self.io_connections.keys())
        for i in indices:
            del self.io_connections[inputs[i]]
        return uid

    # ---------
    # Handle IO
    # ---------
    def connect_io(self, input_uid: str, output_uid: str) -> None:
        self.io_connections[input_uid] = output_uid
        print(self.io_connections)

    def get_connected_inputs(self, output_uids: list[str]) -> list[str]:
        indices = []
        connected_output_uids = list(self.io_connections.values())
        for i in range(len(connected_output_uids)):
            if connected_output_uids[i] in output_uids:
                indices.append(i)
        connected_input_uids = list(self.io_connections.keys())
        affected_inputs = []
        for i in range(len(indices)):
            affected_inputs.append(connected_input_uids[i])
        return affected_inputs

    # -------------
    # Serialization
    # -------------
    def save(self, path: Path) -> Path:
        steps_data = []
        for s in self.pipeline_steps:
            steps_data.append(s.save())
        data = {
            "name": self.name,
            "step_id_counter": self.step_id_counter,
            "io_connections": self.io_connections,
            "steps": steps_data
        }
        if not path.exists():
            path.mkdir(parents=True)
        path = path / f"{self.name}.json"
        if not path.is_file():
            path.touch()
        with path.open("w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4))
            f.close()
        return path

    def load(self, path: Path) -> None:
        with path.open("r", encoding="utf-8")as f:
            data = json.loads(f.read())
            self.name = data["name"]
            self.step_id_counter = data["step_id_counter"]
            self.io_connections = data["io_connections"]
            steps = []
            for s in data["steps"]:
                steps.append(PipelineStep(""))
                steps[len(steps) - 1].load(s)
            self.pipeline_steps = steps
            f.close()

    # -------
    # Helpers
    # -------
    def delete_io_connection_if_exists(self, input_id: str) -> None:
        if input_id in self.io_connections:
            del self.io_connections[input_id]

    def get_step_program(self, step_index: int) -> str:
        return self.pipeline_steps[step_index].program

    def get_uid(self, step_index: int, is_input: bool, io_index=-1) -> str:
        """
        :param step_index: pipeline step index
        :param is_input: whether next index is an input (True) or an output (False)
        :param io_index: index of the input/output
        :returns: uid of the step(io_index=-1) or input/output
        """
        if io_index == -1:
            return self.pipeline_steps[step_index].uid
        else:
            if is_input:
                return self.pipeline_steps[step_index].inputs[io_index].uid
            else:
                return self.pipeline_steps[step_index].outputs[io_index].uid

    def get_next_step_uid(self, current_step_uid: str) -> str:
        for s in self.pipeline_steps:
            if s.uid == current_step_uid:
                return s.next_step
        return ""

    def get_step_index_by_uid(self, step_uid: str) -> int:
        """
        :param step_uid: unique identifier of step
        :returns: corresponding index of pipeline step. If step uid is not found -1 is returned
        """
        for i in range(len(self.pipeline_steps)):
            if self.pipeline_steps[i].uid == step_uid:
                return i
        return -1

    def get_step_uid_from_io(self, io_uid: str) -> str:
        """
        :param io_uid: Input/Output unique id
        :returns: step uid that Input/output is part of
        """
        uid_split = io_uid.split(".")
        return uid_split[0]

    def get_step_name(self, step_uid: str) -> str:
        """
        :param step_uid: unique id of step
        :returns: name of the step
        """
        index = self.get_step_index_by_uid(step_uid)
        return self.pipeline_steps[index].name

    def get_output_name(self, output_uid: str) -> str:
        """
        :param output_uid: unique id of output
        :returns: name of the output
        """
        step_uid = self.get_step_uid_from_io(output_uid)
        step_index = self.get_step_index_by_uid(step_uid)
        output_index = self.pipeline_steps[step_index].get_io_index_by_uid(output_uid)
        return self.pipeline_steps[step_index].outputs[output_index].name

    def set_output_data_type(self, step_index: int, output_index: int, data_type: str) -> None:
        self.pipeline_steps[step_index].outputs[output_index].data_type = data_type


class PipelineStep:
    def __init__(self, uid: str):
        self.name = f"step_{uid}"
        self.next_step = ""
        self.program = ""
        self.config = None
        self.export_data_type = None
        self.inputs: list[PipelineInput] = []
        self.outputs: list[PipelineOutput] = []
        self.has_set_outputs = False
        self.export_all = False
        self.is_plugin = False
        self.uid: str = uid
        self.input_id_counter: int = 0
        self.output_id_counter: int = 0
        self.additional_settings: dict = {}

    def set_program(self, program_name: str) -> None:
        self.program = program_name

    def set_additional_settings(self, settings: dict) -> None:
        self.additional_settings = settings

    def set_next_step(self, next_step_uid: str) -> None:
        self.next_step = next_step_uid

    def set_config(self, config) -> None:
        self.config = config

    def add_input(self) -> str:
        self.inputs.append(PipelineInput(f"{self.uid}.i{self.input_id_counter}"))
        self.input_id_counter += 1
        return self.inputs[len(self.inputs) - 1].uid

    def remove_input(self, index: int) -> str:
        uid = self.inputs[index].uid
        del self.inputs[index]
        return uid

    def add_output(self) -> tuple[str, str]:
        self.outputs.append(PipelineOutput(f"{self.uid}.o{self.output_id_counter}"))
        self.output_id_counter += 1
        return self.outputs[len(self.outputs) - 1].uid, self.outputs[len(self.outputs) - 1].name

    def remove_output(self, index: int) -> str:
        uid = self.outputs[index].uid
        del self.outputs[index]
        return uid

    def get_folder_name(self) -> str:
        return f"{self.uid}_{self.name}"

    def get_io_index_by_uid(self, io_uid: str, is_input=False) -> int:
        """
        :param io_uid: Unique identifier of Input/Output
        :param is_input: Whether to return input or output index (default: output)
        :returns: index of Input/Output in Pipeline step. Returns -1 if nothing found
        """
        if is_input:
            for i in range(len(self.inputs)):
                if self.inputs[i].uid == io_uid:
                    return i
        else:
            for i in range(len(self.outputs)):
                if self.outputs[i].uid == io_uid:
                    return i
        return -1

    # -------------
    # Serialization
    # -------------
    def save(self) -> dict:
        input_data = []
        for i in self.inputs:
            input_data.append(i.save())
        output_data = []
        for o in self.outputs:
            output_data.append(o.save())
        data = {"name": self.name,
                "uid": self.uid,
                "next_step": self.next_step,
                "program": self.program,
                "is_plugin": self.is_plugin,
                "has_set_outputs": self.has_set_outputs,
                "export_all": self.export_all,
                "additional_settings": self.additional_settings,
                "config": self.config,
                "input_id_counter": self.input_id_counter,
                "output_id_counter": self.output_id_counter,
                "inputs": input_data,
                "outputs": output_data}
        return data

    def load(self, data: dict) -> None:
        self.name = data["name"]
        self.uid = data["uid"]
        self.next_step = data["next_step"]
        self.additional_settings = data["additional_settings"]
        self.config = data["config"]
        self.program = data["program"]
        self.is_plugin = data["is_plugin"]
        self.has_set_outputs = data["has_set_outputs"]
        self.export_all = data["export_all"]
        self.input_id_counter = data["input_id_counter"]
        self.output_id_counter = data["output_id_counter"]

        inputs = []
        for i in data["inputs"]:
            inputs.append(PipelineInput(""))
            inputs[len(inputs) - 1].load(i)
        self.inputs = inputs

        outputs = []
        for o in data["outputs"]:
            outputs.append(PipelineOutput(""))
            outputs[len(outputs) - 1].load(o)
        self.outputs = outputs


class PipelineInput:
    def __init__(self, uid: str):
        self.uid: str = uid
        self.name: str = f"input_{uid}"

    def save(self) -> dict:
        return {"uid": self.uid, "name": self.name}

    def load(self, data: dict) -> None:
        self.uid = data["uid"]
        self.name = data["name"]


class PipelineOutput:
    def __init__(self, uid: str):
        self.name: str = f"output_{uid}"
        self.data_type = None
        self.uid: str = uid

    def get_file_name(self):
        return f"{self.uid}_{self.name}"

    def save(self) -> dict:
        if self.data_type is None:
            data_type = ""
        else:
            data_type = self.data_type
        return {"uid": self.uid, "name": self.name, "data_type":data_type}

    def load(self, data: dict) -> None:
        self.name = data["name"]
        self.uid = data["uid"]
        if data["data_type"] == "":
            self.data_type = None
        else:
            self.data_type = data["data_type"]
