'''
 This code was generously provided by Alexander Cowan
 and concerns his paper
Murmurations of Elliptic Curves and Explicit Formulas
'''

import sys
from sage.all import *
import cProfile
import random
import numpy
import math
import json


EPS = 10.0**(-9)
PI = float(pi)
C_FIELD = CDF
C_I = C_FIELD(I)


def main():
    tmp = kronecker_example()


def get_E_labels(Nmin, Nmax, rank, prime_only=False):
    if prime_only:
        iterable = primes(Nmin,Nmax)
    else:
        iterable = range(Nmin,Nmax)
    label_list = []
    cremona_database = CremonaDatabase()
    for N in iterable:
        label_list += [str(N)+k for k,v in sorted(cremona_database.curves(N).items()) if v[1] == rank]
    return label_list


def get_curves(label_list):
    curves = {label: EllipticCurve(label) for label in label_list}
    return curves


def get_zeroes(E, num_zeroes):
    L = E.lseries()
    zeroes = L.zeros(num_zeroes)
    return zeroes


def build_zeroes_dict(Nmin, Nmax, rank, num_zeroes, prime_only=False, zero_dict=None, omit_critical_point=True):
    if zero_dict is None:
        # pass a zero_dict to update in place
        zero_dict = {}
    label_list = get_E_labels(Nmin, Nmax, rank, prime_only=prime_only)
    curves = get_curves(label_list)
    for label, E in sorted(curves.items()):
        zeroes = get_zeroes(E, num_zeroes)
        zeroes = [z for z in zeroes if (not omit_critical_point) or (abs(z) > EPS)]
        zero_dict[label] = zeroes
    return zero_dict


def get_driving_fn(zero_list, normalizing_factor=1):
    # normalizing_factor could be 1/number of elliptic curves for averaging
    def fn(x):
        sumval = 0
        logx = C_FIELD(log(x))
        #C_x = C_FIELD(x)
        for gamma in zero_list: # gamma is imaginary part of zero on the critical line
            #term = x**(C_I*gamma) / (0.5 + C_I*gamma) + x**(-C_I*gamma) / (0.5 - C_I*gamma)
            #term = (x**(C_I*gamma) / (0.5 + C_I*gamma)).real_part() * 2 # doesn't work when x is a float
            term = (exp(C_I*gamma*logx) / (0.5 + C_I*gamma)).real_part() * 2 # this is way too slow
            #term = (C_x**(C_I*gamma) / (0.5 + C_I*gamma)).real_part() * 2 # also really slow
            sumval += term
        sumval *= normalizing_factor
        return sumval
    return fn


def get_eval_pts(eval_range, num_eval_pts):
    log_min = float(log(eval_range[0]))
    log_max = float(log(eval_range[1]))
    delta = (log_max - log_min)/num_eval_pts
    eval_pts = [exp(log_min + i*delta) for i in range(num_eval_pts)]
    return eval_pts


def eval_driving_fn(driving_fn, eval_pts=None, eval_range=(2,10000), num_eval_pts=1000, driving_fn_vals=None):
    if driving_fn_vals is None:
        # pass a dict to update in place
        driving_fn_vals = {}
    if eval_pts is None:
        eval_pts = get_eval_pts(eval_range, num_eval_pts)
    for x in eval_pts:
        if x not in driving_fn_vals:
            driving_fn_vals[x] = driving_fn(x)
    return driving_fn_vals


def build_ap_avgs(Nmin, Nmax, rank, x_max, prime_only=False, ap_avg_vals=None):
    if ap_avg_vals is None:
        # pass a dict to update in place
        # this does not validate that the same set of curves is being averaged
        ap_avg_vals = {}
    label_list = get_E_labels(Nmin, Nmax, rank, prime_only=prime_only)
    curves = get_curves(label_list)
    curve_list = [v for k,v in sorted(curves.items())]
    for p in primes(x_max):
        p_sum = 0
        for E in curve_list:
            ap_val = E.ap(p)
            p_sum += ap_val
        p_sum /= sqrt(float(p))
        avg_val = p_sum / len(curve_list)
        ap_avg_vals[p] = avg_val
    return ap_avg_vals


