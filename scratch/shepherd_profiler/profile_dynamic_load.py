import sys
import time
from collections.abc import Sequence
from pathlib import Path

import click
import zerorpc
from fabric import Connection
from keithley2600 import Keithley2600
from keithley2600.keithley_driver import KeithleyClass

script_path = Path(__file__).parent.parent.parent
shepherd_path = script_path.parent.joinpath(
    "shepherd",
    "software",
    "python-package",
    "shepherd",
).resolve()
sys.path.append(str(shepherd_path))


# SMU Config-Parameters
mode_4wire: bool = True
pwrline_cycles: float = 16  # .001 to 25 allowed, >= 20 SMU throws sporadic errors (timeouts)

adict = {
    "voltage_shp_V": 0,
    "voltage_shp_raw": 1,
    "voltage_ref_V": 2,
    "current_shp_A": 3,
    "current_shp_raw": 4,
    "current_ref_A": 5,
}

INSTR_EMU = """
---------------------- Characterize Shepherd-Frontend -----------------------
- remove targets from target-ports
- remove harvesting source from harvester-input (P6)
- Connect SMU channel A Lo to P10-1 (Target-A GND)
- Connect SMU channel A Hi to P10-2 (Target-A Voltage)
- Resistor (~200 Ohm) and Cap (1-10 uF) between
    - P11-1 (Target-B GND)
    - P11-2 (Target-B Voltage)
- Connect SMU channel B Lo to P6-2 (HRV-Input GND)
- Connect SMU channel B Hi to P6-3 & -4 (VSense and VHarvest connected together)
- NOTE: be sure to use 4-Wire-Cabling to SMU for improved results (can be disabled in script)
"""


def emulator_dyn_load(
    rpc_client: zerorpc.Client, smu: KeithleyClass, voltage_V: float, currents_A: Sequence
) -> None:
    voltage_V = min(max(voltage_V, 0.0), 5.0)

    if smu is not None:
        current_lim = min(max(currents_A[0], 0.0), 0.050)
        smu.sense = smu.SENSE_REMOTE if mode_4wire else smu.SENSE_LOCAL
        smu.source.leveli = -current_lim  # negative current, because smu acts as a drain
        smu.source.limitv = 5.0
        smu.source.func = smu.OUTPUT_DCAMPS
        smu.source.autorangei = smu.AUTORANGE_ON
        smu.source.output = smu.OUTPUT_ON
        print(f"Enabled SMU with V = {voltage_V} V, A = {current_lim * 1000} mA")

    # write both dac-channels of emulator
    dac_voltage_raw = rpc_client.convert_value_to_raw(
        "emulator",
        "dac_voltage_b",
        voltage_V,
    )
    rpc_client.set_aux_target_voltage_raw((2**20) + dac_voltage_raw, also_main=True)

    for current_A in currents_A[1:]:
        current_lim = min(max(current_A, 0.0), 0.050)
        click.confirm(
            f"Confirm to switch to V = {voltage_V} V, A = {current_lim * 1000} mA",
            default=True,
        )
        smu.source.leveli = -current_lim  # negative current, because smu acts as a drain
    click.confirm("Ending Series", default=True)


@click.group(context_settings={"help_option_names": ["-h", "--help"], "obj": {}})
def cli() -> None:
    pass


@cli.command()
@click.argument("host", type=str)
@click.option("--user", "-u", type=str, default="joe", help="Host Username")
@click.option(
    "--password",
    "-p",
    type=str,
    default=None,
    help="Host User Password -> only needed when key-credentials are missing",
)
@click.option("--smu-ip", type=str, default="192.168.1.108")
@click.option("--harvester", "-h", is_flag=True, help="handle harvester")
@click.option("--emulator", "-e", is_flag=True, help="handle emulator")
def measure(
    host: str,
    user: str,
    password: str,
    smu_ip: str,
    *,
    harvester: bool = False,
    emulator: bool = False,
) -> None:
    fabric_args = {} if password is None else {"password": password}

    rpc_client = zerorpc.Client(timeout=60, heartbeat=20)

    if not any([harvester, emulator]):
        harvester = True
        emulator = True

    with (
        Keithley2600(f"TCPIP0::{smu_ip}::INSTR") as kth,
        Connection(
            host,
            user=user,
            connect_kwargs=fabric_args,
        ) as cnx,
    ):
        # kth = Keithley2600(f"TCPIP0::{smu_ip}::INSTR")  # my fork allows context manager
        kth.reset()
        cnx.sudo("systemctl restart shepherd-rpc", hide=True, warn=True)
        time.sleep(4)
        rpc_client.connect(f"tcp://{host}:4242")

        voltage_V = 3.0
        currents_A = [1e-6, 10e-3, 1e-6, 40e-3, 1e-6, 10e-3, 40e-3]

        click.echo(INSTR_EMU)
        print(
            f" -> Profiler will sweep through {len(currents_A)} currents {currents_A}",
        )
        # TODO: switches are too gently, opamp output does not jump :(

        if emulator:
            rpc_client.switch_shepherd_mode("emu_adc_read")
            rpc_client.select_target_for_power_tracking(
                True,
            )  # targetA-Port will get the monitored dac-channel-b
            emulator_dyn_load(rpc_client, kth.smua, voltage_V, currents_A)

        cnx.sudo("systemctl stop shepherd-rpc", hide=True, warn=True)


if __name__ == "__main__":
    cli()
