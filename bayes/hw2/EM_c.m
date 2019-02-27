data = csvread('ratings.csv');
test = csvread('ratings_test.csv');
d = 5;
M = max(data(:,1));
N = max(data(:,2));
R = zeros(M,N);
R_test = zeros(M,N);
I = eye(d,d);
for i = 1:size(data,1)
    R(data(i,1),data(i,2)) = data(i,3);
end
for i = 1:size(test,1)
    R_test(test(i,1),test(i,2)) = test(i,3);
end

U = 0.1*randn(M,d);
V = 0.1*randn(N,d);
lnp_R_U_V = zeros(100,1);
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
    lnp_R_U_V(t) = -(M+N)*d/2*log(2*pi)-(sum(sum(U.^2))+sum(sum(V.^2)))/2+sum(sum(log(heaviside(-R)+R.*normcdf(U*V')).*(R~=0)));
end
predict = normcdf(U*V');
predict(predict > 0.5) = 1;
predict(predict <= 0.5) = -1;

p_p = sum(sum(((R_test == 1) & (predict == 1))));
p_n = sum(sum(((R_test == 1) & (predict == -1))));
n_p = sum(sum(((R_test == -1) & (predict == 1))));
n_n = sum(sum(((R_test == -1) & (predict == -1))));

cNames = {'predicted_like', 'predicted_dislike'};
rNames = {'like', 'dislike'};
predicted_like = [p_p;n_p];
predicted_dislike = [p_n;n_n];
table(predicted_like,predicted_dislike,'RowName',rNames)