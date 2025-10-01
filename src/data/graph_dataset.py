import os
from typing import List, Tuple

import torch
from torch_geometric.data import InMemoryDataset, Data

from src.utils.io import list_graph_folders, read_graph_from_folder


class GraphFolderDataset(InMemoryDataset):
    def __init__(self, root_dir: str, transform=None, pre_transform=None):
        self.root_dir = os.path.abspath(root_dir)
        super().__init__(self.root_dir, transform, pre_transform)
        self.data, self.slices = torch.load(self.processed_paths[0])

    @property
    def raw_file_names(self) -> List[str]:
        # We treat each subfolder as a graph; we do not use raw downloads
        return []

    @property
    def processed_file_names(self) -> List[str]:
        return ["data.pt"]

    def download(self) -> None:
        return

    def process(self) -> None:
        graph_dirs: Tuple[str, ...] = list_graph_folders(self.root_dir)
        data_list: List[Data] = []
        for gdir in graph_dirs:
            data = read_graph_from_folder(gdir)
            data.graph_dir = gdir  # type: ignore[attr-defined]
            data_list.append(data)

        if self.pre_transform is not None:
            data_list = [self.pre_transform(d) for d in data_list]

        data, slices = self.collate(data_list)
        os.makedirs(self.processed_dir, exist_ok=True)
        torch.save((data, slices), self.processed_paths[0])