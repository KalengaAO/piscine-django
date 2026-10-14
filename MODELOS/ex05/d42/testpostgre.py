import psycopg2


def connecte():
	conn = None

	try:
		conn = psycopg2.connect(
			dbname="testdb",
			user="akalenga",
			password="secred",
			port=5432,
			host="localhost",
		)
		print("Conexão estabelecida!")
		conn.close()
	except psycopg2.OperationalError as error:
		print(f"Erro de conexão: {error}")

if __name__ == "__main__":
	connecte()