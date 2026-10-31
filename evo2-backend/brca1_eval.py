import argparse
import json
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)

def evaluate(scores_csv_path, output_json_path="brca1_results.json"):
    print(f"Loading scores from: {scores_csv_path}")
    df = pd.read_csv(scores_csv_path)

    required_cols = {"chrom", "pos", "ref", "alt", "cls", "label", "delta"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing required columns in {scores_csv_path}. Required: {required_cols}")

    total_variants = len(df)
    lof_count = int((df["label"] == 1).sum())
    func_count = int((df["label"] == 0).sum())

    y_true = df["label"].values
    # Negative delta implies loss of function (pathogenic)
    y_scores = -df["delta"].values

    auroc = float(roc_auc_score(y_true, y_scores))

    # Optimal threshold using Youden's J statistic
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    optimal_idx = int((tpr - fpr).argmax())
    optimal_threshold_neg = float(thresholds[optimal_idx])
    optimal_delta_threshold = float(-optimal_threshold_neg)

    # Classify: delta < threshold -> Pathogenic (1), else Benign (0)
    y_pred = (df["delta"] < optimal_delta_threshold).astype(int).values

    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = [int(v) for v in cm.ravel()]

    accuracy = float(accuracy_score(y_true, y_pred))
    precision = float(precision_score(y_true, y_pred))
    recall = float(recall_score(y_true, y_pred))
    f1 = float(f1_score(y_true, y_pred))

    results = {
        "dataset": "BRCA1 Findlay SGE (41586_2018_461_MOESM3_ESM.xlsx)",
        "total_variants": total_variants,
        "ground_truth_counts": {
            "pathogenic_LOF": lof_count,
            "benign_FUNC_INT": func_count
        },
        "auroc": round(auroc, 4),
        "optimal_delta_threshold": round(optimal_delta_threshold, 8),
        "confusion_matrix": {
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "true_negatives": tn
        },
        "metrics": {
            "accuracy": round(accuracy * 100, 2),
            "precision": round(precision * 100, 2),
            "recall": round(recall * 100, 2),
            "f1_score": round(f1_score * 100, 2)
        }
    }

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 60)
    print("           BRCA1 ZERO-SHOT EVALUATION RESULTS")
    print("=" * 60)
    print(f" Total Variants Evaluated: {total_variants}")
    print(f" Ground Truth LOF (Pathogenic) : {lof_count}")
    print(f" Ground Truth FUNC/INT (Benign): {func_count}")
    print(f" Area Under ROC Curve (AUROC)  : {auroc:.4f}")
    print(f" Calibrated Delta Threshold   : {optimal_delta_threshold:.8f}")
    print("-" * 60)
    print(f" Confusion Matrix:")
    print(f"   TP = {tp:<6}  FN = {fn:<6}")
    print(f"   FP = {fp:<6}  TN = {tn:<6}")
    print("-" * 60)
    print(f" Accuracy : {accuracy * 100:.2f}%")
    print(f" Precision: {precision * 100:.2f}%")
    print(f" Recall   : {recall * 100:.2f}%")
    print(f" F1-Score : {f1 * 100:.2f}%")
    print("=" * 60)
    print(f"Saved evaluation metrics to: {output_json_path}")
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Evo2 BRCA1 variant predictions")
    parser.add_argument("--scores", required=True, help="Path to brca1_scores.csv")
    parser.add_argument("--output", default="brca1_results.json", help="Path to output JSON")
    args = parser.parse_args()

    evaluate(args.scores, args.output)

