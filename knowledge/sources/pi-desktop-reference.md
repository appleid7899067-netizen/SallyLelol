# PI-Desktop — Modular Desktop Workspace for AI Agents

**เก็บเมื่อ**: 23 ตุลาคม 2026
**ที่มา**: `NovaAgent-Backup/cowbase/projects/Panupan01/staging/pi-desktop` (ก่อนลบ Backup)
**Repo ต้นทาง**: https://github.com/vastsa/PI-Desktop
**เวอร์ชัน**: 0.21.x (Early Preview)
**ที่เก็บสำเนา**: `knowledge/sources/pi-desktop-reference/` (35 MB, ตัด .git/.cargo ออกแล้ว)

## คืออะไร

Desktop workspace สำหรับ AI agents แบบ **local-first · model-agnostic · plugin-powered**
รองรับ macOS / Windows / Linux

**แนวคิดหลัก**:
- "Your projects stay local · Your models stay replaceable · Your workspace stays yours"
- รวม projects, agents, models, plugins และ workflows ไว้ใน environment เดียวแบบ persistent

## Stack เทคนิค

| ส่วน | รายละเอียด |
|---|---|
| Backend | **Rust** (`Cargo.toml`, `Cargo.lock`, `crates/`) |
| Frontend | **TypeScript** (`apps/`, `biome.json`) |
| Docs | `docs/` 7.3 MB — adr, architecture, diagrams, guide, implementation, plugin-development, spec |
| Agent guide | `AGENTS.md` (33 KB), `CLAUDE.md` (17 KB) |

## ทำไมน่าสนใจสำหรับ NovaAgent

1. **AGENTS.md + CLAUDE.md ขนาดใหญ่** — ตัวอย่างการเขียน instruction ให้ agent แบบละเอียด
2. **Plugin architecture** — `docs/plugin-development.md`, `docs/plugin-plan/` เป็นแนวทางระบบ plugin
3. **ADR (Architecture Decision Records)** — `docs/adr/` ตัวอย่างการบันทึกการตัดสินใจเชิงสถาปัตยกรรม
4. **Rust + TS hybrid** — สถาปัตยกรรมที่ต่างจาก NovaAgent (Python) ศึกษาได้ว่าจัดการ core/UI อย่างไร
5. **Local-first + model-agnostic** — ตรงกับทิศทางที่บอสต้องการ (โมเดลเปลี่ยนได้ ไม่ผูกขาด)

## ข้อควรระวัง

- เป็น Early Preview (0.21.x) — โครงสร้างอาจเปลี่ยน
- LICENSE ต้องตรวจก่อนนำโค้ดไปใช้ซ้ำ (เก็บไฟล์ LICENSE ไว้แล้วในสำเนา)

## Related

- [CodingFleet Desktop Reference](codingfleet-desktop-reference/) — AI coding agent อีกตัวที่ศึกษา guard/tools
- [NovaAgent Backup 20261017](novaagent-backup-20261017/) — knowledge/branding เก่าที่เก็บไว้ก่อนลบ Backup
