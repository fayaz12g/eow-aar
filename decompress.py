import os
import sys
import subprocess
import zstandard as zstd

def decompress_zstd(input_file):
    output_file = os.path.splitext(input_file)[0]  # Remove the .zs extension

    # Decompress the zstd file
    dctx = zstd.ZstdDecompressor()
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        decompressed_data = dctx.decompress(f_in.read())
        f_out.write(decompressed_data)

    decompressed_filename = os.path.basename(output_file)

    print(f"Decompressed {decompressed_filename}")