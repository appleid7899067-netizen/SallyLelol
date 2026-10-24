#!/bin/bash
set -e
BRAND_NAME="${1:-boss.slilelo}"
DRY_RUN=false
[[ "$2" == "--dry-run" ]] && DRY_RUN=true
FILES=("cowbase/README.md" "cowbase/CONTRIBUTING.md" "cowbase/config-template.json")
echo "🎨 Brand: $BRAND_NAME | Dry-run: $DRY_RUN"
if [ "$DRY_RUN" = true ]; then
    for f in "${FILES[@]}"; do
        [ -f "$f" ] && echo "📄 $f: $(grep -c 'CowAgent\|cowagent' "$f" 2>/dev/null || echo 0) matches"
    done
    exit 0
fi
for f in "${FILES[@]}"; do
    if [ -f "$f" ]; then
        sed -i "s/CowAgent/$BRAND_NAME/g; s/cowagent/$BRAND_NAME/g" "$f"
        echo "✅ $f"
    fi
done
echo "" >> knowledge/branding-change-log.md
echo "## $(date '+%Y-%m-%d %H:%M:%S')" >> knowledge/branding-change-log.md
echo "- Renamed to: $BRAND_NAME" >> knowledge/branding-change-log.md
echo "✅ Done!"
