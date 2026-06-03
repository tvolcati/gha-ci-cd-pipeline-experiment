from __future__ import annotations

import argparse
import json
import statistics
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build summarized test metrics from JUnit XML.")
    parser.add_argument("--junitxml", required=True, help="Path to the JUnit XML file.")
    parser.add_argument("--output", required=True, help="Path to the output JSON file.")
    return parser.parse_args()


def parse_junit_metrics(junit_path: Path) -> dict:
    root = ET.fromstring(junit_path.read_text(encoding="utf-8"))
    testcases = root.findall(".//testcase")

    durations = [float(case.attrib.get("time", 0.0)) for case in testcases]
    failures = sum(1 for case in testcases if case.find("failure") is not None)
    errors = sum(1 for case in testcases if case.find("error") is not None)
    skipped = sum(1 for case in testcases if case.find("skipped") is not None)

    slowest = sorted(
        (
            {
                "name": case.attrib.get("name", "unknown"),
                "classname": case.attrib.get("classname", "unknown"),
                "duration_seconds": float(case.attrib.get("time", 0.0)),
            }
            for case in testcases
        ),
        key=lambda item: item["duration_seconds"],
        reverse=True,
    )[:5]

    return {
        "test_count": len(testcases),
        "test_failures": failures + errors,
        "test_skipped": skipped,
        "average_test_duration_seconds": statistics.fmean(durations) if durations else 0.0,
        "total_test_duration_seconds": sum(durations),
        "slowest_tests": slowest,
    }


def main() -> None:
    args = parse_args()
    junit_path = Path(args.junitxml)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    metrics = parse_junit_metrics(junit_path)
    output_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
