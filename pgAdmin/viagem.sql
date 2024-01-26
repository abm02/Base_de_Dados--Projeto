CREATE TABLE viagem (
	idViagem SERIAL PRIMARY KEY, 
	detalhes TEXT,
	distancia FLOAT NOT NULL,
	dataViagem TIMESTAMP NOT NULL,
	duracaoViagem INTERVAL,
	numLugDisp INTEGER NOT NULL,
	numListaEspera INTEGER NOT NULL,
	idOrigem INTEGER NOT NULL,
	idDestino INTEGER NOT NULL,
	idAutocarro INTEGER NOT NULL

-- 	CONSTRAINT viagem_FKorigem FOREIGN KEY (idOrigem) REFERENCES estacao(idEstacao),
-- 	CONSTRAINT viagem_FKdestino FOREIGN KEY (idDestino) REFERENCES estacao(idEstacao),
-- 	CONSTRAINT viagem_FKautocarro FOREIGN KEY (idAutocarro) REFERENCES autocarro(idAutocarro)
);

INSERT INTO viagem (detalhes, distancia, dataViagem, duracaoViagem, numLugDisp, numListaEspera,idOrigem, idDestino, idAutocarro)
VALUES
--Coimbra=1 ; Aveiro=2 ; Lisbon=3 ; Porto=4 ; Braga=5 ; Castelo Branco=6 ; Chaves=7 ; Évora=8 ; Faro=10 ; 
-- Guimarães=11 ; Leiria=12 ; Portimão=13 ; Santarém=14 ; Viana do Castelo=15
('Coimbra to Aveiro', 60, '2023-05-01 10:00:00', '02:00:00', 40, 0, 1, 2, 1), 	--sem reservas
('Aveiro to Coimbra', 60, '2023-05-01 15:00:00', '02:00:00', 25, 0, 2, 1, 2),
('Coimbra to Lisbon', 210, '2023-05-02 08:00:00', '03:30:00', 5, 0, 1, 3, 3),
('Lisbon to Coimbra', 210, '2023-05-02 15:00:00', '03:30:00', 0, 0, 3, 1, 4),
('Coimbra to Porto', 120, '2023-05-03 09:00:00', '02:30:00', 24, 0, 1, 4, 5),
('Porto to Coimbra', 120, '2023-05-03 16:00:00', '02:30:00', 0, 3, 4, 1, 6),
('Coimbra to Braga', 200, '2023-05-04 10:00:00', '04:00:00', 3, 0, 1, 5, 7),
('Braga to Coimbra', 200, '2023-05-04 19:00:00', '04:00:00', 17, 0, 5, 1, 8),
('Coimbra to Castelo Branco', 120, '2023-05-05 08:00:00', '02:30:00', 15, 0, 1, 6, 9),
('Castelo Branco to Coimbra', 120, '2023-05-05 15:00:00', '02:30:00', 0, 8, 6, 1, 10),
('Coimbra to Chaves', 360, '2023-05-06 11:00:00', '06:00:00', 20, 0, 1, 7, 11),
('Chaves to Coimbra', 360, '2023-05-06 21:00:00', '06:00:00', 27, 0, 7, 1, 12),
('Coimbra to Évora', 280, '2023-05-07 08:00:00', '05:00:00', 44, 0, 1, 8, 13),
('Évora to Coimbra', 280, '2023-05-07 17:00:00', '05:00:00', 30, 0, 8, 1, 14), 	--sem reservas
('Coimbra to Faro', 430, '2023-05-08 09:00:00', '06:00:00', 1, 0, 1, 9, 15),
('Faro to Coimbra', 430, '2023-05-08 18:00:00', '06:00:00', 0, 2, 9, 1, 16),
('Coimbra to Guimarães', 180, '2023-05-09 10:00:00', '03:00:00', 5, 0, 1, 10, 17),
('Guimarães to Coimbra', 180, '2023-05-09 16:00:00', '03:00:00', 0, 12, 10, 1, 18),
('Coimbra to Leiria', 40, '2023-05-10 08:00:00', '01:00:00', 6, 0, 1, 11, 19),
('Leiria to Coimbra', 40, '2023-05-10 12:00:00', '01:00:00', 14, 0, 11, 1, 1),
('Coimbra to Portimão', 480, '2023-06-11 09:00:00', '07:00:00', 26, 0, 1, 12, 6),
('Portimão to Coimbra', 480, '2023-06-11 19:00:00', '07:00:00', 0, 4, 12, 1, 9),
('Coimbra to Santarém', 140, '2023-06-12 08:00:00', '02:30:00', 30, 0, 1, 13, 4), 	--sem reservas
('Santarém to Coimbra', 140, '2023-06-12 15:00:00', '02:30:00', 33, 0, 13, 1, 2),
('Coimbra to Viana do Castelo', 270, '2023-11-13 10:00:00', '04:30:00', 21, 0, 1, 14, 14),
('Viana do Castelo to Coimbra', 270, '2023-12-13 18:00:00', '04:30:00', 0, 0, 14, 1, 19);