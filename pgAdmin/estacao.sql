CREATE TABLE estacao(
	idEstacao SERIAL PRIMARY KEY,
	nomeEstacao Text NOT NULL UNIQUE
);

INSERT INTO estacao(nomeEstacao)
VALUES
--Coimbra=1 ; Aveiro=2 ; Lisbon=3 ; Porto=4 ; Braga=5 ; Castelo Branco=6 ; Chaves=7 ; Évora=8 ; Faro=9 ; 
-- Guimarães=10 ; Leiria=11 ; Portimão=12 ; Santarém=13 ; Viana do Castelo=14
  ('Coimbra'),
  ('Aveiro'),
  ('Lisbon'),
  ('Porto'),
  ('Braga'),
  ('Castelo Branco'),
  ('Chaves'),
  ('Évora'),
  ('Faro'),
  ('Guimarães'),
  ('Leiria'),
  ('Portimão'),
  ('Santarém'),
  ('Viana do Castelo');