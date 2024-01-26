ALTER TABLE leitura
	ADD CONSTRAINT leitura_FKcliente FOREIGN KEY (idCliente) REFERENCES cliente(idCliente),
	ADD CONSTRAINT leitura_FKmensagem FOREIGN KEY (idMensagem) REFERENCES mensagem(idMensagem);
	

ALTER TABLE mensagem
ADD CONSTRAINT mensagem_FKadministrador FOREIGN KEY (idAdmin) REFERENCES administrador(idAdmin);


ALTER TABLE preco
	ADD CONSTRAINT preco_FKviagem FOREIGN KEY (idViagem) REFERENCES viagem(idViagem);


ALTER TABLE reserva
	ADD CONSTRAINT reserva_FKviagem FOREIGN KEY (idViagem) REFERENCES viagem(idViagem),
	ADD CONSTRAINT reserva_FKcliente FOREIGN KEY (idCliente) REFERENCES cliente(idCliente);


ALTER TABLE viagem
	ADD CONSTRAINT viagem_FKorigem FOREIGN KEY (idOrigem) REFERENCES estacao(idEstacao),
	ADD CONSTRAINT viagem_FKdestino FOREIGN KEY (idDestino) REFERENCES estacao(idEstacao),
	ADD CONSTRAINT viagem_FKautocarro FOREIGN KEY (idAutocarro) REFERENCES autocarro(idAutocarro);