def eval_ap_partial_sums(ap_avg_vals, weight_at_x=0.5, eval_pts=None, eval_range=(2,10000), num_eval_pts=1000, partial_sum_vals=None):
    # weight_at_x = 0.5 means if x is prime the term is counted half
    # weight_at_x = 0 means sum_{p < x}
    # weight_at_x = 1 means sum_{p <= x}
    if partial_sum_vals is None:
        # pass a dict to update in place
        partial_sum_vals = {}
    if eval_pts is None:
        eval_pts = get_eval_pts(eval_range, num_eval_pts)
    eval_pts_set = set(eval_pts)
    x_max = eval_pts[-1]
    interesting_points = eval_pts + list(primes(int(x_max)+1))
    interesting_points = sorted(list(set(interesting_points)))
    current_partial_sum = 0
    new_sum_chunk = 0
    for x in interesting_points:
        is_prime = (x in ZZ) and (ZZ(x).is_prime())
        is_eval_pt = x in eval_pts_set
        if is_prime and (not is_eval_pt):
            new_sum_chunk += ap_avg_vals[x]
        elif is_prime and is_eval_pt:
            new_sum_chunk += weight_at_x * ap_avg_vals[x]
            current_partial_sum += new_sum_chunk
            coeff = log(float(x)) / sqrt(float(x))
            partial_sum_vals[x] = coeff * current_partial_sum
            new_sum_chunk = (1 - weight_at_x) * ap_avg_vals[x]
        elif (not is_prime) and is_eval_pt:
            current_partial_sum += new_sum_chunk
            coeff = log(float(x)) / sqrt(float(x))
            partial_sum_vals[x] = coeff * current_partial_sum
            new_sum_chunk = 0
        else:
            # ??
            raise ValueError('x = '+str(x))
    return partial_sum_vals


def read_positive_zeros(data_path='./'):
    dirlist = os.listdir(data_path)
    label_to_zeros = {}
    for fname in dirlist:
        if fname[:len('2797positivezeros')] == '2797positivezeros':
            with open(fname,'r') as f:
                data = json.load(f)
            data = data['data']
            for item in data:
                label = int(item['Lhash'].split('.')[-1])
                zeros = [float(tmp) for tmp in item['positive_zeros']]
                label_to_zeros[label] = zeros
    return label_to_zeros


def read_mureal1_labels(data_path='./'):
    dirlist = os.listdir(data_path)
    labels = []
    for fname in dirlist:
        if fname[:len('2797mureal1')] == '2797mureal1':
            with open(fname,'r') as f:
                data = json.load(f)
            data = data['data']
            for item in data:
                labels.append(int(item['Lhash'].split('.')[-1]))
    return labels


def read_conjugates(data_path='./'):
    dirlist = os.listdir(data_path)
    conjugates = {}
    for fname in dirlist:
        if fname[:len('2797conjugate')] == '2797conjugate':
            with open(fname,'r') as f:
                data = json.load(f)
            data = data['data']
            for item in data:
                label = int(item['Lhash'].split('.')[-1])
                conj = int(item['conjugate'].split('.')[-1])
                conjugates[label] = conj
    return conjugates


def build_kronecker_avgs(D_list, x_max, kronecker_avg_vals=None):
    if kronecker_avg_vals is None:
        # pass a dict to update in place
        # this does not validate that the same set is being averaged
        kronecker_avg_vals = {}
    for p in primes(x_max):
        p_sum = 0
        for D in D_list:
            kronecker_val = kronecker(D,p)
            p_sum += kronecker_val
        p_sum *= log(float(p)) # von Mangoldt
        avg_val = p_sum / len(D_list)
        kronecker_avg_vals[p] = avg_val
    return kronecker_avg_vals


def eval_kronecker_partial_sums(kronecker_avg_vals, weight_at_x=0.5, eval_pts=None, eval_range=(2,10000), num_eval_pts=1000, partial_sum_vals=None):
    # weight_at_x = 0.5 means if x is prime the term is counted half
    # weight_at_x = 0 means sum_{p < x}
    # weight_at_x = 1 means sum_{p <= x}
    if partial_sum_vals is None:
        # pass a dict to update in place
        partial_sum_vals = {}
    if eval_pts is None:
        eval_pts = get_eval_pts(eval_range, num_eval_pts)
    eval_pts_set = set(eval_pts)
    x_max = eval_pts[-1]
    interesting_points = eval_pts + list(primes(int(x_max)+1))
    interesting_points = sorted(list(set(interesting_points)))
    current_partial_sum = 0
    new_sum_chunk = 0
    for x in interesting_points:
        is_prime = (x in ZZ) and (ZZ(x).is_prime())
        is_eval_pt = x in eval_pts_set
        if is_prime and (not is_eval_pt):
            new_sum_chunk += kronecker_avg_vals[x]
        elif is_prime and is_eval_pt:
            new_sum_chunk += weight_at_x * kronecker_avg_vals[x]
            current_partial_sum += new_sum_chunk
            coeff = 1.0 / sqrt(float(x))
            partial_sum_vals[x] = coeff * current_partial_sum
            new_sum_chunk = (1 - weight_at_x) * kronecker_avg_vals[x]
        elif (not is_prime) and is_eval_pt:
            current_partial_sum += new_sum_chunk
            coeff = 1.0 / sqrt(float(x))
            partial_sum_vals[x] = coeff * current_partial_sum
            new_sum_chunk = 0
        else:
            # ??
            raise ValueError('x = '+str(x))
    return partial_sum_vals


