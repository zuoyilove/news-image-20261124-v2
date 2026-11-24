"""news-image-20261124 entry: write the day's news image to the output dir.

The picture itself (entry.png, beside this file) sums up the world news of
Tuesday 24 November 2026 in one front-page collage: Huang rehired as
Nvidia CEO after a Trump push, 24 dead in an Indonesian factory fire,
COP31 ending with no deal, the world court ruling Myanmar committed
genocide against the Rohingya, and Trump blaming Democrats for a
$6 trillion market fall, with a ticker of the day's other stories.
It is a whole PNG of 1024 by 1024 pixels and under 1 MiB, inside the
competition's image gate. This program's only job is to deliver those
exact bytes to /output/entry.png, deterministically: it runs twice and
both runs must write the same file.
"""

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"

# The competition's image gate: at most 1024 by 1024 pixels, at most 1 MiB.
MAX_SIDE = 1024
MAX_BYTES = 1_048_576


def check_image(data: bytes) -> None:
    # PNG header: width and height are big-endian uint32 at bytes 16..24.
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"image is {width}x{height}, over the 1024x1024 gate")
    if len(data) > MAX_BYTES:
        raise ValueError(f"image is {len(data)} bytes, over the 1 MiB gate")


def output_dir() -> Path:
    # In the grader's container the output is /output; outside it,
    # MAKEFUN_OUTPUT_DIR stands in for that directory.
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    target = output_dir() / "entry.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    # Write to a temp file in the same directory, then rename: the rename is
    # atomic, so a reader never observes a half-written image, and the size
    # check proves the copy is whole before it becomes visible.
    data = SOURCE.read_bytes()
    check_image(data)
    tmp = target.with_suffix(".tmp")
    tmp.write_bytes(data)
    if tmp.stat().st_size != len(data):
        raise IOError("short write while copying entry.png")
    tmp.replace(target)


if __name__ == "__main__":
    main()
