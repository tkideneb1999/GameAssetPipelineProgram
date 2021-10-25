from pathlib import Path
import json


class Pipeline:
    def __init__(self):
        # Data
        self.name = "Pipeline_1"
        self.pipeline_steps = []
        self.io_connections = {}
        self.step_id_counter = 0

    def add_step(self):
        self.pipeline_steps.append(PipelineStep(f"s{self.step_id_counter}"))
        self.step_id_counter += 1

    def remove_step(self, index: int):
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

    def add_input(self, step: int):
        return self.pipeline_steps[step].add_input()

    def remove_input(self, step: int, index: int):
        uid = self.pipeline_steps[step].remove_input(index)
        self.delete_io_connection_if_exists(uid)
        return uid

    def add_output(self, step: int):
        return self.pipeline_steps[step].add_output()

    def remove_output(self, step: int, index: int):
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
    def connect_io(self, input_uid: str, output_uid: str):
        self.io_connections[input_uid] = output_uid
        print(self.io_connections)

    # -------------
    # Serialization
    # -------------
    def save(self, path: Path):
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
            f.write(json.dumps(data))
            f.close()

    def load(self, path: Path):
        with path.open("r", encoding="utf-8")as f:
            data = json.loads(f.read())
            self.name = data["name"]
            self.step_id_counter = data["step_id_counter"]
            self.io_connections = data["io_connections"]
            steps = []
            for s in data["steps"]:
                steps.append(PipelineStep(""))
                steps[len(steps) - 1].load(s)
            f.close()

    # -------
    # Helpers
    # -------
    def delete_io_connection_if_exists(self, input_id: str):
        if input_id in self.io_connections:
            del self.io_connections[input_id]


class PipelineStep:
    def __init__(self, uid: str):
        self.name = f"step_{uid}"
        self.inputs = []
        self.outputs = []
        self.uid = uid
        self.input_id_counter = 0
        self.output_id_counter = 0

    def add_input(self):
        self.inputs.append(PipelineInput(f"{self.uid}i{self.input_id_counter}"))
        self.input_id_counter += 1
        return self.inputs[len(self.inputs) - 1].uid

    def remove_input(self, index: int):
        uid = self.inputs[index].uid
        del self.inputs[index]
        return uid

    def add_output(self):
        self.outputs.append(PipelineInput(f"{self.uid}i{self.output_id_counter}"))
        self.output_id_counter += 1
        return self.outputs[len(self.outputs) - 1].uid

    def remove_output(self, index: int):
        uid = self.outputs[index].uid
        del self.outputs[index]
        return uid

    # -------------
    # Serialization
    # -------------
    def save(self):
        input_data = []
        for i in self.inputs:
            input_data.append(i.save())
        output_data = []
        for o in self.outputs:
            output_data.append(o.save())
        data = {"name": self.name,
                "uid": self.uid,
                "input_id_counter": self.input_id_counter,
                "output_id_counter": self.output_id_counter,
                "inputs": input_data,
                "outputs": output_data}
        return data

    def load(self, data: dict):
        self.name = data["name"]
        self.uid = data["uid"]
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
        self.uid = uid

    def save(self):
        return {"uid": self.uid}
        pass

    def load(self, data: dict):
        self.uid = data["uid"]
        pass


class PipelineOutput:
    def __init__(self, uid: str):
        self.name = f"output_{uid}"
        self.uid = uid

    def save(self):
        return {"uid": self.uid, "name": self.name}
        pass

    def load(self, data: dict):
        self.name = data["name"]
        self.uid = data["uid"]
        pass
