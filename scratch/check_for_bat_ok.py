from pathlib import Path

import click
import h5py
import numpy as np


@click.command()
@click.argument("database", type=click.Path(exists=True, dir_okay=False))
def cli(database: Path) -> None:
    with h5py.File(database, "r") as db:
        print(f"File got {len(db['gpio']['value'])} entries for GPIO")
        tt = db["gpio"]["value"][:] & ((2**9) + (2**10))  # BitPosition r30_09/out  TARGET_BAT_OK
        counts = np.unique(tt, return_counts=True)
        print("got the following result for BatOK:")
        print(counts)
        counts = np.unique(db["gpio"]["value"][:], return_counts=True)
        print("got the following result (all)")
        print(counts)

        print(f"voltage-attributes keys   {list(db['data']['voltage'].attrs.keys())}")
        print(f"voltage-attributes values {list(db['data']['voltage'].attrs.values())}")
        print(f"current-attributes keys   {list(db['data']['current'].attrs.keys())}")
        print(f"current-attributes values {list(db['data']['current'].attrs.values())}")


if __name__ == "__main__":
    cli()
