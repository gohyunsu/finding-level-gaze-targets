#!/usr/bin/env python3
"""Render the aggregate result figure and verify all README figure assets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "study-results.json"
ASSETS = ROOT / "assets"
PAPER_FIGURE_1 = ASSETS / "paper_figure_1.png"
PAPER_FIGURE_2 = ASSETS / "paper_figure_2.png"
SUMMARY = ASSETS / "results_overview.svg"
MANIFEST = ASSETS / "manifest.json"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def render_results(data: dict) -> str:
    table = {row["method"]: row for row in data["table_1"]}
    structured = table["combined_structured_3_0s"]
    learned = table["ten_indicator_learned_five_seed_mean"]
    inference = data["primary_inference"]["learned_minus_structured_3_0s"]
    substitution = data["record_substitution"]["target_minus_substitution"]

    partition_rows = []
    for index, row in enumerate(data["patient_partitions"]):
        y = 198 + index * 48
        x = 1100 + row["delta_pointing"] / 0.04 * 135
        partition_rows.append(
            f'''  <text x="1063" y="{y + 5}" class="small">{index}</text>
  <line x1="1100" y1="{y}" x2="1240" y2="{y}" class="track"/>
  <circle cx="{x:.1f}" cy="{y}" r="7" fill="#287da3"/>
  <text x="1320" y="{y + 5}" text-anchor="end" class="small">+{row['delta_pointing'] * 100:.2f} pp</text>'''
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="560" viewBox="0 0 1400 560" role="img" aria-labelledby="title desc">
  <title id="title">Finding-level gaze target results</title>
  <desc id="desc">Primary structured and learned localization results, paired inference, matched-record substitution, and patient-partition sensitivity.</desc>
  <defs>
    <style>
      .eyebrow {{ font: 700 13px Arial, Helvetica, sans-serif; letter-spacing: 1.6px; fill: #2f6f8f; }}
      .heading {{ font: 700 25px Arial, Helvetica, sans-serif; fill: #172230; }}
      .section {{ font: 700 19px Arial, Helvetica, sans-serif; fill: #172230; }}
      .value {{ font: 700 34px Arial, Helvetica, sans-serif; fill: #216b8f; }}
      .label {{ font: 16px Arial, Helvetica, sans-serif; fill: #405165; }}
      .small {{ font: 14px Arial, Helvetica, sans-serif; fill: #66778a; }}
      .micro {{ font: 12px Arial, Helvetica, sans-serif; fill: #7b8999; }}
      .card {{ fill: #ffffff; stroke: #d7e0e8; stroke-width: 1.5; }}
      .track {{ stroke: #e5eaf0; stroke-width: 7; stroke-linecap: round; }}
      .structured {{ fill: #a9b7c4; }}
      .learned {{ fill: #287da3; }}
      .rule {{ stroke: #e2e7ec; stroke-width: 1.5; }}
    </style>
  </defs>
  <rect width="1400" height="560" rx="22" fill="#f6f8fb"/>
  <text x="48" y="43" class="eyebrow">REFERENCE STUDY</text>
  <text x="48" y="76" class="heading">Evidence at a glance</text>
  <text x="1352" y="70" text-anchor="end" class="small">987 instances · 398 patients · five optimizer seeds</text>

  <rect x="40" y="100" width="580" height="400" rx="17" class="card"/>
  <text x="70" y="139" class="section">Primary localization</text>
  <text x="70" y="167" class="small">Common renderer, patient split, and validation protocol</text>

  <text x="70" y="211" class="label">Pointing-game accuracy</text>
  <rect x="70" y="232" width="480" height="22" rx="6" fill="#eef2f5"/>
  <rect x="70" y="232" width="{structured['pointing'] * 480:.1f}" height="22" rx="6" class="structured"/>
  <rect x="70" y="270" width="480" height="22" rx="6" fill="#eef2f5"/>
  <rect x="70" y="270" width="{learned['pointing'] * 480:.1f}" height="22" rx="6" class="learned"/>
  <text x="82" y="248" class="small" style="fill:#263849;font-weight:600">Structured · 3.0 s</text>
  <text x="82" y="286" class="small" style="fill:#ffffff;font-weight:600">Learned · five-seed mean</text>
  <text x="565" y="248" text-anchor="end" class="label">{structured['pointing']:.4f}</text>
  <text x="565" y="286" text-anchor="end" class="label">{learned['pointing']:.4f}</text>

  <line x1="70" y1="321" x2="590" y2="321" class="rule"/>
  <text x="70" y="358" class="label">IoU</text>
  <rect x="70" y="378" width="480" height="18" rx="5" fill="#eef2f5"/>
  <rect x="70" y="378" width="{structured['iou'] * 480:.1f}" height="18" rx="5" class="structured"/>
  <rect x="70" y="411" width="480" height="18" rx="5" fill="#eef2f5"/>
  <rect x="70" y="411" width="{learned['iou'] * 480:.1f}" height="18" rx="5" class="learned"/>
  <text x="565" y="393" text-anchor="end" class="label">{structured['iou']:.4f}</text>
  <text x="565" y="426" text-anchor="end" class="label">{learned['iou']:.4f}</text>
  <text x="70" y="465" class="small">Peak localization improves; thresholded overlap remains similar.</text>

  <rect x="650" y="100" width="350" height="190" rx="17" class="card"/>
  <text x="678" y="136" class="eyebrow">PAIRED INFERENCE</text>
  <text x="678" y="183" class="value">+{inference['pointing']['difference'] * 100:.2f} pp</text>
  <text x="678" y="211" class="label">pointing-accuracy difference</text>
  <line x1="678" y1="231" x2="972" y2="231" class="rule"/>
  <text x="678" y="260" class="small">95% CI {inference['pointing']['ci95'][0] * 100:.2f} to {inference['pointing']['ci95'][1] * 100:.2f} pp</text>

  <rect x="650" y="310" width="350" height="190" rx="17" class="card"/>
  <text x="678" y="346" class="eyebrow">RECORD SUBSTITUTION</text>
  <text x="678" y="393" class="value">−{substitution['pointing']['difference'] * 100:.2f} pp</text>
  <text x="678" y="421" class="label">with matched other-patient records</text>
  <line x1="678" y1="441" x2="972" y2="441" class="rule"/>
  <text x="678" y="470" class="small">IoU reduction {substitution['iou']['difference'] * 100:.2f} pp · n={data['record_substitution']['eligible_instances']}</text>

  <rect x="1030" y="100" width="330" height="400" rx="17" class="card"/>
  <text x="1058" y="139" class="section">Patient partitions</text>
  <text x="1058" y="166" class="small">Learned − structured pointing</text>
{chr(10).join(partition_rows)}
  <text x="1100" y="454" class="micro">0</text>
  <text x="1240" y="454" text-anchor="end" class="micro">+4 pp</text>
  <line x1="1058" y1="471" x2="1332" y2="471" class="rule"/>
  <text x="1058" y="488" class="micro">Each partition repeats the five-seed pipeline.</text>

  <text x="700" y="536" text-anchor="middle" class="small">Patient-cluster bootstrap · 10,000 resamples · complete-precision values in results/study-results.json</text>
</svg>
'''


def expected_manifest(summary_svg: str) -> dict:
    return {
        "schema_version": "1.0",
        "source": "results/study-results.json",
        "source_sha256": sha256(RESULTS),
        "assets": {
            "paper_figure_1": {
                "filename": PAPER_FIGURE_1.name,
                "sha256": sha256(PAPER_FIGURE_1),
                "publication_figure": True,
            },
            "paper_figure_2": {
                "filename": PAPER_FIGURE_2.name,
                "sha256": sha256(PAPER_FIGURE_2),
                "publication_figure": True,
            },
            "results_overview": {
                "filename": SUMMARY.name,
                "sha256": sha256_bytes(summary_svg.encode("utf-8")),
                "data_free": True,
            },
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()

    data = json.loads(RESULTS.read_text(encoding="utf-8"))
    summary_svg = render_results(data)
    manifest = expected_manifest(summary_svg)
    if arguments.check:
        observed_manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if SUMMARY.read_text(encoding="utf-8") != summary_svg or observed_manifest != manifest:
            raise SystemExit(
                "README assets are out of date; run scripts/render_readme_assets.py"
            )
        print("README assets: current")
        return 0

    SUMMARY.write_text(summary_svg, encoding="utf-8")
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"registered {PAPER_FIGURE_1.relative_to(ROOT)}")
    print(f"registered {PAPER_FIGURE_2.relative_to(ROOT)}")
    print(f"wrote {SUMMARY.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
