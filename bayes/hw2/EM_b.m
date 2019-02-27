data = csvread('ratings.csv');
d = 5;
M = max(data(:,1));
N = max(data(:,2));
R = zeros(M,N);
I = eye(d,d);
for i = 1:size(data,1)
    R(data(i,1),data(i,2)) = data(i,3);
end

for k = 1:5
    U = 0.1*randn(M,d);
    V = 0.1*randn(N,d);
    for t = 1:100
        E = U*V'.*abs(R) + R.*normpdf(-U*V')./(heaviside(R)-R.*normcdf(-U*V'));
        for i = 1:M
            vi = V;
            vi(R(i,:) == 0,:) = zeros(sum(R(i,:) == 0),d);
            U(i,:) = (E(i,:)*vi)*(I + vi'*vi)^(-1);
        end
        for j = 1:N
            uj = U;
            uj(R(:,j) == 0,:) = zeros(sum(R(:,j) == 0),d);
            V(j,:) = (E(:,j)'*uj)*(I + uj'*uj)^(-1);
        end
        lnp_R_U_V(t,k) = -(M+N)*d/2*log(2*pi)-(sum(sum(U.^2))+sum(sum(V.^2)))/2+sum(sum(log(heaviside(-R)+R.*normcdf(U*V')).*(R~=0)));
    end
    plot(20:100,lnp_R_U_V(20:100,k),'-*');
    hold on
end
legend('sample1','sample2','sample3','sample4','sample5');   
title('Five random starting points');