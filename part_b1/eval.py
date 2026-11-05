def evaluate(reference, prediction):
    if not reference and not prediction:
        return {"TP": 0, "FP": 0, "FN": 0, "Precision": 1.0, "Recall": 1.0, "F1": 1.0}
    tp = len(reference & prediction)
    fp = len(prediction - reference) 
    fn = len(reference - prediction)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0)
    eval_metrics = {
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "Precision": round(precision,2),
        "Recall": round(recall,2),
        "F1": round(f1,2)
    }
    return eval_metrics

def evaluate_per_type(reference, prediction):
    types = {t for _ , t in reference | prediction}
    results = {}
    for t in sorted(types):
        ref_t = {entity for entity in reference if entity[1]==t}
        pred_t = {entity for entity in prediction if entity[1]==t}
        results[t] = evaluate(ref_t, pred_t)
    results["Overall"] = evaluate(reference, prediction)
    return results
    ...