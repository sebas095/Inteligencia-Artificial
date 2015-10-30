def read():
	# recibimos la longitud del tablero NxN
	n = int(input())
	tmp = []
	table = []
	#entrada por teclado o archivo:
	for i in range(n):
		tmp.append(raw_input())

	#convertimos el string a una matriz por ahora de caracteres
	for i in range(len(tmp)):
		table.append(tmp[i].split(" "))
	
	#casteamos los caracteres a enteros
	for i in range(len(table)):
		for j in range(len(table[i])):
			aux = int(table[i][j])
			table[i][j] = aux

	return table
