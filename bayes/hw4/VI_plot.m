x = csvread('x.csv');
L = zeros(3,1000);
c = zeros(3,21);
K = [3 15 50];
figure(1)
for i = 1:3
    [L(i,:),c(i,:)] = VI_GMM(K(i),x);
    plot(L(i,2:1000))
    hold on
end
legend('K=3','K=15','K=50')
hold off
for i = 1:3
    figure(i+1)
    scatter(0:20,c(i,:))
end