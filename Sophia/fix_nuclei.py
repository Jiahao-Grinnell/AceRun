import pathlib

root = pathlib.Path(".").resolve()
nuc_dir = root / "nuclei"

print(f"Working in: {root}")
print(f"Nuclei folder: {nuc_dir}")

if not nuc_dir.is_dir():
    raise SystemExit("ERROR: 'nuclei' folder not found in this directory.")

# Backup originals
backup_dir = root / "nuclei_backup"
backup_dir.mkdir(exist_ok=True)

for nuc_file in sorted(nuc_dir.glob("t*-nuclei")):
    print(f"Processing {nuc_file.name} ...")

    # backup once
    backup_path = backup_dir / nuc_file.name
    if not backup_path.exists():
        backup_path.write_text(nuc_file.read_text())

    lines_out = []
    with nuc_file.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # split & strip
            parts = [p.strip() for p in line.split(",")]

            # drop empty tokens (from ', ,')
            parts = [p for p in parts if p != ""]

            # *** key change: match demo format -> keep only first 11 fields ***
            parts = parts[:11]

            # rebuild line with trailing comma, like demo
            new_line = ", ".join(parts) + ",\n"
            lines_out.append(new_line)

    nuc_file.write_text("".join(lines_out))

print("Done. Cleaned all nuclei files. Originals saved in 'nuclei_backup'.")
