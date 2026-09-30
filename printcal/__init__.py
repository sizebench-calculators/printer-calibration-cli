"""printcal: 3D printer calibration math (e-steps, flow, volumetric speed, magic layer heights).
Same formulas as https://sizebench.com/3d-printing"""

__version__ = "1.0.0"


def esteps(current: float, requested: float = 100.0, mark: float = 120.0, remaining: float = 20.0) -> dict:
    """New E-steps from a marked-filament test.
    extruded = mark - remaining ; new = current × requested ÷ extruded"""
    extruded = mark - remaining
    if extruded <= 0:
        raise ValueError("mark must be greater than the remaining distance")
    new = current * requested / extruded
    return {"extruded": extruded, "error_pct": (extruded - requested) / requested * 100, "new": new,
            "gcode": f"M92 E{new:.2f}\nM500", "klipper_rotation_distance_factor": extruded / requested}


def flow(current: float, expected_wall: float, measured_wall: float) -> dict:
    """New flow (% or ratio) from a single/two-wall cube: new = current × expected ÷ measured."""
    if measured_wall <= 0:
        raise ValueError("measured_wall must be positive")
    return {"new": current * expected_wall / measured_wall, "diff_pct": (measured_wall - expected_wall) / expected_wall * 100}


def volumetric(layer: float, width: float, speed: float, max_flow: float = 15.0) -> dict:
    """Volumetric flow (mm³/s) and the max speed a hotend can melt at this layer/width."""
    f = layer * width * speed
    return {"flow": f, "max_speed": max_flow / (layer * width), "within_limit": f <= max_flow}


def magic_layers(lead: float = 8.0, step_angle: float = 1.8, nozzle: float = 0.4, target: float | None = None) -> dict:
    """Layer heights that are whole multiples of a full Z motor step (≤ 80% of nozzle)."""
    step = lead / (360 / step_angle)
    max_layer = nozzle * 0.8
    layers, k = [], 1
    while k * step <= max_layer + 1e-9:
        if k * step >= 0.05 - 1e-9:
            layers.append(round(k * step, 4))
        k += 1
    out = {"z_step": step, "max_layer": max_layer, "layers": layers}
    if target is not None:
        out["nearest"] = round(max(round(target / step), 1) * step, 4)
    return out
