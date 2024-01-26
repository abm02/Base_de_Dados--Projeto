CREATE OR REPLACE FUNCTION MensagensNaoLidas (idCliente INTEGER)
RETURNS TABLE (dataEnvio VARCHAR[], assunto VARCHAR[], CorpoMensagem VARCHAR[])
AS $$
DECLARE
  linha RECORD;
BEGIN
  FOR linha IN
    SELECT m.dataEnvio, m.assunto, m.CorpoMensagem
    FROM mensagem m, leitura l
    WHERE m.idMensagem = l.idMensagem
    AND l.idCliente = MensagensNaoLidas.idCliente
    AND l.lida = false
  LOOP
    dataEnvio[1] := linha.dataEnvio;
    assunto[1] := linha.assunto;
    CorpoMensagem[1] := linha.CorpoMensagem;
    RETURN NEXT;
  END LOOP;
  
  UPDATE leitura
	SET lida = true
	WHERE leitura.idCliente = MensagensNaoLidas.idCliente
	AND lida = false;

  RETURN;
END;
$$ LANGUAGE plpgsql;

