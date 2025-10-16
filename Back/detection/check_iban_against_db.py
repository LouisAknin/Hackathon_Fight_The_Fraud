#!/usr/bin/env python3
"""
check_iban_against_db.py

Usage:
    echo '{"message":"Paiement urgent à M. Dupont","IBAN":"FR76123456789012ABCDEF"}' | python3 check_iban_against_db.py
    or
    python3 check_iban_against_db.py --input-file input.json

Description:
    Lit un JSON en entrée (stdin ou fichier) avec les clés "message" et "IBAN".
    Charge la base synthétique CSV (par défaut /mnt/data/synth_fraud_ibans.csv).
    Compare l'IBAN donné avec la base (exact match + fuzzy match).
    Produit un JSON de sortie avec un rapport de risque et les enregistrements correspondants.
"""
import argparse
import json
import sys
import re
from difflib import SequenceMatcher
from pathlib import Path
import pandas as pd

# Chemin par défaut vers la base synthétique (modifie si besoin)
DEFAULT_DB_PATH = Path("synth_fraud_ibans.csv")

# Normalisation simple d'un IBAN : retirer espaces et tirets, majuscules
def normalize_iban(iban: str) -> str:
    if iban is None:
        return ""
    return re.sub(r'[^A-Za-z0-9]', '', iban).upper()

# Similarité simple entre deux chaînes (0..1)
def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

# Niveau de risque heuristique basé sur fraud_score et similarité
def compute_risk_level(db_score: float, sim: float) -> str:
    # db_score in [0,1], sim in [0,1]
    combined = 0.7 * db_score + 0.3 * sim  # pondération heuristique
    if combined >= 0.85:
        return "HIGH"
    elif combined >= 0.7:
        return "MEDIUM"
    else:
        return "LOW"

# Charger la DB CSV
def load_db(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"DB file not found: {path}")
    df = pd.read_csv(path, dtype=str)
    # s'assurer de colonnes attendues et types
    for c in ["iban", "account_holder", "bank_name", "country", "fraud_type", "first_seen", "last_seen", "fraud_score", "linked_accounts", "notes"]:
        if c not in df.columns:
            df[c] = ""
    # normaliser IBAN dans DB pour comparaisons
    df["iban_norm"] = df["iban"].fillna("").apply(normalize_iban)
    # convertir fraud_score en float si possible
    df["fraud_score"] = pd.to_numeric(df["fraud_score"], errors="coerce").fillna(0.0)
    return df

# Fonction principale de comparaison
def check_iban(input_json: dict, db: pd.DataFrame, top_k:int=5) -> dict:
    message = input_json.get("message", "")
    iban_input_raw = input_json.get("IBAN", "")
    iban_norm = normalize_iban(iban_input_raw)

    result = {
        "input_iban_raw": iban_input_raw,
        "input_iban_norm": iban_norm,
        "found_exact": False,
        "exact_match_record": None,
        "closest_matches": [],
        "risk_level": "UNKNOWN",
        "reasons": [],
        "message": message
    }

    if not iban_norm:
        result["reasons"].append("No IBAN provided after normalization.")
        return result

    # Recherche exacte
    matches_exact = db[db["iban_norm"] == iban_norm]
    if not matches_exact.empty:
        # On prend le premier si plusieurs
        rec = matches_exact.iloc[0].to_dict()
        result["found_exact"] = True
        # Nettoyage du record (supprimer la colonne interne)
        rec.pop("iban_norm", None)
        result["exact_match_record"] = rec
        result["reasons"].append("Exact IBAN found in fraud DB.")
        # risk compute
        risk = compute_risk_level(float(rec.get("fraud_score", 0.0)), 1.0)
        result["risk_level"] = risk
        return result

    # Si pas d'exact, chercher les correspondances proches
    # On calcule similarity contre chaque IBAN normalisé dans la DB
    db["sim"] = db["iban_norm"].apply(lambda x: similarity(x, iban_norm))
    # Trier par similarité décroissante
    db_sorted = db.sort_values("sim", ascending=False)
    top = db_sorted.head(top_k)

    closest = []
    for _, row in top.iterrows():
        sim = float(row["sim"])
        if sim < 0.6:
            # si la similarité est trop faible, on ignore
            continue
        rec = {
            "iban": row["iban"],
            "iban_norm": row["iban_norm"],
            "fraud_type": row.get("fraud_type", ""),
            "fraud_score": float(row.get("fraud_score", 0.0)),
            "linked_accounts": row.get("linked_accounts", ""),
            "sim": round(sim, 3),
            "notes": row.get("notes", "")
        }
        # niveau de risque combiné
        rec["combined_risk_level"] = compute_risk_level(rec["fraud_score"], sim)
        closest.append(rec)

    result["closest_matches"] = closest

    if closest:
        # Base heuristique : prendre le meilleur match pour le risk
        best = closest[0]
        result["risk_level"] = best["combined_risk_level"]
        reasons = []
        if best["sim"] >= 0.95:
            reasons.append("Très forte similarité (probable même IBAN avec petits formats/espaces).")
        elif best["sim"] >= 0.8:
            reasons.append("Forte similarité — possible faute de frappe ou format différent.")
        else:
            reasons.append("Similatité modérée — vérifier manuellement.")
        if best["fraud_score"] >= 0.9:
            reasons.append("DB fraud_score très élevé pour le compte similaire.")
        elif best["fraud_score"] >= 0.75:
            reasons.append("Score de fraude DB notable.")
        if best["linked_accounts"]:
            reasons.append("Compte lié à d'autres IBANs suspects.")
        result["reasons"].extend(reasons)
    else:
        result["risk_level"] = "LOW"
        result["reasons"].append("Aucune correspondance proche trouvée dans la DB synthétique.")

    return result

# CLI / I/O
def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--db-path", type=str, default=str(DEFAULT_DB_PATH), help="Chemin vers le CSV de la DB d'IBAN frauduleux.")
    p.add_argument("--input-file", type=str, default=None, help="Fichier JSON d'entrée. Si absent, lit depuis stdin.")
    return p.parse_args()

def main():
    args = parse_args()
    db_path = Path(args.db_path)
    try:
        db = load_db(db_path)
    except Exception as e:
        print(json.dumps({"error": f"Could not load DB: {str(e)}"}))
        sys.exit(1)

    # Lire l'input JSON
    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as f:
            input_json = json.load(f)
    else:
        raw = sys.stdin.read()
        if not raw.strip():
            print(json.dumps({"error": "No input provided on stdin and no --input-file given."}))
            sys.exit(1)
        input_json = json.loads(raw)

    # Appel de la logique
    report = check_iban(input_json, db)
    # Imprimer JSON de sortie (pretty pour debug)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
