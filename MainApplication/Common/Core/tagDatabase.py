from pathlib import Path


class TagDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Tag Database Instance is None")
            cls._instance = super(TagDatabase, cls).__new__(cls)
            cls.__tags_ID_Keys: dict = {}  # ID, Name // dict[int, str]
            cls.__tags_Name_Keys: dict = {}  # Name, ID // dict[str, int]
            cls.__tag_count = 0
            cls.__loaded = False
        return cls._instance

    def add_tag(self, tag_name: str) -> int:
        """Adds a new Tag to the Database and returns the ID of the tag"""
        if self.__tags_Name_Keys.get(tag_name) is not None:
            return -1
        self.__tags_ID_Keys[self.__tag_count] = tag_name
        self.__tags_Name_Keys[tag_name] = self.__tag_count
        self.__tag_count += 1
        return self.__tag_count - 1

    def save(self, project_dir: Path):
        path = project_dir / "tags.meta"
        if not path.exists():
            path.touch()
        tag_list = [f"{len(list(self.__tags_ID_Keys.keys()))} amount\n", f"{self.__tag_count} id_count\n"]
        for uid in list(self.__tags_ID_Keys.keys()):
            tag_list.append(f"{uid},{self.__tags_ID_Keys[uid]}\n")
        with path.open("w", encoding="utf-8") as f:
            f.writelines(tag_list)

    def load(self, project_dir: Path):
        print("[GAPA] Loading Tags")
        path = Path(project_dir) / "tags.meta"
        if not path.exists():
            print("[GAPA][Warning] Tag Data not found, using new one")
            return
        if not path.is_file():
            raise Exception("Asset List does not exist.")
        with path.open("r", encoding="utf-8") as f:
            num_tags = int(f.readline().split(' ')[0])
            self._instance.__tag_count = int(f.readline().split(' ')[0])
            for i in range(num_tags):
                tag_data_s = f.readline()
                tag_data = tag_data_s.split(",", 1)
                tag_ID = int(tag_data[0])
                tag_name = tag_data[1].replace('\n', '')
                self.__tags_ID_Keys[tag_ID] = tag_name
                self.__tags_Name_Keys[tag_name] = tag_ID
        print(self.__tags_ID_Keys)
        print(self.__tags_Name_Keys)
        self._instance.__loaded = True

    def import_tags(self, tags: dict):
        for uid in tags:
            self.add_tag(tags[uid])

    def get_tag_name(self, tag_ID: int):
        return self.__tags_ID_Keys[tag_ID]

    def get_tag_ID(self, tag_name: str):
        return self.__tags_Name_Keys[tag_name]

    def get_tag_IDs(self, tag_names: list) -> list:
        tag_IDs = []
        for tn in tag_names:
            tag_IDs.append(self.get_tag_ID(tn))
        return tag_IDs

    @property
    def tag_names(self):
        return list(self.__tags_Name_Keys.keys())

    @property
    def tag_IDs(self):
        return list(self.__tags_ID_Keys.keys())

    def check_if_tag_exists(self, tag_name: str) -> bool:
        return self.__tags_Name_Keys.get(tag_name) is not None

    def is_loaded(self):
        return self.__loaded
