#!/usr/bin/env python3
"""news-image-20261118 entrypoint.

Validates entry.png (a 1024x1024 PNG, at most 1 MiB) that sits next to this
file, then copies it byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output). Standard library only, no network, deterministic:
every run writes identical bytes.
"""
import hashlib
import os
import struct
import sys
import zlib

MAX_BYTES = 1_048_576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        fail("entry.png not found next to main.py")

    with open(source, "rb") as handle:
        data = handle.read()

    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if data[:8] != PNG_SIGNATURE:
        fail("entry.png does not start with the PNG signature")
    if len(data) < 33:
        fail("entry.png is too short to contain an IHDR chunk")

    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail("entry.png is %dx%d, expected 1024x1024" % (width, height))

    # Walk the whole file: every chunk must be well-formed, CRCs must match,
    # and the file must end with IEND. Then confirm the image data decodes
    # to exactly 1024 scanlines of 1024 RGB pixels.
    pos = 8
    seen_iend = False
    idat = bytearray()
    while pos + 8 <= len(data):
        length, chunk_type = struct.unpack(">I4s", data[pos:pos + 8])
        end = pos + 12 + length
        if end > len(data):
            fail("truncated %s chunk" % chunk_type.decode("ascii", "replace"))
        body = data[pos + 8:pos + 8 + length]
        stored_crc, = struct.unpack(">I", data[pos + 8 + length:end])
        actual_crc = zlib.crc32(chunk_type + body) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            fail("bad CRC in %s chunk" % chunk_type.decode("ascii", "replace"))
        if chunk_type == b"IDAT":
            idat += body
        elif chunk_type == b"IEND":
            seen_iend = True
            if end != len(data):
                fail("trailing bytes after IEND chunk")
            break
        pos = end
    if not seen_iend:
        fail("entry.png has no IEND chunk")
    try:
        raw = zlib.decompress(bytes(idat))
    except zlib.error:
        fail("entry.png IDAT data does not decompress")
    if len(raw) != EXPECTED_HEIGHT * (1 + EXPECTED_WIDTH * 3):
        fail("entry.png decodes to %d bytes, expected %d"
             % (len(raw), EXPECTED_HEIGHT * (1 + EXPECTED_WIDTH * 3)))

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        fail("cannot create output directory %s: %s" % (out_dir, exc))
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(data)
    os.chmod(target, 0o644)
    # Prove the copy is byte-for-byte identical to the validated source.
    with open(target, "rb") as handle:
        written = handle.read()
    if written != data:
        fail("written output differs from validated entry.png")
    print("wrote %s (%d bytes, %dx%d, sha256 %s)"
          % (target, len(data), width, height,
             hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
