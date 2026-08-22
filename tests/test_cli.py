from conversor.cli import ejecutar


def test_cli_convertir_usd_a_mxn(capsys):
    codigo = ejecutar(["convertir", "100", "USD", "MXN"])
    salida = capsys.readouterr()
    assert codigo == 0
    assert "1715.00 MXN" in salida.out


def test_cli_divisa_no_soportada(capsys):
    codigo = ejecutar(["convertir", "10", "USD", "XYZ"])
    salida = capsys.readouterr()
    assert codigo == 3
    assert "no soportada" in salida.err.lower()


def test_cli_monto_invalido(capsys):
    codigo = ejecutar(["convertir", "abc", "USD", "MXN"])
    assert codigo == 2
    assert "inválido" in capsys.readouterr().err.lower()


def test_cli_lista_divisas(capsys):
    codigo = ejecutar(["divisas"])
    salida = capsys.readouterr().out
    assert codigo == 0
    assert "USD" in salida
    assert "MXN" in salida


def test_cli_sin_comando_muestra_ayuda(capsys):
    codigo = ejecutar([])
    assert codigo == 1
    assert "Convierte montos" in capsys.readouterr().out
