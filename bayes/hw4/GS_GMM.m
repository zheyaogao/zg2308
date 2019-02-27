x = csvread('x.csv');
n = length(x);
K = 30;
c = randsrc(1,n,1:K);
theta = betarnd(.5,.5,[1,K]);
nj = hist(c,1:K);
output = zeros(1000,6);
Kt = zeros(1000,1);

for t = 1:1000
    for i =1:n        
        nj(c(i)) = nj(c(i))-1;
        
        qc = nchoosek(20,x(i))*theta.^x(i).*(1-theta).^(20-x(i)).*nj/(.75+n-1);
        qc(K+1) = .75/(n+.75-1)*nchoosek(20,x(i))*beta(x(i)+.5,20-x(i)+.5)/beta(.5,.5);
        qc = qc/sum(qc);
        [~,I,V] = find(qc);
        c(i) = randsrc(1,1,[I;V]);
        if c(i) == K+1
            K = K+1;
            nj(K) = 0;
            theta(K) = betarnd(x(i)+.5,20-x(i)+.5);
        end
        
        nj(c(i)) = nj(c(i)) + 1;
    end
    [~,I,nj] = find(nj);
    theta = theta(I);
    K = length(nj);
    maps = containers.Map(I,1:K);
    for i = 1:n
        c(i) = maps(c(i));
    end
    
    for j = 1:K
        theta(j) = betarnd(sum(x(c==j))+.5,sum(20-x(c==j))+.5);
    end
    
    if K >= 6
        Num = sort(nj,'descend');
        output(t,:) = Num(1:6);
    end
    Kt(t) = K;
end

e = find(Kt<6);
figure(1);
for i = 1:6
    plot(output(1:e(1),i))
    hold on
end
hold off
figure(2);
plot(Kt)