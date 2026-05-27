#!/usr/bin/env python3
"""
validate_manifests.py — validate the Claude Code plugin manifests.

Checks:
  1. .claude-plugin/plugin.json exists, parses, has required fields.
  2. .claude-plugin/marketplace.json exists, parses, has required fields.
  3. plugin.json.version matches the VERSION file at repo root.
  4. plugin.json.name matches the skill directory name under skills/.
  5. marketplace.json.plugins[].name matches plugin.json.name.

Run from repo root:
  python3 .github/scripts/validate_manifests.py

Exit codes:
  0  all checks pass
  1  one or more failures (printed)
"""

import json
import sys
from pathlib import Path

PLUGIN_MANIFEST = Path(".claude-plugin/plugin.json")
MARKETPLACE_MANIFEST = Path(".claude-plugin/marketplace.json")
VERSION_FILE = Path("VERSION")
SKILLS_DIR = Path("skills")

REQUIRED_PLUGIN_FIELDS = {"name", "description"}
REQUIRED_MARKETPLACE_FIELDS = {"name", "plugins"}


def fail(errors, msg):
    errors.append(msg)


def main() -> int:
    errors = []

    # Plugin manifest
    if not PLUGIN_MANIFEST.exists():
        fail(errors, f"missing {PLUGIN_MANIFEST}")
        return _report(errors)

    try:
        plugin = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(errors, f"{PLUGIN_MANIFEST} is not valid JSON: {e}")
        return _report(errors)

    missing = REQUIRED_PLUGIN_FIELDS - plugin.keys()
    if missing:
        fail(errors, f"{PLUGIN_MANIFEST} missing required field(s): {sorted(missing)}")

    plugin_name = plugin.get("name")
    plugin_version = plugin.get("version")

    # Marketplace manifest
    if not MARKETPLACE_MANIFEST.exists():
        fail(errors, f"missing {MARKETPLACE_MANIFEST}")
    else:
        try:
            mkt = json.loads(MARKETPLACE_MANIFEST.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            fail(errors, f"{MARKETPLACE_MANIFEST} is not valid JSON: {e}")
        else:
            missing = REQUIRED_MARKETPLACE_FIELDS - mkt.keys()
            if missing:
                fail(errors, f"{MARKETPLACE_MANIFEST} missing required field(s): {sorted(missing)}")
            else:
                plugins = mkt.get("plugins", [])
                if not isinstance(plugins, list) or not plugins:
                    fail(errors, f"{MARKETPLACE_MANIFEST}.plugins must be a non-empty array")
                else:
                    plugin_names_in_mkt = [p.get("name") for p in plugins]
                    if plugin_name and plugin_name not in plugin_names_in_mkt:
                        fail(errors,
                             f"plugin.json.name='{plugin_name}' not listed in "
                             f"marketplace.json.plugins (got {plugin_names_in_mkt})")

    # VERSION file consistency
    if not VERSION_FILE.exists():
        fail(errors, f"missing {VERSION_FILE}")
    elif plugin_version:
        version_file_content = VERSION_FILE.read_text(encoding="utf-8").strip()
        if version_file_content != plugin_version:
            fail(errors,
                 f"VERSION file ({version_file_content!r}) does not match "
                 f"plugin.json.version ({plugin_version!r})")

    # Skill directory exists
    if plugin_name:
        skill_path = SKILLS_DIR / plugin_name
        if not skill_path.exists():
            fail(errors, f"plugin.json.name='{plugin_name}' but {skill_path}/ does not exist")
        else:
            skill_md = skill_path / "SKILL.md"
            if not skill_md.exists():
                fail(errors, f"{skill_md} not found (every plugin skill needs a SKILL.md)")

    return _report(errors)


def _report(errors):
    if errors:
        print(f"FAIL: {len(errors)} manifest issue(s)\n")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK: plugin.json + marketplace.json + VERSION + skill dir all consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
