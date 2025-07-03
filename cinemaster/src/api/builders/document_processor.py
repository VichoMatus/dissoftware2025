"""
Procesador de documentos que toma los objetos Document del Builder 
y los convierte en archivos PDF, HTML, JSON, etc.
"""
import os
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import json
from datetime import datetime
import base64

from .document_builder import Document


class DocumentProcessor:
    """
    Procesador que convierte objetos Document en archivos físicos
    """
    
    def __init__(self, output_directory: str = "generated_documents"):
        self.output_directory = output_directory
        self._ensure_output_directory()
    
    def _ensure_output_directory(self):
        """Asegura que el directorio de salida exista"""
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
    
    def process_to_pdf(self, document: Document) -> Dict[str, Any]:
        """
        Convierte un Document a PDF usando ReportLab
        """
        try:
            filename = f"{document.document_type}_{document.document_id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf_path = os.path.join(self.output_directory, filename)
            
            # Crear el documento PDF
            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Estilos personalizados
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=20,
                alignment=TA_CENTER,
                textColor=colors.darkblue
            )
            
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=15,
                alignment=TA_CENTER,
                textColor=colors.darkgreen
            )
            
            # Encabezado
            if document.header:
                header = Paragraph(document.header, title_style)
                story.append(header)
                story.append(Spacer(1, 12))
            
            # Título
            if document.title:
                title = Paragraph(document.title, title_style)
                story.append(title)
                story.append(Spacer(1, 12))
            
            # Subtítulo
            if document.subtitle:
                subtitle = Paragraph(document.subtitle, subtitle_style)
                story.append(subtitle)
                story.append(Spacer(1, 12))
            
            # Contenido específico por tipo de documento
            if document.document_type == "cinema_ticket":
                story.extend(self._build_ticket_content(document, styles))
            elif document.document_type == "invoice":
                story.extend(self._build_invoice_content(document, styles))
            elif document.document_type == "report":
                story.extend(self._build_report_content(document, styles))
            else:
                story.extend(self._build_generic_content(document, styles))
            
            # Pie de página
            if document.footer:
                story.append(Spacer(1, 20))
                footer = Paragraph(document.footer, styles['Normal'])
                story.append(footer)
            
            # Construir el PDF
            doc.build(story)
            
            return {
                "success": True,
                "message": "PDF generado exitosamente",
                "pdf_path": pdf_path,
                "filename": filename
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error generando PDF: {str(e)}",
                "pdf_path": None,
                "filename": None
            }
    
    def _build_ticket_content(self, document: Document, styles) -> list:
        """Construye el contenido específico para boletos de cine"""
        story = []
        content = document.content
        
        # Agregar imagen de la película si está disponible
        movie_image_path = content.get("movie_image_path")
        if movie_image_path and os.path.exists(movie_image_path):
            try:
                # Agregar imagen de la película
                img = Image(movie_image_path)
                img.drawHeight = 2*inch
                img.drawWidth = 1.5*inch
                
                # Centrar la imagen
                img.hAlign = 'CENTER'
                
                story.append(img)
                story.append(Spacer(1, 12))
            except Exception as e:
                print(f"Error al cargar imagen de película: {e}")
        
        # Información del boleto en tabla
        ticket_data = [
            ["🎬 Película:", content.get("movie_name", "N/A")],
            ["🕐 Horario:", content.get("showtime", "N/A")],
            ["🪑 Asiento:", content.get("seat", "N/A")],
            ["👤 Cliente:", content.get("client_name", "N/A")],
            ["💰 Precio:", f"${content.get('ticket_price', 0.0):.2f}"]
        ]
        
        table = Table(ticket_data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Código de barras simulado
        barcode_text = f"ID: {document.document_id}"
        barcode = Paragraph(f"<b>{barcode_text}</b>", styles['Normal'])
        story.append(barcode)
        
        return story
    
    def _build_invoice_content(self, document: Document, styles) -> list:
        """Construye el contenido específico para facturas"""
        story = []
        content = document.content
        
        # Información del cliente
        client_info = Paragraph(f"<b>Cliente:</b> {content.get('client_name', 'N/A')}", styles['Normal'])
        story.append(client_info)
        story.append(Spacer(1, 12))
        
        # Items de la factura
        items = content.get("items", [])
        if items:
            items_data = [["Descripción", "Cantidad", "Precio Unit.", "Total"]]
            for item in items:
                items_data.append([
                    item.get("description", ""),
                    str(item.get("quantity", 0)),
                    f"${item.get('unit_price', 0.0):.2f}",
                    f"${item.get('total', 0.0):.2f}"
                ])
            
            table = Table(items_data, colWidths=[3*inch, 1*inch, 1*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            story.append(Spacer(1, 12))
        
        # Total
        total = content.get("total_amount", 0.0)
        total_text = Paragraph(f"<b>TOTAL: ${total:.2f}</b>", styles['Heading2'])
        story.append(total_text)
        
        return story
    
    def _build_report_content(self, document: Document, styles) -> list:
        """Construye el contenido específico para reportes"""
        story = []
        content = document.content
        
        for key, value in content.items():
            if key not in ["report_type"]:  # Excluir metadatos
                section = Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {str(value)}", styles['Normal'])
                story.append(section)
                story.append(Spacer(1, 8))
        
        return story
    
    def _build_generic_content(self, document: Document, styles) -> list:
        """Construye contenido genérico para documentos no especializados"""
        story = []
        content = document.content
        
        for key, value in content.items():
            section = Paragraph(f"<b>{key}:</b> {str(value)}", styles['Normal'])
            story.append(section)
            story.append(Spacer(1, 8))
        
        return story
    
    def process_to_json(self, document: Document) -> Dict[str, Any]:
        """
        Convierte un Document a archivo JSON
        """
        try:
            filename = f"{document.document_type}_{document.document_id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            json_path = os.path.join(self.output_directory, filename)
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(document.to_dict(), f, indent=2, ensure_ascii=False, default=str)
            
            return {
                "success": True,
                "message": "JSON generado exitosamente",
                "file_path": json_path,
                "filename": filename
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error generando JSON: {str(e)}",
                "file_path": None,
                "filename": None
            }
    
    def process_to_html(self, document: Document) -> Dict[str, Any]:
        """
        Convierte un Document a archivo HTML
        """
        try:
            filename = f"{document.document_type}_{document.document_id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            html_path = os.path.join(self.output_directory, filename)
            
            html_content = self._generate_html(document)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return {
                "success": True,
                "message": "HTML generado exitosamente",
                "file_path": html_path,
                "filename": filename
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error generando HTML: {str(e)}",
                "file_path": None,
                "filename": None
            }
    
    def _generate_html(self, document: Document) -> str:
        """Genera contenido HTML para el documento"""
        content = document.content
        
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{document.title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ text-align: center; color: #333; }}
                .content {{ margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 40px; color: #666; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{document.header}</h1>
                <h2>{document.title}</h2>
                <h3>{document.subtitle}</h3>
            </div>
            <div class="content">
        """
        
        if document.document_type == "cinema_ticket":
            html += self._generate_ticket_html(content)
        else:
            for key, value in content.items():
                html += f"<p><strong>{key.replace('_', ' ').title()}:</strong> {value}</p>"
        
        html += f"""
            </div>
            <div class="footer">
                <p>{document.footer}</p>
                <p><small>Generado el: {document.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</small></p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _generate_ticket_html(self, content: Dict[str, Any]) -> str:
        """Genera HTML específico para boletos"""
        # Preparar imagen de la película
        movie_image_html = ""
        movie_image_path = content.get("movie_image_path")
        
        if movie_image_path and os.path.exists(movie_image_path):
            try:
                # Convertir imagen a base64 para incluirla en HTML
                with open(movie_image_path, "rb") as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
                    img_ext = os.path.splitext(movie_image_path)[1].lower()[1:]  # Obtener extensión sin el punto
                    
                    # Determinar el tipo MIME
                    mime_type = "image/jpeg" if img_ext in ["jpg", "jpeg"] else f"image/{img_ext}"
                    
                    movie_image_html = f"""
                    <div style="text-align: center; margin: 20px 0;">
                        <img src="data:{mime_type};base64,{img_data}" 
                             alt="Imagen de la película" 
                             style="max-width: 200px; max-height: 300px; border: 2px solid #ddd; border-radius: 8px;">
                    </div>
                    """
            except Exception as e:
                print(f"Error al procesar imagen para HTML: {e}")
                movie_image_html = ""
        
        return f"""
        {movie_image_html}
        <table>
            <tr><th>🎬 Película</th><td>{content.get('movie_name', 'N/A')}</td></tr>
            <tr><th>🕐 Horario</th><td>{content.get('showtime', 'N/A')}</td></tr>
            <tr><th>🪑 Asiento</th><td>{content.get('seat', 'N/A')}</td></tr>
            <tr><th>👤 Cliente</th><td>{content.get('client_name', 'N/A')}</td></tr>
            <tr><th>💰 Precio</th><td>${content.get('ticket_price', 0.0):.2f}</td></tr>
        </table>
        """


# Instancia global del procesador
_global_processor = DocumentProcessor(
    output_directory=os.path.join(os.path.dirname(__file__), "..", "..", "..", "Boletas")
)


def get_document_processor(output_dir: Optional[str] = None) -> DocumentProcessor:
    """
    Función global para obtener el procesador de documentos
    """
    if output_dir:
        return DocumentProcessor(output_dir)
    return _global_processor
