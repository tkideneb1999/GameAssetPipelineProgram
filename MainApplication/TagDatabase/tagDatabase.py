from pathlib import Path


class TagDatabase:
    def __init__(self):
        self.tags: dict[int, str] = {}
        self.tag_count = 0

    def add_tag(self, tag_name: str) -> int:
        """Adds a new Tag to the Database and returns the ID of the tag"""
        self.tags[self.tag_count] = tag_name
        self.tag_count += 1
        return self.tag_count - 1

    def save(self, project_dir: Path):
        path = project_dir / "tags.meta"
        if not path.exists():
            path.touch()
        tag_list = [f"{len(list(self.tags.keys()))} amount\n", f"{self.tag_count} id_count\n"]
        for uid in list(self.tags.keys()):
            tag_list.append(f"{uid},{self.tags[uid]}\n")
        with path.open("w", encoding="utf-8") as f:
            f.writelines(tag_list)

    def load(self, project_dir: Path):
        path = Path(project_dir) / "tags.meta"
        if not path.exists():
            print("[GAPA][Warning] Tag Data not found, using new one")
            return
        if not path.is_file():
            raise Exception("Asset List does not exist.")
        with path.open("r", encoding="utf-8") as f:
            num_tags = int(f.readline().split(' ')[0])
            self.tag_count = int(f.readline().split(' ')[0])
            for i in range(num_tags):
                tag_data_s = f.readline()
                tag_data = tag_data_s.split(",", 1)
                self.tags[int(tag_data[0])] = tag_data[1].replace('\n', '')

    def import_tags(self, tags: dict):
        for uid in tags:
            self.add_tag(tags[uid])
