x = csvread('x.csv');
L = zeros(3,50);
c = zeros(3,21);
K = [3 9 15];
figure(1)
for i = 1:3
    [L(i,:),c(i,:)] = EM_GMM(K(i),x);
    plot(L(i,2:50))
    hold on
end
legend('K=3','K=9','K=15')
hold off
for i = 1:3
    figure(i+1)
    scatter(0:20,c(i,:))
end