CREATE TABLE autocarro (
	idAutocarro SERIAL PRIMARY KEY,
	matricula VARCHAR(20) NOT NULL UNIQUE,
	lotacaoMax INTEGER NOT NULL
);

INSERT INTO autocarro (matricula, lotacaoMax)
VALUES
  ('ABC-1234', 40),		--1
  ('DEF-5678', 35),		--2
  ('GHI-9012', 45),		--3
  ('JKL-3456', 30),		--4
  ('MNO-7890', 50),		--5
  ('PQR-2345', 40),		--6
  ('STU-6789', 35),		--7
  ('VWX-1234', 45),		--8
  ('YZA-5678', 30),		--9
  ('BCD-9012', 50),		--10
  ('EFG-3456', 40),		--11
  ('HIJ-7890', 35),		--12
  ('KLM-2345', 45),		--13
  ('NOP-6789', 30),		--14
  ('QRS-1234', 50),		--15
  ('TUV-5678', 40),		--16
  ('WXY-9012', 35),		--17
  ('ZAB-3456', 45),		--18
  ('CDE-7890', 30);		--19