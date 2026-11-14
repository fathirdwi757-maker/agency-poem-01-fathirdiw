import os
from pathlib import Path
from tempfile import NamedTemporaryFile

POEM = (
    "I gave the machine my errands.\n"
    "It returned an afternoon, still mine.\n"
    "At my sister's door, the checklist ended:\n"
    'there was no prompt for "I was wrong."\n'
    "I said it, hands shaking.\n"
    "Inside, a chair scraped back.\n"
)


def main():
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output").expanduser()
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        if not output_dir.is_dir():
            raise NotADirectoryError(f"Output path is not a directory: {output_dir}") from None
        raise
    if not output_dir.is_dir():
        raise NotADirectoryError(f"Output path is not a directory: {output_dir}")
    if not 1 <= len(POEM) <= 1000 or not POEM.strip():
        raise ValueError("Poem must contain 1 to 1,000 code points and at least one non-whitespace character")
    poem_bytes = POEM.encode("utf-8")
    entry_path = output_dir / "entry.txt"
    temporary_path = None
    try:
        with NamedTemporaryFile(dir=output_dir, prefix=".entry-", delete=False) as temporary:
            temporary.write(poem_bytes)
            temporary_path = Path(temporary.name)
        temporary_path.replace(entry_path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


if __name__ == "__main__":
    main()
