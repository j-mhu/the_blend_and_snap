import numpy as np

N_MOVIES = 17770
N_USERS	 = 458293

def movies_per_user():
	"""
	Returns an array of length N_USERS, with all the movies each user has rated. 
	"""
	filename = "../data/um/valid.dta"
	n_mi_file = "../data/um/movies_per_user.dta"
	movie_file = "../data/um/user_per_movie.dta"
	rate_file = "../data/um/time_and_rate.dta"

	users = [[] for y in range(N_USERS)]
	movies = [[] for y in range(N_MOVIES)]
	ratings = [[] for y in range(N_USERS)]

	print("Starting movies_per_user ")
	with open(filename, "r") as all_um, \
	open(n_mi_file, "w") as n_file, \
	open(movie_file, "w") as m_file, \
	open(rate_file, "w") as r_file:
		print("Loading n_mi")

		for i, line in enumerate(all_um):
			if i % 100000 == 0:
				print("Finished line " + str(i))
			fields = line.split(' ')
			if len(fields) == 4:
				user_id = int(fields[0]) # Offset by 1 of index
				movie_id = int(fields[1]) # Offset by 1 of index
				time_id = int(fields[2])
				rate_id = int(fields[3])
				users[user_id - 1].append(movie_id) # keep list of all movies review by a user(row)
				movies[movie_id - 1].append(user_id)
				ratings[user_id - 1].append([time_id, rate_id])

		print("Writing to movies_per_user file")
		for i in range(len(users)):
			if i % 100000 == 0:
				print("Finished user " + str(i))
			user_l = str(i+1) + ' ' + str(users[i]) + '\n'
			n_file.write(user_l)

		print("Writing to user_per_movie file")
		for i in range(len(movies)):
			if i % 10000 == 0:
				print("Finished movie " + str(i))
			movie_l = str(i+1) + ' ' + str(movies[i]) + '\n'
			m_file.write(movie_l)

		print("Writing to time_and_rate file")
		for i in range(len(ratings)):
			if i % 100000 == 0:
				print("Finished user " + str(i))
			rate_l = str(i+1) + ' ' + str(ratings[i]) + '\n'
			r_file.write(rate_l)

	print("END OF movies_per_user")
	return users, movies

def get_n_mi(users, movies):
	print("Starting get_n_mi")
	m_shared = np.zeros((N_MOVIES, N_MOVIES))
	for i in range(len(movies)):
		if i % 10000 == 0:
			print("Finished user " + str(i))
		for j in range(i + 1, len(movies)):
			i_len = len(movies[i])
			j_len = len(movies[j])
			all_users = set(movies[i] + movies[j])
			m_shared[i][j] += len(set(movies[i]).intersection(movies[j]))
	
	filename = "../data/um/n_mi.dta"
	with open(filename, "w") as file:
		print("Writing n_mi to file ")
		for i in range(N_MOVIES):
			if i % 100000 == 0:
				print("Finished user " + str(i))
			user_l = str(i+1) + ' ' + str(m_shared[i]) + '\n'
			file.write(user_l)

	print("END OF get_n_mi")
	return m_shared

users, movies = movies_per_user()
m_shared = get_n_mi(users, movies)