"""
Cleanup Script - Remove Development Artifacts

This script removes old/deprecated files from the project.
Run this BEFORE pushing to GitHub for final submission.
"""

import os
import shutil
from pathlib import Path

# Get script directory (project root)
PROJECT_ROOT = Path(__file__).parent

# Files to delete
FILES_TO_DELETE = [
    "config.py",                              # Old version
    "crew_setup.py",                          # Old CrewAI version
    "CLEANUP_GUIDE.md",                       # Dev notes
    "DEPLOYMENT.md",                          # Duplicate of README
    "GIT_PUSH_INSTRUCTIONS.md",               # Git howto
    "MIGRATION_SUMMARY.md",                   # Migration log
    "PYDANTIC_INTEGRATION_COMPLETE.md",       # Dev log
    "QUICKSTART.md",                          # Duplicate of README
    "cleanup_old_files.py",                   # Old cleanup script
    "git_cleanup.bat",                        # Git script
    "git_cleanup.sh",                         # Git script
    "test_emails.txt",                        # Old test file
]

# Directories to delete (optional)
DIRS_TO_DELETE = [
    "docs",  # Architecture docs (optional - uncomment to keep)
]

def main():
    print("=" * 70)
    print("🧹 PROJECT CLEANUP - Remove Development Artifacts")
    print("=" * 70)
    print()
    
    deleted_files = []
    deleted_dirs = []
    not_found = []
    
    # Delete files
    print("📄 Deleting files...")
    for filename in FILES_TO_DELETE:
        filepath = PROJECT_ROOT / filename
        if filepath.exists():
            try:
                filepath.unlink()
                deleted_files.append(filename)
                print(f"  ✅ Deleted: {filename}")
            except Exception as e:
                print(f"  ❌ Error deleting {filename}: {e}")
        else:
            not_found.append(filename)
            print(f"  ⚠️  Not found: {filename}")
    
    print()
    
    # Delete directories
    print("📁 Deleting directories...")
    for dirname in DIRS_TO_DELETE:
        dirpath = PROJECT_ROOT / dirname
        if dirpath.exists():
            try:
                shutil.rmtree(dirpath)
                deleted_dirs.append(dirname)
                print(f"  ✅ Deleted: {dirname}/")
            except Exception as e:
                print(f"  ❌ Error deleting {dirname}: {e}")
        else:
            print(f"  ⚠️  Not found: {dirname}/")
    
    print()
    print("=" * 70)
    print("📊 CLEANUP SUMMARY")
    print("=" * 70)
    print(f"✅ Files deleted: {len(deleted_files)}")
    print(f"✅ Directories deleted: {len(deleted_dirs)}")
    print(f"⚠️  Not found: {len(not_found)}")
    print()
    
    if deleted_files or deleted_dirs:
        print("🎉 Cleanup complete! Your project is now production-ready.")
        print()
        print("📌 NEXT STEPS:")
        print("   1. Run app to verify everything still works:")
        print("      python -m streamlit run app.py")
        print()
        print("   2. If all works, commit & push to GitHub:")
        print("      git add -A")
        print("      git commit -m 'Cleanup: Remove development artifacts'")
        print("      git push origin main")
    else:
        print("ℹ️  No files were deleted (all already clean or not found)")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
