from pathlib import Path

from .tagDatabase import TagDatabase


class AssetDatabase:

    def __init__(self):
        self.__project_dir: Path = None

        self.__assets: dict = {}  # Asset ID : (Asset Name, Level) // dict[int, tuple[str, str]]
        self.__asset_ID_counter: int = 0

        self.__level_asset_dict: dict = {}  # Level Name : Set(Asset ID) // dict[str, set[int]]

        self.__tag_asset_dict: dict = {}  # Tag ID : set(Asset ID) // dict[int, set[int]]

    def set_project_dir(self, path: Path):
        self.__project_dir = path
        self.update_tags()

    def add_level(self, level_name: str) -> bool:
        if self.__level_asset_dict.get(level_name) is not None:
            print(f"[GAPA][ERROR] Level already exists with that name")
            return False
        self.__level_asset_dict[level_name] = set()
        return True

    def update_tags(self):
        tag_database = TagDatabase()
        if not tag_database.is_loaded():
            tag_database.load(self.__project_dir)
        for tid in tag_database.tag_IDs:
            if self.__tag_asset_dict.get(tid) is None:
                self.__tag_asset_dict[tid] = set()

    def add_new_asset(self, name: str, level: str, tagIDs: list) -> int:
        self.update_tags()

        if not self.check_asset(name, level):
            print("[GAPA][ERROR] Asset already exists under that name in the selected Level")
            return -1
        if self.__level_asset_dict.get(level) is None:
            print("[GAPA][ERROR] Level does not exist")
            return -2
        for tid in tagIDs:
            if self.__tag_asset_dict.get(tid) is None:
                print(f"[GAPA][ERROR] Tag ID {tid} does not exist")
                return -3

        asset_id = self.__asset_ID_counter
        self.__assets[asset_id] = (name, level)

        self.__level_asset_dict[level].add(asset_id)
        for tid in tagIDs:
            self.__tag_asset_dict[tid].add(asset_id)

        self.__asset_ID_counter += 1
        return asset_id

    def remove_asset(self, asset_id: int) -> tuple:
        asset_data = self.__assets[asset_id]
        for tid in self.__tag_asset_dict:
            self.__tag_asset_dict[tid].remove(asset_id)
        self.__level_asset_dict[asset_data[1]].remove(asset_id)
        self.__assets.pop(asset_id)
        return asset_data

    def remove_level(self, level_name: str) -> None:
        affected_assets = self.__level_asset_dict[level_name]
        for tid in self.__tag_asset_dict:
            self.__tag_asset_dict[tid] = self.__tag_asset_dict[tid] - affected_assets
        for aid in affected_assets:
            del self.__assets[aid]
        del self.__level_asset_dict[level_name]

    def get_assets_by_tag(self, tagIDs: list) -> dict:
        asset_id_set = set()
        for tid in tagIDs:
            asset_id_set = asset_id_set.union(self.__tag_asset_dict[tid])
        asset_names: dict = {}
        for aid in asset_id_set:
            data = self.__assets[aid]
            if asset_names.get(data[1]) is None:
                asset_names[data[1]] = []
            asset_names[data[1]].append((aid, data[0]))
        return asset_names

    def get_all_assets(self) -> dict:
        all_assets = {}
        for aid in self.__assets:
            asset_data = self.__assets[aid]
            if all_assets.get(asset_data[1]) is None:
                all_assets[asset_data[1]] = []
            all_assets[asset_data[1]].append((aid, asset_data[0]))
        return all_assets

    def get_asset_by_id(self, asset_id) -> tuple:
        return self.__assets[asset_id]

    @property
    def levels(self):
        return list(self.__level_asset_dict.keys())

    def check_asset(self, name: str, level: str) -> bool:
        for aid in self.__level_asset_dict[level]:
            if name == self.__assets[aid][0]:
                return False
        return True

    # -------------
    # SERIALIZATION
    # -------------

    def load_asset_list(self) -> None:
        self.__load_asset_mapping()
        self.__load_level_mapping()
        self.__load_tag_mapping()

    def __load_asset_mapping(self) -> None:
        path = self.__project_dir / "assetMapping.meta"
        if not path.exists():
            raise Exception("Asset List does not exist.")
        if not path.is_file():
            raise Exception("Asset List does not exist.")
        with path.open("r", encoding="utf-8") as f:

            amount_info = f.readline()
            amount = int(amount_info.split()[1])

            id_counter_info = f.readline()
            self.__asset_ID_counter = int(id_counter_info.split()[1])
            for a in range(amount):
                raw_data = f.readline()
                asset_data = raw_data.split(':')
                asset_data[1] = asset_data[1].replace('\n', '')
                asset_name_data = asset_data[1].split(',')
                self.__assets[int(asset_data[0])] = (asset_name_data[0], asset_name_data[1])
            f.close()

    def __load_level_mapping(self) -> None:
        path = self.__project_dir / "levelMapping.meta"
        if not path.exists():
            raise Exception("Asset List does not exist.")
        if not path.is_file():
            raise Exception("Asset List does not exist.")
        with path.open("r", encoding="utf-8") as f:
            amount_info = f.readline()
            amount = int(amount_info.split()[1])
            for i in range(amount):
                raw_data = f.readline()
                lvl_data = raw_data.split(':')
                lvl_data[1] = lvl_data[1].replace('\n', '')
                if lvl_data[1] == '':
                    self.__level_asset_dict[lvl_data[0]] = set()
                    f.close()
                    return
                aid_data = lvl_data[1].split(',')
                aids = set()
                for aid in aid_data:
                    if aid == '':
                        continue
                    aids.add(int(aid))
                self.__level_asset_dict[lvl_data[0]] = aids
            f.close()

    def __load_tag_mapping(self) -> None:
        path = self.__project_dir / "tagMapping.meta"
        if not path.exists():
            raise Exception("Asset List does not exist.")
        if not path.is_file():
            raise Exception("Asset List does not exist.")
        with path.open("r", encoding="utf-8") as f:
            amount_info = f.readline()
            amount = int(amount_info.split()[1])
            for i in range(amount):
                raw_data = f.readline()
                tag_data = raw_data.split(':')
                tag_data[1] = tag_data[1].replace('\n', '')
                if tag_data[1] == '':
                    self.__tag_asset_dict[int(tag_data[0])] = set()
                    continue
                aid_data = tag_data[1].split(',')
                aids = set()
                for aid in aid_data:
                    if aid == '':
                        continue
                    aids.add(int(aid))
                self.__tag_asset_dict[int(tag_data[0])] = aids
            f.close()

    def save_asset_list(self) -> None:
        self.__save_asset_mapping()
        self.__save_level_mapping()
        self.__save_tag_mapping()

    def __save_asset_mapping(self) -> None:
        asset_mapping_path = self.__project_dir / "assetMapping.meta"
        if self.__check_if_valid_filepath(asset_mapping_path):
            asset_mapping_path.touch()
        with asset_mapping_path.open("w", encoding="utf-8") as f:
            num_assets = len(self.__assets)
            f.write(f"amount {num_assets}\n")
            f.write(f"IdCounter {self.__asset_ID_counter}\n")
            for aid in self.__assets:
                f.write(f"{aid}:{self.__assets[aid][0]},{self.__assets[aid][1]}\n")
            f.close()

    def __save_level_mapping(self) -> None:
        level_mapping_path = self.__project_dir / "levelMapping.meta"
        if self.__check_if_valid_filepath(level_mapping_path):
            level_mapping_path.touch()
        with level_mapping_path.open("w", encoding="utf-8") as f:
            num_level = len(self.__level_asset_dict.keys())
            f.write(f"amount {num_level}\n")
            for lvl in self.__level_asset_dict:
                asset_ids = ""
                for aid in self.__level_asset_dict[lvl]:
                    asset_ids += str(aid) + ","
                f.write(f"{lvl}:{asset_ids}\n")
            f.close()

    def __save_tag_mapping(self) -> None:
        tag_mapping_path = self.__project_dir / "tagMapping.meta"
        if self.__check_if_valid_filepath(tag_mapping_path):
            tag_mapping_path.touch()
        with tag_mapping_path.open("w", encoding="utf-8") as f:
            num_tags = len(self.__tag_asset_dict.keys())
            f.write(f"amount {num_tags}\n")
            for tid in self.__tag_asset_dict:
                asset_ids = ""
                for aid in self.__tag_asset_dict[tid]:
                    asset_ids += str(aid) + ","
                f.write(f"{tid}:{asset_ids}\n")
            f.close()

    @staticmethod
    def __check_if_valid_filepath(path: Path) -> bool:
        if not path.exists():
            if not path.is_file():
                return False
        return True
