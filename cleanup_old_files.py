"""
Cleanup Script - Remove OLD agent files

This script removes outdated agent files and keeps only the new architecture.

KEEP (New files):
✅ type_amount_extractor.py (Agent 1)
✅ urgency_analyzer.py (Agent 2)
✅ fraud_detector.py (Agent 3)
✅ router.py (Python Router)
✅ response_generator_hybrid.py (Agent 5)
✅ __init__.py

REMOVE (Old files):
❌ categorizer.py
❌ claim_type_classifier.py
❌ classifier.py
❌ fraud_risk_detector.py (old version)
❌ responder.py
❌ response_generator.py (old version)
❌ sentiment.py
❌ smart_router.py (old LLM router)
❌ urgency.py
❌ urgency_amount_analyzer.py
"""

import os
import shutil
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent / "agents"

# Files to KEEP
KEEP_FILES = {
    "type_amount_extractor.py",
    "urgency_analyzer.py",
    "fraud_detector.py",
    "router.py",
    "response_generator_hybrid.py",
    "__init__.py",
    "__pycache__"  # Keep cache folder
}

# Files to DELETE (explicitly listed for safety)
DELETE_FILES = {
    "categorizer.py",
    "claim_type_classifier.py",
    "classifier.py",
    "fraud_risk_detector.py",  # Old version with CrewAI
    "responder.py",
    "response_generator.py",  # Old version
    "sentiment.py",
    "smart_router.py",  # Old LLM router
    "urgency.py",
    "urgency_amount_analyzer.py"
}


def cleanup_agents_folder():
    """Remove old agent files"""
    
    print("=" * 70)
    print("🧹 CLEANUP: Removing old agent files")
    print("=" * 70)
    
    if not BASE_DIR.exists():
        print(f"❌ Error: Directory not found: {BASE_DIR}")
        return
    
    print(f"\n📁 Directory: {BASE_DIR}\n")
    
    # Get all files in agents folder
    all_files = [f for f in os.listdir(BASE_DIR) if os.path.isfile(BASE_DIR / f)]
    
    print(f"Found {len(all_files)} files total\n")
    
    deleted_count = 0
    kept_count = 0
    
    for file in all_files:
        if file in DELETE_FILES:
            file_path = BASE_DIR / file
            try:
                os.remove(file_path)
                print(f"  ❌ DELETED: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"  ⚠️  ERROR deleting {file}: {e}")
        
        elif file in KEEP_FILES:
            print(f"  ✅ KEPT:    {file}")
            kept_count += 1
        
        else:
            print(f"  ⚠️  UNKNOWN: {file} (not in KEEP or DELETE list)")
    
    print("\n" + "=" * 70)
    print(f"✅ Cleanup complete!")
    print(f"   Deleted: {deleted_count} files")
    print(f"   Kept:    {kept_count} files")
    print("=" * 70)
    
    # Show final directory contents
    print("\n📂 Final directory contents:")
    remaining_files = [f for f in os.listdir(BASE_DIR) if os.path.isfile(BASE_DIR / f)]
    for file in sorted(remaining_files):
        print(f"   - {file}")


if __name__ == "__main__":
    cleanup_agents_folder()
