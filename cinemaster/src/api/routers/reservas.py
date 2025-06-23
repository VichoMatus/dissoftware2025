from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from controllers.receipt_controller import ReceiptController
from commands.reserve_seat_command import ReserveSeatCommand
from services.email_observer import EmailSenderObserver
from datetime import datetime

from models.database import Asiento, Funcion, get_db, Reserva_asientos, HorarioAsientos

router = APIRouter()
reservation_history = []

def asiento_disponible_para_funcion(seat_id, id_funcion):
    print(f"DEBUG: seat_id={seat_id}, id_funcion={id_funcion}")
    db = next(get_db())
    HorarioAsiento = db.query(HorarioAsientos).filter(
        HorarioAsientos.asiento_id == seat_id,
        HorarioAsientos.horario_id == id_funcion,
        HorarioAsientos.Available == 1
    ).first()
    return HorarioAsiento is not None

def render_history():
    if not reservation_history:
        return "<p>No hay reservas registradas aún.</p>"
    recent = reservation_history[-10:]
    recent.reverse()
    html = ""
    for r in recent:
        html += f"""
        <div class="action-item">
            <div class="action-time">⏰ {r['timestamp']}</div>
            <div class="action-description">
                {r['cliente']} reservó <b>{r['pelicula']}</b> - Asiento <b>{r['asiento']}</b> ({r['horario']}) - ${r['total']}
            </div>
            <div class="action-details">
                Método de pago: {r['metodo_pago']}
            </div>
        </div>
        """
    return html

