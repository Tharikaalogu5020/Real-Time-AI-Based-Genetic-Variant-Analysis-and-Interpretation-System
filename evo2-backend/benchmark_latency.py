import time
import json
import statistics
import ssl
import urllib.request
import pandas as pd

ssl_context = ssl._create_unverified_context()

def main():
    csv_path = "actual_model_predictions_test.csv"
    df = pd.read_csv(csv_path)
    samples = df.head(20)

    print(f"Loaded {len(samples)} sample variants for latency benchmarking:")
    for idx, row in samples.iterrows():
        print(f" Variant {idx+1}: chr{row['chrom']}:{row['pos']} {row['ref']}>{row['alt']}")

    ucsc_times = []
    evo2_times = []
    clinvar_times = []

    print("\nRunning benchmark across 20 variants...\n")

    for idx, row in samples.iterrows():
        chrom = f"chr{row['chrom']}"
        pos = int(row['pos'])
        ref = str(row['ref'])
        alt = str(row['alt'])
        window_size = 8192

        half_window = window_size // 2
        start = max(0, pos - 1 - half_window)
        end = pos - 1 + half_window + 1

        # 1. Genome Sequence Fetch (UCSC REST API)
        t0 = time.time()
        ucsc_url = f"https://api.genome.ucsc.edu/getData/sequence?genome=hg19;chrom={chrom};start={start};end={end}"
        req_ucsc = urllib.request.Request(ucsc_url, headers={"User-Agent": "Evo2VariantBenchmark/1.0"})
        with urllib.request.urlopen(req_ucsc, timeout=15, context=ssl_context) as resp:
            data_ucsc = json.loads(resp.read().decode())
            seq = data_ucsc.get("dna", "")
        t_ucsc = time.time() - t0
        ucsc_times.append(t_ucsc)

        # 2. Evo 2 Call (FastAPI backend /analyze)
        t0 = time.time()
        payload = json.dumps({
            "variant_position": pos,
            "alternative": alt,
            "genome": "hg19",
            "chromosome": chrom
        }).encode("utf-8")
        req_evo2 = urllib.request.Request(
            "http://127.0.0.1:8000/analyze",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_evo2, timeout=15) as resp:
            data_evo2 = json.loads(resp.read().decode())
        t_evo2 = time.time() - t0
        evo2_times.append(t_evo2)

        # 3. ClinVar Lookup (NCBI E-utilities API)
        t0 = time.time()
        chrom_num = chrom.replace("chr", "")
        # Look up variant at position in ClinVar
        search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term={chrom_num}[chromosome]+AND+{pos}:{pos}[chrpos37]&retmode=json"
        req_clinvar = urllib.request.Request(search_url, headers={"User-Agent": "Evo2VariantBenchmark/1.0"})
        with urllib.request.urlopen(req_clinvar, timeout=15, context=ssl_context) as resp:
            data_cv = json.loads(resp.read().decode())
        t_cv = time.time() - t0
        clinvar_times.append(t_cv)

        print(f"[{idx+1}/20] Pos {pos} | UCSC: {t_ucsc:.3f}s | Evo2: {t_evo2:.3f}s | ClinVar: {t_cv:.3f}s | Total: {t_ucsc+t_evo2+t_cv:.3f}s")
        # Gentle pacing between requests to avoid rate limiting
        time.sleep(0.3)

    print("\n" + "=" * 65)
    print("                    LATENCY BENCHMARK RESULTS (20 VARIANTS)")
    print("=" * 65)
    print(f"{'Pipeline Step':<35} | {'Mean (seconds)':<15} | {'Median (seconds)':<15}")
    print("-" * 65)
    print(f"{'1. Genome sequence fetch (UCSC API)':<35} | {statistics.mean(ucsc_times):.4f} s        | {statistics.median(ucsc_times):.4f} s")
    print(f"{'2. Evo 2 call (Backend)':<35} | {statistics.mean(evo2_times):.4f} s        | {statistics.median(evo2_times):.4f} s")
    print(f"{'3. ClinVar lookup (NCBI API)':<35} | {statistics.mean(clinvar_times):.4f} s        | {statistics.median(clinvar_times):.4f} s")
    print("-" * 65)
    total_times = [u + e + c for u, e, c in zip(ucsc_times, evo2_times, clinvar_times)]
    print(f"{'Total End-to-End Latency':<35} | {statistics.mean(total_times):.4f} s        | {statistics.median(total_times):.4f} s")
    print("=" * 65)

    # Also output raw per-variant timings
    print("\nPer-Variant Breakdown:")
    print("Variant,Position,Ref>Alt,UCSC_s,Evo2_s,ClinVar_s,Total_s")
    for i in range(20):
        row = samples.iloc[i]
        print(f"{i+1},{row['pos']},{row['ref']}>{row['alt']},{ucsc_times[i]:.4f},{evo2_times[i]:.4f},{clinvar_times[i]:.4f},{total_times[i]:.4f}")

if __name__ == "__main__":
    main()
