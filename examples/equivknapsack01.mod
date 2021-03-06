/*
Wolsey, L. A. (1977). Valid inequalities, covering problems and discrete
dynamic programs.
*/
$PARAM[m]{len(a)};

$EXEC{
m = len(a)
W = [a0]+[1]*len(a)
w = [[a[i]]+[1 if j == i else 0 for j in range(m)] for i in range(m)]
b = [1 for i in range(m)]
labels = [i+1 for i in range(m)]
};

$VBP_GRAPH[V,A]{W, w, labels, b};

set I := 1..m;
var pi{{0} union I} >= 0;
var theta{V} >= 0;

minimize obj: pi[0];
s.t. gamma{(u,v,i) in A: v != 'S'}:
    theta[v] >= theta[u]+(if i != 'LOSS' then pi[i] else 0);
s.t. pi0: pi[0] = theta['T'];
s.t. pisum: sum{i in I} pi[i] = 1+2*pi[0];
end;
