#!/bin/bash
# Git cleanup script - removes old files from git tracking

echo "🧹 Removing old files from Git tracking..."
echo ""

# Remove old root files
echo "📄 Removing old root files..."
git rm --cached models.py 2>/dev/null && echo "  ✓ Removed models.py" || echo "  - models.py not in git"
git rm --cached config.py 2>/dev/null && echo "  ✓ Removed config.py" || echo "  - config.py not in git"
git rm --cached test_emails.txt 2>/dev/null && echo "  ✓ Removed test_emails.txt" || echo "  - test_emails.txt not in git"

# Remove old agent files
echo ""
echo "🤖 Removing old agent files..."
git rm --cached agents/categorizer.py 2>/dev/null && echo "  ✓ Removed categorizer.py" || echo "  - categorizer.py not in git"
git rm --cached agents/classifier.py 2>/dev/null && echo "  ✓ Removed classifier.py" || echo "  - classifier.py not in git"
git rm --cached agents/sentiment.py 2>/dev/null && echo "  ✓ Removed sentiment.py" || echo "  - sentiment.py not in git"
git rm --cached agents/urgency.py 2>/dev/null && echo "  ✓ Removed urgency.py" || echo "  - urgency.py not in git"
git rm --cached agents/router.py 2>/dev/null && echo "  ✓ Removed router.py" || echo "  - router.py not in git"
git rm --cached agents/responder.py 2>/dev/null && echo "  ✓ Removed responder.py" || echo "  - responder.py not in git"

echo ""
echo "✅ Git cleanup complete!"
echo ""
echo "📋 Git status:"
git status --short

echo ""
echo "🚀 Next steps:"
echo "  1. Review the changes above"
echo "  2. git add ."
echo "  3. git commit -m 'Complete insurance claims multi-agent system'"
echo "  4. git push origin main"