def build_dirichlet_avgs(label_list, x_max, discrete_logs=None, dirichlet_avg_vals=None):
    if dirichlet_avg_vals is None:
        # pass a dict to update in place
        # this does not validate that the same set is being averaged
        dirichlet_avg_vals = {}
    if discrete_logs is None:
        discrete_logs = get_discrete_logs_2797()
    omega = exp(2*PI*C_I/2796) # hardcoded sorry
    for p in primes(x_max):
        p_sum = 0
        for label in label_list:
            if p != 2797:
                dirichlet_val = eval_dirichlet_char(label, p%2797, discrete_logs, omega) # also hardcoded
            else:
                dirichlet_val = 0
            p_sum += dirichlet_val
        p_sum *= log(float(p)) # von Mangoldt
        avg_val = p_sum / len(label_list)
        dirichlet_avg_vals[p] = avg_val
    return dirichlet_avg_vals


def eval_dirichlet_char(label, x, discrete_logs, omega):
    return omega**(discrete_logs[label] * discrete_logs[x])


def get_discrete_logs_2797():
    R = Integers(2797)
    discrete_logs = {int(R(2)**k) : k for k in range(2796)} # 2 is a primitive root mod 2797
    return discrete_logs


def get_zeta_zeros(T_max=200):
    chi = DirichletGroup(1)[0]
    L = chi.lfunction()
    zeta_zeros = set(L.zeros(200))
    return zeta_zeros


def get_kronecker_zeros(D_min, D_max, T_max=200, kronecker_zeros=None):
    if kronecker_zeros is None:
        # pass a dict to update in place
        # this does not validate that the same set is being averaged
        kronecker_zeros = {}
    zeta_zeros = get_zeta_zeros(T_max=T_max)
    for D in range(D_min,D_max):
        if is_fundamental_discriminant(D):
            if D not in kronecker_zeros:
                K = NumberField(ZZ['x']([-D,0,1]),'z')
                L = K.zeta_function()
                zeros = L.zeros(T_max)
                zeros = [tmp for tmp in zeros if tmp not in zeta_zeros] # Dedekind zeta function is zeta function * quadratic Dirichlet L-function
                kronecker_zeros[D] = zeros
    return kronecker_zeros


def kronecker_example():
    D_min = 9000
    D_max = 9200
    T_max = 50
    num_eval_pts = 200
    eval_range = (2,1e5)
    
    kronecker_zeros = get_kronecker_zeros(D_min, D_max, T_max=T_max)
    driving_fn = get_driving_fn(flatten(kronecker_zeros.values()), normalizing_factor=1.0/len(kronecker_zeros))
    driving_fn_vals = eval_driving_fn(driving_fn, eval_range=eval_range, num_eval_pts=num_eval_pts) # long time
    
    D_list = [tmp for tmp in range(D_min,D_max) if is_fundamental_discriminant(tmp)]
    kronecker_avg_vals = build_kronecker_avgs(D_list, eval_range[1]) # long time
    kronecker_partial_sums = eval_kronecker_partial_sums(kronecker_avg_vals, eval_range=eval_range) # semi-long time
    driving_fn_vals_withlog = [(k, v + log(float(k))/sqrt(k)) for k,v in driving_fn_vals.items()]

    pts_kronecker_partial_sums = points(kronecker_partial_sums.items(), dpi=400, size=3, color='blue', legend_color='black', legend_label=r'Average partial sums  $\frac{1}{\sqrt{x}}\sum_{p<x}^{\,} \,\,\left(\frac{D}{p}\right)\log{\,p}$')
    pts_dfd_withlog = points(driving_fn_vals_withlog, dpi=400, size=3, color='darkgoldenrod', legend_color='black', legend_label=r'Average explicit formula  $\frac{\log{\,x}}{\sqrt{x}} + \sum_{\gamma}^{\,} \,\,\frac{x^{i\gamma}}{\frac{1}{2} + i\gamma}$')
    pts_kronecker_partial_sums.set_legend_options(markerscale=3.0)
    pts_dfd_withlog.set_legend_options(markerscale=3.0)
    show(pts_kronecker_partial_sums + pts_dfd_withlog, title='Primitive quadratic Dirichlet characters with conductor %i - %i' % (D_min, D_max), scale='semilogx')

    show(histogram([tmp for tmp in flatten(kronecker_zeros.values()) if tmp < 15], dpi=400, bins=200, color='blue'))

    to_ret = [kronecker_zeros, driving_fn_vals, kronecker_avg_vals, kronecker_partial_sums, driving_fn_vals_withlog]
    return to_ret



#This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    if '-profile' in sys.argv:
        cProfile.run('main()')
    else:
        main()
