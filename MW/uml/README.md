# UML Domain Model – Build Instructions

Dit pakket bevat het reverse-engineerde domeinmodel voor Open Plan in diverse formaten.

## Bestanden

| Bestand | Beschrijving |
|---------|------------|
| `open-plan-domain.md` | Markdown documentatie (authoritaire bron) |
| `open-plan-domain.mmd` | Mermaid klassendiagram |
| `open-plan-domain.xmi` | UML 2.5.1 / XMI 2.5.1 (importeren in EA, MagicDraw, etc.) |
| `open-plan-domain.docx` | Word-document (gegenereerd) |
| `build_docx.py` | Build-script |

## Word-document genereren

```bash
python3 MW/uml/build_docx.py
```

Dit leest `open-plan-domain.md` en genereert `open-plan-domain.docx`.

**Vereisten:** `python-docx`

```bash
pip3 install python-docx
```

## UML importeren

Open `open-plan-domain.xmi` in:
- Enterprise Architect
- MagicDraw / Cameo
- Modelio
- StarUML
- Papyrus

## Mermaid diagram

Bekijk `open-plan-domain.mmd` op:
- [Mermaid Live Editor](https://mermaid.live)
- In de Markdown documentatie (als `sphinxcontrib-mermaid` geïnstalleerd is)
