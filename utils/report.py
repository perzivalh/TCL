from io import BytesIO
from typing import Any, Dict

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def _fig_to_image(fig, width: float = 5.8 * inch, height: float = 3.6 * inch) -> Image:
    """Convierte una figura de matplotlib a un objeto Image de reportlab."""
    buffer = BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", dpi=160)
    buffer.seek(0)
    img = Image(buffer, width=width, height=height)
    return img


def _format_params(dist_name: str, dist_params: Dict[str, Any]) -> str:
    """Devuelve una linea legible de parametros segun la distribucion."""
    if dist_name == "Uniforme":
        return f"a = {dist_params['a']:.2f}, b = {dist_params['b']:.2f}"
    if dist_name == "Exponencial":
        return f"lambda = {dist_params['lam']:.2f}"
    if dist_name == "Binomial":
        return f"n = {dist_params['n_trials']}, p = {dist_params['p']:.2f}"
    return ""


def _build_table(data, col_widths=None) -> Table:
    table = Table(data, colWidths=col_widths)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f1d33")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#16263d")),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#dfe8f7")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#2c4062")),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#2c4062")),
            ]
        )
    )
    return table


def _draw_background(canvas, doc, hex_color: str) -> None:
    """Pinta un fondo solido en cada pagina."""
    canvas.saveState()
    canvas.setFillColor(colors.HexColor(hex_color))
    canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1, stroke=0)
    canvas.restoreState()


def build_pdf_report(
    inputs: Dict[str, Any],
    pop_empirical: Dict[str, float],
    sample_empirical: Dict[str, float],
    theoretical: Dict[str, float],
    pop_diff: Dict[str, float],
    means_diff: Dict[str, float],
    fig_population,
    fig_means,
) -> bytes:
    """
    Crea un PDF con resumen de entradas, metrica teorica/empirica y graficas.
    Devuelve los bytes listos para descargar en Streamlit.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=42,
        bottomMargin=42,
        title="Reporte TCL",
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="Muted",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#c7d6f3"),
        )
    )
    styles["Title"].textColor = colors.HexColor("#e8eef7")
    styles["Heading2"].textColor = colors.HexColor("#e8eef7")
    styles["Normal"].textColor = colors.HexColor("#dfe8f7")

    elements = []
    title = Paragraph("Reporte del Teorema Central del Limite", styles["Title"])
    subtitle = Paragraph("Entradas y resultados de la simulación", styles["Muted"])
    elements.extend([title, subtitle, Spacer(1, 10)])

    inputs_rows = [
        ["Parametro", "Valor"],
        ["Distribucion", inputs["dist_name"]],
        ["Parametros", _format_params(inputs["dist_name"], inputs["dist_params"])],
        ["Tamano de muestra (n)", str(inputs["sample_size"])],
        ["Numero de simulaciones (k)", str(inputs["n_simulations"])],
        ["Tamano de poblacion graficada", f"{inputs['population_size']:,}"],
    ]
    elements.append(_build_table(inputs_rows, col_widths=[180, 330]))
    elements.append(Spacer(1, 16))

    pop_table = [
        ["Metrica", "Teorica", "Empirica", "Diferencia abs."],
        ["Media", f"{theoretical['mean']:.4f}", f"{pop_empirical['mean']:.4f}", f"{pop_diff.get('mean', 0):.4f}"],
        ["Desviacion estandar", f"{theoretical['std']:.4f}", f"{pop_empirical['std']:.4f}", f"{pop_diff.get('std', 0):.4f}"],
    ]
    elements.append(Paragraph("Población generada", styles["Heading2"]))
    elements.append(_build_table(pop_table))
    elements.append(Spacer(1, 12))

    means_table = [
        ["Metrica", "Teorica", "Empirica", "Diferencia abs."],
        ["Media", f"{theoretical['mean']:.4f}", f"{sample_empirical['mean']:.4f}", f"{means_diff['mean']:.4f}"],
        ["Error estandar / Desv.", f"{theoretical['se']:.4f}", f"{sample_empirical['std']:.4f}", f"{means_diff['std']:.4f}"],
    ]
    elements.append(Paragraph("Medias muestrales", styles["Heading2"]))
    elements.append(_build_table(means_table))
    elements.append(Spacer(1, 16))

    elements.append(Paragraph("Grafica de la poblacion", styles["Heading2"]))
    elements.append(_fig_to_image(fig_population))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Grafica de las medias muestrales", styles["Heading2"]))
    elements.append(_fig_to_image(fig_means))

    doc.build(
        elements,
        onFirstPage=lambda canvas, d: _draw_background(canvas, d, "#0d1523"),
        onLaterPages=lambda canvas, d: _draw_background(canvas, d, "#0d1523"),
    )
    buffer.seek(0)
    return buffer.getvalue()
