"""
COMPONENT 3 — Model Registry (simulates MLflow)

In production: MLflow Tracking Server
  - Stores trained model files
  - Tracks version, accuracy, training date
  - Lets you roll back to previous versions

Here: pickle files in /tmp + a versions.json log
"""

import pickle, json, os
from datetime import datetime
from pathlib import Path

REGISTRY_DIR = Path("/tmp/rec_model_registry")
VERSIONS_FILE = REGISTRY_DIR / "versions.json"


def _load_versions() -> list:
    if VERSIONS_FILE.exists():
        return json.loads(VERSIONS_FILE.read_text())
    return []


def _save_versions(versions: list):
    VERSIONS_FILE.write_text(json.dumps(versions, indent=2))


def save_model(model, metadata: dict = {}) -> str:
    """
    Save a trained model to the registry.
    Returns the version ID (like MLflow run ID).
    """
    REGISTRY_DIR.mkdir(exist_ok=True)
    versions = _load_versions()

    version_id = f"v{len(versions) + 1}"
    model_path = REGISTRY_DIR / f"{version_id}.pkl"

    # Serialize model to disk
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    # Log metadata (like MLflow logs params + metrics)
    entry = {
        "version":    version_id,
        "path":       str(model_path),
        "timestamp":  datetime.now().isoformat(),
        "metadata":   metadata,
    }
    versions.append(entry)
    _save_versions(versions)

    print(f"  [Registry] Saved model {version_id} → {model_path}")
    return version_id


def load_latest_model():
    """Load the most recently saved model (latest version)."""
    versions = _load_versions()
    if not versions:
        raise RuntimeError("No models in registry. Train one first.")

    latest = versions[-1]
    with open(latest["path"], "rb") as f:
        model = pickle.load(f)

    print(f"  [Registry] Loaded {latest['version']} (trained {latest['timestamp'][:19]})")
    return model


def load_model(version_id: str):
    """Load a specific version (for rollback)."""
    versions = _load_versions()
    entry = next((v for v in versions if v["version"] == version_id), None)
    if not entry:
        raise ValueError(f"Version {version_id} not found")
    with open(entry["path"], "rb") as f:
        return pickle.load(f)


def list_versions():
    """Show all saved model versions (like MLflow UI)."""
    versions = _load_versions()
    print(f"\n  [Registry] {len(versions)} model version(s):")
    for v in versions:
        meta = v.get("metadata", {})
        print(f"    {v['version']}  {v['timestamp'][:19]}  {meta}")
    return versions


if __name__ == "__main__":
    from model import RecommendationModel
    from recsys_data import INTERACTIONS

    print("=== Model Registry Demo ===\n")

    # Train and save v1
    m1 = RecommendationModel()
    m1.fit(INTERACTIONS)
    save_model(m1, {"auc": 0.91, "training_rows": len(INTERACTIONS)})

    # Train and save v2 (incremental)
    new_data = [("u1", "p8", 0), ("u2", "p4", 0), ("u3", "p5", 1)]
    m2 = RecommendationModel()
    m2.fit(INTERACTIONS)
    m2.partial_fit(new_data)
    save_model(m2, {"auc": 0.92, "incremental_rows": len(new_data)})

    list_versions()

    print("\nLoading latest model:")
    loaded = load_latest_model()
    print(f"  Model type: {type(loaded).__name__}")
    print(f"  Predict for u1, p1: {loaded.predict('u1', 'p1'):.3f}")
