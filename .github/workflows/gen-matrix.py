#!/usr/bin/env python3
"""Generate GitHub Actions build and merge matrices from images.json.

Reads images.json at the repository root and writes two compact-JSON lines
to stdout, suitable for appending to $GITHUB_OUTPUT:

    build_matrix  -- images x arches, for the build job
    merge_matrix  -- images only, for the manifest-merge job

Usage (in a workflow step):
    python3 .github/workflows/gen-matrix.py >> "$GITHUB_OUTPUT"

Usage (local testing):
    python3 .github/workflows/gen-matrix.py | python3 -m json.tool --no-indent
"""

import json
import pathlib

repo_root = pathlib.Path(__file__).parent.parent.parent
config = json.loads((repo_root / "images.json").read_text())

arches = config["arches"]
build_includes = []
merge_includes = []

for img in config["images"]:
    os_name = img["os"]
    for entry in img["entries"]:
        merge_includes.append({
            "os": os_name,
            "version": entry["version"],
        })
        for arch in arches:
            build_includes.append({
                "os": os_name,
                "version": entry["version"],
                "context": entry["context"],
                "file": entry["file"],
                "platform": arch["platform"],
                "platform_pair": arch["platform"].replace("/", "-"),
                "runner": arch["runner"],
            })

print(f"build_matrix={json.dumps({'include': build_includes})}")
print(f"merge_matrix={json.dumps({'include': merge_includes})}")
