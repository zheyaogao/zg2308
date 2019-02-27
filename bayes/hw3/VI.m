function [ans1,ans2,ans3,ans4] = VI(X,y,i)

N = size(X{i},1);
d = size(X{i},2);
L = zeros(1,500);

a0 = 10^(-16);
b0 = 10^(-16); 
miu = ones(1,d);
sig = ones(d,d);
e = 1+N/2;
f = 1;
a = a0+1/2;
b = b0*ones(1,d);

for t = 1:500
    b = b0+1/2*(diag(sig)'+miu.^2);
    f = 1+1/2*sum((y{i}-X{i}*miu').^2+diag(X{i}*sig*X{i}')); 
    sig = (diag(a./b)+e/f*(X{i}'*X{i}))^(-1);    
    miu = (e/f*y{i}'*X{i})*sig; 
    Eq_likehood = N/2*(psi(e)-log(2*pi*f))-e/f*(f-1);
    Eq_p_w = d/2*(psi(a)-log(2*pi))-sum(a./b.*(b-b0)+1/2*log(b));
    Eq_p_lambda = -e/f;
    Eq_p_a = d*(a0*log(b0)+(a0-1)*psi(a)-log(gamma(a0)))-sum(b0*a./b+(a0-1).*log(b));
    Eq_q_w = -d/2*(1/d*logdet(2*pi*e*sig)+log(2*pi)+1);
    Eq_q_lambda = log(f)-sum(log(1:(e-1)))-e+(e-1)*psi(e);
    Eq_q_a = d*((a-1)*psi(a)-log(gamma(a))-a)+sum(log(b));
    L(t) = Eq_likehood + Eq_p_w + Eq_p_lambda + Eq_p_a - Eq_q_w - Eq_q_lambda - Eq_q_a;
end
miu
ans1 = L;
ans2 = b/a;
ans3 = f/e;
ans4 = miu*X{i}';