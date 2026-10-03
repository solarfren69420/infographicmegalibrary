# SolarFren’s beginner handbook

[Download the complete PDF](https://solarfren69420.github.io/infographicmegalibrary/guides/Infographic-Mega-Library-Beginner-Handbook.pdf) · [Browse the library](https://solarfren69420.github.io/infographicmegalibrary/)

The handbook consolidates the retained infographics and discussion into a beginner learning path. The images were intended as one-shot brainstorming and AI prompt references; the guide distinguishes those concepts from checked instructions and original teaching exercises.

## Practice files

- [Mechanics Playground](exercises/mechanics-playground.html): open in a browser on Windows, macOS, or Linux. One self-contained file, no account or installation. Test stamina, movement, and block rules.
- [Rust exercise](exercises/roll-demo.rs): after installing Rust and creating the chapter 8 Cargo project, save this as that project’s `src/main.rs`. Run `cargo run` and `cargo test` there.
- [JSON mechanic record](exercises/roll.json): structured teaching data; it does not run by itself.
- [SQLite script](exercises/mechanics.sql): paste into SQLite Fiddle or run with SQLite. Rerunning updates the same record rather than duplicating it.

Read the matching chapter before using a source file. A saved `.rs` file is not a universal mod, and a JSON record is not an executable.

## Source and regeneration

`beginner-handbook.md` is the editable text; `sources.json` contains primary references. The PDF generator adds the coverage index from the catalog. Run `python3 scripts/build_handbook.py` from the repository root with ReportLab 5, Pillow, and DejaVu fonts available. The ordinary Pages build publishes the checked-in PDF without regenerating it.

All larger commercial-game mashups remain proposed workflows unless independently built and demonstrated. Verification of documentation is dated 3 October 2026; installation requirements and promotional terms can change.
