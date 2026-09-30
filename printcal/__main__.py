"""Command line: python -m printcal <command> [options]"""
import argparse
from . import esteps, flow, volumetric, magic_layers


def main(argv=None):
    p = argparse.ArgumentParser(prog="printcal", description="3D printer calibration calculator (e-steps, flow, volumetric, layers). More: https://sizebench.com/3d-printing")
    sub = p.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("esteps", help="new E-steps from a marked-filament test")
    e.add_argument("--current", type=float, required=True); e.add_argument("--requested", type=float, default=100)
    e.add_argument("--mark", type=float, default=120); e.add_argument("--remaining", type=float, required=True)
    f = sub.add_parser("flow", help="new flow from a wall-thickness test")
    f.add_argument("--current", type=float, default=100); f.add_argument("--expected", type=float, required=True); f.add_argument("--measured", type=float, required=True)
    v = sub.add_parser("volumetric", help="volumetric flow and max speed")
    v.add_argument("--layer", type=float, default=0.2); v.add_argument("--width", type=float, default=0.45)
    v.add_argument("--speed", type=float, required=True); v.add_argument("--max-flow", type=float, default=15)
    l = sub.add_parser("layers", help="magic layer heights for your Z axis")
    l.add_argument("--lead", type=float, default=8); l.add_argument("--step-angle", type=float, default=1.8)
    l.add_argument("--nozzle", type=float, default=0.4); l.add_argument("--target", type=float)
    a = p.parse_args(argv)
    if a.cmd == "esteps":
        r = esteps(a.current, a.requested, a.mark, a.remaining)
        print(f"Extruded: {r['extruded']:.1f} mm ({r['error_pct']:+.1f}%)\nNew E-steps: {r['new']:.2f}\nSend:\n{r['gcode']}")
    elif a.cmd == "flow":
        r = flow(a.current, a.expected, a.measured)
        print(f"Measured vs expected: {r['diff_pct']:+.1f}%\nNew flow: {r['new']:.3f}" if a.current <= 2 else f"Measured vs expected: {r['diff_pct']:+.1f}%\nNew flow: {r['new']:.1f}%")
    elif a.cmd == "volumetric":
        r = volumetric(a.layer, a.width, a.speed, a.max_flow)
        print(f"Flow: {r['flow']:.1f} mm³/s ({'OK' if r['within_limit'] else 'ABOVE hotend limit'})\nMax speed: {r['max_speed']:.0f} mm/s")
    else:
        r = magic_layers(a.lead, a.step_angle, a.nozzle, a.target)
        print(f"Z per full step: {r['z_step']:.4f} mm\nGood layer heights: {', '.join(f'{x:g}' for x in r['layers'])}")
        if "nearest" in r:
            print(f"Nearest to {a.target}: {r['nearest']:g} mm")


if __name__ == "__main__":
    main()
