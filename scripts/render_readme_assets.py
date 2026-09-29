#!/usr/bin/env python3
"""Render the README result overview from the released result registry."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "study-results.json"
ASSETS = ROOT / "assets"
SUMMARY = ASSETS / "results_overview.svg"
MANIFEST = ASSETS / "manifest.json"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def render(data: dict) -> str:
    table = {row["method"]: row for row in data["table_1"]}
    structured = table["combined_structured_3_0s"]
    learned = table["ten_indicator_learned_five_seed_mean"]
    inference = data["primary_inference"]["learned_minus_structured_3_0s"]
    substitution = data["record_substitution"]["target_minus_substitution"]
    partition_delta = [row["delta_pointing"] for row in data["patient_partitions"]]

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="420" viewBox="0 0 1200 420" role="img" aria-labelledby="title desc">
  <title id="title">Finding-level gaze target results</title>
  <desc id="desc">Primary structured and learned localization results, paired inference, and record-dependence control.</desc>
  <defs>
    <style>
      .heading {{ font: 600 25px Arial, Helvetica, sans-serif; fill: #1d2733; }}
      .value {{ font: 700 36px Arial, Helvetica, sans-serif; fill: #155f8f; }}
      .label {{ font: 18px Arial, Helvetica, sans-serif; fill: #354252; }}
      .small {{ font: 15px Arial, Helvetica, sans-serif; fill: #667383; }}
      .card {{ fill: #ffffff; stroke: #cbd3dc; stroke-width: 1.5; }}
      .rule {{ stroke: #dbe1e7; stroke-width: 1.5; }}
      .structured {{ fill: #a7b3bf; }}
      .learned {{ fill: #2b79a8; }}
    </style>
  </defs>
  <rect width="1200" height="420" rx="14" fill="#f4f7f9"/>
  <text x="52" y="51" class="heading">Results at a glance</text>
  <text x="1148" y="50" text-anchor="end" class="small">987 instances · 398 patients · five optimizer seeds</text>

  <rect x="42" y="78" width="350" height="292" rx="11" class="card"/>
  <text x="70" y="116" class="heading">Primary comparison</text>
  <text x="70" y="154" class="small">Pointing-game accuracy</text>
  <rect x="70" y="172" width="{structured['pointing'] * 280:.1f}" height="22" rx="4" class="structured"/>
  <rect x="70" y="207" width="{learned['pointing'] * 280:.1f}" height="22" rx="4" class="learned"/>
  <text x="360" y="189" text-anchor="end" class="label">{structured['pointing']:.3f}</text>
  <text x="360" y="224" text-anchor="end" class="label">{learned['pointing']:.3f}</text>
  <text x="70" y="190" class="small">Structured</text>
  <text x="70" y="225" class="small" fill="#ffffff">Learned</text>
  <line x1="70" y1="252" x2="364" y2="252" class="rule"/>
  <text x="70" y="283" class="small">IoU: {structured['iou']:.3f} → {learned['iou']:.3f}</text>
  <text x="70" y="316" class="small">Shared renderer and calibration protocol</text>

  <rect x="425" y="78" width="350" height="292" rx="11" class="card"/>
  <text x="453" y="116" class="heading">Paired inference</text>
  <text x="453" y="169" class="value">+{inference['pointing']['difference'] * 100:.2f} pp</text>
  <text x="453" y="202" class="label">Peak-localization gain</text>
  <line x1="453" y1="226" x2="747" y2="226" class="rule"/>
  <text x="453" y="258" class="small">95% CI: {inference['pointing']['ci95'][0] * 100:.2f} to {inference['pointing']['ci95'][1] * 100:.2f} pp</text>
  <text x="453" y="290" class="small">IoU difference: +{inference['iou']['difference'] * 100:.2f} pp</text>
  <text x="453" y="322" class="small">Patient-cluster bootstrap, 10,000 resamples</text>

  <rect x="808" y="78" width="350" height="292" rx="11" class="card"/>
  <text x="836" y="116" class="heading">Record dependence</text>
  <text x="836" y="169" class="value">−{substitution['pointing']['difference'] * 100:.2f} pp</text>
  <text x="836" y="202" class="label">With matched other-patient records</text>
  <line x1="836" y1="226" x2="1130" y2="226" class="rule"/>
  <text x="836" y="258" class="small">IoU reduction: {substitution['iou']['difference'] * 100:.2f} pp</text>
  <text x="836" y="290" class="small">Eligible cohort: {data['record_substitution']['eligible_instances']} instances</text>
  <text x="836" y="322" class="small">Partition PG gains: {min(partition_delta) * 100:.2f}–{max(partition_delta) * 100:.2f} pp</text>
</svg>
'''


def expected_manifest(svg: str) -> dict:
    return {
        "source": "results/study-results.json",
        "source_sha256": sha256(RESULTS),
        "summary": {
            "filename": SUMMARY.name,
            "sha256": sha256_bytes(svg.encode("utf-8")),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()

    data = json.loads(RESULTS.read_text(encoding="utf-8"))
    svg = render(data)
    manifest = expected_manifest(svg)
    if arguments.check:
        observed_manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if SUMMARY.read_text(encoding="utf-8") != svg or observed_manifest != manifest:
            raise SystemExit("README assets are out of date; run scripts/render_readme_assets.py")
        print("README assets: current")
        return 0

    ASSETS.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(svg, encoding="utf-8")
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {SUMMARY.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
