import math

TF_BINARY = 0
TF_RAW_FREQ = 1
TF_LOG_NORM = 2
TF_DBL_NORM = 3
TF_DBL_NORM_K = 4

ICF_UNARY = 0
ICF_INV_FREQ = 1
ICF_INV_FREQ_S = 2
ICF_INV_FREQ_MAX = 3
ICF_PROB_INV_FREQ = 4

####
# TF variants - From Wikipedia
#####
# binary	{0,1}
# raw frequency	 f_{t,d}
# log normalization	 1 + \log f_{t,d}
# double normalization 0.5	0.5 + 0.5 \frac { f_{t,d} }{\max {f_{t,d}}} 
# double normalization K	K + (1 - K) \frac { f_{t,d} }{\max {f_{t,d}}} 


def calc_tf(n, max_n, opt, k):
	
	if(opt == TF_BINARY):
		if(n > 0):
			return 1
		else:
			return 0
	
	elif(opt == TF_RAW_FREQ):
		return n
	
	elif(opt == TF_LOG_NORM):
		return 1 + math.log(n)

	elif(opt == TF_DBL_NORM):
		return 0.5 + 0.5* (n/max_n)

	elif(opt == TF_DBL_NORM_K):
		return k + (1-k)*(n/max_n)

	else:
		raise Exception("Invalid TF calculation option")
		return -1

####
# IDF variants - From Wikipedia
#####
# unary	1
# inverse frequency	 \log \frac {N} {n_t} 
# inverse frequency smooth	 \log (1 + \frac {N} {n_t}) 
# inverse frequency max	 \log (1 + \frac {\max_t n_t} {n_t}) 
# probabilistic inverse frequency	 \log  \frac {N - n_t} {n_t} 

def calc_icf(n_t, max_n_t, N, opt):

	if(ICF_UNARY == opt):
		return 1

	elif(ICF_INV_FREQ == opt):
		return math.log(N/n_t)

	elif(ICF_INV_FREQ_S == opt):
		return math.log(1 + (N/n_t))

	elif(ICF_INV_FREQ_MAX == opt):
		return math.log(1 + (max_n_t/n_t))

	elif(ICF_PROB_INV_FREQ == opt):
		return math.log((N - n_t)/ n_t)

	else:
		raise Exception("Invalid TF calculation option")
		return -1








