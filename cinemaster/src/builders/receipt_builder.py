class ReceiptBuilder:
    def __init__(self):
        self._movie_name = None
        self._showtime = None
        self._seat = None
        self._client_name = None
        self._image = None

    def set_movie_name(self, movie_name):
        self._movie_name = movie_name
        return self

    def set_showtime(self, showtime):
        self._showtime = showtime
        return self

    def set_seat(self, seat):
        self._seat = seat
        return self

    def set_client_name(self, client_name):
        self._client_name = client_name
        return self

    def set_image(self, image):
        self._image = image
        return self

    def build(self):
        # Aquí puedes crear el objeto boleta usando los datos acumulados
        from views.generarBoleta import generarBoleta
        boleta = generarBoleta(
            self._movie_name,
            self._showtime,
            self._seat,
            self._image,
            self._client_name or "Cliente"
        )
        return boleta
