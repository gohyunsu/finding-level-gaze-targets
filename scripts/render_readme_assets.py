#!/usr/bin/env python3
"""Render and verify the public README figures."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "study-results.json"
ASSETS = ROOT / "assets"
METHOD = ASSETS / "method_overview.svg"
SUMMARY = ASSETS / "results_overview.svg"
MANIFEST = ASSETS / "manifest.json"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def render_method() -> str:
    """Return a data-free graphical abstract of the released pipeline."""
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="650" viewBox="0 0 1400 650" role="img" aria-labelledby="title desc">
  <title id="title">Finding-level gaze target construction</title>
  <desc id="desc">A complete chest-radiograph scanpath and a resolved finding mention enter a structured or learned selector. Finding-conditioned fixation weights pass through a shared renderer to produce a separate target for each finding.</desc>
  <defs>
    <style>
      .eyebrow { font: 700 13px Arial, Helvetica, sans-serif; letter-spacing: 1.8px; fill: #2f6f8f; }
      .title { font: 700 27px Arial, Helvetica, sans-serif; fill: #172230; }
      .section { font: 700 19px Arial, Helvetica, sans-serif; fill: #172230; }
      .body { font: 16px Arial, Helvetica, sans-serif; fill: #465668; }
      .small { font: 14px Arial, Helvetica, sans-serif; fill: #68788a; }
      .micro { font: 12px Arial, Helvetica, sans-serif; fill: #718093; }
      .card { fill: #ffffff; stroke: #d7e0e8; stroke-width: 1.5; }
      .soft { fill: #edf5f8; }
      .line { fill: none; stroke: #a8b8c6; stroke-width: 2; }
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7f96a8"/>
    </marker>
    <radialGradient id="heat-a">
      <stop offset="0" stop-color="#e6553b" stop-opacity="0.94"/>
      <stop offset="0.38" stop-color="#f4a340" stop-opacity="0.72"/>
      <stop offset="1" stop-color="#f9d976" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="heat-b">
      <stop offset="0" stop-color="#d9473f" stop-opacity="0.94"/>
      <stop offset="0.4" stop-color="#f08b3e" stop-opacity="0.68"/>
      <stop offset="1" stop-color="#f8d76b" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="1400" height="650" rx="22" fill="#f6f8fb"/>
  <text x="52" y="45" class="eyebrow">GRAPHICAL ABSTRACT</text>
  <text x="52" y="78" class="title">One complete reading → a separate gaze target for each reported finding</text>

  <rect x="40" y="108" width="390" height="480" rx="18" class="card"/>
  <circle cx="76" cy="145" r="17" fill="#dbeaf1"/>
  <text x="76" y="151" text-anchor="middle" class="section" fill="#216b8f">1</text>
  <text x="105" y="151" class="section">Complete reading</text>
  <text x="72" y="181" class="small">A shared scanpath accompanies several findings.</text>

  <rect x="72" y="205" width="326" height="267" rx="13" fill="#16212e"/>
  <path d="M235 232 C203 235 173 270 166 326 C160 382 179 428 225 445 C239 450 247 441 247 421 L247 264 C247 244 245 233 235 232Z" fill="#526273" opacity="0.82"/>
  <path d="M265 232 C297 235 327 270 334 326 C340 382 321 428 275 445 C261 450 253 441 253 421 L253 264 C253 244 255 233 265 232Z" fill="#526273" opacity="0.82"/>
  <path d="M250 248 L250 433" stroke="#8091a2" stroke-width="5" opacity="0.65"/>
  <path d="M176 286 Q250 254 324 286 M169 322 Q250 287 331 322 M168 360 Q250 326 332 360 M174 399 Q250 365 326 399" fill="none" stroke="#8394a5" stroke-width="2" opacity="0.4"/>
  <polyline points="212,287 279,322 194,365 302,392 266,270 226,417" fill="none" stroke="#75d0e8" stroke-width="3" opacity="0.82"/>
  <circle cx="212" cy="287" r="8" fill="#e36b54"/><circle cx="279" cy="322" r="6" fill="#f2b24c"/>
  <circle cx="194" cy="365" r="10" fill="#e36b54"/><circle cx="302" cy="392" r="7" fill="#f2b24c"/>
  <circle cx="266" cy="270" r="5" fill="#75d0e8"/><circle cx="226" cy="417" r="8" fill="#75d0e8"/>
  <rect x="84" y="218" width="105" height="25" rx="12" fill="#223344"/>
  <text x="137" y="235" text-anchor="middle" class="micro" style="fill:#dbe8ef">scanpath</text>

  <rect x="72" y="493" width="326" height="64" rx="11" class="soft"/>
  <text x="90" y="519" class="small">Resolved positive mentions</text>
  <rect x="90" y="530" width="122" height="19" rx="9" fill="#cfe6ee"/><text x="151" y="544" text-anchor="middle" class="micro" fill="#205b76">pleural finding</text>
  <rect x="220" y="530" width="105" height="19" rx="9" fill="#f3ddd7"/><text x="272" y="544" text-anchor="middle" class="micro" fill="#914534">nodule / mass</text>

  <path d="M442 345 L488 345" class="line" marker-end="url(#arrow)"/>

  <rect x="505" y="108" width="390" height="480" rx="18" class="card"/>
  <circle cx="541" cy="145" r="17" fill="#dbeaf1"/>
  <text x="541" y="151" text-anchor="middle" class="section" fill="#216b8f">2</text>
  <text x="570" y="151" class="section">Condition the selector</text>
  <text x="537" y="181" class="small">The target finding changes the weight of each fixation.</text>

  <rect x="537" y="210" width="326" height="56" rx="12" fill="#172a3a"/>
  <text x="557" y="233" class="micro" style="fill:#9fc5d7">TARGET FINDING</text>
  <text x="557" y="254" class="body" style="fill:#ffffff">Finding identity + mention indicators</text>

  <rect x="537" y="287" width="326" height="102" rx="13" fill="#edf5f8" stroke="#c9dee7"/>
  <text x="559" y="315" class="section" fill="#205f7e">Structured cues</text>
  <text x="559" y="342" class="small">anatomical prior · scanpath support</text>
  <text x="559" y="365" class="small">temporal gate · directional terms</text>

  <text x="700" y="416" text-anchor="middle" class="eyebrow">OR</text>

  <rect x="537" y="438" width="326" height="102" rx="13" fill="#f7eee9" stroke="#ead1c8"/>
  <text x="559" y="466" class="section" fill="#9a4c39">Learned reweighting</text>
  <text x="559" y="493" class="small">single attention layer over fixation features</text>
  <text x="559" y="516" class="small">validation-calibrated, five optimizer seeds</text>

  <path d="M907 345 L953 345" class="line" marker-end="url(#arrow)"/>

  <rect x="970" y="108" width="390" height="480" rx="18" class="card"/>
  <circle cx="1006" cy="145" r="17" fill="#dbeaf1"/>
  <text x="1006" y="151" text-anchor="middle" class="section" fill="#216b8f">3</text>
  <text x="1035" y="151" class="section">Render finding-level targets</text>
  <text x="1002" y="181" class="small">The same renderer turns weighted fixations into maps.</text>

  <rect x="1002" y="210" width="145" height="262" rx="13" fill="#172331"/>
  <path d="M1070 236 C1034 244 1020 293 1028 361 C1033 407 1046 440 1074 449 C1080 451 1083 443 1083 428 L1083 260 C1083 245 1078 235 1070 236Z" fill="#566778"/>
  <path d="M1092 236 C1126 244 1139 293 1132 361 C1127 407 1116 440 1092 449 C1087 451 1085 443 1085 428 L1085 260 C1085 245 1087 235 1092 236Z" fill="#566778"/>
  <ellipse cx="1048" cy="303" rx="66" ry="78" fill="url(#heat-a)"/>
  <circle cx="1048" cy="303" r="5" fill="#fff" stroke="#d6503e" stroke-width="3"/>
  <text x="1075" y="496" text-anchor="middle" class="small">pleural finding</text>

  <rect x="1183" y="210" width="145" height="262" rx="13" fill="#172331"/>
  <path d="M1251 236 C1215 244 1201 293 1209 361 C1214 407 1227 440 1255 449 C1261 451 1264 443 1264 428 L1264 260 C1264 245 1259 235 1251 236Z" fill="#566778"/>
  <path d="M1273 236 C1307 244 1320 293 1313 361 C1308 407 1297 440 1273 449 C1268 451 1266 443 1266 428 L1266 260 C1266 245 1268 235 1273 236Z" fill="#566778"/>
  <ellipse cx="1290" cy="360" rx="46" ry="54" fill="url(#heat-b)"/>
  <circle cx="1290" cy="360" r="5" fill="#fff" stroke="#d6503e" stroke-width="3"/>
  <text x="1255" y="496" text-anchor="middle" class="small">nodule / mass</text>

  <rect x="1002" y="522" width="326" height="35" rx="17" fill="#edf5f8"/>
  <text x="1165" y="545" text-anchor="middle" class="small" fill="#205f7e">shared 64×64 renderer + validation calibration</text>

  <text x="700" y="624" text-anchor="middle" class="small">Selector inputs exclude radiograph pixels · diagram uses synthetic, data-free anatomy</text>
</svg>
'''


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


def expected_manifest(method_svg: str, summary_svg: str) -> dict:
    return {
        "schema_version": "1.0",
        "source": "results/study-results.json",
        "source_sha256": sha256(RESULTS),
        "assets": {
            "method_overview": {
                "filename": METHOD.name,
                "sha256": sha256_bytes(method_svg.encode("utf-8")),
                "data_free": True,
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
    method_svg = render_method()
    summary_svg = render_results(data)
    manifest = expected_manifest(method_svg, summary_svg)
    if arguments.check:
        observed_manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        current = (
            METHOD.read_text(encoding="utf-8") == method_svg
            and SUMMARY.read_text(encoding="utf-8") == summary_svg
            and observed_manifest == manifest
        )
        if not current:
            raise SystemExit(
                "README assets are out of date; run scripts/render_readme_assets.py"
            )
        print("README assets: current")
        return 0

    ASSETS.mkdir(parents=True, exist_ok=True)
    METHOD.write_text(method_svg, encoding="utf-8")
    SUMMARY.write_text(summary_svg, encoding="utf-8")
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {METHOD.relative_to(ROOT)}")
    print(f"wrote {SUMMARY.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
