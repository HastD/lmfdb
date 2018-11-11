#compare on load

filename = '/scratch/importing/mf_dim20_hecke_cc_3000.txt'
cols_header = 'hecke_orbit_code:lfunction_label:conrey_label:embedding_index:embedding_m:embedding_root_real:embedding_root_imag:an:first_an:angles:first_angles'
drew_dim12 = {}
cols = cols_header.split(':')
def compare_floats(a, b, prec = 52):
    if b == 0:
        b, a = a, b
    if a == 0:
        return b == 0 or abs(b) < 1e-60
    else:
        return log(abs((a - b)/a))/log(2.) < -prec
def compare_row(a, b, verbose = True):
    for i,c in enumerate(cols):
        if c in ['hecke_orbit_code', 'conrey_label','embedding_index','embedding_m']:
            if a[i] != b[i]:
                print c, a[i], b[i]
                return False
        elif c in ['embedding_root_real', 'embedding_root_imag']:
            if not compare_floats(a[i], b[i]):
                print c, a[i], b[i], a[i] - b[i]
                return False
        elif c in ['an', 'first_an']:
            for j, ((ax, ay), (bx, by)) in enumerate(zip(a[i],b[i])):
                if not compare_floats(ax, bx):
                    print c, j, ax, bx, ax-bx
                    if ax != 0:
                        print log(abs((ax - bx)/ax))/log(2.)
                    return False
                if not compare_floats(ay, by):
                    print c, j, ay, by, ay-by
                    if ay != 0:
                        print log(abs((ay - by)/ay))/log(2.)
                    return False
        elif c in ['angles', 'first_angles']:
            for j, ((ap, at), (bp, bt)) in enumerate(zip(a[i],b[i])):
                if ap != bp:
                    print c, j, ap, bp
                    return False
                if not compare_floats(at, bt):
                    print c, j, ap, at, bt, at-bt
                    if at !=0:
                        print log(abs((at - bt)/at))/log(2.)
                    return False
    return True
        
            
            
        
with open(filename, 'r') as F:
    for i, line in enumerate(F.readlines()):
        if i < 3:
            pass
        else:
            linesplit = line[:-1].split(':')
            for i, c in enumerate(cols):
                if c in ['hecke_orbit_code', 'conrey_label','embedding_index','embedding_m']:
                    linesplit[i] = int(linesplit[i])
                elif c in ['embedding_root_real', 'embedding_root_imag']:
                    linesplit[i] =float(linesplit[i])
                elif c in ['an', 'first_an']:
                    linesplit[i] = [[float(x), float(y)] for x, y in eval(linesplit[i])]
                    if c == 'first_an':
                        linesplit[i] = linesplit[i][:-1]
                elif c in ['angles', 'first_angles']:
                    linesplit[i] = [[int(x), float(y)] for x, y in eval(linesplit[i])]
            # fix trivial character
            if linesplit[2] == 0:
                linesplit[2] = 1
                lfun_label = linesplit[1].split('.')
                lfun_label[-2] = str(1)
                linesplit[1] = '.'.join(lfun_label)
            hc = db.mf_hecke_cc.lucky({'hecke_orbit_code': linesplit[0], 'lfunction_label' : linesplit[1]})
            if hc is None:
                print {'hecke_orbit_code': linesplit[0], 'lfunction_label' : linesplit[1]}
                assert False
            for c in ['an', 'first_an']:
                hc[c] = [[float(x), float(y)] for x, y in hc[c]]
            
            
            hc_list = [ hc[c] for c in cols]
            if not compare_row(hc_list, linesplit):
                print {'hecke_orbit_code': linesplit[0], 'lfunction_label' : linesplit[1]}
                assert False
                

            if i % 10528 == 0:
                print '%.2f %%' % 100*i/105288.
