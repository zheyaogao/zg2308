X = {csvread('X_set1.csv'),csvread('X_set2.csv'),csvread('X_set3.csv')};
y = {csvread('y_set1.csv'),csvread('y_set2.csv'),csvread('y_set3.csv')};
z = {csvread('z_set1.csv'),csvread('z_set2.csv'),csvread('z_set3.csv')};

i = 2;
[ans1,ans2,ans3,ans4] = VI(X,y,i);
figure(1);
plot(ans1);
figure(2);
plot(ans2);
sprintf('1/Eq[¦Ë]=%0.5e',ans3)
figure(3);
plot(z{i},ans4);
hold on;
scatter(z{i},y{i});
hold on;
plot(z{i},10*sinc(z{i}));

