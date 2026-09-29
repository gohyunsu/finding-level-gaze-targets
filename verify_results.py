#!/usr/bin/env python3
"""Validate the released result registry, README asset, and public tree."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_RESULTS = ROOT / "results" / "study-results.json"
PUBLICATION_TITLE = (
    "From Complete Scanpaths to Finding-Level Gaze Targets in Chest Radiography: "
    "Structured Cues and Learned Reweighting"
)
REPOSITORY = "https://github.com/gohyunsu/finding-level-gaze-targets"
AUTHORS = ["Sumin Lee", "Hyunsu Go", "Subeen Lee", "Kyeonghun Kim", "Nam-Joon Kim"]


EXPECTED = {
    "status": "paper_results",
    "project.name": "Finding-Level Gaze Targets",
    "project.python_package": "finding_level_gaze_targets",
    "project.repository": REPOSITORY,
    "associated_publication.title": PUBLICATION_TITLE,
    "associated_publication.venue": "IEEE MedAI 2026",
    "associated_publication.year": 2026,
    "associated_publication.authors": AUTHORS,
    "estimator.optimizer_seeds": [0, 1, 2, 3, 4],
    "estimator.primary_estimand": "instance_weighted_mean_difference",
    "estimator.bootstrap.unit": "patient",
    "estimator.bootstrap.resamples": 10000,
    "cohort.mention_linked_instances.train": 1895,
    "cohort.mention_linked_instances.validation": 547,
    "cohort.mention_linked_instances.test": 987,
    "cohort.annotated_test_instances_before_linking": 1093,
    "cohort.test_patients": 398,
    "cohort.eligible_training_patients": 735,
    "record_substitution.eligible_instances": 948,
    "record_substitution.eligible_patients": 389,
    "record_substitution.matched_records_selected_per_seed": [8, 8, 8, 8, 8],
    "primary_inference.learned_minus_structured_3_0s.pointing.difference": 0.0353,
    "primary_inference.learned_minus_structured_3_0s.pointing.ci95": [0.0067, 0.0634],
    "primary_inference.learned_minus_structured_3_0s.iou.difference": 0.0035,
    "primary_inference.learned_minus_structured_3_0s.iou.ci95": [-0.0034, 0.0102],
    "record_substitution.target_minus_substitution.pointing.difference": 0.2816,
    "record_substitution.target_minus_substitution.pointing.ci95": [0.2473, 0.3159],
    "record_substitution.target_minus_substitution.iou.difference": 0.0769,
    "record_substitution.target_minus_substitution.iou.ci95": [0.0653, 0.0885],
    "table_4.completed_tasks": 25,
    "table_4.patient_subsample_chains": 5,
    "table_4.optimizer_seeds_per_chain": 5,
}

EXPECTED_TABLE_1 = [
    ("complete_scanpath_density", 0.4063, 0.2008),
    ("anatomical_prior", 0.5035, 0.2736),
    ("temporal_1_5s", 0.6211, 0.2773),
    ("prior_x_scanpath", 0.6717, 0.3056),
    ("prior_x_scanpath_directional", 0.7183, 0.3408),
    ("prior_x_scanpath_temporal", 0.7528, 0.3201),
    ("combined_structured_1_5s", 0.7923, 0.3439),
    ("combined_structured_3_0s", 0.7893, 0.3549),
    ("ten_indicator_learned_five_seed_mean", 0.8245, 0.3584),
]

EXPECTED_TABLE_2 = [
    (0.5, 0.3348, 0.7325, 0.3192),
    (1.0, 0.3528, 0.7761, 0.3345),
    (1.5, 0.3620, 0.7923, 0.3439),
    (2.0, 0.3695, 0.7984, 0.3492),
    (3.0, 0.3733, 0.7893, 0.3549),
]

EXPECTED_TABLE_3 = [
    ("ten_indicator_selector", 0.8245, 0.3584),
    ("four_indicator_selector", 0.8373, 0.3574),
    ("finding_temporal_kinematic_only", 0.7295, 0.3135),
    ("positional_features_permuted", 0.5534, 0.2306),
    ("temporal_kinematic_features_permuted", 0.6833, 0.2976),
    ("spatial_indicators_masked", 0.7495, 0.3068),
]

EXPECTED_TABLE_4 = [
    (0.10, 0.767740, 0.778120, 0.319076, 0.345680),
    (0.25, 0.802604, 0.790080, 0.335380, 0.351800),
    (0.50, 0.819048, 0.789480, 0.341512, 0.353480),
    (1.00, 0.824500, 0.789300, 0.358340, 0.354900),
]

EXPECTED_PARTITIONS = [
    (0, 987, 0.0352, 0.0035),
    (1, 1009, 0.0269, 0.0122),
    (2, 971, 0.0356, 0.0040),
    (3, 992, 0.0308, 0.0047),
    (4, 998, 0.0167, 0.0002),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def at(data: dict, dotted: str):
    value = data
    for part in dotted.split("."):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def require(condition: bool, message: str, failures: list[str]) -> int:
    if condition:
        return 1
    failures.append(message)
    return 0


def validate_registry(data: dict) -> tuple[int, list[str]]:
    failures: list[str] = []
    passed = 0
    for path, expected in EXPECTED.items():
        try:
            observed = at(data, path)
        except (KeyError, IndexError, TypeError) as exc:
            failures.append(f"missing {path}: {exc}")
            continue
        passed += require(observed == expected, f"{path}: {observed!r} != {expected!r}", failures)

    got = [(row["method"], row["pointing"], row["iou"]) for row in data.get("table_1", [])]
    passed += require(got == EXPECTED_TABLE_1, "Table I values changed", failures)

    got = [
        (row["lookback_seconds"], row["validation_iou"], row["test_pointing"], row["test_iou"])
        for row in data.get("table_2", [])
    ]
    passed += require(got == EXPECTED_TABLE_2, "Table II values changed", failures)
    if got:
        passed += require(max(got, key=lambda row: row[1])[0] == 3.0, "Validation no longer selects 3.0 s", failures)

    got = [(row["condition"], row["pointing"], row["iou"]) for row in data.get("table_3", [])]
    passed += require(got == EXPECTED_TABLE_3, "Table III values changed", failures)

    got = [
        (
            row["fraction"],
            row["learned_pointing"],
            row["structured_pointing"],
            row["learned_iou"],
            row["structured_iou"],
        )
        for row in data.get("table_4", {}).get("rows", [])
    ]
    passed += require(got == EXPECTED_TABLE_4, "Table IV values changed", failures)
    for row in data.get("table_4", {}).get("rows", []):
        passed += require(set(row["selected_lookbacks"]) == {3}, f"Unexpected lookback at {row['fraction']}", failures)

    got = [
        (row["partition"], row["test_instances"], row["delta_pointing"], row["delta_iou"])
        for row in data.get("patient_partitions", [])
    ]
    passed += require(got == EXPECTED_PARTITIONS, "Patient-partition values changed", failures)
    passed += require(
        all(row.get("optimizer_seeds") == 5 for row in data.get("patient_partitions", [])),
        "Every patient partition must use five optimizer seeds",
        failures,
    )
    passed += require("execution_" + "provenance" not in data, "Internal execution metadata is public", failures)
    return passed, failures


def validate_release_tree(results_path: Path) -> tuple[int, list[str]]:
    failures: list[str] = []
    passed = 0
    excluded = {".git", ".venv", "venv", "runs", "data", "checkpoints"}
    restricted_suffixes = {".pdf", ".tex", ".bib", ".dcm", ".dicom", ".pt", ".pth", ".pkl"}
    files = [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not excluded.intersection(path.relative_to(ROOT).parts)
    ]
    restricted = [str(path.relative_to(ROOT)) for path in files if path.suffix.lower() in restricted_suffixes]
    passed += require(not restricted, f"Restricted files are present: {restricted}", failures)

    blocked_parts = {"sub" + "mission", "revi" + "sion", "pri" + "vate", "prove" + "nance"}
    blocked_paths = [
        str(path.relative_to(ROOT))
        for path in files
        if blocked_parts.intersection(part.lower() for part in path.relative_to(ROOT).parts)
    ]
    passed += require(not blocked_paths, f"Internal paths are present: {blocked_paths}", failures)

    text_extensions = {"", ".md", ".json", ".toml", ".py", ".cff", ".yml", ".yaml", ".svg"}
    public_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in files
        if path.suffix.lower() in text_extensions or path.name == ".gitignore"
    )
    blocked_tokens = (
        "Team" + "Beaver",
        "hs" + "mail02",
        "/" + "home/",
        "/" + "mnt/",
    )
    for token in blocked_tokens:
        passed += require(token not in public_text, f"Public tree contains blocked token {token!r}", failures)

    manifest_path = ROOT / "assets" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    passed += require(
        manifest["source_sha256"] == sha256(results_path),
        "README assets were rendered from different results",
        failures,
    )
    expected_assets = {"paper_figure_1", "paper_figure_2", "results_overview"}
    passed += require(
        set(manifest.get("assets", {})) == expected_assets,
        "README asset manifest is incomplete",
        failures,
    )
    for name, entry in manifest.get("assets", {}).items():
        asset = ROOT / "assets" / entry["filename"]
        passed += require(asset.is_file(), f"README asset is missing: {name}", failures)
        if asset.is_file():
            passed += require(
                entry["sha256"] == sha256(asset),
                f"README asset checksum changed: {name}",
                failures,
            )
        asset_type_is_declared = (
            entry.get("data_free") is True
            or entry.get("publication_figure") is True
        )
        passed += require(
            asset_type_is_declared,
            f"README asset type is not declared: {name}",
            failures,
        )

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for token in (
        "987 mention-linked finding instances",
        "398 patients",
        "0.7893",
        "0.8245",
        "assets/paper_figure_1.png",
        "assets/paper_figure_2.png",
        "assets/results_overview.svg",
    ):
        passed += require(token in readme, f"README is missing {token!r}", failures)
    return passed, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    arguments = parser.parse_args()

    data = json.loads(arguments.results.read_text(encoding="utf-8"))
    passed, failures = validate_registry(data)
    tree_passed, tree_failures = validate_release_tree(arguments.results)
    passed += tree_passed
    failures.extend(tree_failures)

    if failures:
        print(f"FAIL: {len(failures)} assertion(s) failed after {passed} passes")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"PASS: {passed} result and release assertions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
