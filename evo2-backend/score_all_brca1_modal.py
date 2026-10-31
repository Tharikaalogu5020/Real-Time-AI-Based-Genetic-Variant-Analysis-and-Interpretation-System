import modal
import os

evo2_image = (
    modal.Image.from_registry(
        "nvidia/cuda:12.4.0-devel-ubuntu22.04", add_python="3.12"
    )
    .apt_install(
        ["build-essential", "cmake", "ninja-build",
            "libcudnn8", "libcudnn8-dev", "git", "gcc", "g++"]
    )
    .env({
        "CC": "/usr/bin/gcc",
        "CXX": "/usr/bin/g++",
    })
    .run_commands("pip install torch --index-url https://download.pytorch.org/whl/cu124")
    .run_commands("pip install wheel")
    .run_commands("git clone --recurse-submodules https://github.com/ArcInstitute/evo2.git && cd evo2 && pip install .")
    .run_commands("pip uninstall -y transformer-engine transformer_engine")
    .run_commands("pip install 'transformer_engine[pytorch]==1.13' --no-build-isolation")
    .pip_install_from_requirements("requirements.txt")
)

app = modal.App("score-all-brca1", image=evo2_image)
volume = modal.Volume.from_name("hf_cache", create_if_missing=True)
mount_path = "/root/.cache/huggingface"

@app.function(gpu="A10G", volumes={mount_path: volume}, timeout=3600)
def score_all_variants():
    import gzip
    from Bio import SeqIO
    import numpy as np
    import pandas as pd
    from evo2 import Evo2

    WINDOW_SIZE = 8192

    print("Loading evo2_7b model...")
    model = Evo2('evo2_7b')
    print("Evo2 model loaded successfully!")

    excel_path = '/evo2/notebooks/brca1/41586_2018_461_MOESM3_ESM.xlsx'
    fasta_path = '/evo2/notebooks/brca1/GRCh37.p13_chr17.fna.gz'

    print(f"Reading variants from {excel_path}...")
    brca1_df = pd.read_excel(excel_path, header=2)
    brca1_df = brca1_df[['chromosome', 'position (hg19)', 'reference', 'alt', 'function.score.mean', 'func.class']]
    brca1_df.rename(columns={
        'chromosome': 'chrom',
        'position (hg19)': 'pos',
        'reference': 'ref',
        'alt': 'alt',
        'function.score.mean': 'score',
        'func.class': 'class',
    }, inplace=True)

    print(f"Total variants: {len(brca1_df)}")

    # Two-class system
    brca1_df['cls'] = brca1_df['class'].replace(['FUNC', 'INT'], 'FUNC/INT')
    brca1_df['label'] = (brca1_df['cls'] == 'LOF').astype(int)

    print(f"Reading reference genome from {fasta_path}...")
    with gzip.open(fasta_path, "rt") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            seq_chr17 = str(record.seq)
            break

    ref_seqs = []
    ref_seq_to_index = {}
    ref_seq_indexes = []
    var_seqs = []

    for _, row in brca1_df.iterrows():
        p = int(row["pos"]) - 1
        full_seq = seq_chr17

        ref_seq_start = max(0, p - WINDOW_SIZE // 2)
        ref_seq_end = min(len(full_seq), p + WINDOW_SIZE // 2)
        ref_seq = seq_chr17[ref_seq_start:ref_seq_end]
        snv_pos_in_ref = min(WINDOW_SIZE // 2, p)
        var_seq = ref_seq[:snv_pos_in_ref] + str(row["alt"]) + ref_seq[snv_pos_in_ref + 1:]

        if ref_seq not in ref_seq_to_index:
            ref_seq_to_index[ref_seq] = len(ref_seqs)
            ref_seqs.append(ref_seq)

        ref_seq_indexes.append(ref_seq_to_index[ref_seq])
        var_seqs.append(var_seq)

    ref_seq_indexes = np.array(ref_seq_indexes)

    print(f"Scoring {len(ref_seqs)} unique reference sequences...")
    ref_scores = model.score_sequences(ref_seqs, batch_size=4)

    print(f"Scoring {len(var_seqs)} variant sequences...")
    var_scores = model.score_sequences(var_seqs, batch_size=4)

    delta_scores = np.array(var_scores) - np.array(ref_scores)[ref_seq_indexes]
    brca1_df['delta'] = delta_scores

    output_df = brca1_df[['chrom', 'pos', 'ref', 'alt', 'cls', 'label', 'delta']]
    return output_df.to_dict(orient="records")

@app.local_entrypoint()
def main():
    print("Connecting to Modal to score all 3,893 variants with evo2_7b on A10G GPU...")
    records = score_all_variants.remote()
    import pandas as pd
    out_df = pd.DataFrame(records)
    out_path = "brca1_scores.csv"
    out_df.to_csv(out_path, index=False)
    print(f"Saved {len(out_df)} scored variants to {out_path}")

