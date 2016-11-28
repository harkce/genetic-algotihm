import random

# referensi : http://www.firman-its.com/2007/05/17/algoritma-genetika-dan-contoh-aplikasinya/
# S = 0, A = 1, B = 2, B = 3, C = 3, D = 4, E = 5, F = 6, G = 7
graph = [	
		[0,	0.1,	0.233,	0.167,	0,	0,	0,	0],
		[0.1,	0,	0.1,	0,	0.4,	0,	0,	0],
		[0.233,	0.1,	0,	0.067,	0,	0.25,	0,	0],
		[0.167,	0,	0.067,	0,	0,	0,	0.3,	0],
		[0,	0.4,	0,	0,	0,	0.067, 	0,	0.15],
		[0,	0,	0.25,	0,	0.067,	0,	0.067,	0.15],
		[0,	0,	0,	0.3,	0,	0.067,	0,	0.15],
		[0,	0,	0,	0,	0.15,	0.15,	0.15,	0],
	]

#init populasi
def init(populasi):
	res = list()
	for x in xrange(0,populasi):
		individu = [0]
		gen = [random.randint(0,7) for y in xrange(0,7)]
		individu += gen
		res.append(individu)
	return res

# fungsi objektif
def bobot(gene):
	bobot = 0.0
	hitung = len(gene) - 1
	i = 0
	berbobot = True
	finish = False
	while (berbobot) and (i < hitung) and not(finish):
		jarak = graph[ gene[i] ][ gene[i + 1] ]
		if (jarak == 0.0):
			berbobot = False
			bobot = 0.0
		else:
			bobot += jarak
			i += 1
			if gene[i] == 7:
				finish = True
	if not(finish):
		bobot = 0.0
	return bobot

# hitung fitness
def fitness(gene):
	besar = bobot(gene)
	if (besar == 0.0):
		besar += 1
	return 1/besar

# probability untuk roulette
def prob(i, fit, sumfit):
	return fit[i] / sumfit

# parent generator
def genparent(rate, populasi):
	parent = list()
	k = 0
	pops = len(populasi)
	for x in xrange(0,pops):
		roulette = random.random()
		if roulette < rate:
			parent.append([x, populasi[k]])
		k += 1
	return parent

# kawin gan
def crossover(ayah, ibu, cutpoint):
	ayah = list(ayah)
	ibu = list(ibu)
	ayah[cutpoint] = ibu[cutpoint]
	return ayah

# x-men bukan?
def checkmutation(child):
	child = list(child)
	lenchild = len(child)
	mutation_rate = 0.01
	for x in xrange(1,lenchild):
		if (random.random() < mutation_rate):
			end = 7
			child[x] = random.choice(range(1,child[x]) + range(child[x] + 1, end))
	return child

# convert angka ke route
def showroute(ind):
	route = list()
	for x in ind:
		if (x == 0):
			route.append('S')
		if (x == 1):
			route.append('A')
		if (x == 2):
			route.append('B')
		if (x == 3):
			route.append('C')
		if (x == 4):
			route.append('D')
		if (x == 5):
			route.append('E')
		if (x == 6):
			route.append('F')
		if (x == 7):
			route.append('G')
			return route

# main
def main(populasi, generation):
	pops = init(populasi)

	highfit = 0
	ind = list()
	for x in xrange(0, populasi):
		fitx = fitness(pops[x])
		if fitx > highfit:
			ind = list(pops[x])
			highfit = fitx

	for a in range(0, generation):
		fit = list(fitness(x) for x in pops)
		sumfit = sum(fit)

		probs = list(prob(i, fit, sumfit) for i in xrange(0, populasi))
		cumprobs = list()

		cumprobs.append(probs[0])
		for x in xrange(1,populasi - 1):
			cumprobs.append(cumprobs[x - 1] + probs[x])
		cumprobs.append(1.0)

		roulette = list(random.random() for x in xrange(0,populasi))

		newgen = list()

		for x in xrange(0,populasi):
			ketemu = False
			i = 0
			while not(ketemu):
				if roulette[x] < cumprobs[i]:
					ketemu = True
					newgen.append(pops[i])
				else:
					i += 1

		crossrate = 0.25
		parent = genparent(crossrate, newgen)

		jmlcross = len(parent)
		if (jmlcross <= 2) and (jmlcross > 0):
			jmlcross = 1

		for x in xrange(0,jmlcross):
			ayah = parent[x][1]
			if (x != (jmlcross - 1)):
				ibu = parent[x+1][1]
			else:
				ibu = parent[0][1]
			cutpoint = random.randint(1,7)
			child = crossover(ayah, ibu, cutpoint)
			child = checkmutation(child)
			newgen[parent[x][0]] = child

		pops = newgen
		maxfit = 0
		uhuy = pops[0]
		for x in xrange(0,populasi):
			fitx = fitness(pops[x])
			if fitx > maxfit:
				uhuy = list(newgen[x])
				maxfit = fitx

		if maxfit > highfit:
			ind = list(uhuy)
			highfit = maxfit

	route = showroute(ind)

	if (highfit == 1.0):
		print 'No route found'
	else:
		print 'Highest fitness', highfit, 'with route', route

main(200,5)