@router.api_route("/confirmar_pago_web/", methods=["GET", "POST"], response_class=HTMLResponse)
async def confirmar_pago_web(request: Request):
    if request.method == "GET":
        # Obtén los parámetros de la URL
        params = request.query_params
        client_id = params.get("client_id")
        id_funcion = params.get("id_funcion")
        seat_id = params.get("seat_id")
        movie_name = params.get("movie_name")
        showtime_string = params.get("showtime_string")
        imagen = params.get("imagen")
        cliente_nombre = params.get("cliente_nombre")
        costo_entrada = params.get("costo_entrada")
        metodo_pago = params.get("metodo_pago")
        cliente_email = params.get("cliente_email")
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CineMaster - Confirmar Reserva</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 700px;
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    padding: 30px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    text-align: center;
                }}
                h1 {{
                    color: #00bfff;
                    margin-bottom: 16px;
                }}
                .info {{
                    margin-bottom: 24px;
                    font-size: 18px;
                }}
                button {{
                    background: #00bfff;
                    color: #fff;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 32px;
                    font-size: 18px;
                    cursor: pointer;
                    transition: background 0.2s;
                }}
                button:hover {{
                    background: #0099cc;
                }}
                .history-section {{
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    padding: 20px;
                    margin-top: 30px;
                }}
                .history-title {{
                    font-size: 1.5rem;
                    margin-bottom: 20px;
                    border-bottom: 2px solid rgba(255, 255, 255, 0.3);
                    padding-bottom: 10px;
                }}
                .action-item {{
                    background: rgba(255, 255, 255, 0.1);
                    margin-bottom: 10px;
                    padding: 15px;
                    border-radius: 8px;
                    border-left: 4px solid #4CAF50;
                    text-align: left;
                }}
                .action-time {{
                    font-size: 0.9rem;
                    opacity: 0.8;
                    margin-bottom: 5px;
                }}
                .action-description {{
                    font-size: 1.1rem;
                    font-weight: 500;
                }}
                .action-details {{
                    font-size: 0.9rem;
                    opacity: 0.7;
                    margin-top: 5px;
                }}
                .refresh-btn {{
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 1rem;
                    margin-top: 20px;
                }}
                .refresh-btn:hover {{
                    background: #45a049;
                }}
            </style>
            <script>
                setTimeout(function(){{
                    location.reload();
                }}, 10000);
            </script>
        </head>
        <body>
            <div class="container">
                <h1>Confirmar compra</h1>
                <div class="info">
                    <p><b>Cliente:</b> {cliente_nombre}</p>
                    <p><b>Película:</b> {movie_name}</p>
                    <p><b>Asiento:</b> {seat_id}</p>
                    <p><b>Horario:</b> {showtime_string}</p>
                    <p><b>Método de pago:</b> {metodo_pago}</p>
                    <p><b>Total:</b> ${costo_entrada}</p>
                </div>
                <form action="/confirmar_pago_web/" method="post">
                    <input type="hidden" name="client_id" value="{client_id}">
                    <input type="hidden" name="id_funcion" value="{id_funcion}">
                    <input type="hidden" name="seat_id" value="{seat_id}">
                    <input type="hidden" name="movie_name" value="{movie_name}">
                    <input type="hidden" name="showtime_string" value="{showtime_string}">
                    <input type="hidden" name="imagen" value="{imagen}">
                    <input type="hidden" name="cliente_nombre" value="{cliente_nombre}">
                    <input type="hidden" name="costo_entrada" value="{costo_entrada}">
                    <input type="hidden" name="metodo_pago" value="{metodo_pago}">
                    <input type="hidden" name="cliente_email" value="{cliente_email}">
                    <button type="submit">Confirmar compra</button>
                </form>
                <div class="history-section">
                    <div class="history-title">📋 Historial de Reservas</div>
                    {render_history()}
                </div>
                <button class="refresh-btn" onclick="location.reload()">🔄 Actualizar</button>
            </div>
        </body>
        </html>
        """
    elif request.method == "POST":
        form = await request.form()
        client_id = form.get("client_id")
        id_funcion = form.get("id_funcion")
        seat_id = form.get("seat_id")
        movie_name = form.get("movie_name")
        showtime_string = form.get("showtime_string")
        imagen = form.get("imagen")
        cliente_nombre = form.get("cliente_nombre")
        costo_entrada = form.get("costo_entrada")
        metodo_pago = form.get("metodo_pago")
        cliente_email = form.get("cliente_email")

        db = next(get_db())  # Usa una sola sesión

        try:
            if not asiento_disponible_para_funcion(seat_id, id_funcion):
                raise ValueError("El asiento no está disponible para este horario o ya fue reservado.")

            reserve_command = ReserveSeatCommand(client_id, id_funcion, seat_id, db)
            reserva = reserve_command.execute()

            # Recarga la reserva con join para traer la relación client
            reserva = db.query(Reserva_asientos).join(Reserva_asientos.reserva).join("reserva", "client").filter(
                Reserva_asientos.reservationseat_id == reserva.reservationseat_id
            ).first()

            receipt_controller = ReceiptController()
            receipt_controller.generar_boleta(movie_name, showtime_string, seat_id, imagen, cliente_nombre)
            receipt_controller.confirmar_boleta()
            email_sender = EmailSenderObserver()
            email_sender.update(reserva)
            reservation_history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "cliente": cliente_nombre,
                "pelicula": movie_name,
                "asiento": seat_id,
                "horario": showtime_string,
                "metodo_pago": metodo_pago,
                "total": costo_entrada
            })
            return f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>¡Compra confirmada!</title>
                <style>
                    body {{ background: #181c24; color: #fff; font-family: Arial, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }}
                    .container {{ background: #232a36; border-radius: 16px; padding: 32px 40px; box-shadow: 0 4px 24px #0008; text-align: center; }}
                    h1 {{ color: #00ff99; margin-bottom: 16px; }}
                    .info {{ margin-bottom: 24px; font-size: 18px; }}
                    a, .refresh-btn {{ background: #00bfff; color: #fff; border: none; border-radius: 8px; padding: 12px 32px; font-size: 18px; text-decoration: none; transition: background 0.2s; margin-top: 20px; display: inline-block; }}
                    a:hover, .refresh-btn:hover {{ background: #0099cc; }}
                    .history-section {{
                        background: rgba(255, 255, 255, 0.1);
                        border-radius: 10px;
                        padding: 20px;
                        margin-top: 30px;
                    }}
                    .history-title {{
                        font-size: 1.5rem;
                        margin-bottom: 20px;
                        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
                        padding-bottom: 10px;
                    }}
                    .action-item {{
                        background: rgba(255, 255, 255, 0.1);
                        margin-bottom: 10px;
                        padding: 15px;
                        border-radius: 8px;
                        border-left: 4px solid #4CAF50;
                        text-align: left;
                    }}
                    .action-time {{
                        font-size: 0.9rem;
                        opacity: 0.8;
                        margin-bottom: 5px;
                    }}
                    .action-description {{
                        font-size: 1.1rem;
                        font-weight: 500;
                    }}
                    .action-details {{
                        font-size: 0.9rem;
                        opacity: 0.7;
                        margin-top: 5px;
                    }}
                </style>
                <script>
                    setTimeout(function(){{
                        location.href = '/confirmar_pago_web/';
                    }}, 5000);
                </script>
            </head>
            <body>
                <div class="container">
                    <h1>¡Compra confirmada!</h1>
                    <div class="info">
                        <p>La boleta ha sido generada y enviada a tu correo.</p>
                    </div>
                    <div class="history-section">
                        <div class="history-title">📋 Historial de Reservas</div>
                        {render_history()}
                    </div>
                    <a href="/confirmar_pago_web/">Volver</a>
                    <button class="refresh-btn" onclick="location.reload()">🔄 Actualizar</button>
                </div>
            </body>
            </html>
            """
        except ValueError as e:
            return HTMLResponse(
                f"""
                <!DOCTYPE html>
                <html lang="es">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Error en la reserva - CineMaster</title>
                    <style>
                        body {{
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                            margin: 0;
                            padding: 20px;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            min-height: 100vh;
                        }}
                        .container {{
                            max-width: 700px;
                            margin: 0 auto;
                            background: rgba(255, 255, 255, 0.1);
                            border-radius: 15px;
                            padding: 30px;
                            backdrop-filter: blur(10px);
                            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                            text-align: center;
                        }}
                        h1 {{
                            color: #ff4444;
                            margin-bottom: 16px;
                        }}
                        .info {{
                            margin-bottom: 24px;
                            font-size: 18px;
                        }}
                        a, .refresh-btn {{
                            background: #00bfff;
                            color: #fff;
                            border: none;
                            border-radius: 8px;
                            padding: 12px 32px;
                            font-size: 18px;
                            text-decoration: none;
                            transition: background 0.2s;
                            margin-top: 20px;
                            display: inline-block;
                        }}
                        a:hover, .refresh-btn:hover {{
                            background: #0099cc;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>❌ Error en la reserva</h1>
                        <div class="info">
                            <p>{str(e)}</p>
                        </div>
                        <a href="/confirmar_pago_web/">Volver</a>
                        <button class="refresh-btn" onclick="location.reload()">🔄 Actualizar</button>
                    </div>
                </body>
                </html>
                """,
                status_code=400
            )