## Edge-level capacitance prediction on graph folders

This project trains a GNN to predict per-edge capacitance. Each graph is stored in its own folder with two CSV files:

- nodes.csv: columns `x,y` (optionally `id`)
- edges.csv: columns `src,dst,target` (or `src,dst,capacitance`)

The node features are the 2D spatial coordinates `(x, y)`. The supervised target is on edges.

### Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

If PyTorch Geometric wheels are needed for your CUDA version, follow their install guide and then install the remaining packages from `requirements.txt`.

### Data layout

```
graphs_root/
  graph_000/
    nodes.csv   # columns: (id optional), x, y
    edges.csv   # columns: src, dst, target (or capacitance)
  graph_001/
    nodes.csv
    edges.csv
  ...
```

### Train

```bash
python train.py /abs/path/to/graphs_root --out /abs/path/to/outputs --epochs 100 --batch_size 4
```

Artifacts:
- best.pt (best validation MAE)
- latest.pt (last epoch)
- TensorBoard logs under `--out/tb`

### Evaluate

```bash
python evaluate.py /abs/path/to/graphs_root /abs/path/to/outputs/best.pt
```

Prints MAE and MSE over all edges across graphs.

### Inference

```bash
python infer.py /abs/path/to/graphs_root /abs/path/to/outputs/best.pt --out /abs/path/to/predictions
```

Writes one CSV per input graph: `{graph_folder_name}_predictions.csv` with columns `src,dst,prediction`.

### Notes

- Model: GraphSAGE node encoder with MLP edge readout combining `(h_src, h_dst, |h_src-h_dst|, h_src*h_dst)`.
- Inputs assume node coordinates are normalized/consistent across graphs; add transforms if needed.