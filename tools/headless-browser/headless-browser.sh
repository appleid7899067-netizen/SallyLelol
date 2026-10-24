#!/data/data/com.termux/files/usr/bin/bash
# headless-browser.sh — Chromium headless wrapper สำหรับ Termux (aarch64)
#
# ใช้แทน Playwright ที่โหลด binary ของตัวเองไม่ได้บน Termux
# เรียก Chromium ที่ติดตั้งผ่าน x11-repo โดยตรง
#
# Usage:
#   headless-browser.sh dom <URL>            # dump DOM (rendered HTML) ไป stdout
#   headless-browser.sh text <URL>           # ดึงข้อความล้วนจากหน้าเว็บ
#   headless-browser.sh shot <URL> <OUT.png> # ถ่าย screenshot (full page)
#   headless-browser.sh shot <URL> <OUT.png> --viewport   # เฉพาะ viewport
#   headless-browser.sh pdf <URL> <OUT.pdf>  # พิมพ์หน้าออกเป็น PDF
#   headless-browser.sh check                     # ตรวจว่า Chromium พร้อมใช้ไหม
#
# Env override:
#   CHROME_BIN   path ของ chromium-browser (default: หาใน PATH)
#   BROWSER_WAIT extra wait ms (default 0)

set -euo pipefail

CHROME_BIN="${CHROME_BIN:-$(command -v chromium-browser || true)}"
WAIT_MS="${BROWSER_WAIT:-0}"

# flags มาตรฐานสำหรับ Termux/Android (โปรอททักษะที่ทดสอบผ่านจริง)
COMMON_FLAGS=(
  --headless=new
  --no-sandbox
  --disable-gpu
  --disable-dev-shm-usage
  --disable-software-rasterizer
  --no-first-run
  --no-default-browser-check
  --hide-scrollbars
  --window-size=1280,800
)

die() { echo "❌ $*" >&2; exit 1; }

require_chrome() {
  [ -n "$CHROME_BIN" ] && [ -x "$CHROME_BIN" ] \
    || die "ไม่พบ Chromium — ตั้ง CHROME_BIN หรือติดตั้งด้วย: pkg install x11-repo && pkg install chromium"
}

# temp user-data-dir กัน profile ค้าง/ล็อก
make_profile() {
  local d
  d="$(mktemp -d "${TMPDIR:-/tmp}/hb-XXXXXX")"
  echo "$d"
}

cmd="${1:-}"; shift || true

case "$cmd" in
  check)
    require_chrome
    ver="$("$CHROME_BIN" --version 2>/dev/null || echo unknown)"
    echo "✅ Chromium: $ver"
    echo "   path: $CHROME_BIN"
    ;;

  dom)
    url="${1:?ต้องระบุ URL}"
    require_chrome
    prof="$(make_profile)"; trap 'rm -rf "$prof"' EXIT
    "$CHROME_BIN" "${COMMON_FLAGS[@]}" \
      --user-data-dir="$prof" \
      ${WAIT_MS:+--virtual-time-budget="$WAIT_MS"} \
      --dump-dom "$url"
    ;;

  text)
    url="${1:?ต้องระบุ URL}"
    require_chrome
    prof="$(make_profile)"; trap 'rm -rf "$prof"' EXIT
    # ดึง text ด้วยการรัน JS ผ่าน --dump-dom แล้วตัด tag ด้วย sed (เบา, ไม่ต้อง node)
    "$CHROME_BIN" "${COMMON_FLAGS[@]}" \
      --user-data-dir="$prof" \
      --dump-dom "$url" \
    | sed -e 's/<script[^>]*>.*<\/script>//g' \
          -e 's/<style[^>]*>.*<\/style>//g' \
          -e 's/<[^>]*>//g' \
    | sed -e 's/&nbsp;/ /g' -e 's/&amp;/\&/g' -e 's/&lt;/</g' -e 's/&gt;/>/g' \
          -e 's/&quot;/"/g' -e "s/&#39;/'/g" \
    | sed -e '/^[[:space:]]*$/d' \
          -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'
    ;;

  shot)
    url="${1:?ต้องระบุ URL}"
    out="${2:?ต้องระบุชื่อไฟล์ output .png}"
    mode="${3:-}"
    require_chrome
    prof="$(make_profile)"; trap 'rm -rf "$prof"' EXIT
    [ "$mode" = "--viewport" ] && flags=("${COMMON_FLAGS[@]}") || flags=("${COMMON_FLAGS[@]}" --screenshot="$out")
    if [ "$mode" = "--viewport" ]; then
      "$CHROME_BIN" "${flags[@]}" --user-data-dir="$prof" --screenshot="$out" "$url"
    else
      # full-page: ใช้ --screenshot โดยไม่จำกัดความสูงผ่าน window-size สูงมาก
      "$CHROME_BIN" --headless=new --no-sandbox --disable-gpu \
        --disable-dev-shm-usage --hide-scrollbars \
        --window-size=1280,3000 \
        --user-data-dir="$prof" --screenshot="$out" "$url"
    fi
    [ -s "$out" ] || die "screenshot ล้มเหลว: $out ว่าง"
    echo "✅ saved: $out ($(du -h "$out" | cut -f1))"
    ;;

  pdf)
    url="${1:?ต้องระบุ URL}"
    out="${2:?ต้องระบุชื่อไฟล์ output .pdf}"
    require_chrome
    prof="$(make_profile)"; trap 'rm -rf "$prof"' EXIT
    "$CHROME_BIN" "${COMMON_FLAGS[@]}" \
      --user-data-dir="$prof" --print-to-pdf="$out" "$url"
    [ -s "$out" ] || die "pdf ล้มเหลว: $out ว่าง"
    echo "✅ saved: $out ($(du -h "$out" | cut -f1))"
    ;;

  *)
    sed -n '2,25p' "$0" | sed 's/^# \{0,1\}//'
    exit 1
    ;;
esac
