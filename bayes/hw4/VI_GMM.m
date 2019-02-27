function [L,c] = VI_GMM(K,x)
n = length(x);
alpha = 0.05+0.05*rand(1,K);
a = 0.25+0.25*rand(1,K);
b = 0.25+0.25*rand(1,K);
L = zeros(1000,1);


for t = 1:1000
    phi = exp(x*(psi(a)-psi(a+b))+(20-x)*(psi(b)-psi(a+b))+repmat(psi(alpha),[n,1])-psi(sum(alpha)));
    phi = phi./repmat(sum(phi,2),[1,K]);
    nj = sum(phi,1);
    alpha = 0.1+nj;
    a = x'*phi+0.5;
    b = (20-x)'*phi+0.5;
    Eq_likehood = sum(sum(phi.*(x*(psi(a)-psi(a+b))+(20-x)*(psi(b)-psi(a+b))+repmat(psi(alpha),[n,1])-psi(sum(alpha)))));
    Eq_p_theta = -0.5*sum(psi(a)+psi(b)-2*psi(a+b));
    Eq_p_pi = -0.9*sum(psi(alpha)-psi(sum(alpha)));
    Eq_q_c = sum(sum(phi.*log(phi)));
    Eq_q_theta = -sum(betaln(a,b)-(a-1).*psi(a)-(b-1).*psi(b)+(a+b-2).*psi(a+b));
    Eq_q_pi = -sum(gammaln(alpha))+gammaln(sum(alpha))-(sum(alpha)-K)*psi(sum(alpha))+sum((alpha-1).*psi(alpha));
    L(t) = Eq_likehood + Eq_p_theta + Eq_p_pi- Eq_q_c - Eq_q_theta - Eq_q_pi;
end

v = (0:20)';
qc = exp(v*(psi(a)-psi(a+b))+(20-v)*(psi(b)-psi(a+b))+repmat(psi(alpha),[21,1])-psi(sum(alpha)));
[~,c] = max(qc,[],2);
