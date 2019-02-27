function [L,c] = EM_GMM(K,x)

n = length(x);
theta = rand(1,K);
pi = rand(1,K);
pi = pi/sum(pi);
L = zeros(50,1);

for t = 1:50
    phi = exp(repmat(log(pi),[n,1])+x*log(theta)+(20-x)*log(1-theta));
    phi =  phi./repmat(sum(phi,2),[1,K]);
    nk = sum(phi,1);
    theta = x'*phi./(20*nk);
    pi = nk/n;
    L(t) = sum(sum(phi.*(x*log(theta)+(20-x)*log(1-theta)+repmat(log(pi),[n,1]))));
end

v = (0:20)';
qc = exp(repmat(log(pi),[21,1])+v*log(theta)+(20-v)*log(1-theta));
[~,c] = max(qc,[],2);
    
