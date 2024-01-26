CREATE OR REPLACE FUNCTION MensagensLidas (idCliente INTEGER)
RETURNS TABLE (dataEnvio VARCHAR[], assunto VARCHAR[], CorpoMensagem VARCHAR[])
AS $$
DECLARE
  linha RECORD;
BEGIN
  FOR linha IN
    SELECT m.dataEnvio, m.assunto, m.CorpoMensagem
    FROM mensagem m, leitura l
    WHERE m.idMensagem = l.idMensagem
    AND l.idCliente = MensagensLidas.idCliente
    AND l.lida = true
  LOOP
    dataEnvio[1] := linha.dataEnvio;
    assunto[1] := linha.assunto;
    CorpoMensagem[1] := linha.CorpoMensagem;
    RETURN NEXT;
  END LOOP;

  RETURN;
END;
$$ LANGUAGE plpgsql;

