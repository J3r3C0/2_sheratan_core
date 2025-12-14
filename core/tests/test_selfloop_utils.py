import textwrap

from core.sheratan_core_v2.selfloop_utils import parse_selfloop_markdown, build_next_loop_state


def test_parse_selfloop_markdown_happy_path():
    text = textwrap.dedent("""        A) Standortanalyse
    - Wir sind am Anfang.

    B) Nächster sinnvoller Schritt
    - Eine einfache Testantwort bauen.

    C) Umsetzung
    - Dies ist die konkrete Umsetzung.

    D) Vorschlag für nächsten Loop
    - Nächster Schritt: Integration testen.
    """)

    parsed = parse_selfloop_markdown(text)
    assert parsed["A"].startswith("- Wir sind am Anfang")
    assert "Testantwort" in parsed["B"]
    assert "konkrete Umsetzung" in parsed["C"]
    assert "Nächster Schritt" in parsed["D"]


def test_build_next_loop_state_basic():
    prev_state = {
        "iteration": 1,
        "history_summary": "",
        "constraints": ["bleibe im A/B/C/D-Format"]
    }
    parsed = {
        "A": "Kurze Lagebeschreibung.",
        "B": "Nächster Schritt.",
        "C": "Konkrete Umsetzung eines simplen Tests.",
        "D": "- Im nächsten Loop Output-Pfade prüfen."
    }

    next_state = build_next_loop_state(prev_state, parsed)
    assert next_state["iteration"] == 2
    assert "Konkrete Umsetzung" in next_state["history_summary"]
    assert next_state["constraints"] == ["bleibe im A/B/C/D-Format"]
    assert any("Output-Pfade" in q for q in next_state["open_questions"])
