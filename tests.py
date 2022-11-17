from collections import Counter
from statistics import NormalDist


def test_check_equlity(vect, a):
    m = len(vect)
    n = m / 256
    byte_count = Counter(vect)
    l = 255
    
    for i in range(256):
        stat = sum([((byte_count[j] - n)**2)/n for j in range(1,255)])
        gran_stat = ((2*255)**0.5) * NormalDist().inv_cdf(1-a) + l
        
    return stat <= gran_stat, stat, gran_stat

def test_check_independ(vect, a):
    n = len(vect)//2
    stat = 0
    l = 255**2
    
    pair = [(vect[2*i], vect[2*i+1]) for i in range(n-1)]
    
    count_pair = Counter(pair)
    count_first = Counter(vect[::2])
    count_second = Counter(vect[1::2])
    
    for i in count_pair:
        v_ij = count_pair[i]
        v_i = count_first[i[0]]
        a_j = count_second[i[1]]
        if v_i == 0 or a_j == 0:
            continue
        stat += ((v_ij**2)/(v_i*a_j)-1)
    
    stat *= n
    gran_stat = ((2*255)**0.5) * NormalDist().inv_cdf(1-a) + l
    return stat <= gran_stat, stat, gran_stat

def test_check_homog(vect, a):
    n = len(vect)
    r = int(n**0.5) + 1
    inter_len = n//r
    l = 255*(r-1)
    stat = 0
    
    inter_count =  [Counter(vect[inter_len*i:inter_len*(i+1)]) for i in range(r)]
    byte_count = Counter(vect)
    for i in inter_count:
        for j in i:
            v_ij = i[j]
            v_i = byte_count[j]
            stat+= ((v_ij**2)/(v_i * inter_len)) - 1

    stat*=n
    gran_stat = ((2*255)**0.5) * NormalDist().inv_cdf(1-a) + l
    return stat <= gran_stat, stat, gran_stat
    
