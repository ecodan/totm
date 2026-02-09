#!/usr/bin/env python3
import shutil
import os
from pathlib import Path

"""
Cicadas Migration Script
-----------------------
This script syncs the Cicadas methodology tools and documentation from the 
sibling 'cicadas' project to this project. 

Use this to keep your test project updated with the latest Cicadas changes.
"""

def migrate():
    # Paths are relative to this script at the root of the project
    totm_root = Path(__file__).parent.absolute()
    cicadas_root = totm_root.parent / "cicadas"
    
    if not cicadas_root.exists():
        print(f"Error: Upstream cicadas project not found at {cicadas_root}")
        return

    print(f"Migrating Cicadas files from {cicadas_root} to {totm_root}...")

    # 1. Sync scripts/chorus
    src_scripts = cicadas_root / "scripts" / "chorus"
    dest_scripts = totm_root / "scripts" / "chorus"
    
    if src_scripts.exists():
        if dest_scripts.exists():
            shutil.rmtree(dest_scripts)
        shutil.copytree(src_scripts, dest_scripts)
        print(f"✅ Synced scripts/chorus")
    else:
        print(f"⚠️  Source scripts/chorus not found")

    # 2. copy HOW-TO.md
    shutil.copyfile(cicadas_root / "HOW-TO.md", totm_root / "HOW-TO.md")
    print(f"✅ Copied HOW-TO.md")


    print("\nMigration complete. Run 'python scripts/chorus/scripts/status.py' to verify.")

if __name__ == "__main__":
    migrate()
