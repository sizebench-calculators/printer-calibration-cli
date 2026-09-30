import pytest
from printcal import esteps, flow, volumetric, magic_layers


def test_esteps():
    r = esteps(93, 100, 120, 23)
    assert r["extruded"] == pytest.approx(97)
    assert r["new"] == pytest.approx(95.876, abs=0.01)
    assert r["gcode"].startswith("M92 E95.88")


def test_esteps_invalid():
    with pytest.raises(ValueError):
        esteps(93, 100, 20, 30)


def test_flow_percent_and_ratio():
    assert flow(100, 0.9, 0.95)["new"] == pytest.approx(94.74, abs=0.01)
    assert flow(1.0, 0.9, 0.95)["new"] == pytest.approx(0.9474, abs=0.0001)


def test_volumetric():
    r = volumetric(0.2, 0.45, 150, 15)
    assert r["flow"] == pytest.approx(13.5)
    assert r["max_speed"] == pytest.approx(166.7, abs=0.1)
    assert r["within_limit"]


def test_magic_layers():
    r = magic_layers(8, 1.8, 0.4, 0.21)
    assert r["z_step"] == pytest.approx(0.04)
    assert r["layers"][:4] == [0.08, 0.12, 0.16, 0.2]
    assert r["nearest"] == pytest.approx(0.2)
    assert max(r["layers"]) <= 0.32
